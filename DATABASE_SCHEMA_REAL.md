# 🗄️ Реальная структура БД "Еду на базар"

> **Актуальная схема базы данных из production**  
> **Дата снимка:** 29.11.2025

---

## 📊 Общая статистика

### Схемы:
- **config** - конфигурация и пользователи
- **market** - маркетплейс (товары, заказы, магазины)
- **geo** - геоданные (PostGIS)
- **temp** - временные данные миграции

### Размер БД:
```
config.users:             1224 kB (2573 записей)
config.sms_codes:           48 kB (4 записи)
market.products:           224 kB (154 товара)
market.categories:          64 kB (12 категорий)
market.store_owners:       392 kB (676 продавцов)
market.stores:              16 kB (0 магазинов)
market.orders:              64 kB (26 заказов)
market.order_items:         56 kB (29 позиций)
market.cart_items:          72 kB (0 товаров в корзине)
market.product_images:      96 kB (38 изображений)
market.product_reviews:    368 kB (941 отзыв)
market.product_questions:   80 kB (19 вопросов)
market.review_responses:    32 kB (ответы на отзывы)
market.review_votes:        72 kB (голоса за отзывы)
market.question_answers:    80 kB (ответы на вопросы)
market.messages:            56 kB (сообщения)
market.moderation_logs:     64 kB (логи модерации)
```

---

## 📋 Детальная структура таблиц

### 1. **config.users** - Пользователи

```sql
CREATE TABLE config.users (
    id              BIGSERIAL PRIMARY KEY,
    email           TEXT NOT NULL UNIQUE,
    phone           TEXT NOT NULL UNIQUE,
    full_name       TEXT NOT NULL,
    address         TEXT,
    is_active       BOOLEAN NOT NULL DEFAULT true,
    is_verified     BOOLEAN NOT NULL DEFAULT false,
    is_moderator    BOOLEAN DEFAULT false,
    status          TEXT DEFAULT 'active',
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login      TIMESTAMP
);

-- Индексы
CREATE INDEX idx_config_users_email ON config.users(email);
CREATE INDEX idx_config_users_phone ON config.users(phone);
CREATE INDEX idx_users_last_login ON config.users(last_login DESC);
CREATE INDEX idx_users_status ON config.users(status);
```

**Описание полей:**
- `id` - уникальный идентификатор
- `email` - email (уникальный, может быть пустым при регистрации)
- `phone` - телефон (уникальный, используется для входа)
- `full_name` - полное имя
- `address` - адрес доставки
- `is_active` - активен ли аккаунт
- `is_verified` - подтвержден ли телефон через SMS
- `is_moderator` - является ли модератором
- `status` - статус: active, blocked
- `created_at` - дата регистрации
- `updated_at` - дата последнего обновления
- `last_login` - дата последнего входа

**Связи:**
- → `market.cart_items` (user_id)
- → `market.orders` (user_id)
- → `market.product_reviews` (user_id)
- → `market.product_questions` (user_id)
- → `market.store_owners` (owner_id)
- → `market.messages` (from_user_id, to_user_id)
- → `market.review_votes` (user_id)
- → `market.question_answers` (user_id)
- → `market.moderation_logs` (moderator_id)

---

### 2. **config.sms_codes** - SMS коды для аутентификации

```sql
CREATE TABLE config.sms_codes (
    id          BIGSERIAL PRIMARY KEY,
    phone       TEXT NOT NULL,
    code        TEXT NOT NULL,
    is_used     BOOLEAN DEFAULT false,
    attempts    TEXT DEFAULT '0',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at  TIMESTAMP NOT NULL,
    used_at     TIMESTAMP
);

CREATE INDEX idx_sms_codes_phone ON config.sms_codes(phone);
CREATE INDEX idx_sms_codes_expires_at ON config.sms_codes(expires_at);
```

**Описание:**
- SMS коды для входа (без паролей)
- Срок действия: 5 минут
- После использования `is_used = true`

---

### 3. **market.products** - Товары

