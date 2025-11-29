# 📚 База знаний проекта "Еду на базар"

> **Полное руководство для AI-ассистента по работе с проектом**

---

## 🎯 О проекте

**Название:** Еду на базар  
**Тип:** Маркетплейс прямых продаж от фермеров без посредников  
**Миссия:** Убрать посредников между фермерами и покупателями  
**Технологии:** FastAPI + React + PostgreSQL + PostGIS + Docker

---

## 📁 Структура проекта

```
edu-na-bazar/
├── backend/                    # FastAPI Backend
│   ├── models/                # SQLAlchemy модели (БД)
│   │   ├── user.py           # User, SMSCode
│   │   ├── product.py        # Product (с геолокацией)
│   │   ├── category.py       # Category
│   │   ├── store.py          # Store (PostGIS)
│   │   ├── store_owner.py    # StoreOwner
│   │   ├── order.py          # Order, OrderItem
│   │   ├── cart.py           # CartItem
│   │   ├── product_image.py  # ProductImage
│   │   ├── review.py         # ProductReview, ProductQuestion
│   │   ├── geography.py      # DeliveryZone (PostGIS)
│   │   └── message.py        # Message (чат)
│   ├── schemas/              # Pydantic схемы (валидация)
│   │   ├── auth.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── cart.py
│   │   └── ...
│   ├── api/                  # API endpoints
│   │   ├── routers/
│   │   │   ├── auth.py       # SMS аутентификация
│   │   │   ├── products.py   # CRUD товаров
│   │   │   ├── categories.py
│   │   │   ├── stores.py     # Магазины с геолокацией
│   │   │   ├── orders.py
│   │   │   ├── cart.py       # Корзина
│   │   │   ├── reviews.py    # Отзывы и вопросы
│   │   │   ├── my_stores.py  # Личный кабинет продавца
│   │   │   ├── store_products.py
│   │   │   ├── moderation.py # Модерация
│   │   │   └── admin.py      # Админка
│   │   └── dependencies.py   # JWT авторизация
│   ├── alembic/              # Миграции БД
│   │   ├── versions/         # История миграций
│   │   └── env.py
│   ├── scripts/              # Утилиты (seed data, миграция)
│   ├── uploads/              # Загруженные изображения
│   ├── database.py           # Async SQLAlchemy setup
│   ├── config.py             # Настройки (env vars)
│   ├── main.py               # FastAPI app
│   ├── requirements.txt      # Python зависимости
│   ├── Dockerfile            # Production build
│   └── Dockerfile.dev        # Dev build (hot-reload)
│
├── frontend/                 # React + TypeScript + DevExtreme
│   ├── src/
│   │   ├── api/             # API клиент
│   │   │   ├── client.ts    # Axios instance (JWT interceptor)
│   │   │   ├── types.ts     # TypeScript типы
│   │   │   └── services/    # API сервисы
│   │   ├── store/           # Zustand state management
│   │   │   ├── authStore.ts # Аутентификация (persist)
│   │   │   ├── cartStore.ts # Корзина (гостевая + серверная)
│   │   │   └── filtersStore.ts # Фильтры каталога
│   │   ├── components/      # UI компоненты
│   │   │   ├── Header/
│   │   │   ├── ProductCard/
│   │   │   ├── CartButton/
│   │   │   └── ...
│   │   ├── pages/           # Страницы
│   │   │   ├── Home/        # Главная
│   │   │   ├── Catalog/     # Каталог с фильтрами
│   │   │   ├── Product/     # Детальная страница товара
│   │   │   ├── Cart/        # Корзина
│   │   │   ├── Checkout/    # Оформление заказа
│   │   │   ├── Map/         # Карта товаров (Mapbox)
│   │   │   ├── Stores/      # Магазины
│   │   │   ├── MyStores/    # Личный кабинет продавца
│   │   │   ├── Admin/       # Админка
│   │   │   └── Moderation/  # Модерация
│   │   ├── App.tsx          # Роутинг
│   │   └── main.tsx         # Entry point
│   ├── package.json         # Node зависимости
│   ├── Dockerfile           # Production build (Nginx)
│   ├── Dockerfile.dev       # Dev build (Vite dev server)
│   └── nginx.conf           # Nginx конфиг
│
├── .github/                 # CI/CD
│   └── workflows/
│       ├── deploy.yml       # Автодеплой на production
│       └── ci.yml           # Тесты и проверки
│
├── docker-compose.yml       # Production (Postgres + Redis + Backend + Frontend)
├── docker-compose.dev.yml   # Development с hot-reload 🔥
├── docker-compose.prod.yml  # Production конфиг
├── docker-compose.ssl.yml   # Production с SSL
│
├── .env.example             # Шаблон переменных окружения
├── README.md                # Документация
├── PROJECT_RULES.md         # Правила разработки
└── _корзина/                # Устаревшие файлы (не трогать)
```

