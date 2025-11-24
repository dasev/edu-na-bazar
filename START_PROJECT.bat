@echo off
chcp 65001 >nul
echo.
echo ========================================
echo 🚀 Запуск проекта "Еду на базар"
echo ========================================
echo.

REM Проверка Docker
echo [1/4] Проверка Docker контейнеров...
docker-compose ps | findstr "Up" >nul
if %errorlevel% neq 0 (
    echo ⚠️  Docker контейнеры не запущены. Запускаем...
    docker-compose up -d
    timeout /t 5 >nul
) else (
    echo ✅ Docker контейнеры запущены
)
echo.

REM Backend
echo [2/4] Запуск Backend (FastAPI)...
cd backend
start "Backend - FastAPI" cmd /k "venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000"
timeout /t 3 >nul
cd ..
echo ✅ Backend запущен на http://localhost:8000
echo.

REM Frontend
echo [3/4] Запуск Frontend (React + Vite)...
cd frontend
start "Frontend - React" cmd /k "npm run dev"
timeout /t 5 >nul
cd ..
echo ✅ Frontend запущен на http://localhost:3001
echo.

REM Открыть браузер
echo [4/4] Открываем браузер...
timeout /t 2 >nul
start http://localhost:3001
echo.

echo ========================================
echo ✅ Проект успешно запущен!
echo ========================================
echo.
echo 📊 Доступные сервисы:
echo    - Frontend:  http://localhost:3001
echo    - Backend:   http://localhost:8000
echo    - API Docs:  http://localhost:8000/docs
echo    - PostgreSQL: localhost:5432
echo    - Redis:     localhost:6380
echo.
echo 📝 Для остановки закройте окна Backend и Frontend
echo.
pause
