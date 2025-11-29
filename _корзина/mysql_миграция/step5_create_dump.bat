@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║         ШАГ 5: СОЗДАНИЕ ДАМПА                                 ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

cd C:\mysql57\bin

echo Создаём дамп таблицы companies...
.\mysqldump.exe -u root --protocol=TCP --skip-lock-tables --complete-insert enb companies > C:\python\edu-na-bazar\companies_dump.sql

if %errorLevel% neq 0 (
    echo ❌ Ошибка создания дампа
    pause
    exit /b 1
)

echo ✅ Дамп создан!
echo.

for %%A in (C:\python\edu-na-bazar\companies_dump.sql) do (
    set /a size_kb=%%~zA/1024
    echo Файл: companies_dump.sql
    echo Размер: !size_kb! KB
)

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║         ✅ ДАМП УСПЕШНО СОЗДАН!                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Файл: C:\python\edu-na-bazar\companies_dump.sql
echo.
echo Теперь можно:
echo 1. Остановить MySQL 5.7 (Ctrl+C)
echo 2. Импортировать дамп в MariaDB
echo 3. Запустить миграцию в PostgreSQL
echo.
pause
