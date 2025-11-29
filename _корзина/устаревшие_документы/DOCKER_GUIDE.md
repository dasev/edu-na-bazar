# 🐳 Docker Guide - Еду на базар

## 📦 Архитектура контейнеров

### Production (4 контейнера)
```
┌─────────────────────────────────────────┐
│         Frontend (Nginx + React)        │
│         Port: 80, 443                   │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      Backend (FastAPI + Uvicorn)        │
│         Port: 8000                      │
└─────────────────────────────────────────┘
         ↓                    ↓
┌──────────────────┐  ┌──────────────────┐
│   PostgreSQL     │  │      Redis       │
│   + PostGIS      │  │                  │
│   Port: 5432     │  │   Port: 6379     │
└──────────────────┘  └──────────────────┘
```

### Development (4 контейнера с hot-reload)
- Код монтируется через volumes
- Автоматическая перезагрузка при изменениях
- Отладочные инструменты включены

---

## 🚀 Быстрый старт

### 1. Создать .env файл
```bash
copy .env.example .env
```

Обязательно заполните:
- `SECRET_KEY` - криптостойкий ключ (минимум 32 символа)
- `POSTGRES_PASSWORD` - пароль для БД
- `REACT_APP_MAPBOX_TOKEN` - токен Mapbox (опционально)

### 2. Запуск Production
```bash
START_DOCKER.bat
# или
docker-compose up -d --build
```

**Доступ:**
- Frontend: http://localhost
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs (только в dev)

### 3. Запуск Development (с hot-reload)
```bash
START_DOCKER_DEV.bat
# или
docker-compose -f docker-compose.dev.yml up -d --build
```

**Доступ:**
- Frontend: http://localhost:3000 (hot-reload)
- Backend: http://localhost:8000 (hot-reload)
- API Docs: http://localhost:8000/docs

---

## 📋 Управление контейнерами

### Просмотр статуса
```bash
docker-compose ps
```

### Просмотр логов
```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
docker-compose logs -f redis
```

### Остановка
```bash
STOP_DOCKER.bat
# или
docker-compose stop
```

### Перезапуск
```bash
docker-compose restart
docker-compose restart backend  # только backend
```

### Пересборка
```bash
docker-compose up -d --build
docker-compose up -d --build backend  # только backend
```

### Полное удаление (с данными!)
```bash
docker-compose down -v
```

---

## 🔧 Работа с контейнерами

### Выполнение команд внутри контейнера

**Backend:**
```bash
# Bash
docker-compose exec backend bash

# Python shell
docker-compose exec backend python

# Alembic миграции
docker-compose exec backend alembic upgrade head
docker-compose exec backend alembic revision --autogenerate -m "description"
```

**Frontend:**
```bash
# Bash
docker-compose exec frontend sh

# Установка пакетов (в dev режиме)
docker-compose exec frontend npm install package-name
```

**PostgreSQL:**
```bash
# psql
docker-compose exec postgres psql -U postgres -d edu_na_bazar

# Backup
docker-compose exec postgres pg_dump -U postgres edu_na_bazar > backup.sql

# Restore
docker-compose exec -T postgres psql -U postgres edu_na_bazar < backup.sql
```

**Redis:**
```bash
# redis-cli
docker-compose exec redis redis-cli

# Очистка кэша
docker-compose exec redis redis-cli FLUSHALL
```

---

## 📁 Volumes (Постоянное хранение данных)

### Production
- `postgres_data` - данные PostgreSQL
- `redis_data` - данные Redis
- `backend_uploads` - загруженные файлы

### Development
- `./backend:/app` - код backend (hot-reload)
- `./frontend:/app` - код frontend (hot-reload)
- `/app/node_modules` - node_modules (не монтируется)
- `/app/venv` - venv (не монтируется)

### Просмотр volumes
```bash
docker volume ls
docker volume inspect edu-na-bazar_postgres_data
```

