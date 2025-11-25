@echo off
chcp 65001 > nul
echo ========================================
echo 🛠️  Запуск Еду на базар (Development)
echo ========================================
echo.

REM Проверка наличия .env файла
if not exist .env (
    echo ⚠️  Файл .env не найден!
    echo 📝 Создайте .env файл из .env.example
    echo.
    echo Команда: copy .env.example .env
    echo.
    pause
    exit /b 1
)

echo 📦 Сборка и запуск контейнеров (Development режим)...
echo 🔥 Hot-reload включен для backend и frontend
echo.

docker-compose -f docker-compose.dev.yml up -d --build

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo ✅ Development контейнеры запущены!
    echo ========================================
    echo.
    echo 🌐 Сервисы доступны:
    echo    Frontend:  http://localhost:3000 (hot-reload)
    echo    Backend:   http://localhost:8000 (hot-reload)
    echo    API Docs:  http://localhost:8000/docs
    echo    Postgres:  localhost:5432
    echo    Redis:     localhost:6380
    echo.
    echo 🔥 Hot-reload:
    echo    - Изменения в коде автоматически применяются
    echo    - Backend: uvicorn --reload
    echo    - Frontend: npm start
    echo.
    echo 📊 Проверка статуса:
    echo    docker-compose -f docker-compose.dev.yml ps
    echo.
    echo 📋 Просмотр логов:
    echo    docker-compose -f docker-compose.dev.yml logs -f [service]
    echo.
    echo 🛑 Остановка:
    echo    docker-compose -f docker-compose.dev.yml stop
    echo.
) else (
    echo.
    echo ❌ Ошибка при запуске контейнеров!
    echo.
    pause
    exit /b 1
)

pause
