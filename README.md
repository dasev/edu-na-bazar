# 🛒 Еду на базар

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue.svg)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Маркетплейс прямых продаж от фермеров без посредников**

> 🌾 Платформа, которая убирает посредников между фермерами и покупателями. Свежие продукты по честным ценам!

**Платформа прямых продаж от сельхозпроизводителей без посредников**

Современный маркетплейс, соединяющий фермеров и покупателей напрямую. Помогаем местным производителям продавать свою продукцию, а покупателям - получать свежие продукты по честным ценам.

## 🎯 Миссия проекта

**Убрать посредников между фермерами и покупателями**

- 🌾 Фермеры получают справедливую цену за свой труд
- 🛒 Покупатели платят меньше, получая продукты напрямую
- ✨ 100% свежесть - продукты прямо с полей и ферм
- 🤝 Поддержка местных производителей

## 🎯 Особенности

- ✅ **Прямые продажи** - без посредников и наценок
- ✅ **Геолокация** - карты магазинов и зон доставки (PostGIS + Mapbox)
- ✅ **Современный UI** - DevExtreme компоненты
- ✅ **FastAPI Backend** - async API с высокой производительностью
- ✅ **Фильтры и поиск** - удобный подбор товаров
- ✅ **Docker** - простое развертывание

## 🚀 Быстрый старт

### Требования

- Node.js 18+
- Python 3.11+
- Docker Desktop
- Mapbox Access Token

### Установка

```bash
# 1. Клонировать репозиторий
git clone <repo-url>
cd edu-na-bazar

# 2. Запустить Docker (PostgreSQL + Redis)
docker-compose up -d

# 3. Установить backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 4. Применить миграции
alembic upgrade head

# 5. Запустить backend
uvicorn main:app --reload --port 8000

# 6. Установить frontend (в новом терминале)
cd frontend
npm install

# 7. Создать .env файл
cp .env.example .env
# Добавить REACT_APP_MAPBOX_TOKEN

# 8. Запустить frontend
npm start
```

Откройте http://localhost:3000

## 📁 Структура проекта

```
edu-na-bazar/
├── frontend/              # DevExtreme React App
│   ├── src/
│   │   ├── components/   # UI компоненты
│   │   ├── pages/        # Страницы
│   │   ├── api/          # API клиент
│   │   └── styles/       # Стили
│   └── package.json
├── backend/              # FastAPI
│   ├── api/             # API endpoints
│   ├── models/          # SQLAlchemy модели
│   ├── schemas/         # Pydantic схемы
│   └── main.py
├── docker-compose.yml   # Docker конфигурация
└── README.md
```

## 🎨 Технологии

**Frontend:**
- React 18
- DevExtreme 24.1
- Mapbox GL JS
- TanStack Query
- Zustand

**Backend:**
- FastAPI
- SQLAlchemy 2.0
- PostGIS
- Alembic

**База данных:**
- PostgreSQL 15
- PostGIS 3.4
- Redis 7

## 📖 Документация

- [Архитектура](./docs/ARCHITECTURE.md)
- [API документация](http://localhost:8000/docs)
- [Компоненты UI](./docs/COMPONENTS.md)
- [Деплой](./docs/DEPLOYMENT.md)

## 🔧 Разработка

```bash
# Frontend
cd frontend
npm run dev

# Backend
cd backend
uvicorn main:app --reload

# Миграции
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## 📝 Лицензия

MIT
