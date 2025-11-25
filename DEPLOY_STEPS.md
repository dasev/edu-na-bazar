# 🚀 Пошаговый деплой на ваш сервер REG.RU

## 📋 Данные сервера
- **IP**: 176.99.5.211
- **User**: root
- **Password**: sIAS6APDsKh0bL

---

## ⚡ Быстрый старт (выберите вариант)

### Вариант 1: Автоматический скрипт (15 минут)

**На локальной машине (PowerShell):**

```powershell
# 1. Загрузить скрипт на сервер
scp QUICK_DEPLOY.sh root@176.99.5.211:/root/
# Пароль: sIAS6APDsKh0bL

# 2. Загрузить архив проекта (если нет Git)
# Создать архив (исключая ненужное)
tar.exe -czf edu-na-bazar.tar.gz --exclude=node_modules --exclude=venv --exclude=__pycache__ --exclude=.git .

# Загрузить
scp edu-na-bazar.tar.gz root@176.99.5.211:/opt/
# Пароль: sIAS6APDsKh0bL

# 3. Загрузить изображения
.\CREATE_UPLOADS_ARCHIVE.bat
scp uploads.zip root@176.99.5.211:/opt/
# Пароль: sIAS6APDsKh0bL
```

**На сервере:**

```bash
# Подключиться
ssh root@176.99.5.211
# Пароль: sIAS6APDsKh0bL

# Запустить автоустановку
bash /root/QUICK_DEPLOY.sh

# Следовать инструкциям на экране
```

---

### Вариант 2: Пошаговый ручной (1 час)

## Шаг 1: Подключение к серверу

```powershell
# На локальной машине
ssh root@176.99.5.211
# Пароль: sIAS6APDsKh0bL
```

---

## Шаг 2: Установка Docker

```bash
# Обновить систему
apt update && apt upgrade -y

# Установить Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
rm get-docker.sh

# Установить Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Проверить
docker --version
docker-compose --version

# Настроить автозапуск
systemctl enable docker
systemctl start docker
```

---

## Шаг 3: Загрузка проекта

### Если есть Git репозиторий:

```bash
cd /opt
git clone https://github.com/YOUR_USERNAME/edu-na-bazar.git
cd edu-na-bazar
```

### Если нет Git (загружаем архив):

**На локальной машине:**
```powershell
# Создать архив
cd C:\python\edu-na-bazar
tar.exe -czf edu-na-bazar.tar.gz --exclude=node_modules --exclude=venv --exclude=__pycache__ --exclude=.git .

# Загрузить на сервер
scp edu-na-bazar.tar.gz root@176.99.5.211:/opt/
```

**На сервере:**
```bash
cd /opt
tar -xzf edu-na-bazar.tar.gz
mv edu-na-bazar-main edu-na-bazar  # Если нужно
cd edu-na-bazar
```

---

## Шаг 4: Настройка .env

```bash
cd /opt/edu-na-bazar

# Создать .env из примера
cp .env.example .env

# Отредактировать
nano .env
```

### Настроить следующие параметры:

```env
# Environment
ENVIRONMENT=production

# Database
POSTGRES_DB=edu_na_bazar
POSTGRES_USER=postgres
POSTGRES_PASSWORD=СГЕНЕРИРОВАТЬ_НИЖЕ

# Redis
REDIS_URL=redis://redis:6379/0

# Security - ВАЖНО!
SECRET_KEY=СГЕНЕРИРОВАТЬ_НИЖЕ

# CORS - указать ваш домен (или оставить localhost пока нет домена)
ALLOWED_ORIGINS=http://176.99.5.211,http://localhost

# SMS (пока отключено)
SMS_ENABLED=false
SMSC_LOGIN=your_login
SMSC_PASSWORD=your_password

# Mapbox (если нужна карта)
MAPBOX_ACCESS_TOKEN=
REACT_APP_MAPBOX_TOKEN=

# API URL
REACT_APP_API_URL=http://176.99.5.211:8000
```

### Сгенерировать пароли:

```bash
# SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
# Скопировать результат в SECRET_KEY

# POSTGRES_PASSWORD
openssl rand -base64 24
# Скопировать результат в POSTGRES_PASSWORD

# Сохранить (Ctrl+X, Y, Enter)
```

---

## Шаг 5: Запуск контейнеров

```bash
cd /opt/edu-na-bazar

# Запустить все контейнеры
docker-compose up -d --build

# Это займет 5-10 минут при первом запуске

# Проверить статус
docker-compose ps

# Должны быть запущены:
# - edu-na-bazar-postgres
# - edu-na-bazar-redis
# - edu-na-bazar-backend
# - edu-na-bazar-frontend
```

---

## Шаг 6: Применить миграции БД

```bash
# Подождать 30 секунд пока БД запустится
sleep 30

# Применить миграции
docker-compose exec -T backend alembic upgrade head

# Проверить версию
docker-compose exec -T backend alembic current
# Должно показать: 8828a8665651 (head)
```

---

## Шаг 7: Загрузить изображения

**На локальной машине:**
```powershell
# Создать архив
cd C:\python\edu-na-bazar
.\CREATE_UPLOADS_ARCHIVE.bat

# Загрузить на сервер
scp uploads.zip root@176.99.5.211:/opt/edu-na-bazar/
```