---

## 🗄️ Модель данных (PostgreSQL + PostGIS)

### Схемы БД:
- **`config`** - конфигурация (users, sms_codes)
- **`market`** - маркетплейс (products, orders, stores, categories)

### Основные таблицы:

#### 1. **config.users** - Пользователи
```python
id: BigInteger (PK)
phone: Text (unique, index) - телефон (логин)
email: Text (unique, nullable)
full_name: Text
address: Text - адрес доставки
is_active: Boolean
is_verified: Boolean - подтвержден ли телефон
is_moderator: Boolean - модератор
status: Text - active, blocked
created_at, updated_at, last_login: DateTime
```
**Аутентификация:** SMS-коды (без паролей!)

#### 2. **market.products** - Товары
```python
id: BigInteger (PK)
name: Text (index)
description: Text
price: Double
image: Text - основное изображение
category_id: BigInteger (FK → categories)
store_owner_id: BigInteger (FK → store_owners)
rating: Double (0.0-5.0)
reviews_count: BigInteger
in_stock: Boolean
unit: Text - шт, кг, л, упак
views: BigInteger
location: Text - адрес
status: Text - active, archived, moderation

# Геолокация (PostGIS)
latitude: Double
longitude: Double
geo_location: Geometry(POINT, 4326) - для карты

created_at, updated_at: DateTime

# Relationships:
category: Category
store_owner: StoreOwner
images: List[ProductImage] - галерея
cart_items: List[CartItem]
order_items: List[OrderItem]
product_reviews: List[ProductReview]
product_questions: List[ProductQuestion]
```

#### 3. **market.categories** - Категории
```python
id: BigInteger (PK)
name: Text (unique, index)
slug: Text (unique, index)
icon: Text - эмодзи (🍎, 🥕, 🥛)
description: Text
parent_id: BigInteger (FK → self) - для подкатегорий
image: Text
is_active: Boolean
sort_order: Integer

# Relationships:
products: List[Product]
parent: Category
children: List[Category]
```

#### 4. **market.stores** - Магазины (PostGIS)
```python
id: BigInteger (PK)
name: Text (index)
description: Text
address: Text
phone, email: Text
working_hours: Text - "8:00 - 22:00"

# Геолокация (PostGIS)
location: Geometry(POINT, 4326) - координаты магазина
delivery_zone: Geometry(POLYGON, 4326) - зона доставки

image: Text
is_active: Boolean
created_at, updated_at: DateTime
```

#### 5. **market.store_owners** - Владельцы магазинов
```python
id: BigInteger (PK)
user_id: BigInteger (FK → users)
store_name: Text
description: Text
logo: Text
rating: Double
total_sales: BigInteger
is_verified: Boolean - проверенный продавец
status: Text - active, pending, blocked
created_at, updated_at: DateTime

# Relationships:
user: User
products: List[Product]
```

#### 6. **market.orders** - Заказы
```python
id: BigInteger (PK)
user_id: BigInteger (FK → users)
store_id: BigInteger (nullable)
total_amount: Double
status: Text - pending, created, paid, processing, delivering, completed, cancelled
delivery_address: Text
delivery_phone: Text
payment_method: Text - card, cash, online
notes: Text - комментарий
created_at, updated_at: DateTime

# Relationships:
user: User
items: List[OrderItem]
```

#### 7. **market.order_items** - Товары в заказе
```python
id: BigInteger (PK)
order_id: BigInteger (FK → orders)
product_id: BigInteger (FK → products)
quantity: BigInteger
price: Double - цена на момент заказа (фиксируется!)
created_at: DateTime

# Relationships:
order: Order
product: Product
```