```sql
CREATE TABLE market.products (
    id              BIGSERIAL PRIMARY KEY,
    name            TEXT NOT NULL,
    description     TEXT,
    price           DOUBLE PRECISION NOT NULL,
    category_id     BIGINT REFERENCES market.categories(id) ON DELETE SET NULL,
    store_owner_id  BIGINT REFERENCES market.store_owners(id),
    image           TEXT,
    in_stock        BOOLEAN NOT NULL DEFAULT true,
    rating          DOUBLE PRECISION DEFAULT 0.0,
    reviews_count   BIGINT DEFAULT 0,
    unit            TEXT DEFAULT 'шт',
    views           INTEGER DEFAULT 0,
    location        TEXT,
    status          TEXT DEFAULT 'active',
    
    -- Геолокация (PostGIS)
    latitude        DOUBLE PRECISION,
    longitude       DOUBLE PRECISION,
    geo_location    GEOMETRY(Point, 4326),
    
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Индексы
CREATE INDEX idx_market_products_category_id ON market.products(category_id);
CREATE INDEX idx_products_store_owner_id ON market.products(store_owner_id);
CREATE INDEX idx_products_status ON market.products(status);
CREATE INDEX idx_products_views ON market.products(views DESC);
CREATE INDEX idx_products_latitude ON market.products(latitude);
CREATE INDEX idx_products_longitude ON market.products(longitude);
CREATE INDEX idx_products_geo_location ON market.products USING GIST(geo_location);
```

**Описание полей:**
- `id` - уникальный идентификатор
- `name` - название товара
- `description` - описание
- `price` - цена (double precision)
- `category_id` - категория (FK → categories)
- `store_owner_id` - владелец магазина (FK → store_owners)
- `image` - основное изображение (URL)
- `in_stock` - в наличии
- `rating` - рейтинг (0.0-5.0)
- `reviews_count` - количество отзывов
- `unit` - единица измерения (шт, кг, л, упак)
- `views` - количество просмотров
- `location` - адрес/местоположение
- `status` - статус: active, archived, moderation
- `latitude`, `longitude` - координаты (для карты)
- `geo_location` - PostGIS точка (POINT, SRID 4326)

**Связи:**
- ← `market.categories` (category_id)
- ← `market.store_owners` (store_owner_id)
- → `market.cart_items` (product_id)
- → `market.order_items` (product_id)
- → `market.product_images` (product_id)
- → `market.product_reviews` (product_id)
- → `market.product_questions` (product_id)

---

### 4. **market.categories** - Категории

```sql
CREATE TABLE market.categories (
    id          BIGSERIAL PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    slug        TEXT NOT NULL UNIQUE,
    icon        TEXT,
    description TEXT,
    parent_id   BIGINT REFERENCES market.categories(id),
    is_active   BOOLEAN DEFAULT true
);

CREATE INDEX idx_categories_parent_id ON market.categories(parent_id);
CREATE INDEX idx_categories_slug ON market.categories(slug);
```

**Описание:**
- Иерархические категории (parent_id для подкатегорий)
- `icon` - эмодзи (🍎, 🥕, 🥛)
- `slug` - URL-friendly имя

**Примеры категорий:**
- Фрукты 🍎
- Овощи 🥕
- Молочные продукты 🥛
- Мясо и птица 🍗
- Рыба и морепродукты 🐟

---

### 5. **market.store_owners** - Владельцы магазинов

```sql
CREATE TABLE market.store_owners (
    id                  BIGSERIAL PRIMARY KEY,
    owner_id            BIGINT NOT NULL REFERENCES config.users(id) ON DELETE CASCADE,
    store_name          TEXT NOT NULL,
    description         TEXT,
    logo                TEXT,
    rating              DOUBLE PRECISION DEFAULT 0.0,
    total_sales         BIGINT DEFAULT 0,
    is_verified         BOOLEAN DEFAULT false,
    status              TEXT DEFAULT 'active',
    
    -- Контакты
    phone               TEXT,
    email               TEXT,
    address             TEXT,
    website             TEXT,
    
    -- Социальные сети
    instagram           TEXT,
    facebook            TEXT,
    vk                  TEXT,
    
    -- Дополнительно
    delivery_available  BOOLEAN DEFAULT false,
    min_order_amount    DOUBLE PRECISION,
    
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_store_owners_owner_id ON market.store_owners(owner_id);
CREATE INDEX idx_store_owners_status ON market.store_owners(status);
CREATE INDEX idx_store_owners_rating ON market.store_owners(rating DESC);
```

**Описание:**
- Продавцы (фермеры, магазины)
- `is_verified` - проверенный продавец (бейдж)
- `status` - active, pending, blocked
- `total_sales` - общее количество продаж

---

### 6. **market.stores** - Магазины (с геолокацией)

```sql
CREATE TABLE market.stores (
    id              BIGSERIAL PRIMARY KEY,
    name            TEXT NOT NULL,
    description     TEXT,
    address         TEXT NOT NULL,
    phone           TEXT,
    email           TEXT,
    working_hours   TEXT,
    image           TEXT,
    is_active       BOOLEAN DEFAULT true,
    
    -- Геолокация (PostGIS)
    location        GEOMETRY(Point, 4326),
    delivery_zone   GEOMETRY(Polygon, 4326),
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_stores_location ON market.stores USING GIST(location);
CREATE INDEX idx_stores_delivery_zone ON market.stores USING GIST(delivery_zone);
```

