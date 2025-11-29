# 📋 План маппинга данных из temp в основные таблицы

## 🎯 Цель
Перенести данные из схемы `temp` в основные таблицы проекта "Еду на базар"

---

## 📊 Доступные данные в temp

| Таблица | Записей | Статус | Приоритет |
|---------|---------|--------|-----------|
| `temp.categories` | 331 | ✅ Готово | 🔴 Высокий |
| `temp.companies` | 678 | ✅ Готово | 🔴 Высокий |
| `temp.sub_categories` | 500 | ✅ Готово | 🟡 Средний |
| `temp.file` | 9,765 | ✅ Готово | 🟢 Низкий |
| `temp.user` | 2,571 | ✅ Готово | 🔴 Высокий |
| `temp.advert` | 14,139 | ✅ Готово | 🔴 Высокий |
| `temp.review` | 15 | ✅ Готово | 🟢 Низкий |
| `temp.seller` | 0 | ❌ Пусто | - |

---

## 🗺️ Маппинг таблиц

### 1. 🔴 КАТЕГОРИИ (Высокий приоритет)

**Источник:** `temp.categories` (331 записей)  
**Цель:** `market.categories`

#### Структура temp.categories:
```sql
id          INTEGER         -- ID категории
name        VARCHAR         -- Название (например: /agrotovary/)
parent_id   INTEGER         -- Родительская категория
created_at  INTEGER         -- UNIX timestamp
updated_at  INTEGER         -- UNIX timestamp
```

#### Структура market.categories:
```sql
id          BIGINT          -- ID категории
name        TEXT            -- Название
description TEXT            -- Описание
image       TEXT            -- Изображение
parent_id   BIGINT          -- Родительская категория
created_at  TIMESTAMP       -- Дата создания
updated_at  TIMESTAMP       -- Дата обновления
```

#### Маппинг:
```sql
INSERT INTO market.categories (name, parent_id, created_at, updated_at)
SELECT 
    -- Очищаем название от слешей
    TRIM(BOTH '/' FROM name) as name,
    parent_id,
    TO_TIMESTAMP(created_at) as created_at,
    TO_TIMESTAMP(updated_at) as updated_at
FROM temp.categories
WHERE name IS NOT NULL;
```

#### Что получим:
- ✅ 331 категория
- ✅ Иерархическая структура (parent_id)
- ✅ Временные метки

---

### 2. 🔴 КОМПАНИИ → МАГАЗИНЫ (Высокий приоритет)

**Источник:** `temp.companies` (678 записей)  
**Цель:** `market.stores`

#### Структура temp.companies:
```sql
id          INTEGER         -- ID компании
name        VARCHAR         -- Название
description TEXT            -- Описание
user_id     INTEGER         -- Владелец
phone       VARCHAR         -- Телефон
email       VARCHAR         -- Email
address     TEXT            -- Адрес
logo        VARCHAR         -- Логотип
status      INTEGER         -- Статус (1=active)
created_at  INTEGER         -- UNIX timestamp
updated_at  INTEGER         -- UNIX timestamp
category_id INTEGER         -- Категория компании
```

#### Структура market.stores:
```sql
id              BIGINT          -- ID магазина
name            TEXT            -- Название
description     TEXT            -- Описание
address         TEXT            -- Адрес
phone           TEXT            -- Телефон
email           TEXT            -- Email
working_hours   TEXT            -- Время работы
location        GEOMETRY        -- Координаты (PostGIS)
delivery_zone   GEOMETRY        -- Зона доставки
image           TEXT            -- Изображение
is_active       BOOLEAN         -- Активен
created_at      TIMESTAMP       -- Дата создания
updated_at      TIMESTAMP       -- Дата обновления
```

#### Маппинг:
```sql
INSERT INTO market.stores (name, description, address, phone, email, image, is_active, created_at, updated_at)
SELECT 
    name,
    description,
    address,
    NULLIF(phone, '') as phone,
    NULLIF(email, '') as email,
    logo as image,
    (status = 1) as is_active,
    TO_TIMESTAMP(created_at) as created_at,
    TO_TIMESTAMP(updated_at) as updated_at
FROM temp.companies
WHERE name IS NOT NULL;
```

