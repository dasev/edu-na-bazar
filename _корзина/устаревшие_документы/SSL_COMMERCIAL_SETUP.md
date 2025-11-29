# 🔐 Установка купленного SSL сертификата

## 📋 Что нужно иметь

После покупки SSL сертификата у провайдера (REG.RU, Comodo, DigiCert и т.д.) вы получите:

1. **Сертификат домена** - `your_domain.crt` или `certificate.crt`
2. **Приватный ключ** - `private.key` (создается при генерации CSR)
3. **Промежуточные сертификаты** - `ca_bundle.crt` или `intermediate.crt`
4. **Корневой сертификат** (опционально) - `root.crt`

---

## 🚀 Быстрая установка

### Шаг 1: Подготовка файлов сертификатов

**На локальной машине:**

Создайте папку с вашими сертификатами:
```
ssl-certs/
├── certificate.crt          # Ваш сертификат
├── private.key             # Приватный ключ
├── ca_bundle.crt           # Промежуточные сертификаты
└── fullchain.crt           # (создадим позже)
```

### Шаг 2: Создание fullchain.crt

Объединить сертификат домена и промежуточные сертификаты:

**Windows (PowerShell):**
```powershell
# Объединить сертификаты
Get-Content certificate.crt, ca_bundle.crt | Set-Content fullchain.crt
```

**Linux/Mac:**
```bash
cat certificate.crt ca_bundle.crt > fullchain.crt
```

**Проверка порядка:**
```
fullchain.crt должен содержать:
1. Ваш сертификат (-----BEGIN CERTIFICATE-----)
2. Промежуточный сертификат
3. Корневой сертификат (если есть)
```

### Шаг 3: Загрузка на сервер

**Создать директорию для сертификатов:**
```bash
ssh root@176.99.5.211
# Пароль: sIAS6APDsKh0bL

# Создать директорию
mkdir -p /etc/ssl/edunabazar.ru
chmod 700 /etc/ssl/edunabazar.ru
```

**Загрузить файлы (с локальной машины):**
```powershell
# Загрузить сертификаты
scp fullchain.crt root@176.99.5.211:/etc/ssl/edunabazar.ru/
scp private.key root@176.99.5.211:/etc/ssl/edunabazar.ru/
scp ca_bundle.crt root@176.99.5.211:/etc/ssl/edunabazar.ru/

# Пароль: sIAS6APDsKh0bL
```

**Установить правильные права:**
```bash
# На сервере
chmod 644 /etc/ssl/edunabazar.ru/fullchain.crt
chmod 644 /etc/ssl/edunabazar.ru/ca_bundle.crt
chmod 600 /etc/ssl/edunabazar.ru/private.key
```

---

## 📝 Шаг 4: Настройка Nginx

### Создать nginx-ssl.conf

```bash
cd /opt/edu-na-bazar/frontend
nano nginx-ssl.conf
```

**Содержимое:**
```nginx
# HTTP -> HTTPS redirect
server {
    listen 80;
    server_name edunabazar.ru www.edunabazar.ru;
    
    # Redirect all HTTP to HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name edunabazar.ru www.edunabazar.ru;
    
    # SSL certificates (КОММЕРЧЕСКИЙ СЕРТИФИКАТ)
    ssl_certificate /etc/ssl/edunabazar.ru/fullchain.crt;
    ssl_certificate_key /etc/ssl/edunabazar.ru/private.key;
    ssl_trusted_certificate /etc/ssl/edunabazar.ru/ca_bundle.crt;
    
    # SSL configuration (Mozilla Intermediate)
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;
    
    # SSL session cache
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_session_tickets off;
    
    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
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
    gzip_comp_level 6;
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

---

## 🐳 Шаг 5: Обновление Docker конфигурации

### Обновить docker-compose.yml

```bash
cd /opt/edu-na-bazar
nano docker-compose.yml
```

**Добавить volumes в frontend сервис:**
```yaml
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.ssl
      args:
        VITE_API_URL: ${REACT_APP_API_URL}
        VITE_MAPBOX_TOKEN: ${VITE_MAPBOX_TOKEN}
    container_name: edu-na-bazar-frontend
    ports:
      - "80:80"
      - "443:443"
    volumes:
      # Коммерческие SSL сертификаты (read-only)
      - /etc/ssl/edunabazar.ru:/etc/ssl/edunabazar.ru:ro
    depends_on:
      - backend
    networks:
      - app-network
    restart: unless-stopped