**Описание:**
- Физические магазины с геолокацией
- `location` - координаты магазина (PostGIS POINT)
- `delivery_zone` - зона доставки (PostGIS POLYGON)
- `working_hours` - время работы (например: "8:00 - 22:00")

---

### 7. **market.orders** - Заказы

```sql
CREATE TABLE market.orders (
    id                  BIGSERIAL PRIMARY KEY,
    user_id             BIGINT NOT NULL REFERENCES config.users(id) ON DELETE CASCADE,
    store_id            BIGINT,
    total_amount        DOUBLE PRECISION NOT NULL,
    status              TEXT NOT NULL DEFAULT 'pending',
    delivery_address    TEXT NOT NULL,
    delivery_phone      TEXT NOT NULL,
    payment_method      TEXT NOT NULL,
    notes               TEXT,
    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_orders_user_id ON market.orders(user_id);
CREATE INDEX idx_orders_status ON market.orders(status);
CREATE INDEX idx_orders_created_at ON market.orders(created_at DESC);
```

**Статусы заказа:**
- `pending` - ожидает
- `created` - создан
- `paid` - оплачен
- `processing` - в обработке
- `delivering` - доставляется
- `completed` - выполнен
- `cancelled` - отменен

**Способы оплаты:**
- `card` - банковская карта
- `cash` - наличные
- `online` - онлайн оплата

---

### 8. **market.order_items** - Товары в заказе

```sql
CREATE TABLE market.order_items (
    id          BIGSERIAL PRIMARY KEY,
    order_id    BIGINT NOT NULL REFERENCES market.orders(id) ON DELETE CASCADE,
    product_id  BIGINT NOT NULL REFERENCES market.products(id) ON DELETE CASCADE,
    quantity    BIGINT NOT NULL,
    price       DOUBLE PRECISION NOT NULL,  -- Цена фиксируется на момент заказа!
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_market_order_items_order_id ON market.order_items(order_id);
CREATE INDEX idx_market_order_items_product_id ON market.order_items(product_id);
```

**Важно:** Цена фиксируется на момент создания заказа!

---

### 9. **market.cart_items** - Корзина

```sql
CREATE TABLE market.cart_items (
    id          BIGSERIAL PRIMARY KEY,
    user_id     BIGINT NOT NULL REFERENCES config.users(id) ON DELETE CASCADE,
    product_id  BIGINT NOT NULL REFERENCES market.products(id) ON DELETE CASCADE,
    quantity    BIGINT NOT NULL DEFAULT 1,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id, product_id)  -- Один товар = одна запись
);

CREATE INDEX idx_market_cart_items_user_id ON market.cart_items(user_id);
CREATE INDEX idx_market_cart_items_product_id ON market.cart_items(product_id);
```

**Особенности:**
- Серверная корзина (для авторизованных)
- Гостевая корзина в `localStorage` (для гостей)
- Автосинхронизация при входе

---

### 10. **market.product_images** - Галерея товара

```sql
CREATE TABLE market.product_images (
    id          BIGSERIAL PRIMARY KEY,
    product_id  BIGINT REFERENCES market.products(id) ON DELETE CASCADE,
    image_url   TEXT NOT NULL,
    is_main     BOOLEAN DEFAULT false,
    sort_order  INTEGER DEFAULT 0,
    old_id      INTEGER,  -- Для миграции
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_product_images_product_id ON market.product_images(product_id);
CREATE INDEX idx_product_images_sort_order ON market.product_images(product_id, sort_order);
CREATE INDEX idx_product_images_old_id ON market.product_images(old_id);
```

**Описание:**
- Множественные изображения для товара
- `is_main` - главное изображение
- `sort_order` - порядок отображения

---

### 11. **market.product_reviews** - Отзывы о товарах

```sql
CREATE TABLE market.product_reviews (
    id                      BIGSERIAL PRIMARY KEY,
    product_id              BIGINT NOT NULL REFERENCES market.products(id) ON DELETE CASCADE,
    user_id                 BIGINT REFERENCES config.users(id) ON DELETE SET NULL,
    rating                  INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title                   VARCHAR(200),
    comment                 TEXT NOT NULL,
    advantages              TEXT,
    disadvantages           TEXT,
    is_verified_purchase    BOOLEAN DEFAULT false,
    helpful_count           INTEGER DEFAULT 0,
    not_helpful_count       INTEGER DEFAULT 0,
    created_at              TIMESTAMP DEFAULT NOW(),
    updated_at              TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_product_reviews_product_id ON market.product_reviews(product_id);
CREATE INDEX idx_product_reviews_user_id ON market.product_reviews(user_id);
CREATE INDEX idx_product_reviews_rating ON market.product_reviews(rating);
CREATE INDEX idx_product_reviews_created_at ON market.product_reviews(created_at DESC);
```

