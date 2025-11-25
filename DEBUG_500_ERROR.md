# 🐛 Отладка ошибки 500 на production

## ❌ Ошибка
```
GET http://176.99.5.211:8000/api/categories/ 500 (Internal Server Error)
```

**Хорошая новость:** Backend отвечает! Это не проблема с контейнерами или firewall.

**Плохая новость:** Ошибка 500 = проблема на стороне сервера (скорее всего БД).

---

## 🔍 Диагностика (выполнить на сервере)

### Шаг 1: Подключиться и посмотреть логи

```bash
ssh root@176.99.5.211
# Пароль: sIAS6APDsKh0bL

cd /opt/edu-na-bazar

# Смотреть логи backend в реальном времени
docker-compose logs -f backend
```

### Шаг 2: Типичные ошибки в логах

#### ❌ "relation 'market.categories' does not exist"
**Причина:** Миграции не применены

**Решение:**
```bash
# Проверить версию миграций
docker-compose exec backend alembic current

# Применить миграции
docker-compose exec backend alembic upgrade head

# Проверить что применилось
docker-compose exec backend alembic current
# Должно показать: 8828a8665651 (head)
```

#### ❌ "could not connect to server: Connection refused"
**Причина:** PostgreSQL не запущен или неправильный DATABASE_URL

**Решение:**
```bash
# Проверить что PostgreSQL запущен
docker-compose ps postgres

# Проверить что он отвечает
docker exec edu-na-bazar-postgres-1 pg_isready -U postgres

# Проверить переменные окружения backend
docker exec edu-na-bazar-backend-1 env | grep DATABASE_URL

# Должно быть примерно:
# DATABASE_URL=postgresql+asyncpg://postgres:PASSWORD@postgres:5432/edu_na_bazar
```

#### ❌ "password authentication failed for user 'postgres'"
**Причина:** Неправильный пароль в .env

**Решение:**
```bash
# Проверить .env
cat .env | grep POSTGRES_PASSWORD

# Пароли должны совпадать в:
# 1. POSTGRES_PASSWORD (для контейнера postgres)
# 2. DATABASE_URL (для backend)

# Если не совпадают - исправить .env и перезапустить
nano .env
docker-compose down
docker-compose up -d
```

#### ❌ "database 'edu_na_bazar' does not exist"
**Причина:** БД не создана

**Решение:**
```bash
# Создать БД
docker exec -it edu-na-bazar-postgres-1 psql -U postgres -c "CREATE DATABASE edu_na_bazar;"

# Применить миграции
docker-compose exec backend alembic upgrade head
```

### Шаг 3: Проверить структуру БД

```bash
# Подключиться к PostgreSQL
docker exec -it edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar

# Проверить схемы
\dn

# Должны быть:
# - market
# - config
# - public

# Проверить таблицы в схеме market
\dt market.*

# Должны быть:
# - market.categories
# - market.products
# - market.stores
# и другие...

# Проверить данные
SELECT COUNT(*) FROM market.categories;
SELECT COUNT(*) FROM market.products;

# Выйти
\q
```

### Шаг 4: Если БД пустая - загрузить данные

**На локальной машине (Windows PowerShell):**
```powershell
# Создать дамп локальной БД
docker exec edu-na-bazar-postgres-dev pg_dump -U postgres edu_na_bazar > edu_na_bazar_dump.sql

# Проверить размер файла
ls -lh edu_na_bazar_dump.sql

# Загрузить на сервер
scp edu_na_bazar_dump.sql root@176.99.5.211:/tmp/
# Пароль: sIAS6APDsKh0bL
```

**На сервере:**
```bash
# Восстановить дамп
docker exec -i edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar < /tmp/edu_na_bazar_dump.sql

# Проверить что данные загрузились
docker exec -it edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar -c "SELECT COUNT(*) FROM market.categories"
docker exec -it edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar -c "SELECT COUNT(*) FROM market.products"

# Должно показать количество записей (не 0)
```

### Шаг 5: Проверить работу API

```bash
# Health check
curl http://localhost:8000/health
# Должно вернуть: {"status":"ok"}

# Категории
curl http://localhost:8000/api/categories/
# Должно вернуть JSON с категориями

# Если все ОК - проверить из браузера
curl http://176.99.5.211:8000/api/categories/
```

---

## 🔧 Быстрое решение (если миграции не применены)

```bash
ssh root@176.99.5.211
cd /opt/edu-na-bazar

# Применить миграции
docker-compose exec backend alembic upgrade head

# Проверить
curl http://localhost:8000/api/categories/

# Если вернул JSON - готово!
```

---

## 🔧 Быстрое решение (если БД пустая)

```bash
# На локальной машине
docker exec edu-na-bazar-postgres-dev pg_dump -U postgres edu_na_bazar > dump.sql
scp dump.sql root@176.99.5.211:/tmp/

# На сервере
ssh root@176.99.5.211
docker exec -i edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar < /tmp/dump.sql
curl http://localhost:8000/api/categories/
```

---

## 📋 Команды для копирования

### Проверить логи
```bash
ssh root@176.99.5.211
cd /opt/edu-na-bazar
docker-compose logs backend --tail=100
```

### Применить миграции
```bash
ssh root@176.99.5.211
cd /opt/edu-na-bazar
docker-compose exec backend alembic upgrade head
```

### Проверить БД
```bash
ssh root@176.99.5.211
docker exec -it edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar -c "\dt market.*"
docker exec -it edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar -c "SELECT COUNT(*) FROM market.categories"
```

### Загрузить дамп
```powershell
# Локально
docker exec edu-na-bazar-postgres-dev pg_dump -U postgres edu_na_bazar > dump.sql
scp dump.sql root@176.99.5.211:/tmp/
```

```bash
# На сервере
ssh root@176.99.5.211
docker exec -i edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar < /tmp/dump.sql
```

---

## ✅ Критерии успеха

После исправления должно работать:

1. `curl http://localhost:8000/health` → `{"status":"ok"}`
2. `curl http://localhost:8000/api/categories/` → JSON с категориями
3. `curl http://176.99.5.211:8000/api/categories/` → JSON с категориями
4. В браузере на http://176.99.5.211 нет ошибок 500
5. Категории и товары загружаются

---

**Время на исправление: 5-10 минут**

**Самая вероятная причина:** Миграции не применены или БД пустая