#### 8. **market.cart_items** - Корзина
```python
id: BigInteger (PK)
user_id: BigInteger (FK → users)
product_id: BigInteger (FK → products)
quantity: BigInteger
created_at, updated_at: DateTime

# Relationships:
user: User
product: Product
```

#### 9. **market.product_images** - Галерея товара
```python
id: BigInteger (PK)
product_id: BigInteger (FK → products)
image_url: Text
is_main: Boolean - главное изображение
sort_order: Integer
created_at: DateTime

# Relationships:
product: Product
```

#### 10. **market.product_reviews** - Отзывы
```python
id: BigInteger (PK)
product_id: BigInteger (FK → products)
user_id: BigInteger (FK → users)
rating: Integer (1-5)
comment: Text
is_verified_purchase: Boolean
status: Text - pending, approved, rejected
created_at, updated_at: DateTime

# Relationships:
product: Product
user: User
```

#### 11. **market.product_questions** - Вопросы о товаре
```python
id: BigInteger (PK)
product_id: BigInteger (FK → products)
user_id: BigInteger (FK → users)
question: Text
answer: Text (nullable)
answered_by: BigInteger (FK → users, nullable)
answered_at: DateTime (nullable)
status: Text - pending, answered
created_at, updated_at: DateTime

# Relationships:
product: Product
user: User
answerer: User
```

---

## 🔧 Технологии и зависимости

### Backend (Python 3.11+)
```
FastAPI 0.104.1          - Async web framework
uvicorn 0.24.0           - ASGI server
SQLAlchemy 2.0.23        - ORM (async)
asyncpg 0.29.0           - PostgreSQL async driver
psycopg2-binary 2.9.9    - PostgreSQL sync (для Alembic)
alembic 1.12.1           - Миграции БД
geoalchemy2 0.14.2       - PostGIS support
pydantic 2.5.0           - Валидация данных
PyJWT 2.8.0              - JWT токены
redis 5.0.1              - Кэш
httpx 0.25.2             - HTTP клиент (SMS)
aiofiles 23.2.1          - Async файлы
Pillow 10.1.0            - Обработка изображений
python-dotenv 1.0.0      - .env файлы
```

### Frontend (Node.js 18+)
```
React 18.2.0             - UI библиотека
TypeScript 5.3.0         - Типизация
Vite 5.0.0               - Build tool (hot-reload)
DevExtreme 24.1.0        - UI компоненты (DataGrid, Form, Popup)
Mapbox GL JS 3.16.0      - Карты
TanStack Query 5.0.0     - Server state management
Zustand 4.5.7            - Client state management
Axios 1.6.0              - HTTP клиент
React Router 6.20.0      - Роутинг
React Hot Toast 2.6.0    - Уведомления
Sass 1.69.0              - CSS препроцессор
```

### Инфраструктура
```
PostgreSQL 15            - БД
PostGIS 3.4              - Геоданные
Redis 7                  - Кэш
Docker & Docker Compose  - Контейнеризация
Nginx                    - Reverse proxy (frontend)
GitHub Actions           - CI/CD
```

---

## 🚀 Запуск проекта

### 1. **Локальная разработка (БЕЗ Docker)**

#### Backend:
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Применить миграции
alembic upgrade head

# Запустить (hot-reload)
uvicorn main:app --reload --port 8000
```

#### Frontend:
```bash
cd frontend
npm install

# Создать .env
cp .env.example .env
# Добавить VITE_MAPBOX_TOKEN

# Запустить (hot-reload)
npm run dev
```

#### Docker (только БД):
```bash
docker-compose up -d postgres redis
```

---

### 2. **Development режим (Docker с hot-reload) 🔥**

```bash
# Остановить production контейнеры (если запущены)
docker-compose down

# Запустить dev режим
docker-compose -f docker-compose.dev.yml up -d --build

# Логи
docker-compose -f docker-compose.dev.yml logs -f backend
docker-compose -f docker-compose.dev.yml logs -f frontend

# Остановка
docker-compose -f docker-compose.dev.yml stop
```

**Особенности dev режима:**
- ✅ Backend: `uvicorn --reload` (автоперезагрузка при изменении кода)
- ✅ Frontend: `vite` (hot module replacement)
- ✅ Volumes: код монтируется из хоста (изменения сразу применяются)
- ✅ Порты: Backend 8000, Frontend 3000
- ✅ CORS: разрешены все origins для Cascade browser preview

**Доступ:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6380

---

### 3. **Production режим (Docker)**

```bash
# Создать .env из .env.example
cp .env.example .env
# Заполнить переменные окружения

