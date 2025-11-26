# 🔒 Настройка SSL сертификатов Let's Encrypt

## 📋 Предварительные требования

- ✅ Сервер развернут и работает (176.99.5.211)
- ✅ Docker контейнеры запущены
- ⏳ **Домен привязан к серверу** (DNS A-запись)
- ⏳ Порты 80 и 443 открыты

---

## 🌐 Шаг 1: Привязка домена

### 1.1 Купить/настроить домен

Если домена еще нет:
- Купить на REG.RU, Cloudflare, Namecheap и т.д.
- Рекомендуемые варианты: `edunabazar.ru`, `edunabazar.com`

### 1.2 Настроить DNS записи

В панели управления доменом добавить A-записи:

```
Тип    Имя    Значение           TTL
A      @      176.99.5.211       3600
A      www    176.99.5.211       3600
```

**Проверка DNS (выполнить локально):**
```bash
# Проверить основной домен
nslookup edunabazar.ru

# Проверить www
nslookup www.edunabazar.ru

# Должны вернуть IP: 176.99.5.211
```

⏰ **Важно:** DNS изменения могут занять от 5 минут до 48 часов.

---

## 🚀 Шаг 2: Подготовка сервера

### 2.1 Подключиться к серверу

```bash
ssh root@176.99.5.211
# Пароль: sIAS6APDsKh0bL
```

### 2.2 Остановить Docker контейнеры

```bash
cd /opt/edu-na-bazar
docker-compose down
```

### 2.3 Установить Certbot

```bash
# Обновить систему
apt update

# Установить Certbot и плагин для Nginx
apt install -y certbot python3-certbot-nginx

# Проверить установку
certbot --version
```

---

## 🔐 Шаг 3: Получение SSL сертификатов

### Вариант A: Автоматическая настройка (рекомендуется)

```bash
# Certbot автоматически настроит Nginx
certbot --nginx -d edunabazar.ru -d www.edunabazar.ru

# Следовать инструкциям:
# 1. Ввести email для уведомлений
# 2. Согласиться с Terms of Service (Y)
# 3. Выбрать: Redirect HTTP to HTTPS (2)
```

### Вариант B: Только получить сертификаты (ручная настройка)

```bash
# Получить сертификаты без изменения конфигурации
certbot certonly --standalone -d edunabazar.ru -d www.edunabazar.ru

# Сертификаты будут сохранены в:
# /etc/letsencrypt/live/edunabazar.ru/fullchain.pem
# /etc/letsencrypt/live/edunabazar.ru/privkey.pem
```

---

## 📝 Шаг 4: Настройка Nginx в Docker

### 4.1 Создать конфигурацию Nginx с SSL

Создать файл `frontend/nginx-ssl.conf`:

```nginx
# HTTP -> HTTPS redirect
server {
    listen 80;
    server_name edunabazar.ru www.edunabazar.ru;
    
    # Let's Encrypt challenge
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    
    # Redirect all HTTP to HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name edunabazar.ru www.edunabazar.ru;
    
    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/edunabazar.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/edunabazar.ru/privkey.pem;
    
    # SSL configuration (Mozilla Intermediate)
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/edunabazar.ru/chain.pem;
    
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
        try_files $uri $uri/ /index.html;
    }
    
    # API proxy to backend
    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;
    }
    
    # Static files (uploads)
    location /uploads {
        proxy_pass http://backend:8000/uploads;
        proxy_set_header Host $host;
    }
    
    # Health check
    location /health {
        access_log off;
        return 200 "OK\n";
        add_header Content-Type text/plain;
    }
}
```

### 4.2 Обновить Dockerfile frontend

Изменить `frontend/Dockerfile`:

```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build arguments
ARG VITE_API_URL
ARG VITE_MAPBOX_TOKEN

# Set environment variables for build
ENV VITE_API_URL=$VITE_API_URL
ENV VITE_MAPBOX_TOKEN=$VITE_MAPBOX_TOKEN

# Build app
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy custom nginx config
COPY nginx-ssl.conf /etc/nginx/conf.d/default.conf

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

# Create directory for certbot challenges
RUN mkdir -p /var/www/certbot

# Expose ports
EXPOSE 80 443

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/health || exit 1

CMD ["nginx", "-g", "daemon off;"]
```

