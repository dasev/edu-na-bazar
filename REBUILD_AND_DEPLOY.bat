@echo off
chcp 65001 > nul
echo ========================================
echo Пересборка и деплой Frontend
echo ========================================
echo.

cd frontend

echo [1/3] Установка зависимостей...
call npm install
if errorlevel 1 (
    echo ❌ Ошибка установки зависимостей
    pause
    exit /b 1
)

echo.
echo [2/3] Сборка production версии...
call npm run build
if errorlevel 1 (
    echo ❌ Ошибка сборки
    pause
    exit /b 1
)

echo.
echo [3/3] ✅ Сборка завершена!
echo.
echo Файлы находятся в: frontend\dist\
echo.
echo Следующий шаг:
echo 1. Загрузите содержимое frontend\dist\ на сервер
echo 2. Путь на сервере: /var/www/edu-na-bazar/
echo 3. Используйте WinSCP или команду:
echo    scp -r frontend\dist\* root@176.99.5.211:/var/www/edu-na-bazar/
echo.
pause