# Запустить
docker-compose up -d --build

# Логи
docker-compose logs -f

# Остановка
docker-compose stop

# Полная остановка с удалением контейнеров
docker-compose down
```

**Доступ:**
- Frontend: http://localhost (порт 80)
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs (только в dev)

---

## 🔄 Работа с миграциями БД (Alembic)

### Создание миграции:
```bash
cd backend

# Автогенерация (на основе изменений в models/)
alembic revision --autogenerate -m "Add new field to products"

# Ручная миграция
alembic revision -m "Custom migration"
```

### Применение миграций:
```bash
# Применить все
alembic upgrade head

# Применить конкретную
alembic upgrade +1

# Откатить
alembic downgrade -1

# История
alembic history

# Текущая версия
alembic current
```

### В Docker:
```bash
# Dev режим
docker-compose -f docker-compose.dev.yml exec backend alembic upgrade head

# Production
docker-compose exec backend alembic upgrade head
```

---

## 🔐 Аутентификация (SMS без паролей)

### Процесс:
1. **Отправка кода:** `POST /api/auth/send-code` → SMS на телефон
2. **Проверка кода:** `POST /api/auth/verify-code` → JWT токен
3. **Использование токена:** `Authorization: Bearer <token>`

### Хранение токена (Frontend):
- **Zustand persist** → `localStorage['auth-storage']`
- **API client** → `localStorage['auth_token']` (для axios interceptor)
- **Синхронизация** → автоматическая при загрузке

### JWT токен:
- **Алгоритм:** HS256
- **Срок действия:** 30 минут (настраивается)
- **Payload:** `{ sub: user_id, phone: "+79991234567" }`

### Защищенные endpoints:
```python
from api.dependencies import get_current_user

@router.get("/profile")
async def get_profile(user: User = Depends(get_current_user)):
    return user
```

---

## 🛒 Корзина (гостевая + серверная)

### Логика:
- **Гость (не авторизован):** корзина в `localStorage['guest_cart']`
- **Авторизован:** корзина в БД (`market.cart_items`)
- **При входе:** автоматическая синхронизация гостевой корзины с серверной

### API:
```typescript
// Добавить в корзину
cartApi.addToCart(productId, quantity)

// Обновить количество
cartApi.updateCartItem(itemId, quantity)

// Удалить
cartApi.removeFromCart(itemId)

// Очистить
cartApi.clearCart()

// Получить корзину
cartApi.getCart()
```

### Zustand store:
```typescript
const { cart, guestCart, addToCart, getItemsCount, getTotal } = useCartStore()
```

---

## 🗺️ Геолокация (PostGIS + Mapbox)

### PostGIS типы:
- **POINT** - координаты (долгота, широта)
- **POLYGON** - зона доставки
- **SRID 4326** - стандарт WGS84 (GPS, Google Maps, Mapbox)

### Модели с геолокацией:
- **Product:** `latitude`, `longitude`, `geo_location` (POINT)
- **Store:** `location` (POINT), `delivery_zone` (POLYGON)

### Mapbox карта (Frontend):
```typescript
// MapPage.tsx
import mapboxgl from 'mapbox-gl'

// Инициализация
const map = new mapboxgl.Map({
  container: mapRef.current,
  style: 'mapbox://styles/mapbox/streets-v12',
  center: [37.6173, 55.7558], // Москва
  zoom: 10
})

// Добавление маркеров
const marker = new mapboxgl.Marker()
  .setLngLat([longitude, latitude])
  .addTo(map)
```

### API endpoint:
```python
@router.get("/products/map/geojson")
async def get_products_geojson(
    category_id: int = None,
    in_stock: bool = None,
    limit: int = 1000
):
    # Возвращает GeoJSON с товарами
    return {
        "type": "FeatureCollection",
        "features": [...]
    }
```

---

## 📦 Работа с Git

### Клонирование:
```bash
git clone <repo-url>
cd edu-na-bazar
```

### Ветки:
- **main** - production (автодеплой при push)
- **develop** - разработка
- **feature/*** - новые фичи
- **fix/*** - исправления

### Conventional Commits:
```bash
git commit -m "feat: add product filters"
git commit -m "fix: resolve cart calculation bug"
git commit -m "docs: update API documentation"
git commit -m "refactor: improve database queries"
git commit -m "style: format code with prettier"
git commit -m "test: add unit tests for cart"
```

### Workflow:
```bash
# Создать ветку
git checkout -b feature/product-filters

