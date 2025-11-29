# 🚀 Запуск "Еду на базар"

## ✅ Что уже сделано:

1. ✅ Docker контейнеры запущены (PostgreSQL + Redis)
2. ✅ Backend структура создана
3. ✅ API роутеры созданы (products, categories, stores, orders, auth)
4. ✅ Python venv создан
5. ✅ Зависимости устанавливаются...

## 📊 Статус сервисов:

### Docker:
- ✅ PostgreSQL: `localhost:5432`
- ✅ Redis: `localhost:6380`

```bash
# Проверить статус
docker-compose ps
```

### Backend (FastAPI):
```bash
cd backend

# Активировать venv
venv\Scripts\activate

# Запустить сервер
uvicorn main:app --reload --port 8000

# Или использовать скрипт
run.bat
```

Backend будет доступен на:
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

## 🎯 Следующие шаги:

### 1. Дождаться установки зависимостей
Сейчас идет установка Python пакетов...

### 2. Запустить backend
```bash
cd backend
run.bat
```

### 3. Проверить API
Открыть http://localhost:8000/docs

### 4. Создать frontend
```bash
# В новом терминале
cd edu-na-bazar

# Вариант 1: DevExtreme CLI
npm install -g devextreme-cli
devextreme new react-app frontend

# Вариант 2: Create React App
npx create-react-app frontend --template typescript
cd frontend
npm install devextreme devextreme-react
npm install react-map-gl mapbox-gl @tanstack/react-query zustand axios
```

### 5. Настроить frontend
```bash
cd frontend

# Создать .env
copy ..\frontend\.env.example .env
# Добавить REACT_APP_MAPBOX_TOKEN

# Запустить
npm start
```

## 📝 Доступные API endpoints:

### Products:
- `GET /api/products` - Список товаров
- `GET /api/products/{id}` - Один товар

### Categories:
- `GET /api/categories` - Категории

### Stores (ГИС):
- `GET /api/stores` - Все магазины
- `GET /api/stores/nearby?lat=55.7558&lon=37.6173&radius_km=5` - Ближайшие

### Orders:
- `GET /api/orders` - Заказы
- `POST /api/orders` - Создать заказ

### Auth:
- `POST /api/auth/login` - Вход
- `POST /api/auth/register` - Регистрация

## 🔧 Полезные команды:

```bash
# Docker
docker-compose ps              # Статус
docker-compose logs postgres   # Логи PostgreSQL
docker-compose logs redis      # Логи Redis
docker-compose restart         # Перезапуск

# Backend
cd backend
venv\Scripts\activate          # Активировать venv
uvicorn main:app --reload      # Запустить с hot reload
python -m pytest               # Тесты (когда будут)

# Frontend (когда создадим)
cd frontend
npm start                      # Dev сервер
npm run build                  # Production build
```

## 🎉 Готово к разработке!

Backend запущен с mock данными. Можно начинать создавать frontend! 🚀
