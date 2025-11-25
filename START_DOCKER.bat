@echo off
chcp 65001 > nul
echo ========================================
echo 🚀 Запуск Еду на базар (Docker)
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

echo 📦 Сборка и запуск контейнеров...
echo.

docker-compose up -d --build

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo ✅ Контейнеры успешно запущены!
    echo ========================================
    echo.
    echo 🌐 Сервисы доступны:
    echo    Frontend:  http://localhost
    echo    Backend:   http://localhost:8000
    echo    API Docs:  http://localhost:8000/docs
    echo    Postgres:  localhost:5432
    echo    Redis:     localhost:6380
    echo.
    echo 📊 Проверка статуса:
    echo    docker-compose ps
    echo.
    echo 📋 Просмотр логов:
    echo    docker-compose logs -f [service]
    echo.
    echo 🛑 Остановка:
    echo    docker-compose stop
    echo.
) else (
    echo.
    echo ❌ Ошибка при запуске контейнеров!
    echo.
    pause
    exit /b 1
)

pause
