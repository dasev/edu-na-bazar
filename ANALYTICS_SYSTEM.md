# 📊 Система аналитики маркетплейса

## Обзор

Полная система аналитики с 6 дашбордами, отслеживанием событий и микро-конверсий.

## 🎯 Реализованные дашборды

### 1. **Общая динамика** (базовый)
- Новые товары за 30 дней
- Новые магазины за 30 дней
- Новые заказы за 30 дней
- Топ категорий (Pie Chart)

**Endpoint:** `/api/analytics/dashboard`

### 2. **💰 Финансовая аналитика**
- Общая выручка
- Средний чек
- Выручка по категориям
- Динамика выручки по дням

**Endpoint:** `/api/analytics/financial`

### 3. **👥 Активность пользователей**
- Новые регистрации
- Активные пользователи
- Средняя сессия
- Динамика регистраций
- Активность по дням недели

**Endpoint:** `/api/analytics/user-activity`

### 4. **🎯 Конверсия и воронка**

**Основные метрики:**
- Общая конверсия (просмотры → заказы)
- Конверсия корзина → заказ
- Брошенные корзины

**Микро-конверсии:**
- Клики по товарам
- Клики "Добавить в корзину"
- Начало оформления заказа

**Временные метрики:**
- Среднее время до покупки (минуты)
- Средняя сумма брошенной корзины

**Визуализация:**
- Воронка продаж (Funnel)
- Динамика конверсии по дням
- Конверсия по категориям

**Endpoint:** `/api/analytics/conversion`

### 5. **📦 Товарная аналитика**
- Топ-10 товаров по конверсии
- Худшие товары по конверсии
- Товары-локомотивы (покупаются с другими)
- Cross-sell пары (часто покупаемые вместе)

**Endpoint:** `/api/analytics/products`

### 6. **🗺️ География**
- Топ-10 городов
- Заказы по городам
- Выручка по городам (Pie Chart)
- Конверсия по городам

**Endpoint:** `/api/analytics/geography`

---

## 📈 Система отслеживания событий

### Таблица `market.user_events`

**Поля:**
- `id` - ID события
- `user_id` - ID пользователя (nullable)
- `session_id` - ID сессии
- `event_type` - тип события
- `product_id` - ID товара (nullable)
- `order_id` - ID заказа (nullable)
- `event_data` - дополнительные данные (JSON)
- `created_at` - время события

**Типы событий:**
- `product_click` - клик по товару
- `add_to_cart_click` - клик "Добавить в корзину"
- `checkout_start` - начало оформления заказа
- `checkout_complete` - завершение оформления

### API для трекинга

**Endpoint:** `POST /api/events/track`

**Body:**
```json
{
  "event_type": "add_to_cart_click",
  "product_id": 123,
  "order_id": null,
  "event_data": null
}
```

### Frontend интеграция

**Утилита:** `frontend/src/utils/analytics.ts`

```typescript
import { trackEvent } from '../utils/analytics'

// Трекинг клика "В корзину"
trackEvent('add_to_cart_click', productId)

// Трекинг начала оформления
trackEvent('checkout_start')

// Трекинг завершения заказа
trackEvent('checkout_complete', undefined, orderId)
```

**Интегрировано в:**
- `ProductPage.tsx` - клик "Добавить в корзину"
- `CheckoutPage.tsx` - начало и завершение оформления

---

## 📊 Отслеживание просмотров товаров

### Таблица `market.product_views`

**Поля:**
- `id` - ID просмотра
- `user_id` - ID пользователя (nullable)
- `product_id` - ID товара
- `session_id` - ID сессии
- `created_at` - время просмотра

### API

**Endpoint:** `POST /api/product-views/{product_id}`

**Интегрировано в:** `ProductPage.tsx` (автоматически при открытии товара)

---

## 🗺️ Система оптимизации маршрутов доставки

### Концепция

Решение задачи коммивояжера (TSP) для оптимизации маршрута доставки товаров из разных магазинов.

### Компоненты

