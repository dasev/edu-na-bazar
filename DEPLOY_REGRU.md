# 🚀 Деплой на сервер REG.RU

## � Два способа деплоя

### Способ 1: Автоматический через CI/CD (Рекомендуется)
- ✅ Автоматический деплой при `git push`
- ✅ Backup перед каждым деплоем
- ✅ Автоматические миграции
- ✅ Health check
- ⏱️ **Время: 30 минут настройки, потом 3-5 минут на каждый деплой**
- 📚 **Инструкция**: `CICD_SETUP_REGRU.md`

### Способ 2: Ручной деплой (Этот документ)
- ✅ Полный контроль над процессом
- ✅ Не требует GitHub/Docker Hub
- ⏱️ **Время: 1-1.5 часа первый раз, 10-15 минут обновления**

---

## �📋 Что нужно от REG.RU

После аренды сервера у вас должны быть:
- ✅ IP адрес сервера
- ✅ Root пароль (или SSH ключ)
- ✅ Домен (если есть)

---

## 🎯 Этап 1: Подключение к серверу (5 минут)

### Windows (PowerShell):

```powershell
# Подключиться по SSH
ssh root@YOUR_SERVER_IP

# Или через PuTTY:
# 1. Скачать PuTTY: https://www.putty.org/
# 2. Host Name: YOUR_SERVER_IP
# 3. Port: 22
# 4. Connection type: SSH
# 5. Open → ввести root и пароль
```

### После подключения:

```bash
# Обновить систему
apt update && apt upgrade -y

# Установить необходимые пакеты
apt install -y curl git nano htop
```

---

## 🐳 Этап 2: Установка Docker (10 минут)

```bash
# Установить Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Установить Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Проверить установку
docker --version
docker-compose --version

# Настроить автозапуск
systemctl enable docker
systemctl start docker
```

---

## 📦 Этап 3: Загрузка проекта (5 минут)

### Вариант 1: Через Git (Рекомендуется)

```bash
# Создать директорию
mkdir -p /opt
cd /opt

# Клонировать репозиторий
git clone https://github.com/YOUR_USERNAME/edu-na-bazar.git
cd edu-na-bazar

# Или если приватный репозиторий:
git clone https://YOUR_TOKEN@github.com/YOUR_USERNAME/edu-na-bazar.git
```

### Вариант 2: Через архив

```bash
# На локальной машине создать архив (без node_modules и venv)
tar -czf edu-na-bazar.tar.gz \
  --exclude='node_modules' \
  --exclude='venv' \
  --exclude='__pycache__' \
  --exclude='.git' \
  edu-na-bazar/

# Загрузить на сервер (с локальной машины)
scp edu-na-bazar.tar.gz root@YOUR_SERVER_IP:/opt/

# На сервере распаковать
cd /opt
tar -xzf edu-na-bazar.tar.gz
cd edu-na-bazar
```

---

## ⚙️ Этап 4: Настройка окружения (10 минут)

```bash
# Создать .env файл
cp .env.example .env
nano .env
```

### Настроить .env:

```env
# Environment
ENVIRONMENT=production

# Database
POSTGRES_DB=edu_na_bazar
POSTGRES_USER=postgres
POSTGRES_PASSWORD=СГЕНЕРИРОВАТЬ_СИЛЬНЫЙ_ПАРОЛЬ

# Redis
REDIS_URL=redis://redis:6379/0

# Security - ВАЖНО! Сгенерировать новый ключ
SECRET_KEY=СГЕНЕРИРОВАТЬ_НОВЫЙ_КЛЮЧ

# CORS - указать ваш домен
ALLOWED_ORIGINS=https://yourdomain.ru,https://www.yourdomain.ru

# SMS (если нужно)
SMS_ENABLED=false
SMSC_LOGIN=your_login
SMSC_PASSWORD=your_password

# Mapbox (если нужна карта)
MAPBOX_ACCESS_TOKEN=your_token
REACT_APP_MAPBOX_TOKEN=your_token

# API URL для frontend
REACT_APP_API_URL=https://yourdomain.ru
```

### Сгенерировать SECRET_KEY:

```bash
# На сервере
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Или
openssl rand -hex 32

# Скопировать результат в .env
```

### Сгенерировать пароль для БД:

```bash
openssl rand -base64 24
# Скопировать в POSTGRES_PASSWORD
```

---

## 🗄️ Этап 5: Загрузка изображений (5 минут)

```bash
# На локальной машине создать архив
# Windows PowerShell:
cd C:\python\edu-na-bazar
.\CREATE_UPLOADS_ARCHIVE.bat

# Загрузить на сервер
scp uploads.zip root@YOUR_SERVER_IP:/opt/edu-na-bazar/

# На сервере будет распаковано автоматически после запуска
```

---

## 🚀 Этап 6: Запуск проекта (5 минут)

