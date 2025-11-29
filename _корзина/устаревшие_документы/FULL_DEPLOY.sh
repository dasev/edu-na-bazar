#!/bin/bash

###############################################
# Полный автоматический деплой "Еду на базар"
# Для Ubuntu сервера REG.RU
# IP: 176.99.5.211
###############################################

set -e

echo "========================================="
echo "🚀 Полный деплой Еду на базар"
echo "========================================="
echo ""

# Цвета
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

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
    print_error "Запустите с правами root: sudo bash FULL_DEPLOY.sh"
    exit 1
fi

# ============================================
# 1. ОБНОВЛЕНИЕ СИСТЕМЫ
# ============================================
print_step "1/10 Обновление системы..."
apt update && apt upgrade -y
apt install -y curl git nano htop wget unzip

# ============================================
# 2. УСТАНОВКА DOCKER
# ============================================
print_step "2/10 Установка Docker..."
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

# ============================================
# 3. УСТАНОВКА DOCKER COMPOSE
# ============================================
print_step "3/10 Установка Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose установлен"
else
    echo "✅ Docker Compose уже установлен"
fi

docker --version
docker-compose --version

# ============================================
# 4. КЛОНИРОВАНИЕ ПРОЕКТА
# ============================================
print_step "4/10 Клонирование проекта с GitHub..."

mkdir -p /opt
cd /opt

if [ -d "edu-na-bazar" ]; then
    print_warning "Директория edu-na-bazar уже существует"
    cd edu-na-bazar
    git pull origin main || git pull origin master
else
    # Укажите URL вашего репозитория
    echo "Введите URL GitHub репозитория:"
    echo "Пример: https://github.com/username/edu-na-bazar.git"
    read REPO_URL
    
    if [ -z "$REPO_URL" ]; then
        print_error "URL репозитория не указан!"
        exit 1
    fi
    
    git clone "$REPO_URL" edu-na-bazar
    cd edu-na-bazar
fi

# ============================================
# 5. СОЗДАНИЕ .ENV ФАЙЛА
# ============================================
print_step "5/10 Создание .env файла..."

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
        
        # Установка ALLOWED_ORIGINS
        sed -i "s|ALLOWED_ORIGINS=.*|ALLOWED_ORIGINS=http://176.99.5.211,http://localhost|" .env
        
        # Установка API_URL
        sed -i "s|REACT_APP_API_URL=.*|REACT_APP_API_URL=http://176.99.5.211:8000|" .env
        
        echo "✅ .env файл создан"
        echo ""
        echo "📝 Сгенерированные пароли:"
        echo "SECRET_KEY: $SECRET_KEY"
        echo "POSTGRES_PASSWORD: $DB_PASSWORD"
        echo ""
        echo "⚠️  СОХРАНИТЕ ЭТИ ПАРОЛИ!"
        echo ""
    else
        print_error ".env.example не найден!"
        exit 1
    fi
else
    echo "✅ .env файл уже существует"
fi

# ============================================
# 6. ЗАПУСК КОНТЕЙНЕРОВ
# ============================================
print_step "6/10 Запуск Docker контейнеров..."

docker-compose down 2>/dev/null || true
docker-compose up -d --build

echo "⏳ Ожидание запуска контейнеров (30 секунд)..."
sleep 30

# ============================================
# 7. ПРИМЕНЕНИЕ МИГРАЦИЙ
# ============================================
print_step "7/10 Применение миграций БД..."

docker-compose exec -T backend alembic upgrade head

echo "✅ Миграции применены"

# ============================================
# 8. НАСТРОЙКА FIREWALL
# ============================================
print_step "8/10 Настройка firewall..."

apt install -y ufw

# Разрешить SSH (ВАЖНО!)
ufw allow 22/tcp

# Разрешить HTTP/HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Разрешить порты приложения
ufw allow 8000/tcp
ufw allow 3000/tcp

# Включить firewall
ufw --force enable

echo "✅ Firewall настроен"

# ============================================
# 9. СОЗДАНИЕ ДИРЕКТОРИЙ
# ============================================
print_step "9/10 Создание директорий для backup..."

mkdir -p /backups
chmod +x backup.sh 2>/dev/null || true
chmod +x uptime-monitor.sh 2>/dev/null || true
chmod +x DEPLOY_UPLOADS.sh 2>/dev/null || true

# ============================================
# 10. ПРОВЕРКА РАБОТЫ
# ============================================
print_step "10/10 Проверка работы..."

echo ""
echo "📊 Статус контейнеров:"
docker-compose ps

echo ""
echo "🔍 Проверка API..."
sleep 5
API_STATUS=$(curl -s http://localhost:8000/api/health || echo "FAILED")
if echo "$API_STATUS" | grep -q "ok"; then
    echo "✅ API работает: $API_STATUS"
else
    echo "⚠️  API не отвечает, проверьте логи: docker-compose logs backend"
fi

echo ""
echo "========================================="
echo "✅ БАЗОВЫЙ ДЕПЛОЙ ЗАВЕРШЕН!"
echo "========================================="
echo ""
echo "🌐 Доступ к приложению:"
echo "   Frontend:  http://176.99.5.211"
echo "   Backend:   http://176.99.5.211:8000"
echo "   API Docs:  http://176.99.5.211:8000/docs"
echo "   API Health: http://176.99.5.211:8000/api/health"
echo ""
echo "📋 Следующие шаги:"
echo ""
echo "1. 📸 Загрузить изображения:"
echo "   На локальной машине:"
echo "   - Запустить: CREATE_UPLOADS_ARCHIVE.bat"
echo "   - Загрузить: scp uploads.zip root@176.99.5.211:/opt/edu-na-bazar/"
echo "   На сервере:"
echo "   - Запустить: ./DEPLOY_UPLOADS.sh"
echo ""
echo "2. 📊 Настроить мониторинг:"
echo "   - UptimeRobot: https://uptimerobot.com"
echo "   - Telegram Bot: nano uptime-monitor.sh"
echo ""
echo "3. 💾 Настроить автоматический backup:"
echo "   crontab -e"
echo "   Добавить: 0 2 * * * /opt/edu-na-bazar/backup.sh >> /var/log/backup.log 2>&1"
echo ""
echo "4. 🔒 Настроить домен и SSL (если есть домен):"
echo "   - Следовать инструкции в DEPLOY_REGRU.md"
echo ""
echo "📚 Документация:"
echo "   - DEPLOY_STEPS.md - пошаговая инструкция"
echo "   - CICD_SETUP_REGRU.md - настройка CI/CD"
echo ""
echo "🐛 Если что-то не работает:"
echo "   docker-compose logs -f backend"
echo "   docker-compose logs -f frontend"
echo ""
echo "🎉 Готово! Откройте в браузере: http://176.99.5.211"
echo ""