**Описание:**
- Рейтинг: 1-5 звезд
- `is_verified_purchase` - подтвержденная покупка
- `helpful_count` - количество "полезно"
- `advantages` / `disadvantages` - плюсы/минусы

---

### 12. **market.product_questions** - Вопросы о товаре

```sql
CREATE TABLE market.product_questions (
    id              BIGSERIAL PRIMARY KEY,
    product_id      BIGINT NOT NULL REFERENCES market.products(id) ON DELETE CASCADE,
    user_id         BIGINT REFERENCES config.users(id) ON DELETE SET NULL,
    question_text   TEXT NOT NULL,
    is_anonymous    BOOLEAN DEFAULT false,
    helpful_count   INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_product_questions_product_id ON market.product_questions(product_id);
CREATE INDEX idx_product_questions_user_id ON market.product_questions(user_id);
CREATE INDEX idx_product_questions_created_at ON market.product_questions(created_at DESC);
```

**Связи:**
- → `market.question_answers` (ответы на вопросы)

---

### 13. **market.question_answers** - Ответы на вопросы

```sql
CREATE TABLE market.question_answers (
    id              BIGSERIAL PRIMARY KEY,
    question_id     BIGINT NOT NULL REFERENCES market.product_questions(id) ON DELETE CASCADE,
    user_id         BIGINT REFERENCES config.users(id) ON DELETE SET NULL,
    answer_text     TEXT NOT NULL,
    is_seller       BOOLEAN DEFAULT false,
    is_verified     BOOLEAN DEFAULT false,
    helpful_count   INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_question_answers_question_id ON market.question_answers(question_id);
CREATE INDEX idx_question_answers_user_id ON market.question_answers(user_id);
```

**Описание:**
- `is_seller` - ответ от продавца
- `is_verified` - проверенный ответ

---

### 14. **market.review_responses** - Ответы на отзывы

```sql
CREATE TABLE market.review_responses (
    id              BIGSERIAL PRIMARY KEY,
    review_id       BIGINT NOT NULL REFERENCES market.product_reviews(id) ON DELETE CASCADE,
    store_id        BIGINT REFERENCES market.stores(id) ON DELETE CASCADE,
    response_text   TEXT NOT NULL,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_review_responses_review_id ON market.review_responses(review_id);
CREATE INDEX idx_review_responses_store_id ON market.review_responses(store_id);
```

**Описание:**
- Ответы продавца на отзывы покупателей

---

### 15. **market.review_votes** - Голоса за отзывы

```sql
CREATE TABLE market.review_votes (
    id          BIGSERIAL PRIMARY KEY,
    review_id   BIGINT NOT NULL REFERENCES market.product_reviews(id) ON DELETE CASCADE,
    user_id     BIGINT NOT NULL REFERENCES config.users(id) ON DELETE CASCADE,
    vote_type   TEXT NOT NULL,  -- 'helpful' или 'not_helpful'
    created_at  TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(review_id, user_id)  -- Один голос от пользователя
);

CREATE INDEX idx_review_votes_review_id ON market.review_votes(review_id);
CREATE INDEX idx_review_votes_user_id ON market.review_votes(user_id);
```

**Описание:**
- Пользователи могут отметить отзыв как полезный/бесполезный

---

### 16. **market.messages** - Сообщения (чат)

```sql
CREATE TABLE market.messages (
    id              BIGSERIAL PRIMARY KEY,
    from_user_id    BIGINT NOT NULL REFERENCES config.users(id) ON DELETE CASCADE,
    to_user_id      BIGINT NOT NULL REFERENCES config.users(id) ON DELETE CASCADE,
    product_id      BIGINT REFERENCES market.products(id) ON DELETE SET NULL,
    message_text    TEXT NOT NULL,
    is_read         BOOLEAN DEFAULT false,
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_messages_from_user_id ON market.messages(from_user_id);
CREATE INDEX idx_messages_to_user_id ON market.messages(to_user_id);
CREATE INDEX idx_messages_product_id ON market.messages(product_id);
```

**Описание:**
- Чат между покупателями и продавцами
- Привязка к товару (опционально)

---

### 17. **market.moderation_logs** - Логи модерации

