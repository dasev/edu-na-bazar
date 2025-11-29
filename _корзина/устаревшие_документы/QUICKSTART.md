# ⚡ Быстрый старт "Еду на базар"

## 🚀 Запуск за 5 минут

### Шаг 1: Подготовка

```bash
# Клонировать репозиторий
git clone <repo-url>
cd edu-na-bazar

# Получить Mapbox токен
# https://account.mapbox.com/access-tokens/
```

### Шаг 2: Docker (PostgreSQL + Redis)

```bash
# Запустить контейнеры
docker-compose up -d

# Проверить статус
docker-compose ps
```

### Шаг 3: Backend

```bash
cd backend

# Создать виртуальное окружение
python -m venv venv

# Активировать (Windows)
venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Создать .env файл
copy .env.example .env
# Отредактировать .env (добавить SECRET_KEY)

# Применить миграции
alembic upgrade head

# Запустить сервер
uvicorn main:app --reload --port 8000
```

Backend будет доступен на http://localhost:8000
API документация: http://localhost:8000/docs

### Шаг 4: Frontend

```bash
# Открыть новый терминал
cd frontend

# Установить зависимости
npm install

# Создать .env файл
copy .env.example .env
# Добавить REACT_APP_MAPBOX_TOKEN

# Запустить dev сервер
npm start
```

Frontend будет доступен на http://localhost:3000

## ✅ Проверка

1. Откройте http://localhost:3000
2. Должна загрузиться главная страница
3. Откройте http://localhost:8000/docs
4. Должна открыться Swagger документация

## 🔧 Полезные команды

### Backend:
```bash
# Создать миграцию
alembic revision --autogenerate -m "description"

# Применить миграции
alembic upgrade head

# Откатить миграцию
alembic downgrade -1

# Запустить с hot reload
uvicorn main:app --reload
```

### Frontend:
```bash
# Запустить dev сервер
npm start

# Собрать production
npm run build

# Проверить код
npm run lint

# Форматировать код
npm run format
```

### Docker:
```bash
# Запустить
docker-compose up -d

# Остановить
docker-compose stop

# Удалить (с данными)
docker-compose down -v

# Логи
docker-compose logs -f postgres
docker-compose logs -f redis
```

## 🐛 Troubleshooting

### Проблема: Docker не запускается
```bash
# Проверить Docker Desktop запущен
docker ps

# Перезапустить Docker Desktop
```

### Проблема: Порт 5432 занят
```bash
# Изменить порт в docker-compose.yml
ports:
  - "5433:5432"  # Изменить на 5433

# Обновить DATABASE_URL в .env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5433/edu_na_bazar
```

### Проблема: Frontend не подключается к API
```bash
# Проверить REACT_APP_API_URL в frontend/.env
REACT_APP_API_URL=http://localhost:8000

# Проверить CORS в backend
# Должен быть http://localhost:3000 в ALLOWED_ORIGINS
```

### Проблема: Миграции не применяются
```bash
# Проверить подключение к БД
docker-compose exec postgres psql -U postgres -d edu_na_bazar

# Пересоздать БД
docker-compose down -v
docker-compose up -d
alembic upgrade head
```

## 📚 Следующие шаги

1. Изучить [PROJECT_RULES.md](./PROJECT_RULES.md)
2. Посмотреть примеры компонентов в `frontend/src/components/`
3. Изучить API endpoints в `backend/api/routers/`
4. Прочитать [ARCHITECTURE.md](./ARCHITECTURE.md)

## 🎯 Готово!

Теперь можно начинать разработку! 🚀