**На сервере:**
```bash
cd /opt/edu-na-bazar

# Распаковать в контейнер
chmod +x DEPLOY_UPLOADS.sh
./DEPLOY_UPLOADS.sh

# Или вручную:
docker cp uploads.zip edu-na-bazar-backend:/tmp/
docker exec edu-na-bazar-backend unzip -o /tmp/uploads.zip -d /app/
docker exec edu-na-bazar-backend rm /tmp/uploads.zip
docker exec edu-na-bazar-backend chmod -R 755 /app/uploads/
```

---

## Шаг 8: Проверка работы

```bash
# Проверить контейнеры
docker-compose ps

# Проверить API
curl http://localhost:8000/api/health
# Должно вернуть: {"status":"ok"}

# Проверить Frontend
curl http://localhost
# Должен вернуть HTML

# Проверить изображения
docker exec edu-na-bazar-backend ls -la /app/uploads/products/original/ | head -20

# Проверить логи
docker-compose logs -f backend
# Ctrl+C для выхода
```

---

## Шаг 9: Настройка firewall

```bash
# Установить UFW
apt install -y ufw

# Разрешить SSH (ВАЖНО! Иначе потеряете доступ)
ufw allow 22/tcp

# Разрешить HTTP/HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Разрешить порты приложения (временно, пока нет Nginx)
ufw allow 8000/tcp
ufw allow 3000/tcp

# Включить firewall
ufw --force enable

# Проверить
ufw status
```

---

## Шаг 10: Проверка через браузер

Откройте в браузере:

1. **Frontend**: http://176.99.5.211
2. **API Health**: http://176.99.5.211:8000/api/health
3. **API Docs**: http://176.99.5.211:8000/docs
4. **Категории**: http://176.99.5.211:8000/api/categories

Если все открывается - **поздравляю, базовый деплой готов!** 🎉

---

## Шаг 11: Настройка мониторинга (10 минут)

### UptimeRobot:

```
1. Зарегистрироваться на uptimerobot.com
2. Добавить мониторы:
   - http://176.99.5.211 (Frontend)
   - http://176.99.5.211:8000/api/health (API)
3. Настроить Email уведомления
```

### Telegram Bot:

```bash
# 1. Создать бота через @BotFather
# 2. Получить BOT_TOKEN и CHAT_ID

# 3. Настроить скрипт
cd /opt/edu-na-bazar
nano uptime-monitor.sh

# Заменить:
BOT_TOKEN="YOUR_BOT_TOKEN"
CHAT_ID="YOUR_CHAT_ID"
FRONTEND_URL="http://176.99.5.211"
API_HEALTH_URL="http://176.99.5.211:8000/api/health"

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

## Шаг 12: Настройка backup (5 минут)

```bash
# Создать директорию
mkdir -p /backups

# Настроить скрипт
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

## ✅ Базовый деплой завершен!

### Что работает:
- ✅ Docker контейнеры запущены
- ✅ БД с миграциями
- ✅ Изображения загружены
- ✅ API доступен
- ✅ Frontend доступен
- ✅ Firewall настроен
- ✅ Мониторинг настроен
- ✅ Backup настроен

### Доступ:
- 🌐 Frontend: http://176.99.5.211
- 🔌 API: http://176.99.5.211:8000/api/health
- 📚 API Docs: http://176.99.5.211:8000/docs

---

## 🎯 Следующие шаги (опционально)

### 1. Настроить домен (если есть)

**В панели REG.RU:**
```
DNS настройки:
A запись: @ → 176.99.5.211
A запись: www → 176.99.5.211
```

**На сервере:**
```bash
# Установить Nginx
apt install -y nginx certbot python3-certbot-nginx

# Создать конфигурацию
nano /etc/nginx/sites-available/edu-na-bazar
# Скопировать конфигурацию из DEPLOY_REGRU.md

# Активировать
ln -s /etc/nginx/sites-available/edu-na-bazar /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx

# Получить SSL
certbot --nginx -d yourdomain.ru -d www.yourdomain.ru
```

### 2. Настроить CI/CD

Следовать инструкции в `CICD_SETUP_REGRU.md`

---

## 🐛 Если что-то не работает

### Контейнеры не запускаются:
```bash
docker-compose logs backend
docker-compose logs frontend
docker-compose down
docker-compose up -d --build
```

### Сайт не открывается:
```bash
# Проверить firewall
ufw status

# Проверить порты
netstat -tulpn | grep -E ':(80|8000)'

# Проверить контейнеры
docker-compose ps
```

### Изображения не отображаются:
```bash
docker exec edu-na-bazar-backend ls /app/uploads/products/original/
curl http://localhost:8000/uploads/products/original/test.jpg -I
```

---

## 📞 Полезные команды

```bash
# Перезапуск
docker-compose restart

# Остановка
docker-compose stop

# Просмотр логов
docker-compose logs -f

# Просмотр ресурсов
docker stats

# Очистка
docker system prune -a

# Backup БД вручную
docker-compose exec postgres pg_dump -U postgres edu_na_bazar > backup.sql
```

---

**Готово! Проект развернут на сервере REG.RU** 🎉

**Время деплоя: 30-60 минут**