#### Что получим:
- ✅ 678 магазинов
- ✅ Контакты (телефон, email)
- ✅ Адреса
- ⚠️ Координаты нужно будет добавить отдельно (геокодирование)

---

### 3. 🔴 ПОЛЬЗОВАТЕЛИ (Высокий приоритет)

**Источник:** `temp.user` (2,571 записей)  
**Цель:** `config.users`

#### Структура temp.user:
```sql
id              INTEGER         -- ID пользователя
name            VARCHAR         -- Имя
email           VARCHAR         -- Email (UNIQUE)
phone           VARCHAR         -- Телефон
password_hash   VARCHAR         -- Хэш пароля (NULL)
role            VARCHAR         -- Роль (user)
status          INTEGER         -- Статус (1=active)
created_at      INTEGER         -- UNIX timestamp
updated_at      INTEGER         -- UNIX timestamp
last_login      INTEGER         -- Последний вход
```

#### Структура config.users:
```sql
id              BIGINT          -- ID пользователя
phone           TEXT            -- Телефон (UNIQUE, NOT NULL)
email           TEXT            -- Email (UNIQUE)
full_name       TEXT            -- Полное имя
address         TEXT            -- Адрес
is_active       BOOLEAN         -- Активен
is_verified     BOOLEAN         -- Подтвержден
status          TEXT            -- Статус (active, blocked)
created_at      TIMESTAMP       -- Дата создания
updated_at      TIMESTAMP       -- Дата обновления
last_login      TIMESTAMP       -- Последний вход
```

#### Маппинг:
```sql
INSERT INTO config.users (phone, email, full_name, is_active, status, created_at, updated_at, last_login)
SELECT 
    -- Если телефона нет, генерируем временный
    COALESCE(NULLIF(phone, ''), 'temp_' || id || '@temp.com') as phone,
    NULLIF(email, '') as email,
    name as full_name,
    (status = 1) as is_active,
    CASE WHEN status = 1 THEN 'active' ELSE 'blocked' END as status,
    TO_TIMESTAMP(created_at) as created_at,
    TO_TIMESTAMP(updated_at) as updated_at,
    CASE WHEN last_login IS NOT NULL THEN TO_TIMESTAMP(last_login) ELSE NULL END as last_login
FROM temp.user
WHERE email IS NOT NULL
ON CONFLICT (email) DO NOTHING;  -- Пропускаем дубликаты
```

#### Что получим:
- ✅ ~2,571 пользователь
- ✅ Email адреса
- ⚠️ Телефоны могут быть пустыми (нужна обработка)
- ⚠️ Пароли НЕ мигрируются (пользователи войдут через SMS)

---

### 4. 🔴 ОБЪЯВЛЕНИЯ → ТОВАРЫ (Высокий приоритет)

**Источник:** `temp.advert` (14,139 записей)  
**Цель:** `market.products`

#### Структура temp.advert:
```sql
id              INTEGER         -- ID объявления
title           VARCHAR         -- Название
description     TEXT            -- Описание
price           NUMERIC         -- Цена
company_id      INTEGER         -- Компания
category_id     INTEGER         -- Категория
contact_phone   VARCHAR         -- Контактный телефон
status          INTEGER         -- Статус (1=active)
views           INTEGER         -- Просмотры
created_at      INTEGER         -- UNIX timestamp
updated_at      INTEGER         -- UNIX timestamp
```

#### Структура market.products:
```sql
id              BIGINT          -- ID товара
name            TEXT            -- Название
description     TEXT            -- Описание
price           DOUBLE          -- Цена
image           TEXT            -- Изображение
category_id     BIGINT          -- Категория
store_owner_id  BIGINT          -- Владелец магазина
rating          DOUBLE          -- Рейтинг
reviews_count   BIGINT          -- Количество отзывов
in_stock        BOOLEAN         -- В наличии
unit            TEXT            -- Единица измерения
views           BIGINT          -- Просмотры
location        TEXT            -- Местоположение
status          TEXT            -- Статус (active, archived)
created_at      TIMESTAMP       -- Дата создания
updated_at      TIMESTAMP       -- Дата обновления
```

