# Пересборка Frontend для Production

## Проблема
Frontend обращался к `localhost:8000` вместо `176.99.5.211:8000` в production.

## Что исправлено
1. ✅ Создан `.env.production` с правильным API URL
2. ✅ Заменены все hardcoded `localhost:8000` на переменную окружения
3. ✅ Исправлены файлы:
   - `src/pages/Map/MapPage.tsx`
   - `src/components/FilterPanel/FilterPanel.tsx`
   - `src/components/ImageUpload/ImageUpload.tsx`
   - `src/components/Auth/AuthModal.tsx`

## Команды для пересборки

### 1. Пересобрать frontend
```bash
cd c:\python\edu-na-bazar\frontend
npm run build
```

### 2. Загрузить на сервер
```bash
# Из корня проекта
scp -r frontend/dist/* root@176.99.5.211:/var/www/edu-na-bazar/
```

### 3. Или использовать WinSCP/FileZilla
- Подключиться к `176.99.5.211` (root / sIAS6APDsKh0bL)
- Загрузить содержимое `frontend/dist/` в `/var/www/edu-na-bazar/`

## Проверка
После загрузки откройте `http://176.99.5.211` и проверьте:
- ✅ Нет ошибок CORS в консоли
- ✅ API запросы идут на `http://176.99.5.211:8000`
- ✅ Категории и товары загружаются

## Дополнительно: Backend ошибки 500

Если после исправления frontend всё ещё есть ошибки 500 от API:
1. Подключиться к серверу: `ssh root@176.99.5.211`
2. Проверить логи: `docker logs edu-na-bazar-backend-1`
3. Проверить БД: `docker exec -it edu-na-bazar-db-1 psql -U postgres -d edu_na_bazar`