### Backup volumes
```bash
docker run --rm -v edu-na-bazar_postgres_data:/data -v %cd%:/backup alpine tar czf /backup/postgres_backup.tar.gz /data
```

---

## 🌐 Сети

### Production/Development
- `app-network` / `dev-network` - bridge сеть для всех контейнеров

### Внутренние адреса
- `postgres:5432` - PostgreSQL (внутри сети)
- `redis:6379` - Redis (внутри сети)
- `backend:8000` - Backend (внутри сети)

---

## 🐛 Troubleshooting

### Контейнер не запускается
```bash
# Проверить логи
docker-compose logs backend

# Проверить health check
docker-compose ps
```

### Порт занят
```bash
# Найти процесс
netstat -ano | findstr :8000

# Убить процесс
taskkill /PID <PID> /F

# Или изменить порт в docker-compose.yml
```

### База данных не подключается
```bash
# Проверить health check
docker-compose ps postgres

# Проверить логи
docker-compose logs postgres

# Пересоздать контейнер
docker-compose up -d --force-recreate postgres
```

### Изменения не применяются (dev режим)
```bash
# Проверить volumes
docker-compose -f docker-compose.dev.yml config

# Пересобрать без кэша
docker-compose -f docker-compose.dev.yml build --no-cache

# Перезапустить
docker-compose -f docker-compose.dev.yml restart
```

### Ошибки сборки
```bash
# Очистить кэш Docker
docker system prune -a

# Пересобрать
docker-compose build --no-cache
```

---

## 🔐 Безопасность

### Production checklist
- ✅ Сгенерировать криптостойкий `SECRET_KEY`
- ✅ Установить сильный `POSTGRES_PASSWORD`
- ✅ Настроить `ALLOWED_ORIGINS` (только нужные домены)
- ✅ Установить `ENVIRONMENT=production`
- ✅ Отключить API docs в production (автоматически)
- ✅ Использовать HTTPS (настроить SSL)
- ✅ Регулярные backup'ы БД

### Генерация SECRET_KEY
```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -hex 32
```

---

## 📊 Мониторинг

### Использование ресурсов
```bash
docker stats
```

### Размер образов
```bash
docker images
```

### Очистка неиспользуемых ресурсов
```bash
# Осторожно! Удалит все неиспользуемые образы, контейнеры, сети
docker system prune -a
```

---

## 🚀 Деплой на сервер

### 1. Подготовка сервера
```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Установка Docker Compose
apt install docker-compose-plugin -y
```

### 2. Копирование файлов
```bash
scp -r . user@server:/opt/edu-na-bazar
```

### 3. Настройка .env
```bash
ssh user@server
cd /opt/edu-na-bazar
nano .env
# Заполнить production значения
```

### 4. Запуск
```bash
docker-compose up -d --build
```

### 5. Настройка Nginx (на хосте)
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📚 Дополнительно

### Docker Compose файлы
- `docker-compose.yml` - Production (4 контейнера)
- `docker-compose.dev.yml` - Development (hot-reload)
- `docker-compose.prod.yml` - Production для CI/CD

### Dockerfiles
- `backend/Dockerfile` - Production (multi-stage)
- `backend/Dockerfile.dev` - Development (hot-reload)
- `frontend/Dockerfile` - Production (multi-stage)
- `frontend/Dockerfile.dev` - Development (hot-reload)

### .dockerignore
- `backend/.dockerignore` - исключения для backend
- `frontend/.dockerignore` - исключения для frontend

---

## ✅ Готово!

Теперь весь проект работает в контейнерах:
- ✅ Изолированное окружение
- ✅ Легкий деплой на любой сервер
- ✅ Консистентность между dev и prod
- ✅ Hot-reload в development
- ✅ Автоматические health checks
- ✅ Персистентность данных

**Следующие шаги:**
1. Настроить CI/CD (GitHub Actions)
2. Добавить SSL сертификаты
3. Настроить мониторинг
4. Настроить backup стратегию