**1. Модель:** `backend/models/delivery_route.py`
- Хранит оптимизированные маршруты
- Waypoints (точки маршрута)
- Метрики: distance, duration
- Геометрия маршрута (polyline)

**2. Сервис:** `backend/services/route_optimizer.py`
- Интеграция с Yandex Routes API
- Алгоритмы оптимизации:
  - Полный перебор (≤3 точки)
  - Жадный алгоритм (>3 точки)

**3. Таблица:** `market.delivery_routes`

```sql
CREATE TABLE market.delivery_routes (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL UNIQUE,
    waypoints JSONB NOT NULL,
    optimized_order JSONB,
    total_distance FLOAT,
    total_duration FLOAT,
    route_geometry TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

### Использование

```python
from services.route_optimizer import RouteOptimizer

optimizer = RouteOptimizer(api_key="your-yandex-key")
result = await optimizer.optimize_waypoints(
    start_point=(55.75, 37.61),  # Склад
    waypoints=[(55.76, 37.62), (55.77, 37.63)],  # Магазины
    end_point=(55.78, 37.64)  # Покупатель
)
# result: {optimized_order, distance, duration, geometry}
```

**TODO:**
- Получить Yandex API ключ: https://developer.tech.yandex.ru/
- Выполнить SQL миграцию
- Добавить endpoint в orders.py
- Интегрировать в процесс создания заказа

---

## 🚀 Запуск и использование

### Backend

```bash
# Перезапуск
docker-compose -f docker-compose.dev.yml restart backend

# Логи
docker-compose -f docker-compose.dev.yml logs backend --tail=100
```

### Frontend

Открыть: `http://localhost:5173/dashboard`

**Вкладки:**
1. 📊 Общая динамика
2. 💰 Финансовая аналитика
3. 👥 Активность пользователей
4. 🎯 Конверсия и воронка
5. 📦 Товарная аналитика
6. 🗺️ География

---

## 📝 SQL миграции

### 1. Таблица user_events

```sql
CREATE TABLE market.user_events (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT,
    session_id VARCHAR(255),
    event_type VARCHAR(50) NOT NULL,
    product_id BIGINT,
    order_id BIGINT,
    event_data TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_user_events_user_id 
        FOREIGN KEY (user_id) REFERENCES config.users(id) ON DELETE SET NULL,
    CONSTRAINT fk_user_events_product_id 
        FOREIGN KEY (product_id) REFERENCES market.products(id) ON DELETE SET NULL,
    CONSTRAINT fk_user_events_order_id 
        FOREIGN KEY (order_id) REFERENCES market.orders(id) ON DELETE SET NULL
);

CREATE INDEX ix_market_user_events_user_id ON market.user_events(user_id);
CREATE INDEX ix_market_user_events_session_id ON market.user_events(session_id);
CREATE INDEX ix_market_user_events_event_type ON market.user_events(event_type);
CREATE INDEX ix_market_user_events_product_id ON market.user_events(product_id);
CREATE INDEX ix_market_user_events_order_id ON market.user_events(order_id);
CREATE INDEX ix_market_user_events_created_at ON market.user_events(created_at);
```

### 2. Таблица product_views

```sql
CREATE TABLE market.product_views (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT,
    product_id BIGINT NOT NULL,
    session_id VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_product_views_user_id 
        FOREIGN KEY (user_id) REFERENCES config.users(id) ON DELETE SET NULL,
    CONSTRAINT fk_product_views_product_id 
        FOREIGN KEY (product_id) REFERENCES market.products(id) ON DELETE CASCADE
);

CREATE INDEX ix_market_product_views_user_id ON market.product_views(user_id);
CREATE INDEX ix_market_product_views_product_id ON market.product_views(product_id);
CREATE INDEX ix_market_product_views_session_id ON market.product_views(session_id);
CREATE INDEX ix_market_product_views_created_at ON market.product_views(created_at);
```

### 3. Таблица delivery_routes (TODO)