#### Маппинг (СЛОЖНЫЙ - требует связей):
```sql
-- Шаг 1: Создать таблицу маппинга старых ID на новые
CREATE TABLE IF NOT EXISTS temp.id_mapping (
    old_table VARCHAR(50),
    old_id INTEGER,
    new_id BIGINT,
    PRIMARY KEY (old_table, old_id)
);

-- Шаг 2: Сохранить маппинг категорий
INSERT INTO temp.id_mapping (old_table, old_id, new_id)
SELECT 'categories', tc.id, mc.id
FROM temp.categories tc
JOIN market.categories mc ON TRIM(BOTH '/' FROM tc.name) = mc.name;

-- Шаг 3: Сохранить маппинг компаний → магазинов
INSERT INTO temp.id_mapping (old_table, old_id, new_id)
SELECT 'companies', tco.id, ms.id
FROM temp.companies tco
JOIN market.stores ms ON tco.name = ms.name;

-- Шаг 4: Вставить товары с маппингом
INSERT INTO market.products (
    name, description, price, category_id, store_owner_id, 
    in_stock, views, status, created_at, updated_at
)
SELECT 
    ta.title as name,
    ta.description,
    ta.price::DOUBLE PRECISION,
    cat_map.new_id as category_id,
    store_map.new_id as store_owner_id,
    (ta.status = 1) as in_stock,
    COALESCE(ta.views, 0) as views,
    CASE WHEN ta.status = 1 THEN 'active' ELSE 'archived' END as status,
    TO_TIMESTAMP(ta.created_at) as created_at,
    TO_TIMESTAMP(ta.updated_at) as updated_at
FROM temp.advert ta
LEFT JOIN temp.id_mapping cat_map ON cat_map.old_table = 'categories' AND cat_map.old_id = ta.category_id
LEFT JOIN temp.id_mapping store_map ON store_map.old_table = 'companies' AND store_map.old_id = ta.company_id
WHERE ta.title IS NOT NULL;
```

#### Что получим:
- ✅ ~14,139 товаров
- ✅ Цены
- ✅ Описания
- ✅ Связи с категориями
- ✅ Связи с магазинами
- ✅ Количество просмотров

---

### 5. 🟡 ПОДКАТЕГОРИИ (Средний приоритет)

**Источник:** `temp.sub_categories` (500 записей)  
**Цель:** `market.categories` (как дочерние категории)

#### Структура temp.sub_categories:
```sql
id          INTEGER         -- ID подкатегории
name        VARCHAR         -- Название
category_id INTEGER         -- Родительская категория
created_at  INTEGER         -- UNIX timestamp
updated_at  INTEGER         -- UNIX timestamp
```

#### Маппинг:
```sql
INSERT INTO market.categories (name, parent_id, created_at, updated_at)
SELECT 
    tsc.name,
    cat_map.new_id as parent_id,
    TO_TIMESTAMP(tsc.created_at) as created_at,
    TO_TIMESTAMP(tsc.updated_at) as updated_at
FROM temp.sub_categories tsc
LEFT JOIN temp.id_mapping cat_map ON cat_map.old_table = 'categories' AND cat_map.old_id = tsc.category_id
WHERE tsc.name IS NOT NULL;
```

#### Что получим:
- ✅ 500 подкатегорий
- ✅ Связь с родительскими категориями

---

### 6. 🟢 ФАЙЛЫ → ИЗОБРАЖЕНИЯ ТОВАРОВ (Низкий приоритет)

**Источник:** `temp.file` (9,765 записей)  
**Цель:** `market.product_images`

#### Структура temp.file:
```sql
id          INTEGER         -- ID файла
filename    VARCHAR         -- Имя файла
path        VARCHAR         -- Путь к файлу
type        VARCHAR         -- Тип (image)
advert_id   INTEGER         -- ID объявления
company_id  INTEGER         -- ID компании
size        INTEGER         -- Размер файла
created_at  INTEGER         -- UNIX timestamp
```