### 4.3 Обновить docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgis/postgis:15-3.4
    container_name: edu-na-bazar-postgres
    environment:
      POSTGRES_DB: edu_na_bazar
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: edu-na-bazar-redis
    command: redis-server --appendonly yes
    ports:
      - "6380:6379"
    volumes:
      - redis_data:/data
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: edu-na-bazar-backend
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:${POSTGRES_PASSWORD}@postgres:5432/edu_na_bazar
      REDIS_URL: redis://redis:6379/0
      SECRET_KEY: ${SECRET_KEY}
      ENVIRONMENT: ${ENVIRONMENT:-production}
      SMS_ENABLED: ${SMS_ENABLED:-false}
      SMSC_LOGIN: ${SMSC_LOGIN:-}
      SMSC_PASSWORD: ${SMSC_PASSWORD:-}
      MAPBOX_ACCESS_TOKEN: ${MAPBOX_ACCESS_TOKEN:-}
      ALLOWED_ORIGINS: ${ALLOWED_ORIGINS}
    volumes:
      - backend_uploads:/app/uploads
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - app-network
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      args:
        VITE_API_URL: ${REACT_APP_API_URL}
        VITE_MAPBOX_TOKEN: ${VITE_MAPBOX_TOKEN}
    container_name: edu-na-bazar-frontend
    ports:
      - "80:80"
      - "443:443"
    volumes:
      # Mount SSL certificates
      - /etc/letsencrypt:/etc/letsencrypt:ro
      - /var/www/certbot:/var/www/certbot
    depends_on:
      - backend
    networks:
      - app-network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  backend_uploads:

networks:
  app-network:
    driver: bridge
```

### 4.4 Обновить .env

```env
# Domain
DOMAIN=edunabazar.ru

# CORS Origins (с HTTPS!)
ALLOWED_ORIGINS=https://edunabazar.ru,https://www.edunabazar.ru

# API URL (с HTTPS!)
REACT_APP_API_URL=https://edunabazar.ru

# Остальные настройки...
ENVIRONMENT=production
SECRET_KEY=your-secret-key-here
POSTGRES_PASSWORD=your-postgres-password
```

---

## 🔄 Шаг 5: Перезапуск с SSL

```bash
# Пересобрать и запустить контейнеры
docker-compose build --no-cache frontend
docker-compose up -d

# Проверить логи
docker-compose logs -f frontend

# Проверить статус
docker-compose ps
```

---

## ✅ Шаг 6: Проверка SSL

### 6.1 Проверить в браузере

Открыть: `https://edunabazar.ru`

Должен быть:
- ✅ Зеленый замочек в адресной строке
- ✅ Сертификат от Let's Encrypt
- ✅ Автоматический редирект с HTTP на HTTPS

### 6.2 Проверить через SSL Labs

Открыть: https://www.ssllabs.com/ssltest/analyze.html?d=edunabazar.ru

Должна быть оценка: **A или A+**

### 6.3 Проверить через curl

```bash
# Проверить HTTP -> HTTPS редирект
curl -I http://edunabazar.ru

# Должен вернуть: 301 Moved Permanently
# Location: https://edunabazar.ru

# Проверить HTTPS
curl -I https://edunabazar.ru

# Должен вернуть: 200 OK
```

---

## 🔄 Шаг 7: Автоматическое обновление сертификатов

### 7.1 Настроить cron для обновления

Let's Encrypt сертификаты действительны 90 дней. Нужно автоматически обновлять.

```bash
# Открыть crontab
crontab -e

# Добавить задачу (проверка каждый день в 3:00)
0 3 * * * certbot renew --quiet --post-hook "docker-compose -f /opt/edu-na-bazar/docker-compose.yml restart frontend"
```

### 7.2 Проверить автообновление