```sql
CREATE TABLE market.moderation_logs (
    id              BIGSERIAL PRIMARY KEY,
    moderator_id    BIGINT REFERENCES config.users(id),
    product_id      BIGINT REFERENCES market.products(id),
    action          TEXT NOT NULL,
    reason          TEXT,
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_moderation_logs_moderator_id ON market.moderation_logs(moderator_id);
CREATE INDEX idx_moderation_logs_product_id ON market.moderation_logs(product_id);
```

**Действия:**
- `approved` - одобрено
- `rejected` - отклонено
- `blocked` - заблокировано

---

## 🔗 Диаграмма связей

```
config.users (2573)
    ├─→ market.cart_items (0)
    ├─→ market.orders (26)
    ├─→ market.product_reviews (941)
    ├─→ market.product_questions (19)
    ├─→ market.store_owners (676)
    ├─→ market.messages (from/to)
    ├─→ market.review_votes
    └─→ market.question_answers

market.products (154)
    ├─→ market.product_images (38)
    ├─→ market.product_reviews (941)
    ├─→ market.product_questions (19)
    ├─→ market.cart_items (0)
    ├─→ market.order_items (29)
    └─→ market.messages

market.categories (12)
    └─→ market.products (154)

market.store_owners (676)
    └─→ market.products (154)

market.orders (26)
    └─→ market.order_items (29)

market.product_reviews (941)
    ├─→ market.review_responses
    └─→ market.review_votes

market.product_questions (19)
    └─→ market.question_answers
```

---

## 📈 Статистика данных

| Таблица | Записей | Размер |
|---------|---------|--------|
| config.users | 2,573 | 1.2 MB |
| market.products | 154 | 224 KB |
| market.categories | 12 | 64 KB |
| market.store_owners | 676 | 392 KB |
| market.product_reviews | 941 | 368 KB |
| market.orders | 26 | 64 KB |
| market.order_items | 29 | 56 KB |
| market.product_images | 38 | 96 KB |
| market.product_questions | 19 | 80 KB |
| market.cart_items | 0 | 72 KB |
| market.stores | 0 | 16 KB |

**Итого:** ~3,800 записей в основных таблицах

---

## 🎯 Ключевые особенности БД

### 1. **PostGIS геолокация**
- `GEOMETRY(Point, 4326)` - координаты товаров и магазинов
- `GEOMETRY(Polygon, 4326)` - зоны доставки
- SRID 4326 = WGS84 (GPS, Google Maps, Mapbox)

### 2. **Каскадное удаление**
- При удалении пользователя → удаляются его заказы, корзина, сообщения
- При удалении товара → удаляются изображения, отзывы, вопросы
- При удалении заказа → удаляются позиции заказа

### 3. **Индексы для производительности**
- B-tree индексы на FK и часто запрашиваемые поля
- GIST индексы на геоданные (PostGIS)
- Уникальные индексы на email, phone, slug

### 4. **Временные метки**
- `created_at` - дата создания
- `updated_at` - дата обновления (автообновление)
- `last_login` - последний вход

### 5. **Мягкое удаление**
- `is_active` - вместо физического удаления
- `status` - для управления состоянием

---

## 🔍 Полезные запросы

### Топ товаров по рейтингу:
```sql
SELECT id, name, rating, reviews_count 
FROM market.products 
WHERE rating > 4.0 
ORDER BY rating DESC, reviews_count DESC 
LIMIT 10;
```

### Товары с геолокацией:
```sql
SELECT id, name, latitude, longitude, 
       ST_AsText(geo_location) as location
FROM market.products 
WHERE geo_location IS NOT NULL;
```

### Статистика по категориям:
```sql
SELECT c.name, COUNT(p.id) as products_count, 
       AVG(p.rating) as avg_rating
FROM market.categories c
LEFT JOIN market.products p ON c.id = p.category_id
GROUP BY c.id, c.name
ORDER BY products_count DESC;
```

### Активные заказы:
```sql
SELECT o.id, u.full_name, o.total_amount, o.status, o.created_at
FROM market.orders o
JOIN config.users u ON o.user_id = u.id
WHERE o.status NOT IN ('completed', 'cancelled')
ORDER BY o.created_at DESC;
```

---

## 🎉 Готово!

Теперь у меня есть полное понимание реальной структуры БД проекта "Еду на базар"!

**Основные выводы:**
- ✅ 18 таблиц в 2 схемах (config, market)
- ✅ PostGIS для геолокации
- ✅ Полная система отзывов и вопросов
- ✅ Модерация и логирование
- ✅ Чат между пользователями
- ✅ ~3,800 записей в production

**Дата снимка:** 29.11.2025
