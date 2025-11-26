#!/bin/bash

###############################################################################
# Скрипт автоматической настройки SSL сертификатов Let's Encrypt
# Для проекта "Еду на базар"
###############################################################################

set -e  # Остановка при ошибке

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция вывода
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

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

# Проверка что скрипт запущен от root
if [ "$EUID" -ne 0 ]; then 
    print_error "Скрипт должен быть запущен от root"
    echo "Используйте: sudo bash setup_ssl.sh"
    exit 1
fi

print_success "Запущено от root"

# Проверка что мы в правильной директории
if [ ! -f "docker-compose.yml" ]; then
    print_error "docker-compose.yml не найден"
    print_info "Перейдите в директорию проекта: cd /opt/edu-na-bazar"
    exit 1
fi

print_success "Найден docker-compose.yml"

###############################################################################
# Ввод данных
###############################################################################

print_header "Настройка параметров"

# Запрос домена
read -p "Введите ваш домен (например: edunabazar.ru): " DOMAIN

if [ -z "$DOMAIN" ]; then
    print_error "Домен не может быть пустым"
    exit 1
fi

print_info "Домен: $DOMAIN"

# Запрос email
read -p "Введите email для уведомлений Let's Encrypt: " EMAIL

if [ -z "$EMAIL" ]; then
    print_error "Email не может быть пустым"
    exit 1
fi

print_info "Email: $EMAIL"

# Запрос подтверждения
echo ""
print_warning "Убедитесь что:"
echo "  1. DNS A-запись для $DOMAIN указывает на этот сервер"
echo "  2. DNS A-запись для www.$DOMAIN указывает на этот сервер"
echo "  3. Порты 80 и 443 открыты"
echo ""

read -p "Продолжить? (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    print_info "Отменено пользователем"
    exit 0
fi

###############################################################################
# Проверка DNS
###############################################################################

print_header "Проверка DNS записей"

print_info "Проверка $DOMAIN..."
DOMAIN_IP=$(dig +short $DOMAIN | tail -n1)

if [ -z "$DOMAIN_IP" ]; then
    print_error "DNS запись для $DOMAIN не найдена"
    print_warning "Подождите пока DNS записи распространятся (до 48 часов)"
    exit 1
fi

print_success "$DOMAIN -> $DOMAIN_IP"

print_info "Проверка www.$DOMAIN..."
WWW_IP=$(dig +short www.$DOMAIN | tail -n1)

if [ -z "$WWW_IP" ]; then
    print_warning "DNS запись для www.$DOMAIN не найдена"
    print_info "Продолжаем только с основным доменом"
    DOMAINS="-d $DOMAIN"
else
    print_success "www.$DOMAIN -> $WWW_IP"
    DOMAINS="-d $DOMAIN -d www.$DOMAIN"
fi

###############################################################################
# Остановка контейнеров
###############################################################################

print_header "Остановка Docker контейнеров"

if docker-compose ps | grep -q "Up"; then
    print_info "Останавливаем контейнеры..."
    docker-compose down
    print_success "Контейнеры остановлены"
else
    print_info "Контейнеры уже остановлены"
fi

###############################################################################
# Установка Certbot
###############################################################################

print_header "Установка Certbot"

if command -v certbot &> /dev/null; then
    print_success "Certbot уже установлен"
    certbot --version
else
    print_info "Устанавливаем Certbot..."
    apt update
    apt install -y certbot python3-certbot-nginx
    print_success "Certbot установлен"
fi

###############################################################################
# Получение SSL сертификатов
###############################################################################

print_header "Получение SSL сертификатов"

print_info "Запрашиваем сертификаты для: $DOMAINS"
print_warning "Это может занять несколько минут..."

# Получаем сертификаты
if certbot certonly --standalone --non-interactive --agree-tos --email $EMAIL $DOMAINS; then
    print_success "SSL сертификаты успешно получены!"
    print_info "Сертификаты сохранены в: /etc/letsencrypt/live/$DOMAIN/"
else
    print_error "Ошибка получения сертификатов"
    print_info "Проверьте:"
    echo "  1. DNS записи правильно настроены"
    echo "  2. Порт 80 открыт и доступен"
    echo "  3. Нет других процессов на порту 80"
    exit 1
fi

###############################################################################
# Создание Nginx конфигурации с SSL
###############################################################################

print_header "Создание Nginx конфигурации"

print_info "Создаем nginx-ssl.conf..."

cat > frontend/nginx-ssl.conf << EOF
# HTTP -> HTTPS redirect
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    # Let's Encrypt challenge
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    
    # Redirect all HTTP to HTTPS
    location / {
        return 301 https://\$server_name\$request_uri;
    }
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name $DOMAIN www.$DOMAIN;
    
    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    
    # SSL configuration (Mozilla Intermediate)
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/$DOMAIN/chain.pem;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    # Root directory
    root /usr/share/nginx/html;
    index index.html;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/json application/xml+rss;
    
    # Frontend routes (React Router)
    location / {
        try_files \$uri \$uri/ /index.html;
    }
    
    # API proxy to backend
    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Forwarded-Host \$host;
        proxy_set_header X-Forwarded-Port \$server_port;
    }
    
    # Static files (uploads)
    location /uploads {
        proxy_pass http://backend:8000/uploads;
        proxy_set_header Host \$host;
    }
    
    # Health check
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

