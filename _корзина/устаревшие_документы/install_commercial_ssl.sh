#!/bin/bash

###############################################################################
# Скрипт установки купленного (коммерческого) SSL сертификата
# Для проекта "Еду на базар"
###############################################################################

set -e

# Цвета
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_header() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo ""
}

###############################################################################
# Проверка предварительных условий
###############################################################################

print_header "Проверка предварительных условий"

if [ "$EUID" -ne 0 ]; then 
    print_error "Скрипт должен быть запущен от root"
    exit 1
fi

if [ ! -f "docker-compose.yml" ]; then
    print_error "docker-compose.yml не найден"
    exit 1
fi

print_success "Предварительные проверки пройдены"

###############################################################################
# Ввод данных
###############################################################################

print_header "Настройка параметров"

read -p "Введите ваш домен (например: edunabazar.ru): " DOMAIN

if [ -z "$DOMAIN" ]; then
    print_error "Домен не может быть пустым"
    exit 1
fi

print_info "Домен: $DOMAIN"

echo ""
print_info "Укажите пути к файлам сертификатов:"
echo ""

read -p "Путь к сертификату домена (certificate.crt): " CERT_FILE

if [ ! -f "$CERT_FILE" ]; then
    print_error "Файл $CERT_FILE не найден"
    exit 1
fi

read -p "Путь к приватному ключу (private.key): " KEY_FILE

if [ ! -f "$KEY_FILE" ]; then
    print_error "Файл $KEY_FILE не найден"
    exit 1
fi

read -p "Путь к промежуточным сертификатам (ca_bundle.crt): " CA_FILE

if [ ! -f "$CA_FILE" ]; then
    print_error "Файл $CA_FILE не найден"
    exit 1
fi

print_success "Все файлы найдены"

###############################################################################
# Проверка сертификатов
###############################################################################

print_header "Проверка сертификатов"

print_info "Проверка срока действия..."
EXPIRY_DATE=$(openssl x509 -in "$CERT_FILE" -noout -enddate | cut -d= -f2)
print_info "Сертификат действителен до: $EXPIRY_DATE"

print_info "Проверка соответствия ключа и сертификата..."
CERT_MD5=$(openssl x509 -noout -modulus -in "$CERT_FILE" | openssl md5)
KEY_MD5=$(openssl rsa -noout -modulus -in "$KEY_FILE" 2>/dev/null | openssl md5)

if [ "$CERT_MD5" != "$KEY_MD5" ]; then
    print_error "Приватный ключ не соответствует сертификату!"
    print_info "Cert MD5: $CERT_MD5"
    print_info "Key MD5:  $KEY_MD5"
    exit 1
fi

print_success "Ключ соответствует сертификату"

###############################################################################
# Создание fullchain.crt
###############################################################################

print_header "Создание fullchain.crt"

TEMP_DIR=$(mktemp -d)
FULLCHAIN="$TEMP_DIR/fullchain.crt"

print_info "Объединяем сертификаты..."
cat "$CERT_FILE" "$CA_FILE" > "$FULLCHAIN"

print_success "fullchain.crt создан"

###############################################################################
# Создание директории на сервере
###############################################################################

print_header "Подготовка директории"

SSL_DIR="/etc/ssl/$DOMAIN"

print_info "Создаем директорию: $SSL_DIR"
mkdir -p "$SSL_DIR"
chmod 700 "$SSL_DIR"

print_success "Директория создана"

###############################################################################
# Копирование файлов
###############################################################################

print_header "Копирование сертификатов"

print_info "Копируем fullchain.crt..."
cp "$FULLCHAIN" "$SSL_DIR/fullchain.crt"
chmod 644 "$SSL_DIR/fullchain.crt"

print_info "Копируем private.key..."
cp "$KEY_FILE" "$SSL_DIR/private.key"
chmod 600 "$SSL_DIR/private.key"

print_info "Копируем ca_bundle.crt..."
cp "$CA_FILE" "$SSL_DIR/ca_bundle.crt"
chmod 644 "$SSL_DIR/ca_bundle.crt"

