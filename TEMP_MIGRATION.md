# 🔄 Миграция данных в схему temp

## 📋 Обзор

Скрипт `migrate_to_temp_schema.py` автоматически:
1. Создаёт схему `temp` в PostgreSQL
2. Парсит SQL файлы с данными
3. Конвертирует MySQL синтаксис в PostgreSQL
4. Создаёт таблицы в схеме `temp`
5. Загружает данные из SQL файлов

---

## 📁 Мигрируемые таблицы

| SQL файл | Таблица | Описание |
|----------|---------|----------|
| `seller_inserts.sql` | `temp.seller` | Продавцы |
| `categories_inserts.sql` | `temp.categories` | Категории |
| `companies_inserts.sql` | `temp.companies` | Компании |
| `sub_categories_inserts.sql` | `temp.sub_categories` | Подкатегории |
| `user_inserts.sql` | `temp.user` | Пользователи |
| `review_inserts.sql` | `temp.review` | Отзывы |
| `file_inserts.sql` | `temp.file` | Файлы |
| `advert_inserts.sql` | `temp.advert` | Объявления |

---

## 🚀 Запуск миграции

### Способ 1: BAT файл (Windows)

```bash
migrate_to_temp.bat
```

### Способ 2: Вручную

```bash
cd backend
venv\Scripts\activate
python scripts\migrate_to_temp_schema.py
```

---

## 🔧 Конвертация типов данных

Скрипт автоматически конвертирует MySQL типы в PostgreSQL:

| MySQL | PostgreSQL |
|-------|------------|
| `INT PRIMARY KEY AUTO_INCREMENT` | `SERIAL PRIMARY KEY` |
| `INT` | `INTEGER` |
| `VARCHAR(255)` | `VARCHAR(255)` |
| `TEXT` | `TEXT` |
| `UNIX_TIMESTAMP()` | `EXTRACT(EPOCH FROM NOW())::INTEGER` |

---

## 📊 Проверка результатов

### 1. Список таблиц в схеме temp

```sql
SELECT schemaname, tablename 
FROM pg_tables 
WHERE schemaname = 'temp';
```

### 2. Количество записей в каждой таблице

```sql
SELECT 
    'temp.seller' as table_name, COUNT(*) as count FROM temp.seller
UNION ALL
SELECT 'temp.categories', COUNT(*) FROM temp.categories
UNION ALL
SELECT 'temp.companies', COUNT(*) FROM temp.companies
UNION ALL
SELECT 'temp.sub_categories', COUNT(*) FROM temp.sub_categories
UNION ALL
SELECT 'temp.user', COUNT(*) FROM temp.user
UNION ALL
SELECT 'temp.review', COUNT(*) FROM temp.review
UNION ALL
SELECT 'temp.file', COUNT(*) FROM temp.file
UNION ALL
SELECT 'temp.advert', COUNT(*) FROM temp.advert;
```

### 3. Примеры данных

```sql
-- Категории
SELECT * FROM temp.categories LIMIT 10;

-- Компании
SELECT * FROM temp.companies LIMIT 10;

-- Пользователи
SELECT * FROM temp.user LIMIT 10;

-- Объявления
SELECT * FROM temp.advert LIMIT 10;
```

---

## 🔄 Следующие шаги

После успешной миграции в схему `temp`:

### 1. Маппинг данных на новую структуру

Создать скрипт для переноса данных из `temp.*` в основные таблицы:

```sql
-- Пример: Категории
INSERT INTO categories (name, slug, parent_id, created_at, updated_at)
SELECT 
    name,
    LOWER(REGEXP_REPLACE(name, '[^a-zA-Z0-9]+', '-', 'g')) as slug,
    parent_id,
    TO_TIMESTAMP(created_at) as created_at,
    TO_TIMESTAMP(updated_at) as updated_at
FROM temp.categories;
```

### 2. Маппинг пользователей

```sql
-- Пользователи из temp.user -> users
INSERT INTO users (phone, name, email, created_at, updated_at)
SELECT 
    COALESCE(phone, ''),
    name,
    email,
    TO_TIMESTAMP(created_at),
    TO_TIMESTAMP(updated_at)
FROM temp.user
WHERE email IS NOT NULL;
```

