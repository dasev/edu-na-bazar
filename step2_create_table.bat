@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║         ШАГ 2: СОЗДАНИЕ БАЗЫ И ТАБЛИЦЫ                        ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

cd C:\mysql57\bin

echo Создаём базу данных enb...
.\mysql.exe -u root --protocol=TCP -e "CREATE DATABASE IF NOT EXISTS enb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

if %errorLevel% neq 0 (
    echo ❌ Ошибка создания базы
    echo Убедитесь что MySQL 5.7 запущен (step1_start_mysql57.bat)
    pause
    exit /b 1
)

echo ✅ База создана
echo.

echo Создаём таблицу companies...
.\mysql.exe -u root --protocol=TCP enb < C:\python\edu-na-bazar\create_companies_table.sql

if %errorLevel% neq 0 (
    echo ❌ Ошибка создания таблицы
    pause
    exit /b 1
)

echo ✅ Таблица создана
echo.

echo Отключаем tablespace...
.\mysql.exe -u root --protocol=TCP enb -e "ALTER TABLE companies DISCARD TABLESPACE;"

echo ✅ Tablespace отключён
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║         ГОТОВО! Переходите к шагу 3                           ║
echo ╚════════════════════════════════════════════════════════════════╝
pause
