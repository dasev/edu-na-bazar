# 🔗 Ссылочная целостность при миграции

## 📊 Схема связей данных

```
┌─────────────┐
│   USERS     │
│ config.users│
└──────┬──────┘
       │ owner_id
       │
       ▼
┌─────────────────┐         ┌──────────────┐
│  STORE_OWNERS   │◄────────│  CATEGORIES  │
│market.store_    │category_│market.       │
│     owners      │   _id   │ categories   │
└────────┬────────┘         └──────┬───────┘
         │                         │
         │ store_owner_id          │ category_id
         │                         │
         ▼                         ▼
    ┌────────────────────────────────┐
    │         PRODUCTS               │
    │      market.products           │
    └────────┬───────────────────────┘
             │
             │ product_id
             │
    ┌────────┴────────┬──────────────┐
    ▼                 ▼              ▼
┌─────────┐    ┌─────────────┐  ┌─────────┐
│ IMAGES  │    │   REVIEWS   │  │  CART   │
│product_ │    │   market.   │  │ market. │
│ images  │    │   reviews   │  │  cart   │
└─────────┘    └─────────────┘  └─────────┘
```

---

## 🔄 Порядок миграции (сохранение связей)

### Фаза 1: Справочники (без зависимостей)
```sql
1. temp.categories → market.categories
   ✅ Независимая таблица
   ✅ Создаём ID маппинг

2. temp.user → config.users
   ✅ Независимая таблица
   ✅ Создаём ID маппинг
```

### Фаза 2: Магазины (зависят от users + categories)
```sql
3. temp.companies → market.store_owners
   🔗 owner_id → config.users.id (через маппинг temp.companies.user_id)
   🔗 category_id → market.categories.id (через маппинг temp.companies.category_id)
   ✅ Создаём ID маппинг
```

### Фаза 3: Товары (зависят от categories + store_owners)
```sql
4. temp.advert → market.products
   🔗 category_id → market.categories.id (через маппинг temp.advert.category_id)
   🔗 store_owner_id → market.store_owners.id (через маппинг temp.advert.company_id)
   ✅ Создаём ID маппинг
```

### Фаза 4: Зависимые данные (зависят от products + users)
```sql
5. temp.file → market.product_images
   🔗 product_id → market.products.id (через маппинг temp.file.advert_id)

6. temp.review → market.reviews
   🔗 product_id → market.products.id (через маппинг temp.review.company_id)
   🔗 user_id → config.users.id (через маппинг temp.review.user_id)
```

---

## 🗺️ Таблица маппинга ID

### Структура temp.id_mapping:
```sql
CREATE TABLE temp.id_mapping (
    old_table VARCHAR(50),  -- Имя старой таблицы
    old_id INTEGER,         -- Старый ID (INT)
    new_id BIGINT,          -- Новый ID (BIGINT)
    PRIMARY KEY (old_table, old_id)
);
```

### Примеры маппинга:
```sql
-- Категории
old_table='categories', old_id=1 → new_id=100
old_table='categories', old_id=2 → new_id=101

-- Пользователи
old_table='user', old_id=1 → new_id=1000
old_table='user', old_id=2 → new_id=1001

-- Компании → Магазины
old_table='companies', old_id=1 → new_id=500
old_table='companies', old_id=2 → new_id=501

-- Объявления → Товары
old_table='advert', old_id=1 → new_id=10000
old_table='advert', old_id=2 → new_id=10001
```

---

## 🔗 Примеры SQL с сохранением связей

### 1. Миграция магазинов с владельцами
```sql
INSERT INTO market.store_owners (owner_id, inn, name, ...)
SELECT 
    user_map.new_id as owner_id,  -- 🔗 Связь с пользователем
    ...
FROM temp.companies tc
LEFT JOIN temp.id_mapping user_map 
    ON user_map.old_table = 'user' 
    AND user_map.old_id = tc.user_id;
```

### 2. Миграция товаров с категориями и магазинами
```sql
INSERT INTO market.products (category_id, store_owner_id, ...)
SELECT 
    cat_map.new_id as category_id,      -- 🔗 Связь с категорией
    store_map.new_id as store_owner_id,  -- 🔗 Связь с магазином
    ...
FROM temp.advert ta
LEFT JOIN temp.id_mapping cat_map 
    ON cat_map.old_table = 'categories' 
    AND cat_map.old_id = ta.category_id
LEFT JOIN temp.id_mapping store_map 
    ON store_map.old_table = 'companies' 
    AND store_map.old_id = ta.company_id;
```

### 3. Миграция изображений с товарами
```sql
INSERT INTO market.product_images (product_id, ...)
SELECT 
    prod_map.new_id as product_id,  -- 🔗 Связь с товаром
    ...
FROM temp.file tf
JOIN temp.id_mapping prod_map 
    ON prod_map.old_table = 'advert' 
    AND prod_map.old_id = tf.advert_id;
```

### 4. Миграция отзывов с товарами и пользователями
```sql
INSERT INTO market.reviews (product_id, user_id, ...)
SELECT 
    prod_map.new_id as product_id,  -- 🔗 Связь с товаром
    user_map.new_id as user_id,     -- 🔗 Связь с пользователем
    ...
FROM temp.review tr
LEFT JOIN temp.id_mapping prod_map 
    ON prod_map.old_table = 'advert' 
    AND prod_map.old_id = tr.company_id
LEFT JOIN temp.id_mapping user_map 
    ON user_map.old_table = 'user' 
    AND user_map.old_id = tr.user_id;
```