### 3. Маппинг компаний -> магазины

```sql
-- Компании -> stores
INSERT INTO stores (name, description, address, phone, email, status, created_at, updated_at)
SELECT 
    name,
    description,
    address,
    phone,
    email,
    CASE 
        WHEN status = 1 THEN 'active'::store_status
        ELSE 'suspended'::store_status
    END,
    TO_TIMESTAMP(created_at),
    TO_TIMESTAMP(updated_at)
FROM temp.companies;
```

### 4. Маппинг объявлений -> товары

```sql
-- Объявления -> products
INSERT INTO products (name, description, price, category_id, store_id, in_stock, created_at, updated_at)
SELECT 
    a.name,
    a.description,
    a.price::NUMERIC(10,2),
    c.new_category_id,  -- Нужен маппинг категорий
    s.new_store_id,     -- Нужен маппинг магазинов
    a.status = 1,
    TO_TIMESTAMP(a.created_at),
    TO_TIMESTAMP(a.updated_at)
FROM temp.advert a
LEFT JOIN category_mapping c ON c.old_id = a.category_id
LEFT JOIN store_mapping s ON s.old_id = a.company_id;
```

---

## ⚠️ Важные замечания

### 1. Пароли пользователей

**ВАЖНО:** Пароли из старой БД НЕ мигрируются!

Причина: Старые хэши паролей несовместимы с новой системой JWT аутентификации.

Решение:
- Пользователи должны войти через SMS-аутентификацию
- Или сбросить пароль через email

### 2. Временные метки

Старые данные используют UNIX timestamp (INTEGER).
При маппинге конвертируем в PostgreSQL TIMESTAMP:

```sql
TO_TIMESTAMP(unix_timestamp)
```

### 3. Статусы

Старая БД использует INTEGER статусы (0, 1, 2...).
Новая БД использует ENUM типы.

Нужен маппинг:
```sql
CASE 
    WHEN old_status = 1 THEN 'active'::store_status
    WHEN old_status = 0 THEN 'suspended'::store_status
    ELSE 'pending'::store_status
END
```

### 4. ID маппинг

Старые ID (INT) могут конфликтовать с новыми UUID.

Решение:
- Создать таблицы маппинга: `old_id -> new_uuid`
- Использовать при связывании данных

---

## 🗑️ Очистка после миграции

После успешного переноса данных в основные таблицы:

```sql
-- Удалить схему temp со всеми таблицами
DROP SCHEMA temp CASCADE;
```

---

## 📝 Логи миграции

Скрипт выводит детальные логи:

```
🚀 Начинаем миграцию данных в схему temp...
📊 База данных: postgresql+asyncpg://...
📁 Файлов для миграции: 8

📁 Создаём схему temp...
✅ Схема temp создана

============================================================
🔄 Обрабатываем: categories_inserts.sql
============================================================
📋 Создаём таблицу temp.categories...
✅ Таблица temp.categories создана
📥 Загружаем данные в temp.categories...
  ✓ Прогресс: 500/349 (100.0%)
✅ Загружено 349 записей в temp.categories

...

🎉 Миграция завершена!
```

---

## 🐛 Устранение проблем

### Ошибка: "relation temp.xxx already exists"

Решение: Удалите таблицу и запустите снова
```sql
DROP TABLE temp.xxx CASCADE;
```

### Ошибка: "invalid input syntax for type integer"

Причина: Некорректные данные в SQL файле

Решение: Скрипт пропускает такие записи и продолжает

### Ошибка: "connection refused"

Причина: PostgreSQL не запущен

Решение:
```bash
docker-compose up -d
```

---

## 📚 Дополнительные ресурсы

- [PostgreSQL Data Types](https://www.postgresql.org/docs/current/datatype.html)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)

---

## ✅ Чек-лист миграции

- [ ] PostgreSQL запущен (docker-compose up -d)
- [ ] Виртуальное окружение активировано
- [ ] Запущен скрипт migrate_to_temp_schema.py
- [ ] Проверено количество записей в temp таблицах
- [ ] Создан скрипт маппинга данных
- [ ] Данные перенесены в основные таблицы
- [ ] Проверена целостность данных
- [ ] Схема temp удалена

---

**Готово к миграции!** 🚀
