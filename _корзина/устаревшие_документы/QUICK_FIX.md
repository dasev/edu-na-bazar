# Быстрое исправление ошибок Production

## Проблемы

### 1. CORS Error - Frontend обращается к localhost
❌ `Access to fetch at 'http://localhost:8000' from origin 'http://176.99.5.211' has been blocked`

### 2. Backend возвращает 500 ошибки
❌ `GET http://176.99.5.211:8000/api/categories/ 500 (Internal Server Error)`

---

## Быстрое решение

### 1️⃣ Пересобрать Frontend (2 минуты)

```bash
# Запустить bat-файл
REBUILD_AND_DEPLOY.bat
```

Или вручную:
```bash
cd frontend
npm run build
```

### 2️⃣ Загрузить на сервер

**Через WinSCP:**
1. Подключиться к `176.99.5.211` (root / sIAS6APDsKh0bL)
2. Загрузить `frontend/dist/*` → `/var/www/edu-na-bazar/`

**Через командную строку:**
```bash
scp -r frontend/dist/* root@176.99.5.211:/var/www/edu-na-bazar/
```

### 3️⃣ Проверить Backend

```bash
# Подключиться к серверу
ssh root@176.99.5.211

# Проверить логи
docker logs edu-na-bazar-backend-1 --tail=50

# Проверить БД
docker exec -it edu-na-bazar-db-1 psql -U postgres -d edu_na_bazar -c "SELECT COUNT(*) FROM market.categories;"
```

### 4️⃣ Если БД пустая

```bash
# На локальной машине
pg_dump -h localhost -U postgres -d edu_na_bazar > dump.sql

# Загрузить на сервер
scp dump.sql root@176.99.5.211:/tmp/

# На сервере восстановить
ssh root@176.99.5.211
docker exec -i edu-na-bazar-db-1 psql -U postgres -d edu_na_bazar < /tmp/dump.sql
```

---

## Что исправлено в коде

✅ Создан `.env.production`:
```
VITE_API_URL=http://176.99.5.211:8000
```

✅ Заменены hardcoded URL в файлах:
- `src/pages/Map/MapPage.tsx`
- `src/components/FilterPanel/FilterPanel.tsx`
- `src/components/ImageUpload/ImageUpload.tsx`
- `src/components/Auth/AuthModal.tsx`

---

## Проверка

После загрузки откройте `http://176.99.5.211` и проверьте консоль (F12):
- ✅ Нет ошибок CORS
- ✅ Запросы идут на `http://176.99.5.211:8000`
- ✅ Категории и товары загружаются