#### Маппинг:
```sql
INSERT INTO market.product_images (product_id, image_url, is_primary, created_at)
SELECT 
    prod_map.new_id as product_id,
    tf.path as image_url,
    false as is_primary,  -- Первое изображение сделаем primary отдельно
    TO_TIMESTAMP(tf.created_at) as created_at
FROM temp.file tf
JOIN temp.id_mapping prod_map ON prod_map.old_table = 'advert' AND prod_map.old_id = tf.advert_id
WHERE tf.type = 'image' AND tf.advert_id IS NOT NULL;
```

#### Что получим:
- ✅ ~9,765 изображений товаров
- ✅ Связь с товарами

---

### 7. 🟢 ОТЗЫВЫ (Низкий приоритет)

**Источник:** `temp.review` (15 записей)  
**Цель:** `market.reviews`

#### Структура temp.review:
```sql
id          INTEGER         -- ID отзыва
company_id  INTEGER         -- ID компании
user_id     INTEGER         -- ID пользователя
rating      INTEGER         -- Рейтинг (1-5)
text        TEXT            -- Текст отзыва
status      INTEGER         -- Статус
created_at  INTEGER         -- UNIX timestamp
updated_at  INTEGER         -- UNIX timestamp
```

#### Маппинг:
```sql
INSERT INTO market.reviews (product_id, user_id, rating, comment, created_at, updated_at)
SELECT 
    prod_map.new_id as product_id,
    user_map.new_id as user_id,
    tr.rating,
    tr.text as comment,
    TO_TIMESTAMP(tr.created_at) as created_at,
    TO_TIMESTAMP(tr.updated_at) as updated_at
FROM temp.review tr
LEFT JOIN temp.id_mapping prod_map ON prod_map.old_table = 'companies' AND prod_map.old_id = tr.company_id
LEFT JOIN temp.id_mapping user_map ON user_map.old_table = 'user' AND user_map.old_id = tr.user_id
WHERE tr.text IS NOT NULL;
```

---

## 📝 Порядок миграции

### Фаза 1: Справочники (без зависимостей)
1. ✅ **Категории** (`temp.categories` → `market.categories`)
2. ✅ **Магазины** (`temp.companies` → `market.stores`)
3. ✅ **Пользователи** (`temp.user` → `config.users`)

### Фаза 2: Создание маппинга ID
4. ✅ **Таблица маппинга** (`temp.id_mapping`)
5. ✅ **Заполнение маппинга** (категории, магазины, пользователи)

### Фаза 3: Основные данные (с зависимостями)
6. ✅ **Подкатегории** (`temp.sub_categories` → `market.categories`)
7. ✅ **Товары** (`temp.advert` → `market.products`)

### Фаза 4: Дополнительные данные
8. ✅ **Изображения** (`temp.file` → `market.product_images`)
9. ✅ **Отзывы** (`temp.review` → `market.reviews`)

---

## ⚠️ Важные замечания

### 1. Пароли пользователей
**НЕ мигрируются!** Пользователи должны войти через SMS-аутентификацию.

### 2. Телефоны пользователей
Многие пустые. Решение:
- Генерировать временные: `temp_{id}@temp.com`
- Пользователи обновят при первом входе

### 3. Координаты магазинов
В temp нет координат. Решение:
- Использовать геокодирование адресов
- Или добавить вручную позже

### 4. ID маппинг
Старые INT ID → новые BIGINT ID. Нужна таблица маппинга.

### 5. Дубликаты
Использовать `ON CONFLICT DO NOTHING` для email/phone.

---

## 🚀 Следующий шаг

Создать скрипт миграции:
```bash
python backend/scripts/migrate_from_temp.py
```

Этот скрипт выполнит все фазы миграции автоматически.

---

## 📊 Ожидаемый результат

После миграции получим:
- ✅ ~331 категория
- ✅ ~500 подкатегорий
- ✅ ~678 магазинов
- ✅ ~2,571 пользователь
- ✅ ~14,139 товаров
- ✅ ~9,765 изображений
- ✅ ~15 отзывов

**Итого:** ~28,000 записей в основных таблицах! 🎉