```sql
CREATE TABLE market.delivery_routes (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL UNIQUE,
    waypoints JSONB NOT NULL,
    optimized_order JSONB,
    total_distance FLOAT,
    total_duration FLOAT,
    route_geometry TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_delivery_routes_order_id 
        FOREIGN KEY (order_id) REFERENCES market.orders(id) ON DELETE CASCADE
);

CREATE INDEX ix_market_delivery_routes_order_id ON market.delivery_routes(order_id);
CREATE INDEX ix_market_delivery_routes_created_at ON market.delivery_routes(created_at);
```

---

## 🐛 Исправленные ошибки

1. **ORM mapping errors:**
   - Исправлены relationships в User, Order, CartItem
   - Заменены `backref` на `back_populates`

2. **SQLAlchemy reserved names:**
   - `metadata` → `event_data` в UserEvent

3. **PostgreSQL compatibility:**
   - `SPLIT_PART` → `SUBSTRING` в географических запросах

4. **Export/Import errors:**
   - Исправлены named exports в дашбордах

---

## 📚 Структура файлов

### Backend

```
backend/
├── models/
│   ├── user_event.py          # Модель событий
│   ├── product_view.py        # Модель просмотров
│   └── delivery_route.py      # Модель маршрутов (TODO)
├── services/
│   └── route_optimizer.py     # Сервис оптимизации маршрутов
└── api/routers/
    ├── analytics.py           # 6 endpoints аналитики
    ├── events.py              # Трекинг событий
    └── product_views.py       # Трекинг просмотров
```

### Frontend

```
frontend/src/pages/Dashboard/
├── DashboardPage.tsx          # Главная страница с вкладками
├── hooks/
│   ├── useDashboardData.ts    # Базовый дашборд
│   ├── useFinancialData.ts    # Финансы
│   ├── useUserActivityData.ts # Активность
│   ├── useConversionData.ts   # Конверсия
│   ├── useProductAnalytics.ts # Товары
│   └── useGeoAnalytics.ts     # География
└── components/
    ├── FinancialDashboard.tsx
    ├── UserActivityDashboard.tsx
    ├── ConversionDashboard.tsx
    ├── ProductAnalyticsDashboard.tsx
    └── GeoDashboard.tsx
```

---

## 🎯 Следующие шаги (TODO)

1. **Оптимизация маршрутов:**
   - Получить Yandex API ключ
   - Выполнить миграцию delivery_routes
   - Добавить endpoint в orders.py
   - Интегрировать в создание заказа
   - Показать маршрут на карте

2. **Улучшения аналитики:**
   - Когортный анализ
   - A/B тесты
   - Тепловая карта конверсии
   - Экспорт отчетов (PDF/Excel)

3. **Производительность:**
   - Кэширование аналитики (Redis)
   - Предрасчет метрик (Celery)
   - Индексы БД

---

## 📞 API Reference

### Analytics Endpoints

| Endpoint | Method | Описание |
|----------|--------|----------|
| `/api/analytics/dashboard` | GET | Базовый дашборд |
| `/api/analytics/financial` | GET | Финансовая аналитика |
| `/api/analytics/user-activity` | GET | Активность пользователей |
| `/api/analytics/conversion` | GET | Конверсия и воронка |
| `/api/analytics/products` | GET | Товарная аналитика |
| `/api/analytics/geography` | GET | География |

### Tracking Endpoints

| Endpoint | Method | Описание |
|----------|--------|----------|
| `/api/events/track` | POST | Трекинг событий |
| `/api/product-views/{id}` | POST | Трекинг просмотров |

---

## 🔧 Конфигурация

### Environment Variables

```env
# Yandex Routes API (TODO)
YANDEX_ROUTES_API_KEY=your-key-here
```

### DevExtreme Components

Используемые компоненты:
- `Chart` - линейные и столбчатые графики
- `PieChart` - круговые диаграммы
- `Funnel` - воронка продаж
- `DataGrid` - таблицы данных
- `TabPanel` - вкладки дашбордов

---

**Дата создания:** 30.11.2025  
**Версия:** 1.0  
**Статус:** ✅ Готово к использованию
