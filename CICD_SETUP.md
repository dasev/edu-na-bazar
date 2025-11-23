# 🚀 CI/CD Setup для Production

## ✅ Что создано:

1. **`.github/workflows/deploy.yml`** - GitHub Actions workflow
2. **`backend/Dockerfile`** - Docker образ для backend
3. **`frontend/Dockerfile`** - Docker образ для frontend
4. **`frontend/nginx.conf`** - Nginx конфигурация
5. **`docker-compose.prod.yml`** - Production compose

---

## 📋 Что нужно для деплоя:

### 1. **Сервер (VPS/Cloud)**
- Ubuntu 20.04+ / Debian 11+
- Минимум: 2 CPU, 4GB RAM, 40GB SSD
- Docker и Docker Compose установлены
- Открыты порты: 80, 443, 22

### 2. **Docker Hub аккаунт**
- Регистрация: https://hub.docker.com/signup
- Создайте Access Token

### 3. **GitHub Secrets**
Добавьте в Settings → Secrets and variables → Actions:

```
DOCKER_USERNAME=ваш_docker_username
DOCKER_PASSWORD=ваш_docker_token
SERVER_HOST=IP_вашего_сервера
SERVER_USER=root (или другой пользователь)
SSH_PRIVATE_KEY=ваш_приватный_SSH_ключ
API_URL=https://api.yourdomain.com
```

---

## 🔧 Пошаговая настройка:

### Шаг 1: Создайте Docker Hub аккаунт

1. Откройте: https://hub.docker.com/signup
2. Зарегистрируйтесь
3. Account Settings → Security → New Access Token
4. Скопируйте токен

### Шаг 2: Настройте GitHub Secrets

1. Откройте: https://github.com/dasev/edu-na-bazar/settings/secrets/actions
2. Нажмите "New repository secret"
3. Добавьте каждый secret:

**DOCKER_USERNAME:**
```
ваш_docker_username
```

**DOCKER_PASSWORD:**
```
ваш_docker_access_token
```

**SERVER_HOST:**
```
123.456.789.012  (IP вашего сервера)
```

**SERVER_USER:**
```
root
```

**SSH_PRIVATE_KEY:**
```
-----BEGIN OPENSSH PRIVATE KEY-----
ваш_приватный_ключ
-----END OPENSSH PRIVATE KEY-----
```

**API_URL:**
```
https://api.yourdomain.com
```

### Шаг 3: Настройте сервер

Подключитесь к серверу:
```bash
ssh root@ваш_сервер_ip
```

Установите Docker:
```bash
# Обновление системы
apt update && apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Установка Docker Compose
apt install docker-compose-plugin -y

# Проверка
docker --version
docker compose version
```

Создайте директорию проекта:
```bash
mkdir -p /opt/edu-na-bazar
cd /opt/edu-na-bazar
```

Создайте `.env` файл:
```bash
nano .env
```

Содержимое:
```env
# Database
POSTGRES_DB=edu_na_bazar
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password_here

# Backend
SECRET_KEY=your_secret_key_here
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Docker
DOCKER_USERNAME=ваш_docker_username
```

Скопируйте `docker-compose.prod.yml` на сервер:
```bash
# На локальной машине:
scp docker-compose.prod.yml root@ваш_ip:/opt/edu-na-bazar/docker-compose.yml
```

### Шаг 4: Настройте SSH ключи

Если у вас нет SSH ключа:
```bash
# На локальной машине:
ssh-keygen -t ed25519 -C "deploy@edu-na-bazar"
```

Скопируйте публичный ключ на сервер:
```bash
ssh-copy-id root@ваш_сервер_ip
```

Скопируйте приватный ключ в GitHub Secrets:
```bash
cat ~/.ssh/id_ed25519
# Скопируйте весь вывод в GitHub Secret SSH_PRIVATE_KEY
```

### Шаг 5: Первый деплой

Сделайте коммит и push:
```bash
git add .
git commit -m "🚀 Add CI/CD configuration"
git push
```

GitHub Actions автоматически:
1. Соберет Docker образы
2. Загрузит их в Docker Hub
3. Подключится к серверу
4. Запустит контейнеры

Проверьте: https://github.com/dasev/edu-na-bazar/actions

---

## 🌐 Настройка домена (опционально)

### Вариант 1: Cloudflare (бесплатно)

1. Зарегистрируйтесь: https://cloudflare.com
2. Добавьте домен
3. Настройте DNS:
   ```
   A    @         ваш_сервер_ip
   A    www       ваш_сервер_ip
   A    api       ваш_сервер_ip
   ```
4. Включите SSL/TLS (Full)

### Вариант 2: Let's Encrypt (бесплатно)

На сервере:
```bash
# Установка Certbot
apt install certbot python3-certbot-nginx -y

# Получение сертификата
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## 📊 Мониторинг

### Проверка статуса:
```bash
# На сервере
docker ps
docker logs edu-na-bazar-backend-prod
docker logs edu-na-bazar-frontend-prod
```

### Health checks:
```bash
# Backend
curl http://localhost:8000/health

# Frontend
curl http://localhost/health
```

---

## 🔄 Обновление проекта

После каждого push в main:
1. GitHub Actions автоматически соберет новые образы
2. Загрузит их в Docker Hub
3. Обновит контейнеры на сервере

Вручную:
```bash
# На сервере
cd /opt/edu-na-bazar
docker compose pull
docker compose up -d --force-recreate
```

---

## 🐛 Troubleshooting

### Проблема: GitHub Actions не запускается
**Решение:** Проверьте Actions → Settings → Actions → General → Allow all actions

### Проблема: Docker build fails
**Решение:** Проверьте Dockerfile и зависимости

### Проблема: SSH connection failed
**Решение:** Проверьте SSH_PRIVATE_KEY secret (должен быть полный ключ с заголовками)

### Проблема: Контейнеры не запускаются
**Решение:** 
```bash
docker logs <container_name>
docker compose logs
```

---

## 📦 Альтернативные платформы

### 1. **Vercel** (Frontend only)
- Бесплатно для фронтенда
- Автоматический деплой из GitHub
- https://vercel.com

### 2. **Railway** (Full stack)
- $5/месяц
- Автоматический деплой
- https://railway.app

### 3. **Render** (Full stack)
- Бесплатный tier
- Автоматический деплой
- https://render.com

### 4. **DigitalOcean App Platform**
- От $5/месяц
- Managed платформа
- https://digitalocean.com

---

## ✅ Checklist перед деплоем

- [ ] Docker Hub аккаунт создан
- [ ] GitHub Secrets добавлены (все 6)
- [ ] Сервер настроен (Docker установлен)
- [ ] SSH ключи настроены
- [ ] `.env` файл создан на сервере
- [ ] Домен настроен (опционально)
- [ ] SSL сертификат получен (опционально)
- [ ] Первый push сделан
- [ ] GitHub Actions успешно выполнен

---

## 🎉 Готово!

После настройки каждый push в `main` будет автоматически деплоиться на продакшен!

**Workflow:**
```
git add .
git commit -m "✨ New feature"
git push
→ GitHub Actions → Docker Hub → Production Server → Live! 🚀
```
