# 🔧 Исправление ошибки "schema does not exist"

## ❌ Ошибка
```
psycopg2.errors.InvalidSchemaName: schema "geo" does not exist
```

## ✅ Причина найдена
Миграция Alembic пытается создать таблицы в схемах `config`, `market`, `geo`, но не создает сами схемы.

## 🔧 Решение

Я исправил файл миграции локально. Теперь нужно загрузить его на сервер.

### Вариант 1: Через SCP (рекомендую)

```powershell
# На локальной машине (PowerShell)
scp backend\alembic\versions\8828a8665651_initial_schema.py root@176.99.5.211:/opt/edu-na-bazar/backend/alembic/versions/
# Пароль: sIAS6APDsKh0bL
```

```bash
# На сервере - применить миграцию
ssh root@176.99.5.211
cd /opt/edu-na-bazar
docker-compose exec backend alembic upgrade head
```

### Вариант 2: Создать схемы вручную (быстрее)

```bash
# Подключиться к серверу
ssh root@176.99.5.211
# Пароль: sIAS6APDsKh0bL

# Создать схемы в БД
docker exec -it edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar

# В psql выполнить:
CREATE SCHEMA IF NOT EXISTS config;
CREATE SCHEMA IF NOT EXISTS market;
CREATE SCHEMA IF NOT EXISTS geo;
\q

# Теперь применить миграцию
cd /opt/edu-na-bazar
docker-compose exec backend alembic upgrade head
```

### Вариант 3: Через Docker (если SCP не работает)

```bash
# На сервере
ssh root@176.99.5.211
cd /opt/edu-na-bazar

# Создать схемы
docker exec -it edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar -c "CREATE SCHEMA IF NOT EXISTS config"
docker exec -it edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar -c "CREATE SCHEMA IF NOT EXISTS market"
docker exec -it edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar -c "CREATE SCHEMA IF NOT EXISTS geo"

# Применить миграцию
docker-compose exec backend alembic upgrade head
```

## ✅ Проверка успеха

После применения миграции:

```bash
# 1. Проверить схемы
docker exec -it edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar -c "\dn"

# Должны быть:
# - config
# - geo
# - market
# - public

# 2. Проверить таблицы
docker exec -it edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar -c "\dt market.*"

# Должны быть:
# - market.categories
# - market.products
# - market.stores
# и другие...

# 3. Проверить API
curl http://localhost:8000/api/categories/

# Должно вернуть: [] (пустой массив, т.к. данных пока нет)
```

## 📦 Загрузка данных

После успешного применения миграций нужно загрузить данные:

```powershell
# На локальной машине
docker exec edu-na-bazar-postgres-dev pg_dump -U postgres edu_na_bazar > dump.sql
scp dump.sql root@176.99.5.211:/tmp/
```

```bash
# На сервере
ssh root@176.99.5.211
docker exec -i edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar < /tmp/dump.sql

# Проверить
curl http://localhost:8000/api/categories/
# Должно вернуть JSON с категориями
```

## 🎯 Быстрое решение (копировать и выполнить)

```bash
# Подключиться
ssh root@176.99.5.211

# Создать схемы
docker exec -it edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar << EOF
CREATE SCHEMA IF NOT EXISTS config;
CREATE SCHEMA IF NOT EXISTS market;
CREATE SCHEMA IF NOT EXISTS geo;
EOF

# Применить миграцию
cd /opt/edu-na-bazar
docker-compose exec backend alembic upgrade head

# Проверить
curl http://localhost:8000/api/categories/
```

---

**Время на исправление: 1 минута**

**Рекомендую:** Вариант 2 (создать схемы вручную) - самый быстрый
