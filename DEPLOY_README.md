# 🚀 Деплой на REG.RU - Быстрый старт

## 📋 Что у вас должно быть

После аренды сервера на REG.RU:
- ✅ IP адрес сервера
- ✅ Root пароль
- ✅ Домен (опционально, но рекомендуется)

---

## ⚡ Вариант 1: Автоматический деплой (15 минут)

### На локальной машине:

```powershell
# 1. Загрузить скрипт на сервер
scp QUICK_DEPLOY.sh root@YOUR_SERVER_IP:/root/

# 2. Загрузить проект (если нет Git)
# Создать архив
tar -czf edu-na-bazar.tar.gz --exclude='node_modules' --exclude='venv' --exclude='__pycache__' --exclude='.git' .

# Загрузить
scp edu-na-bazar.tar.gz root@YOUR_SERVER_IP:/opt/
```

### На сервере:

```bash
# 1. Подключиться
ssh root@YOUR_SERVER_IP

# 2. Запустить скрипт
bash /root/QUICK_DEPLOY.sh

# Скрипт автоматически:
# - Установит Docker
# - Установит Docker Compose
# - Клонирует проект (или распакует архив)
# - Создаст .env с автогенерированными паролями
# - Запустит контейнеры
# - Применит миграции
# - Настроит firewall

# 3. Следовать инструкциям на экране
```

---

## 📖 Вариант 2: Ручной деплой (1 час)

Следуйте подробной инструкции в **`DEPLOY_REGRU.md`**

---

## 🎯 После установки

### 1. Загрузить изображения (5 минут)

**На локальной машине:**
```powershell
# Создать архив
.\CREATE_UPLOADS_ARCHIVE.bat

# Загрузить на сервер
scp uploads.zip root@YOUR_SERVER_IP:/opt/edu-na-bazar/
```

**На сервере:**
```bash
cd /opt/edu-na-bazar
chmod +x DEPLOY_UPLOADS.sh
./DEPLOY_UPLOADS.sh
```

### 2. Настроить домен и SSL (15 минут)

**Если у вас есть домен:**

1. В панели REG.RU настроить DNS:
   - A запись: `@` → IP сервера
   - A запись: `www` → IP сервера

2. Подождать 5-15 минут (пока DNS обновится)

3. На сервере настроить Nginx:
```bash
# Создать конфигурацию
nano /etc/nginx/sites-available/edu-na-bazar

# Скопировать конфигурацию из DEPLOY_REGRU.md
# Заменить yourdomain.ru на ваш домен

# Активировать
ln -s /etc/nginx/sites-available/edu-na-bazar /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx

# Получить SSL сертификат
certbot --nginx -d yourdomain.ru -d www.yourdomain.ru
```

### 3. Настроить мониторинг (10 минут)

**UptimeRobot (3 минуты):**
1. Зарегистрироваться на https://uptimerobot.com
2. Добавить мониторы:
   - `https://yourdomain.ru` (Frontend)
   - `https://yourdomain.ru/api/health` (API)
3. Настроить Email уведомления

**Telegram Bot (5 минут):**
```bash
# 1. Создать бота через @BotFather
# 2. Получить BOT_TOKEN и CHAT_ID

# 3. Настроить скрипт
cd /opt/edu-na-bazar
nano uptime-monitor.sh
# Заменить BOT_TOKEN, CHAT_ID, домен

# 4. Добавить в cron
chmod +x uptime-monitor.sh
crontab -e
# Добавить: */5 * * * * /opt/edu-na-bazar/uptime-monitor.sh
```

### 4. Настроить backup (5 минут)

```bash
# Создать директорию
mkdir -p /backups

# Настроить автоматический backup
chmod +x /opt/edu-na-bazar/backup.sh
crontab -e
# Добавить: 0 2 * * * /opt/edu-na-bazar/backup.sh >> /var/log/backup.log 2>&1

# Протестировать
/opt/edu-na-bazar/backup.sh
ls -lh /backups/
```

---

## ✅ Проверка

```bash
# 1. Проверить контейнеры
docker-compose ps

# 2. Проверить API
curl http://localhost:8000/api/health
# Должно вернуть: {"status":"ok"}

# 3. Проверить Frontend
curl http://localhost

# 4. Проверить через домен
curl https://yourdomain.ru/api/health

# 5. Открыть в браузере
# https://yourdomain.ru
```

---

## 🐛 Проблемы?

### Контейнеры не запускаются:
```bash
docker-compose logs backend
docker-compose logs frontend
docker-compose down
docker-compose up -d --build
```

### Сайт не открывается:
```bash
# Проверить Nginx
systemctl status nginx
nginx -t

# Проверить firewall
ufw status

# Проверить порты
netstat -tulpn | grep -E ':(80|443|8000)'
```

### Изображения не отображаются:
```bash
# Проверить файлы
docker exec edu-na-bazar-backend ls -la /app/uploads/products/original/

# Проверить доступ
curl http://localhost:8000/uploads/products/original/test.jpg -I
```

### SSL не работает:
```bash
# Проверить DNS
nslookup yourdomain.ru

# Проверить сертификат
certbot certificates

# Обновить сертификат
certbot renew
```

---

## 📚 Документация

- **`DEPLOY_REGRU.md`** - Полная инструкция по деплою
- **`SETUP_MONITORING.md`** - Настройка мониторинга
- **`UPLOAD_IMAGES_GUIDE.md`** - Загрузка изображений
- **`ALEMBIC_MIGRATIONS.md`** - Работа с миграциями
- **`DOCKER_GUIDE.md`** - Работа с Docker

---

## 📞 Полезные команды

```bash
# Перезапуск
docker-compose restart

# Просмотр логов
docker-compose logs -f

# Обновление проекта
cd /opt/edu-na-bazar
git pull
docker-compose up -d --build

# Backup БД
docker-compose exec postgres pg_dump -U postgres edu_na_bazar > backup.sql

# Очистка Docker
docker system prune -a
```

---

## 🎉 Готово!

Ваш проект развернут и работает!

**Доступ:**
- 🌐 Frontend: `https://yourdomain.ru`
- 🔌 API: `https://yourdomain.ru/api/health`
- 📊 Мониторинг: UptimeRobot + Telegram
- 💾 Backup: Каждый день в 2:00

**Время полного деплоя: 1-1.5 часа**

---

## 🚀 Следующие шаги

1. ✅ Протестировать все функции сайта
2. ✅ Настроить SMS (если нужно)
3. ✅ Добавить контент
4. ✅ Настроить аналитику (Google Analytics, Яндекс.Метрика)
5. ✅ Настроить CDN (Cloudflare)
6. ✅ Оптимизировать производительность

**Успешного запуска!** 🎊
