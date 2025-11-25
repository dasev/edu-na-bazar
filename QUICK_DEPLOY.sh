#!/bin/bash

###############################################
# Быстрый деплой "Еду на базар" на REG.RU
# Запускать на сервере после подключения по SSH
###############################################

set -e

echo "========================================="
echo "🚀 Быстрый деплой Еду на базар"
echo "========================================="
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функция для вывода с цветом
print_step() {
    echo -e "${GREEN}▶ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Проверка root
if [ "$EUID" -ne 0 ]; then 
    print_error "Запустите скрипт с правами root: sudo bash quick-deploy.sh"
    exit 1
fi

# 1. Обновление системы
print_step "Обновление системы..."
apt update && apt upgrade -y

# 2. Установка Docker
print_step "Установка Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    systemctl enable docker
    systemctl start docker
    echo "✅ Docker установлен"
else
    echo "✅ Docker уже установлен"
fi

# 3. Установка Docker Compose
print_step "Установка Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose установлен"
else
    echo "✅ Docker Compose уже установлен"
fi

# 4. Установка дополнительных пакетов
print_step "Установка дополнительных пакетов..."
apt install -y curl git nano htop nginx certbot python3-certbot-nginx ufw

# 5. Клонирование проекта
print_step "Клонирование проекта..."
mkdir -p /opt
cd /opt

if [ -d "edu-na-bazar" ]; then
    print_warning "Директория edu-na-bazar уже существует"
    read -p "Удалить и клонировать заново? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf edu-na-bazar
        echo "Введите URL репозитория (или Enter для пропуска):"
        read REPO_URL
        if [ -n "$REPO_URL" ]; then
            git clone "$REPO_URL" edu-na-bazar
        fi
    fi
else
    echo "Введите URL репозитория (или Enter для пропуска):"
    read REPO_URL
    if [ -n "$REPO_URL" ]; then
        git clone "$REPO_URL" edu-na-bazar
    else
        print_warning "Клонирование пропущено. Загрузите проект вручную."
    fi
fi

cd /opt/edu-na-bazar

# 6. Создание .env файла
print_step "Настройка .env файла..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        
        # Генерация SECRET_KEY
        SECRET_KEY=$(openssl rand -hex 32)
        sed -i "s/your-secret-key-here-min-32-chars-use-openssl-rand-hex-32/$SECRET_KEY/" .env
        
        # Генерация пароля БД
        DB_PASSWORD=$(openssl rand -base64 24)
        sed -i "s/your_secure_postgres_password_here/$DB_PASSWORD/" .env
        
        # Установка ENVIRONMENT=production
        sed -i "s/ENVIRONMENT=development/ENVIRONMENT=production/" .env
        
        echo "✅ .env файл создан с автогенерированными паролями"
        print_warning "ВАЖНО: Отредактируйте .env и укажите ваш домен в ALLOWED_ORIGINS"
        echo "Команда: nano .env"
        read -p "Нажмите Enter для продолжения..."
    else
        print_error ".env.example не найден!"
        exit 1
    fi
else
    echo "✅ .env файл уже существует"
fi

# 7. Запуск контейнеров
print_step "Запуск Docker контейнеров..."
docker-compose up -d --build

# Ждем запуска
echo "Ожидание запуска контейнеров (30 секунд)..."
sleep 30

# 8. Применение миграций
print_step "Применение миграций БД..."
docker-compose exec -T backend alembic upgrade head

# 9. Проверка статуса
print_step "Проверка статуса..."
docker-compose ps

# 10. Настройка firewall
print_step "Настройка firewall..."
ufw --force enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw reload

# 11. Создание директории для backup
print_step "Создание директории для backup..."
mkdir -p /backups
chmod +x backup.sh 2>/dev/null || true

echo ""
echo "========================================="
echo "✅ Базовая установка завершена!"
echo "========================================="
echo ""
echo "📋 Следующие шаги:"
echo ""
echo "1. Отредактировать .env файл:"
echo "   nano /opt/edu-na-bazar/.env"
echo "   - Указать домен в ALLOWED_ORIGINS"
echo "   - Настроить SMS (если нужно)"
echo "   - Настроить Mapbox (если нужна карта)"
echo ""
echo "2. Загрузить изображения:"
echo "   scp uploads.zip root@YOUR_SERVER_IP:/opt/edu-na-bazar/"
echo "   cd /opt/edu-na-bazar"
echo "   ./DEPLOY_UPLOADS.sh"
echo ""
echo "3. Настроить Nginx и SSL (если есть домен):"
echo "   nano /etc/nginx/sites-available/edu-na-bazar"
echo "   # Скопировать конфигурацию из DEPLOY_REGRU.md"
echo "   ln -s /etc/nginx/sites-available/edu-na-bazar /etc/nginx/sites-enabled/"
echo "   nginx -t"
echo "   systemctl restart nginx"
echo "   certbot --nginx -d yourdomain.ru -d www.yourdomain.ru"
echo ""
echo "4. Настроить мониторинг:"
echo "   - UptimeRobot: https://uptimerobot.com"
echo "   - Telegram Bot: nano uptime-monitor.sh"
echo ""
echo "5. Настроить backup:"
echo "   crontab -e"
echo "   # Добавить: 0 2 * * * /opt/edu-na-bazar/backup.sh"
echo ""
echo "📊 Проверка:"
echo "   curl http://localhost:8000/api/health"
echo "   curl http://localhost"
echo ""
echo "📚 Полная документация: /opt/edu-na-bazar/DEPLOY_REGRU.md"
echo ""
