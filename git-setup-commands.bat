@echo off
echo ========================================
echo Git Setup for Edu-na-bazar
echo ========================================
echo.

REM Настройка Git
echo Настройка имени пользователя...
git config --global user.name "dasev"

echo Настройка email...
git config --global user.email "dasev@bk.ru"

echo.
echo Проверка настроек:
git config --global --list

echo.
echo ========================================
echo Инициализация репозитория...
echo ========================================
git init

echo.
echo Добавление всех файлов...
git add .

echo.
echo Первый коммит...
git commit -m "🎉 Initial commit: Еду на базар - маркетплейс прямых продаж"

echo.
echo ========================================
echo Готово! Теперь создайте репозиторий на GitHub
echo ========================================
echo.
echo 1. Откройте: https://github.com/new
echo 2. Название: edu-na-bazar
echo 3. Описание: Маркетплейс прямых продаж от фермеров
echo 4. Public
echo 5. Create repository
echo.
echo Затем выполните:
echo git remote add origin https://github.com/ВАШ_USERNAME/edu-na-bazar.git
echo git branch -M main
echo git push -u origin main
echo.
pause