```bash
cd /opt/edu-na-bazar

# Запустить контейнеры
docker-compose up -d --build

# Проверить статус
docker-compose ps

# Должны быть запущены:
# - edu-na-bazar-postgres
# - edu-na-bazar-redis
# - edu-na-bazar-backend
# - edu-na-bazar-frontend
```

### Применить миграции БД:

```bash
# Применить миграции
docker-compose exec -T backend alembic upgrade head

# Проверить
docker-compose exec -T backend alembic current
```

### Загрузить изображения:

```bash
# Распаковать архив в контейнер
chmod +x DEPLOY_UPLOADS.sh
./DEPLOY_UPLOADS.sh

# Или вручную:
docker cp uploads.zip edu-na-bazar-backend:/tmp/
docker exec edu-na-bazar-backend unzip -o /tmp/uploads.zip -d /app/
docker exec edu-na-bazar-backend rm /tmp/uploads.zip
docker exec edu-na-bazar-backend chmod -R 755 /app/uploads/
```

---

## 🔒 Этап 7: Настройка SSL (15 минут)

### Если у вас есть домен:

```bash
# Установить Certbot
apt install -y certbot python3-certbot-nginx

# Установить Nginx
apt install -y nginx

# Создать конфигурацию Nginx
nano /etc/nginx/sites-available/edu-na-bazar
```

### Конфигурация Nginx:

```nginx
# HTTP -> HTTPS редирект
server {
    listen 80;
    server_name yourdomain.ru www.yourdomain.ru;
    
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }
    
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS
server {
    listen 443 ssl http2;
    server_name yourdomain.ru www.yourdomain.ru;

    # SSL сертификаты (будут созданы Certbot)
    ssl_certificate /etc/letsencrypt/live/yourdomain.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.ru/privkey.pem;
    
    # SSL настройки
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Frontend
    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Backend uploads
    location /uploads {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
    }
    
    # WebSocket (если будет)
    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Активировать конфигурацию:

```bash
# Создать симлинк
ln -s /etc/nginx/sites-available/edu-na-bazar /etc/nginx/sites-enabled/

# Удалить дефолтную конфигурацию
rm /etc/nginx/sites-enabled/default

# Проверить конфигурацию
nginx -t

# Перезапустить Nginx
systemctl restart nginx
systemctl enable nginx
```

### Получить SSL сертификат:

```bash
# Получить сертификат
certbot --nginx -d yourdomain.ru -d www.yourdomain.ru

# Следовать инструкциям:
# 1. Ввести email
# 2. Согласиться с условиями (Y)
# 3. Выбрать опцию 2 (Redirect HTTP to HTTPS)

# Проверить автообновление
certbot renew --dry-run

# Сертификат будет обновляться автоматически
```

---

## 🔍 Этап 8: Проверка (5 минут)

```bash
# 1. Проверить контейнеры
docker-compose ps

# 2. Проверить логи
docker-compose logs -f backend
docker-compose logs -f frontend

# 3. Проверить API
curl http://localhost:8000/api/health
# Должно вернуть: {"status":"ok"}

# 4. Проверить Frontend
curl http://localhost
# Должен вернуть HTML

# 5. Проверить через домен (если настроен)
curl https://yourdomain.ru/api/health
```

### Проверить в браузере:

1. Открыть `https://yourdomain.ru`
2. Проверить что сайт загружается
3. Проверить что изображения отображаются
4. Попробовать зарегистрироваться/войти

---

## 📊 Этап 9: Настройка мониторинга (10 минут)

### UptimeRobot:

```bash
# 1. Зарегистрироваться на uptimerobot.com
# 2. Добавить мониторы:
#    - https://yourdomain.ru (Frontend)
#    - https://yourdomain.ru/api/health (API)
#    - https://yourdomain.ru/api/categories (Database)
# 3. Настроить Email/Telegram уведомления
```

### Telegram Bot:

```bash
# 1. Создать бота через @BotFather
# 2. Получить BOT_TOKEN и CHAT_ID

# 3. Настроить скрипт
cd /opt/edu-na-bazar
nano uptime-monitor.sh

# Заменить:
# - BOT_TOKEN
# - CHAT_ID
# - FRONTEND_URL=https://yourdomain.ru
# - API_HEALTH_URL=https://yourdomain.ru/api/health

# 4. Сделать исполняемым
chmod +x uptime-monitor.sh

# 5. Добавить в cron
crontab -e
# Добавить строку:
*/5 * * * * /opt/edu-na-bazar/uptime-monitor.sh >> /var/log/uptime-monitor.log 2>&1

# 6. Протестировать
./uptime-monitor.sh
```

---

## 💾 Этап 10: Настройка Backup (10 минут)

```bash
# Создать директорию для backup
mkdir -p /backups

# Создать скрипт backup
nano /opt/edu-na-bazar/backup.sh
```

### Скрипт backup.sh:

```bash
#!/bin/bash

# Директория для backup
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup БД
docker-compose -f /opt/edu-na-bazar/docker-compose.yml exec -T postgres \
  pg_dump -U postgres edu_na_bazar | gzip > "${BACKUP_DIR}/db_${DATE}.sql.gz"

# Backup изображений (раз в неделю)
if [ $(date +%u) -eq 1 ]; then
  tar -czf "${BACKUP_DIR}/uploads_${DATE}.tar.gz" /opt/edu-na-bazar/backend/uploads/
fi

# Удалить старые backup (старше 30 дней)
find "${BACKUP_DIR}" -name "db_*.sql.gz" -mtime +30 -delete
find "${BACKUP_DIR}" -name "uploads_*.tar.gz" -mtime +90 -delete

echo "Backup completed: ${DATE}"
```

### Настроить автоматический backup:

```bash
# Сделать исполняемым
chmod +x /opt/edu-na-bazar/backup.sh

# Добавить в cron (каждый день в 2:00)
crontab -e
# Добавить строку:
0 2 * * * /opt/edu-na-bazar/backup.sh >> /var/log/backup.log 2>&1

# Протестировать
/opt/edu-na-bazar/backup.sh
ls -lh /backups/
```

---

## 🔧 Этап 11: Оптимизация (опционально)

### Настроить firewall:

```bash
# Установить UFW
apt install -y ufw

# Разрешить SSH
ufw allow 22/tcp

# Разрешить HTTP/HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Включить firewall
ufw enable

# Проверить статус
ufw status
```

### Настроить swap (если мало RAM):

```bash
# Создать swap файл 2GB
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

# Добавить в fstab для автозагрузки
echo '/swapfile none swap sw 0 0' >> /etc/fstab

# Проверить
free -h
```

### Настроить автоперезапуск контейнеров:

```bash
# Уже настроено в docker-compose.yml:
# restart: unless-stopped

# Проверить
docker-compose ps
```

---

## ✅ Checklist деплоя

- [ ] Подключился к серверу
- [ ] Установил Docker и Docker Compose
- [ ] Загрузил проект на сервер
- [ ] Создал и настроил .env файл
- [ ] Сгенерировал SECRET_KEY
- [ ] Загрузил изображения
- [ ] Запустил контейнеры
- [ ] Применил миграции БД
- [ ] Настроил Nginx
- [ ] Получил SSL сертификат
- [ ] Проверил работу сайта
- [ ] Настроил мониторинг (UptimeRobot + Telegram)
- [ ] Настроил backup БД
- [ ] Настроил firewall
- [ ] Проверил все функции сайта

---

## 🐛 Troubleshooting

### Контейнеры не запускаются:

```bash
# Проверить логи
docker-compose logs backend
docker-compose logs frontend

# Проверить порты
netstat -tulpn | grep -E ':(80|443|8000|5432|6379)'

# Перезапустить
docker-compose down
docker-compose up -d --build
```

### Ошибка подключения к БД:

```bash
# Проверить что PostgreSQL запущен
docker-compose ps postgres

# Проверить логи
docker-compose logs postgres

# Проверить подключение
docker-compose exec backend python -c "from database import engine; print('OK')"
```

### Nginx не запускается:

```bash
# Проверить конфигурацию
nginx -t

# Проверить логи
tail -f /var/log/nginx/error.log

# Проверить порты
netstat -tulpn | grep :80
netstat -tulpn | grep :443
```

### SSL сертификат не получается:

```bash
# Проверить что домен указывает на сервер
nslookup yourdomain.ru

# Проверить что порт 80 открыт
curl http://yourdomain.ru

# Попробовать снова
certbot --nginx -d yourdomain.ru -d www.yourdomain.ru --dry-run
```

---

## 📞 Полезные команды

```bash
# Перезапуск всех контейнеров
docker-compose restart

# Остановка
docker-compose stop

# Просмотр логов
docker-compose logs -f

# Просмотр ресурсов
docker stats

# Очистка неиспользуемых образов
docker system prune -a

# Обновление проекта
cd /opt/edu-na-bazar
git pull
docker-compose up -d --build

# Backup БД вручную
docker-compose exec postgres pg_dump -U postgres edu_na_bazar > backup.sql

# Восстановление БД
docker-compose exec -T postgres psql -U postgres edu_na_bazar < backup.sql
```

---

## 🎉 Готово!

Ваш проект развернут на сервере REG.RU!

**Доступ:**
- Frontend: `https://yourdomain.ru`
- API: `https://yourdomain.ru/api/health`
- API Docs: `https://yourdomain.ru/docs` (только в development)

**Мониторинг:**
- UptimeRobot: проверка каждые 5 минут
- Telegram Bot: уведомления о проблемах

**Backup:**
- БД: каждый день в 2:00
- Хранение: 30 дней

---

**Время деплоя: 1-1.5 часа**
**Создано**: 25.11.2025