```bash
# Тестовый запуск обновления (dry-run)
certbot renew --dry-run

# Должен вывести: Congratulations, all simulated renewals succeeded
```

---

## 🐛 Troubleshooting

### Проблема: "Connection refused" при получении сертификата

**Причина:** Порт 80 занят или закрыт

**Решение:**
```bash
# Остановить все контейнеры
docker-compose down

# Проверить что порт 80 свободен
netstat -tulpn | grep :80

# Получить сертификат
certbot certonly --standalone -d edunabazar.ru -d www.edunabazar.ru

# Запустить контейнеры
docker-compose up -d
```

### Проблема: "DNS problem: NXDOMAIN"

**Причина:** DNS записи еще не распространились

**Решение:**
```bash
# Проверить DNS
nslookup edunabazar.ru

# Подождать 1-24 часа
# Попробовать снова
```

### Проблема: Nginx не запускается с SSL

**Причина:** Неправильные пути к сертификатам

**Решение:**
```bash
# Проверить что сертификаты существуют
ls -la /etc/letsencrypt/live/edunabazar.ru/

# Должны быть файлы:
# - fullchain.pem
# - privkey.pem
# - chain.pem

# Проверить логи Nginx
docker-compose logs frontend
```

### Проблема: Mixed Content (HTTP ресурсы на HTTPS странице)

**Причина:** API или изображения загружаются по HTTP

**Решение:**
```bash
# Убедиться что в .env указан HTTPS
REACT_APP_API_URL=https://edunabazar.ru

# Пересобрать frontend
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

---

## 📋 Чеклист настройки SSL

- [ ] Домен куплен и привязан к серверу (DNS A-записи)
- [ ] DNS записи распространились (проверить через nslookup)
- [ ] Порты 80 и 443 открыты на сервере
- [ ] Certbot установлен
- [ ] SSL сертификаты получены
- [ ] nginx-ssl.conf создан
- [ ] Dockerfile frontend обновлен
- [ ] docker-compose.yml обновлен (volumes для сертификатов)
- [ ] .env обновлен (HTTPS URLs)
- [ ] Контейнеры пересобраны и запущены
- [ ] HTTPS работает (зеленый замочек)
- [ ] HTTP редиректит на HTTPS
- [ ] SSL Labs оценка A/A+
- [ ] Cron для автообновления настроен
- [ ] Тестовое обновление прошло успешно

---

## 🎯 Быстрая команда для всего процесса

После привязки домена и распространения DNS:

```bash
# На сервере (176.99.5.211)
cd /opt/edu-na-bazar

# 1. Остановить контейнеры
docker-compose down

# 2. Установить Certbot
apt update && apt install -y certbot python3-certbot-nginx

# 3. Получить сертификаты
certbot certonly --standalone -d edunabazar.ru -d www.edunabazar.ru

# 4. Обновить конфигурацию (скопировать nginx-ssl.conf, обновить docker-compose.yml)

# 5. Обновить .env
nano .env
# Изменить URLs на HTTPS

# 6. Пересобрать и запустить
docker-compose build --no-cache frontend
docker-compose up -d

# 7. Настроить автообновление
crontab -e
# Добавить: 0 3 * * * certbot renew --quiet --post-hook "docker-compose -f /opt/edu-na-bazar/docker-compose.yml restart frontend"

# 8. Проверить
curl -I https://edunabazar.ru
```

---

## 📚 Дополнительные ресурсы

- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Certbot Documentation](https://certbot.eff.org/docs/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [SSL Labs Test](https://www.ssllabs.com/ssltest/)

---

## 🎉 Результат

После выполнения всех шагов:
- ✅ Сайт доступен по HTTPS с валидным сертификатом
- ✅ Автоматический редирект с HTTP на HTTPS
- ✅ Оценка безопасности A/A+ на SSL Labs
- ✅ Автоматическое обновление сертификатов каждые 90 дней
- ✅ Все данные передаются в зашифрованном виде

**Ваш проект полностью защищен и готов к production!** 🔒