# Коммиты
git add .
git commit -m "feat: add price range filter"

# Push
git push origin feature/product-filters

# Pull Request → main
# После мержа → автодеплой на production
```

---

## 🚀 Деплой на Production

### Автоматический (GitHub Actions):
1. **Push в main** → триггер CI/CD
2. **Build Docker images** → push в Docker Hub
3. **Deploy на сервер** → SSH + docker-compose
4. **Миграции БД** → `alembic upgrade head`
5. **Health check** → проверка API и Frontend

### Ручной:
```bash
# На сервере
cd /opt/edu-na-bazar

# Backup БД
docker-compose exec postgres pg_dump -U postgres edu_na_bazar | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Pull код
git pull origin main

# Pull images
docker-compose pull

# Перезапуск
docker-compose down
docker-compose up -d

# Миграции
docker-compose exec backend alembic upgrade head

# Проверка
docker-compose ps
curl http://localhost:8000/health
```

### Переменные окружения (GitHub Secrets):
```
DOCKER_USERNAME       - Docker Hub логин
DOCKER_PASSWORD       - Docker Hub пароль
SERVER_HOST           - IP сервера
SERVER_USER           - SSH пользователь
SSH_PRIVATE_KEY       - SSH ключ
API_URL               - https://api.yourdomain.com
SECRET_KEY            - JWT secret
POSTGRES_PASSWORD     - БД пароль
MAPBOX_ACCESS_TOKEN   - Mapbox токен
```

---

## 🧪 Тестирование

### Backend:
```bash
cd backend
pytest
```

### Frontend:
```bash
cd frontend
npm test
```

### E2E:
```bash
# Playwright (если настроен)
npm run test:e2e
```

---

## 📊 Мониторинг и логи

### Логи Docker:
```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# Последние 100 строк
docker-compose logs --tail=100 backend
```

### Health checks:
```bash
# API
curl http://localhost:8000/health

# Frontend
curl http://localhost/

# БД
docker-compose exec postgres pg_isready -U postgres
```

### Статус контейнеров:
```bash
docker-compose ps
```

---

## 🐛 Отладка

### Backend:
```python
# В коде
import pdb; pdb.set_trace()

# Логирование
import logging
logger = logging.getLogger(__name__)
logger.info("Debug message")
```

### Frontend:
```typescript
// DevTools
console.log('Debug:', data)

// React DevTools
// Zustand DevTools
```

### SQL запросы:
```bash
# Подключиться к БД
docker-compose exec postgres psql -U postgres -d edu_na_bazar

# Запросы
SELECT * FROM market.products LIMIT 10;
SELECT COUNT(*) FROM config.users;
```

---

## 📝 Частые задачи

### 1. Добавить новую модель:
```python
# 1. Создать models/new_model.py
# 2. Импортировать в models/__init__.py
# 3. Создать schemas/new_model.py
# 4. Создать миграцию
alembic revision --autogenerate -m "Add new_model"
# 5. Применить
alembic upgrade head
```

### 2. Добавить новый API endpoint:
```python
# 1. Создать api/routers/new_router.py
# 2. Добавить в main.py
app.include_router(new_router.router, prefix="/api/new", tags=["new"])
```

### 3. Добавить новую страницу (Frontend):
```typescript
// 1. Создать pages/NewPage/NewPage.tsx
// 2. Добавить роут в App.tsx
<Route path="/new" element={<NewPage />} />
```

### 4. Обновить зависимости:
```bash
# Backend
cd backend
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt

# Frontend
cd frontend
npm update
npm audit fix
```

---

## ⚠️ Важные правила

### 1. **НИКОГДА не удаляй данные из БД без backup!**
```bash
# Всегда делай backup перед изменениями
docker-compose exec postgres pg_dump -U postgres edu_na_bazar > backup.sql
```

### 2. **Всегда используй миграции для изменения схемы БД**
```bash
# НЕ изменяй БД вручную через SQL!
# Используй Alembic
alembic revision --autogenerate -m "Change"
alembic upgrade head
```

### 3. **Проверяй типы (TypeScript/Python)**
```python
# Python - type hints
async def get_product(product_id: int) -> Product:
    ...

