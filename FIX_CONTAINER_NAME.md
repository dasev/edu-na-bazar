# 🔧 Исправление: Неправильное имя контейнера

## ❌ Ошибка
```
Error response from daemon: No such container: edu-na-bazar-postgres-1
```

## ✅ Решение

### Шаг 1: Найти правильное имя контейнера

```bash
# На сервере
docker ps | grep postgres

# Или посмотреть все контейнеры
docker-compose ps
```

### Шаг 2: Создать схемы с правильным именем

Возможные варианты имени контейнера:
- `edu-na-bazar-postgres-1`
- `edu-na-bazar_postgres_1`
- `edu-na-bazar-postgres`
- `edu_na_bazar-postgres-1`

**Попробуйте каждый вариант:**

```bash
# Вариант 1
docker ps | grep postgres

# После того как узнаете имя (например: edu-na-bazar_postgres_1)
# Замените CONTAINER_NAME на реальное имя:

docker exec -it CONTAINER_NAME psql -U postgres -d edu_na_bazar << EOF
CREATE SCHEMA IF NOT EXISTS config;
CREATE SCHEMA IF NOT EXISTS market;
CREATE SCHEMA IF NOT EXISTS geo;
EOF
```

### Шаг 3: Или используйте docker-compose

```bash
cd /opt/edu-na-bazar

# Через docker-compose (не требует знания имени контейнера)
docker-compose exec postgres psql -U postgres -d edu_na_bazar << EOF
CREATE SCHEMA IF NOT EXISTS config;
CREATE SCHEMA IF NOT EXISTS market;
CREATE SCHEMA IF NOT EXISTS geo;
EOF
```

### Шаг 4: Применить миграцию

```bash
cd /opt/edu-na-bazar
docker-compose exec backend alembic upgrade head
```

## 🎯 БЫСТРОЕ РЕШЕНИЕ (копировать целиком)

```bash
cd /opt/edu-na-bazar

# Создать схемы через docker-compose
docker-compose exec postgres psql -U postgres -d edu_na_bazar -c "CREATE SCHEMA IF NOT EXISTS config"
docker-compose exec postgres psql -U postgres -d edu_na_bazar -c "CREATE SCHEMA IF NOT EXISTS market"
docker-compose exec postgres psql -U postgres -d edu_na_bazar -c "CREATE SCHEMA IF NOT EXISTS geo"

# Применить миграцию
docker-compose exec backend alembic upgrade head

# Проверить
curl http://localhost:8000/api/categories/
```

## 📋 Проверка имени контейнера

```bash
# Показать все контейнеры проекта
docker-compose ps

# Показать только postgres
docker-compose ps postgres

# Показать все запущенные контейнеры
docker ps --format "table {{.Names}}\t{{.Status}}"
```

---

**Используйте `docker-compose exec postgres` вместо имени контейнера - это всегда работает!**
