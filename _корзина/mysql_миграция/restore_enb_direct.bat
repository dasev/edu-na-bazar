@echo off
chcp 65001 >nul
echo.
echo ========================================
echo Восстановление базы enb в MariaDB
echo ========================================
echo.

set MYSQL_PATH="C:\Program Files\MariaDB 12.1\bin\mysql.exe"
set MYSQLDUMP_PATH="C:\Program Files\MariaDB 12.1\bin\mysqldump.exe"

:: Проверка наличия mysql
if not exist %MYSQL_PATH% (
    echo ERROR: MySQL не найден по пути:
    echo %MYSQL_PATH%
    echo.
    echo Проверьте установку MariaDB
    pause
    exit /b 1
)

:: Проверка наличия дампа
if not exist "enb_export.sql" (
    echo ERROR: Файл enb_export.sql не найден
    echo Положите дамп базы в папку проекта
    pause
    exit /b 1
)

echo ✅ MySQL найден: %MYSQL_PATH%
echo ✅ Дамп найден: enb_export.sql
echo.

:: Запрос пароля
set /p MYSQL_PASSWORD="Введите пароль root для MariaDB (обычно: root): "
if "%MYSQL_PASSWORD%"=="" set MYSQL_PASSWORD=root

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 1/3: Создание базы данных enb
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

%MYSQL_PATH% -u root -p%MYSQL_PASSWORD% -e "DROP DATABASE IF EXISTS enb; CREATE DATABASE enb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

if %errorLevel% neq 0 (
    echo.
    echo ❌ Ошибка создания базы данных
    echo.
    echo Возможные причины:
    echo 1. MariaDB не запущена - запустите: net start MariaDB
    echo 2. Неверный пароль
    echo.
    pause
    exit /b 1
)

echo ✅ База данных enb создана
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 2/3: Импорт данных из дампа
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo Это может занять несколько минут...
echo.

%MYSQL_PATH% -u root -p%MYSQL_PASSWORD% enb < enb_export.sql

if %errorLevel% neq 0 (
    echo.
    echo ❌ Ошибка импорта данных
    pause
    exit /b 1
)

echo ✅ Данные импортированы
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 3/3: Проверка данных
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

%MYSQL_PATH% -u root -p%MYSQL_PASSWORD% -e "USE enb; SELECT 'Users' as Таблица, COUNT(*) as Записей FROM user UNION SELECT 'Companies', COUNT(*) FROM companies UNION SELECT 'Adverts', COUNT(*) FROM advert UNION SELECT 'Categories', COUNT(*) FROM categories UNION SELECT 'Files', COUNT(*) FROM file;"

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║              ✅ БАЗА ENB УСПЕШНО ВОССТАНОВЛЕНА!                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Теперь можно запустить миграцию в PostgreSQL:
echo.
echo   cd backend\scripts
echo   python migrate_data.py
echo.
pause