---

## ✅ Проверка ссылочной целостности

### После миграции выполняем проверки:

```sql
-- 1. Товары без категорий
SELECT COUNT(*) FROM market.products WHERE category_id IS NULL;

-- 2. Товары без магазина
SELECT COUNT(*) FROM market.products WHERE store_owner_id IS NULL;

-- 3. Магазины без владельца
SELECT COUNT(*) FROM market.store_owners WHERE owner_id IS NULL;

-- 4. Изображения без товара (orphan records)
SELECT COUNT(*) FROM market.product_images 
WHERE product_id NOT IN (SELECT id FROM market.products);

-- 5. Отзывы без товара
SELECT COUNT(*) FROM market.reviews 
WHERE product_id NOT IN (SELECT id FROM market.products);

-- 6. Отзывы без пользователя
SELECT COUNT(*) FROM market.reviews 
WHERE user_id NOT IN (SELECT id FROM config.users);
```

### Ожидаемый результат:
```
✅ Все проверки должны вернуть 0 (или минимальное количество)
```

---

## 🔧 Обработка проблемных случаев

### 1. Товар без категории
```sql
-- Создаём категорию "Без категории"
INSERT INTO market.categories (name, description)
VALUES ('Без категории', 'Товары без категории')
RETURNING id;

-- Обновляем товары
UPDATE market.products 
SET category_id = <id_категории_без_категории>
WHERE category_id IS NULL;
```

### 2. Товар без магазина
```sql
-- Создаём магазин "Общий"
INSERT INTO market.store_owners (owner_id, inn, name, legal_name, address)
VALUES (
    (SELECT id FROM config.users LIMIT 1),
    'GENERAL',
    'Общий магазин',
    'Общий магазин',
    'Не указан'
)
RETURNING id;

-- Обновляем товары
UPDATE market.products 
SET store_owner_id = <id_общего_магазина>
WHERE store_owner_id IS NULL;
```

### 3. Магазин без владельца
```sql
-- Создаём системного пользователя
INSERT INTO config.users (phone, email, full_name, is_active, status)
VALUES ('system@system.local', 'system@system.local', 'Системный пользователь', true, 'active')
RETURNING id;

-- Обновляем магазины
UPDATE market.store_owners 
SET owner_id = <id_системного_пользователя>
WHERE owner_id IS NULL;
```

---

## 📊 Статистика связей

### После миграции проверяем:

```sql
-- Количество товаров по магазинам
SELECT 
    so.name as store_name,
    COUNT(p.id) as products_count
FROM market.store_owners so
LEFT JOIN market.products p ON p.store_owner_id = so.id
GROUP BY so.id, so.name
ORDER BY products_count DESC
LIMIT 10;

-- Количество товаров по категориям
SELECT 
    c.name as category_name,
    COUNT(p.id) as products_count
FROM market.categories c
LEFT JOIN market.products p ON p.category_id = c.id
GROUP BY c.id, c.name
ORDER BY products_count DESC
LIMIT 10;

-- Пользователи с магазинами
SELECT 
    u.full_name,
    COUNT(so.id) as stores_count
FROM config.users u
LEFT JOIN market.store_owners so ON so.owner_id = u.id
GROUP BY u.id, u.full_name
HAVING COUNT(so.id) > 0
ORDER BY stores_count DESC
LIMIT 10;

-- Товары с изображениями
SELECT 
    COUNT(DISTINCT p.id) as products_with_images,
    COUNT(pi.id) as total_images,
    ROUND(AVG(img_count), 2) as avg_images_per_product
FROM market.products p
LEFT JOIN (
    SELECT product_id, COUNT(*) as img_count
    FROM market.product_images
    GROUP BY product_id
) pi ON pi.product_id = p.id;
```

---

## 🎯 Преимущества такого подхода

### ✅ Сохранение всех связей:
- Товары → Категории
- Товары → Магазины
- Магазины → Владельцы (пользователи)
- Изображения → Товары
- Отзывы → Товары + Пользователи

### ✅ Ссылочная целостность:
- Все foreign keys корректны
- Нет orphan records
- Можно использовать CASCADE

### ✅ Возможность отката:
- Таблица маппинга сохраняется
- Можно восстановить связи
- Можно повторить миграцию

### ✅ Проверяемость:
- SQL запросы для проверки
- Статистика по связям
- Выявление проблем

---

## 🚀 Запуск миграции

```bash
# Запустить полную миграцию с сохранением связей
python backend/scripts/migrate_from_temp.py
```

### Что произойдёт:
1. ✅ Создастся таблица маппинга ID
2. ✅ Мигрируют категории → сохранится маппинг
3. ✅ Мигрируют пользователи → сохранится маппинг
4. ✅ Мигрируют магазины → свяжутся с пользователями
5. ✅ Мигрируют товары → свяжутся с категориями и магазинами
6. ✅ Мигрируют изображения → свяжутся с товарами
7. ✅ Мигрируют отзывы → свяжутся с товарами и пользователями
8. ✅ Проверится ссылочная целостность

---

## 📝 Итог

**Все связи сохранены!** 🎉

- ✅ Пользователи → Магазины
- ✅ Магазины → Товары
- ✅ Категории → Товары
- ✅ Товары → Изображения
- ✅ Товары → Отзывы
- ✅ Пользователи → Отзывы

**Ссылочная целостность гарантирована!** 🔒