```

### Обновить .env

```bash
nano .env
```

**Изменить URLs на HTTPS:**
```env
DOMAIN=edunabazar.ru
ALLOWED_ORIGINS=https://edunabazar.ru,https://www.edunabazar.ru
REACT_APP_API_URL=https://edunabazar.ru
ENVIRONMENT=production
```

---

## 🚀 Шаг 6: Перезапуск

```bash
cd /opt/edu-na-bazar

# Пересобрать frontend
docker-compose build --no-cache frontend

# Запустить все контейнеры
docker-compose up -d

# Проверить логи
docker-compose logs -f frontend
```

---

## ✅ Шаг 7: Проверка

### Проверка в браузере

Открыть: `https://edunabazar.ru`

Должен быть:
- ✅ Зеленый замочек 🔒
- ✅ Сертификат от вашего провайдера (не Let's Encrypt)
- ✅ Автоматический редирект с HTTP на HTTPS

### Проверка через curl

```bash
# HTTP редирект
curl -I http://edunabazar.ru
# Должен вернуть: 301 Moved Permanently

# HTTPS работает
curl -I https://edunabazar.ru
# Должен вернуть: 200 OK

# Проверка сертификата
openssl s_client -connect edunabazar.ru:443 -servername edunabazar.ru
```

### Проверка через SSL Labs

Открыть: https://www.ssllabs.com/ssltest/analyze.html?d=edunabazar.ru

Должна быть оценка: **A или A+**

---

## 🔄 Обновление сертификата (перед истечением)

Коммерческие сертификаты обычно действительны 1-2 года. Перед истечением:

### 1. Получить новый сертификат

От вашего провайдера получите:
- Новый `certificate.crt`
- Новый `ca_bundle.crt`
- Приватный ключ остается тот же (если не перегенерировали CSR)

### 2. Создать новый fullchain.crt

```bash
cat certificate.crt ca_bundle.crt > fullchain.crt
```

### 3. Загрузить на сервер

```bash
# Создать backup старых сертификатов
ssh root@176.99.5.211
cd /etc/ssl/edunabazar.ru
cp fullchain.crt fullchain.crt.old
cp ca_bundle.crt ca_bundle.crt.old

# Загрузить новые (с локальной машины)
scp fullchain.crt root@176.99.5.211:/etc/ssl/edunabazar.ru/
scp ca_bundle.crt root@176.99.5.211:/etc/ssl/edunabazar.ru/
```

### 4. Перезапустить Nginx

```bash
cd /opt/edu-na-bazar
docker-compose restart frontend

# Проверить
curl -I https://edunabazar.ru
```

---

## 🐛 Troubleshooting

### Проблема: "SSL certificate problem"

**Причина:** Неправильный порядок сертификатов в fullchain.crt

**Решение:**
```bash
# Проверить порядок
openssl crl2pkcs7 -nocrl -certfile fullchain.crt | openssl pkcs7 -print_certs -noout

# Должен быть порядок:
# 1. Ваш сертификат (subject=CN=edunabazar.ru)
# 2. Промежуточный сертификат
# 3. Корневой сертификат

# Пересоздать в правильном порядке
cat certificate.crt intermediate.crt root.crt > fullchain.crt
```

---

### Проблема: "Private key does not match certificate"

**Причина:** Приватный ключ не соответствует сертификату

**Решение:**
```bash
# Проверить соответствие
openssl x509 -noout -modulus -in certificate.crt | openssl md5
openssl rsa -noout -modulus -in private.key | openssl md5

# MD5 должны совпадать
# Если не совпадают - используете неправильный ключ
```

---

### Проблема: "Certificate has expired"

**Причина:** Сертификат истек

**Решение:**
```bash
# Проверить срок действия
openssl x509 -in fullchain.crt -noout -dates

# Обновить сертификат у провайдера
```

---

### Проблема: Nginx не запускается

**Причина:** Неправильные пути к сертификатам

**Решение:**
```bash
# Проверить что файлы существуют
ls -la /etc/ssl/edunabazar.ru/

# Должны быть:
# -rw-r--r-- fullchain.crt
# -rw-r--r-- ca_bundle.crt
# -rw------- private.key

# Проверить конфигурацию Nginx
docker-compose exec frontend nginx -t

# Проверить логи
docker-compose logs frontend
```

---

## 📋 Различия между Let's Encrypt и коммерческим

| Параметр | Let's Encrypt | Коммерческий |
|----------|---------------|--------------|
| **Стоимость** | Бесплатно | Платно ($10-$500/год) |
| **Срок действия** | 90 дней | 1-2 года |
| **Автообновление** | Да (certbot) | Нет (вручную) |
| **Wildcard** | Да (DNS challenge) | Да |
| **EV сертификаты** | Нет | Да |
| **Поддержка** | Сообщество | Техподдержка |
| **Доверие** | Высокое | Высокое |
| **Warranty** | Нет | Да ($10k-$1.75M) |

---

## 🎯 Когда использовать коммерческий сертификат

### Используйте коммерческий если:

- ✅ Нужен **EV (Extended Validation)** - зеленая строка в браузере
- ✅ Требуется **warranty** (страховка)
- ✅ Нужна **техподдержка** от провайдера
- ✅ Корпоративные требования
- ✅ Не хотите настраивать автообновление

### Используйте Let's Encrypt если:

- ✅ Бесплатно
- ✅ Автоматическое обновление
- ✅ Подходит для большинства сайтов
- ✅ Быстрая выдача (5 минут)

---

## 📞 Поддержка провайдеров

### REG.RU
- Документация: https://www.reg.ru/support/ssl-sertifikaty
- Поддержка: support@reg.ru
- Телефон: 8 (800) 505-42-85

### Comodo/Sectigo
- Документация: https://sectigo.com/support
- Поддержка: support@sectigo.com

### DigiCert
- Документация: https://www.digicert.com/support
- Поддержка: support@digicert.com

---

## ✅ Чеклист установки

- [ ] Получены все файлы сертификатов
- [ ] Создан fullchain.crt (правильный порядок)
- [ ] Проверено соответствие ключа и сертификата
- [ ] Создана директория /etc/ssl/edunabazar.ru
- [ ] Загружены файлы на сервер
- [ ] Установлены правильные права (600 для ключа)
- [ ] Создан nginx-ssl.conf
- [ ] Обновлен docker-compose.yml (volumes)
- [ ] Обновлен .env (HTTPS URLs)
- [ ] Пересобран frontend контейнер
- [ ] Контейнеры запущены
- [ ] HTTPS работает (зеленый замочек)
- [ ] HTTP редиректит на HTTPS
- [ ] SSL Labs оценка A/A+
- [ ] Добавлено напоминание об обновлении (календарь)

---

## 🎉 Готово!

Ваш коммерческий SSL сертификат установлен и работает!

**Не забудьте:**
- Добавить напоминание об обновлении сертификата (за 1 месяц до истечения)
- Сохранить backup старых сертификатов
- Проверять срок действия: `openssl x509 -in fullchain.crt -noout -dates`

---

## 🔗 Полезные команды

```bash
# Проверить срок действия
openssl x509 -in /etc/ssl/edunabazar.ru/fullchain.crt -noout -dates

# Проверить информацию о сертификате
openssl x509 -in /etc/ssl/edunabazar.ru/fullchain.crt -noout -text

# Проверить цепочку сертификатов
openssl verify -CAfile /etc/ssl/edunabazar.ru/ca_bundle.crt /etc/ssl/edunabazar.ru/fullchain.crt

# Проверить соответствие ключа
openssl x509 -noout -modulus -in certificate.crt | openssl md5
openssl rsa -noout -modulus -in private.key | openssl md5

# Тест SSL соединения
openssl s_client -connect edunabazar.ru:443 -servername edunabazar.ru

# Проверить OCSP
openssl ocsp -issuer ca_bundle.crt -cert certificate.crt -url http://ocsp.provider.com
```

---

**Ваш сайт защищен коммерческим SSL сертификатом! 🔒🎉**