print_success "Все файлы скопированы"

# Очистка временной директории
rm -rf "$TEMP_DIR"

###############################################################################
# Создание nginx-ssl.conf
###############################################################################

print_header "Создание Nginx конфигурации"

print_info "Создаем nginx-ssl.conf..."

cat > frontend/nginx-ssl.conf << EOF
# HTTP -> HTTPS redirect
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    location / {
        return 301 https://\$server_name\$request_uri;
    }
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name $DOMAIN www.$DOMAIN;
    
    # SSL certificates (КОММЕРЧЕСКИЙ)
    ssl_certificate $SSL_DIR/fullchain.crt;
    ssl_certificate_key $SSL_DIR/private.key;
    ssl_trusted_certificate $SSL_DIR/ca_bundle.crt;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    root /usr/share/nginx/html;
    index index.html;
    
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/json;
    
    location / {
        try_files \$uri \$uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    location /uploads {
        proxy_pass http://backend:8000/uploads;
        proxy_set_header Host \$host;
    }
    
    location /health {
        access_log off;
        return 200 "OK\n";
        add_header Content-Type text/plain;
    }
}
EOF

print_success "nginx-ssl.conf создан"

###############################################################################
# Обновление .env
###############################################################################

print_header "Обновление .env"

if [ -f ".env" ]; then
    cp .env .env.backup
    sed -i "s|http://$DOMAIN|https://$DOMAIN|g" .env
    sed -i "s|http://www.$DOMAIN|https://www.$DOMAIN|g" .env
    sed -i "s|ALLOWED_ORIGINS=.*|ALLOWED_ORIGINS=https://$DOMAIN,https://www.$DOMAIN|" .env
    sed -i "s|REACT_APP_API_URL=.*|REACT_APP_API_URL=https://$DOMAIN|" .env
    print_success ".env обновлен"
else
    print_warning ".env не найден"
fi

###############################################################################
# Обновление docker-compose.yml
###############################################################################

print_header "Обновление docker-compose.yml"

# Проверяем есть ли уже volumes
if grep -A 10 "frontend:" docker-compose.yml | grep -q "volumes:"; then
    print_info "Volumes уже настроены"
else
    print_info "Добавляем volumes..."
    # Добавляем volumes для коммерческого сертификата
    sed -i "/frontend:/,/restart:/ {
        /ports:/a\    volumes:\n      - $SSL_DIR:$SSL_DIR:ro
    }" docker-compose.yml
    print_success "Volumes добавлены"
fi

###############################################################################
# Пересборка и запуск
###############################################################################

print_header "Пересборка и запуск"

print_info "Пересобираем frontend..."
docker-compose build --no-cache frontend

print_info "Запускаем контейнеры..."
docker-compose up -d

print_success "Контейнеры запущены"

sleep 10

###############################################################################
# Проверка
###############################################################################

print_header "Проверка результата"

print_info "Проверяем HTTPS..."
if curl -k -I https://$DOMAIN 2>/dev/null | grep -q "200 OK"; then
    print_success "HTTPS работает!"
else
    print_warning "HTTPS пока не отвечает"
fi

###############################################################################
# Итоги
###############################################################################

print_header "Установка завершена!"

echo ""
print_success "Коммерческий SSL сертификат установлен!"
echo ""
echo "📋 Информация:"
echo "  • Домен: $DOMAIN"
echo "  • Сертификаты: $SSL_DIR/"
echo "  • Срок действия: $EXPIRY_DATE"
echo ""
echo "🌐 Проверьте ваш сайт:"
echo "  • https://$DOMAIN"
echo "  • https://www.$DOMAIN"
echo ""
echo "🔍 Проверка безопасности:"
echo "  • SSL Labs: https://www.ssllabs.com/ssltest/analyze.html?d=$DOMAIN"
echo ""
echo "⏰ Не забудьте:"
echo "  • Добавить напоминание об обновлении (за 1 месяц до $EXPIRY_DATE)"
echo "  • Сохранить backup сертификатов"
echo ""
print_success "Готово! 🔒"
echo ""
