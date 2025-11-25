# Исправление ошибок в Production

## Обнаруженные проблемы

### 1. ❌ CORS + Private Network Access Error
```
Access to fetch at 'http://localhost:8000/api/store-owners/all' from origin 'http://176.99.5.211' 
has been blocked by CORS policy: The request client is not a secure context and the resource 
is in more-private address space `loopback`.
```

**Причина:** Frontend обращается к `localhost:8000` вместо `176.99.5.211:8000`

**Решение:** ✅ Исправлено
- Создан `.env.production` с `VITE_API_URL=http://176.99.5.211:8000`
- Заменены все hardcoded `localhost:8000` на переменную окружения
- Исправлены файлы:
  - `src/pages/Map/MapPage.tsx`
  - `src/components/FilterPanel/FilterPanel.tsx`
  - `src/components/ImageUpload/ImageUpload.tsx`
  - `src/components/Auth/AuthModal.tsx`

### 2. ❌ Internal Server Error 500
```
GET http://176.99.5.211:8000/api/categories/ 500 (Internal Server Error)
GET http://176.99.5.211:8000/api/products/ 500 (Internal Server Error)
```

**Причина:** Проблемы на backend (скорее всего БД)

**Нужно проверить:**
1. Подключение к БД
2. Наличие данных в таблицах
3. Логи backend

---

## Шаги для исправления

### Шаг 1: Пересобрать Frontend

```bash
cd c:\python\edu-na-bazar\frontend
npm run build
```

### Шаг 2: Загрузить на сервер

**Вариант A: через SCP**
```bash
scp -r frontend/dist/* root@176.99.5.211:/var/www/edu-na-bazar/
```

**Вариант B: через WinSCP/FileZilla**
1. Подключиться к `176.99.5.211`
2. Логин: `root`
3. Пароль: `sIAS6APDsKh0bL`
4. Загрузить содержимое `frontend/dist/` в `/var/www/edu-na-bazar/`

### Шаг 3: Проверить Backend на сервере

```bash
# Подключиться к серверу
ssh root@176.99.5.211

# Проверить статус контейнеров
docker ps

# Проверить логи backend
docker logs edu-na-bazar-backend-1 --tail=100

# Проверить логи БД
docker logs edu-na-bazar-db-1 --tail=100
```

### Шаг 4: Проверить БД

```bash
# Подключиться к PostgreSQL
docker exec -it edu-na-bazar-db-1 psql -U postgres -d edu_na_bazar

# Проверить наличие данных
SELECT COUNT(*) FROM market.categories;
SELECT COUNT(*) FROM market.products;
SELECT COUNT(*) FROM market.stores;

# Выйти
\q
```

### Шаг 5: Если БД пустая - загрузить данные

```bash
# На локальной машине создать дамп
pg_dump -h localhost -U postgres -d edu_na_bazar > edu_na_bazar_dump.sql

# Загрузить на сервер
scp edu_na_bazar_dump.sql root@176.99.5.211:/tmp/

# На сервере восстановить
docker exec -i edu-na-bazar-db-1 psql -U postgres -d edu_na_bazar < /tmp/edu_na_bazar_dump.sql
```

### Шаг 6: Перезапустить backend (если нужно)

```bash
docker restart edu-na-bazar-backend-1
```

---

## Проверка после исправления

1. Открыть `http://176.99.5.211`
2. Открыть DevTools (F12) → Console
3. Проверить:
   - ✅ Нет ошибок CORS
   - ✅ API запросы идут на `http://176.99.5.211:8000`
   - ✅ Категории загружаются
   - ✅ Товары загружаются
   - ✅ Карта работает

---

## Дополнительная диагностика

### Проверить CORS настройки

```bash
# На сервере
docker exec -it edu-na-bazar-backend-1 cat /app/config.py | grep CORS
```

Должно быть:
```python
CORS_ORIGINS = ["http://176.99.5.211", "http://localhost:3000"]
```

### Проверить переменные окружения

```bash
docker exec -it edu-na-bazar-backend-1 env | grep DATABASE
```

### Тестовый запрос к API

```bash
curl http://176.99.5.211:8000/api/categories/
curl http://176.99.5.211:8000/api/products/?limit=5
```

---

## Контакты для помощи

- Сервер: `176.99.5.211`
- Логин: `root`
- Пароль: `sIAS6APDsKh0bL`
- Frontend: `/var/www/edu-na-bazar/`
- Backend: Docker контейнер `edu-na-bazar-backend-1`
- БД: Docker контейнер `edu-na-bazar-db-1`