# TypeScript - interfaces
interface Product {
  id: string
  name: string
  price: number
}
```

### 4. **Используй DevExtreme компоненты**
```typescript
// ✅ Правильно
import { DataGrid, Button, Form } from 'devextreme-react'

// ❌ Неправильно
import { Table } from '@mui/material'  // Конфликт!
```

### 5. **Async/await везде**
```python
# Backend
async def get_products(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()
```

```typescript
// Frontend
const { data } = useQuery({
  queryKey: ['products'],
  queryFn: async () => await api.getProducts()
})
```

---

## 🔍 Полезные команды

### Docker:
```bash
# Пересобрать образы
docker-compose build --no-cache

# Удалить все контейнеры и volumes
docker-compose down -v

# Очистить неиспользуемые образы
docker system prune -a

# Войти в контейнер
docker-compose exec backend bash
docker-compose exec frontend sh
```

### PostgreSQL:
```bash
# Подключиться
docker-compose exec postgres psql -U postgres -d edu_na_bazar

# Backup
docker-compose exec postgres pg_dump -U postgres edu_na_bazar > backup.sql

# Restore
docker-compose exec -T postgres psql -U postgres edu_na_bazar < backup.sql

# Список таблиц
\dt market.*
\dt config.*

# Описание таблицы
\d market.products
```

### Alembic:
```bash
# История миграций
alembic history --verbose

# Текущая версия
alembic current

# Откат на конкретную версию
alembic downgrade <revision>

# Применить до конкретной версии
alembic upgrade <revision>
```

---

## 📚 Документация

- **API Docs:** http://localhost:8000/docs (Swagger UI)
- **ReDoc:** http://localhost:8000/redoc
- **DevExtreme:** https://js.devexpress.com/Documentation/
- **Mapbox:** https://docs.mapbox.com/mapbox-gl-js/
- **FastAPI:** https://fastapi.tiangolo.com/
- **SQLAlchemy:** https://docs.sqlalchemy.org/en/20/
- **Alembic:** https://alembic.sqlalchemy.org/
- **PostGIS:** https://postgis.net/documentation/

---

## 🎯 Чек-лист перед коммитом

- [ ] ✅ Код работает локально
- [ ] ✅ Нет `console.log` / `print` для отладки
- [ ] ✅ Добавлены типы (TypeScript/Python)
- [ ] ✅ Код отформатирован
- [ ] ✅ Нет ошибок ESLint/Pylint
- [ ] ✅ Миграции созданы (если изменена БД)
- [ ] ✅ Обновлена документация (если нужно)
- [ ] ✅ Тесты проходят
- [ ] ✅ Conventional commit message

---

## 🆘 Troubleshooting

### 1. **Backend не запускается**
```bash
# Проверить логи
docker-compose logs backend

# Проверить БД
docker-compose exec postgres pg_isready

# Пересоздать контейнер
docker-compose up -d --force-recreate backend
```

### 2. **Frontend не собирается**
```bash
# Очистить node_modules
rm -rf node_modules package-lock.json
npm install

# Проверить переменные окружения
cat .env
```

### 3. **Миграции не применяются**
```bash
# Проверить текущую версию
alembic current

# Проверить историю
alembic history

# Откатить и применить заново
alembic downgrade -1
alembic upgrade head
```

### 4. **CORS ошибки**
```python
# В config.py проверить ALLOWED_ORIGINS
# В development режиме должно быть "*"
```

### 5. **JWT токен не работает**
```typescript
// Проверить localStorage
console.log(localStorage.getItem('auth_token'))

// Проверить синхронизацию
import { useAuthStore } from './store/authStore'
const { token } = useAuthStore()
console.log(token)
```

---

## 🎉 Готово!

Теперь у тебя есть полное понимание проекта "Еду на базар". Используй эту базу знаний для эффективной работы над проектом!

**Основные принципы:**
1. 🐳 Всегда работай через Docker (dev режим с hot-reload)
2. 🔄 Используй миграции для изменения БД
3. 📝 Следуй Conventional Commits
4. ✅ Проверяй типы (TypeScript/Python)
5. 🧪 Пиши тесты
6. 📚 Обновляй документацию

**Удачи в разработке!** 🚀