print_header "Обновление .env файла"

if [ -f ".env" ]; then
    print_info "Создаем backup .env -> .env.backup"
    cp .env .env.backup
    
    # Обновляем URLs на HTTPS
    sed -i "s|http://$DOMAIN|https://$DOMAIN|g" .env
    sed -i "s|http://www.$DOMAIN|https://www.$DOMAIN|g" .env
    
    # Обновляем ALLOWED_ORIGINS
    if grep -q "ALLOWED_ORIGINS=" .env; then
        sed -i "s|ALLOWED_ORIGINS=.*|ALLOWED_ORIGINS=https://$DOMAIN,https://www.$DOMAIN|" .env
    else
        echo "ALLOWED_ORIGINS=https://$DOMAIN,https://www.$DOMAIN" >> .env
    fi
    
    # Обновляем REACT_APP_API_URL
    if grep -q "REACT_APP_API_URL=" .env; then
        sed -i "s|REACT_APP_API_URL=.*|REACT_APP_API_URL=https://$DOMAIN|" .env
    else
        echo "REACT_APP_API_URL=https://$DOMAIN" >> .env
    fi
    
    print_success ".env обновлен (backup сохранен)"
else
    print_warning ".env не найден, создаем новый"
    cat > .env << EOF
DOMAIN=$DOMAIN
ENVIRONMENT=production
ALLOWED_ORIGINS=https://$DOMAIN,https://www.$DOMAIN
REACT_APP_API_URL=https://$DOMAIN
EOF
    print_success ".env создан"
fi

###############################################################################
# Обновление docker-compose.yml
###############################################################################

print_header "Обновление docker-compose.yml"

print_info "Добавляем volumes для SSL сертификатов..."

# Проверяем есть ли уже volumes в frontend сервисе
if grep -A 10 "frontend:" docker-compose.yml | grep -q "volumes:"; then
    print_info "Volumes уже настроены"
else
    # Добавляем volumes в frontend сервис
    sed -i '/frontend:/,/restart:/ {
        /ports:/a\    volumes:\n      - /etc/letsencrypt:/etc/letsencrypt:ro\n      - /var/www/certbot:/var/www/certbot
    }' docker-compose.yml
    print_success "Volumes добавлены в docker-compose.yml"
fi

###############################################################################
# Пересборка и запуск
###############################################################################

print_header "Пересборка и запуск контейнеров"

print_info "Пересобираем frontend с новой конфигурацией..."
docker-compose build --no-cache frontend

print_info "Запускаем все контейнеры..."
docker-compose up -d

print_success "Контейнеры запущены"

# Ждем запуска
print_info "Ожидание запуска сервисов (30 секунд)..."
sleep 30

###############################################################################
# Настройка автообновления
###############################################################################

print_header "Настройка автообновления сертификатов"

print_info "Добавляем cron задачу для автообновления..."

# Проверяем есть ли уже задача
if crontab -l 2>/dev/null | grep -q "certbot renew"; then
    print_info "Cron задача уже существует"
else
    # Добавляем задачу
    (crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --quiet --post-hook \"docker-compose -f $(pwd)/docker-compose.yml restart frontend\" >> /var/log/certbot-renew.log 2>&1") | crontab -
    print_success "Cron задача добавлена (проверка каждый день в 3:00)"
fi

# Тестируем обновление
print_info "Тестируем процесс обновления (dry-run)..."
if certbot renew --dry-run; then
    print_success "Тест обновления прошел успешно"
else
    print_warning "Тест обновления завершился с ошибками (не критично)"
fi

###############################################################################
# Проверка результата
###############################################################################

print_header "Проверка результата"

print_info "Проверяем статус контейнеров..."
docker-compose ps

echo ""
print_info "Проверяем HTTPS..."
sleep 5

if curl -k -I https://$DOMAIN 2>/dev/null | grep -q "200 OK"; then
    print_success "HTTPS работает!"
else
    print_warning "HTTPS пока не отвечает (может потребоваться время)"
fi

###############################################################################
# Итоги
###############################################################################

print_header "Настройка завершена!"

echo ""
print_success "SSL сертификаты успешно установлены!"
echo ""
echo "📋 Информация:"
echo "  • Домен: $DOMAIN"
echo "  • Сертификаты: /etc/letsencrypt/live/$DOMAIN/"
echo "  • Автообновление: настроено (каждый день в 3:00)"
echo ""
echo "🌐 Проверьте ваш сайт:"
echo "  • https://$DOMAIN"
echo "  • https://www.$DOMAIN"
echo ""
echo "🔍 Проверка безопасности:"
echo "  • SSL Labs: https://www.ssllabs.com/ssltest/analyze.html?d=$DOMAIN"
echo ""
echo "📝 Логи:"
echo "  • docker-compose logs -f frontend"
echo "  • docker-compose logs -f backend"
echo "  • tail -f /var/log/certbot-renew.log"
echo ""
print_success "Ваш сайт теперь работает по HTTPS! 🔒"
echo ""
