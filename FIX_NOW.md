# ⚡ ИСПРАВИТЬ СЕЙЧАС - Ошибка 500

## 🎯 Проблема
```
GET http://176.99.5.211:8000/api/categories/ 500 (Internal Server Error)
```

## ✅ Хорошие новости
- Backend работает (отвечает на запросы)
- Контейнеры запущены
- Это НЕ проблема с CORS или firewall

## ❌ Плохие новости
- Ошибка 500 = проблема на сервере
- Скорее всего: миграции не применены или БД пустая

---

## 🚀 РЕШЕНИЕ ЗА 2 МИНУТЫ

### Вариант 1: Автоматическая диагностика

```bash
# Подключиться к серверу
ssh root@176.99.5.211
# Пароль: sIAS6APDsKh0bL

# Перейти в проект
cd /opt/edu-na-bazar

# Загрузить скрипт диагностики (если его нет)
# Скопируйте содержимое diagnose.sh на сервер

# Запустить диагностику
chmod +x diagnose.sh
bash diagnose.sh
```

### Вариант 2: Ручная проверка (БЫСТРО)

```bash
# 1. Подключиться
ssh root@176.99.5.211
cd /opt/edu-na-bazar

# 2. Посмотреть логи backend (САМОЕ ВАЖНОЕ!)
docker-compose logs backend --tail=50

# Ищите в логах:
# - "relation does not exist" → нужны миграции
# - "could not connect" → проблема с БД
# - "password authentication failed" → неправильный пароль
```

---

## 🔧 ТИПИЧНЫЕ РЕШЕНИЯ

### Решение 1: Применить миграции (90% случаев)

```bash
ssh root@176.99.5.211
cd /opt/edu-na-bazar

# Применить миграции
docker-compose exec backend alembic upgrade head

# Проверить
curl http://localhost:8000/api/categories/

# Если вернул JSON - ГОТОВО! ✅
```

### Решение 2: Загрузить данные в БД

**Если миграции применены, но БД пустая:**

```powershell
# На локальной машине (Windows)
docker exec edu-na-bazar-postgres-dev pg_dump -U postgres edu_na_bazar > dump.sql
scp dump.sql root@176.99.5.211:/tmp/
```

```bash
# На сервере
ssh root@176.99.5.211
docker exec -i edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar < /tmp/dump.sql

# Проверить
curl http://localhost:8000/api/categories/
```

### Решение 3: Перезапустить все

**Если ничего не помогло:**

```bash
ssh root@176.99.5.211
cd /opt/edu-na-bazar

# Остановить
docker-compose down

# Запустить заново
docker-compose up -d

# Подождать 30 секунд
sleep 30

# Применить миграции
docker-compose exec backend alembic upgrade head

# Проверить
curl http://localhost:8000/api/categories/
```

---

## 📋 КОМАНДЫ ДЛЯ КОПИРОВАНИЯ

### Посмотреть логи
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
curl http://localhost:8000/api/categories/
```

### Проверить БД
```bash
ssh root@176.99.5.211
docker exec -it edu-na-bazar-postgres-1 psql -U postgres -d edu_na_bazar
\dt market.*
SELECT COUNT(*) FROM market.categories;
\q
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

## ✅ ПРОВЕРКА УСПЕХА

После исправления проверьте:

```bash
# 1. Health endpoint
curl http://176.99.5.211:8000/health
# Должно вернуть: {"status":"ok"}

# 2. Categories API
curl http://176.99.5.211:8000/api/categories/
# Должно вернуть: JSON с категориями

# 3. В браузере
# Откройте: http://176.99.5.211
# Должны загрузиться категории и товары
```

---

## 🎯 САМОЕ ВЕРОЯТНОЕ РЕШЕНИЕ

**99% что нужно просто применить миграции:**

```bash
ssh root@176.99.5.211
cd /opt/edu-na-bazar
docker-compose exec backend alembic upgrade head
```

**Время: 30 секунд**

---

## 📞 ЕСЛИ НЕ ПОМОГЛО

Пришлите вывод команды:
```bash
docker-compose logs backend --tail=50
```

Это покажет точную ошибку.
