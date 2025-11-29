@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║         ВОССТАНОВЛЕНИЕ БАЗЫ ENB ПО ТАБЛИЦАМ                   ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

set MYSQL="C:\Program Files\MariaDB 12.1\bin\mysql.exe"
set SOURCE_DIR=C:\python\sites_mysql\enb
set TARGET_DIR=C:\Program Files\MariaDB 12.1\data\enb

echo Проверка исходной папки...
if not exist "%SOURCE_DIR%" (
    echo ❌ Папка %SOURCE_DIR% не найдена
    pause
    exit /b 1
)

echo ✅ Исходная папка найдена
echo.

set /p MYSQL_PASSWORD="Введите пароль root для MariaDB (обычно: root): "
if "%MYSQL_PASSWORD%"=="" set MYSQL_PASSWORD=root

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 1: Создание базы данных enb
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

%MYSQL% -u root -p%MYSQL_PASSWORD% -e "CREATE DATABASE IF NOT EXISTS enb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
if %errorLevel% neq 0 (
    echo ❌ Ошибка создания базы
    pause
    exit /b 1
)

echo ✅ База данных создана
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 2: Создание структуры основных таблиц
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo Создаём таблицу user...
%MYSQL% -u root -p%MYSQL_PASSWORD% enb -e "CREATE TABLE IF NOT EXISTS user (id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(255), email VARCHAR(255), phone VARCHAR(20), created_at DATETIME, updated_at DATETIME, status INT DEFAULT 10) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"

echo Создаём таблицу companies...
%MYSQL% -u root -p%MYSQL_PASSWORD% enb -e "CREATE TABLE IF NOT EXISTS companies (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), description TEXT, user_id INT, phone VARCHAR(20), email VARCHAR(255), address TEXT, logo VARCHAR(255), status INT DEFAULT 1, created_at DATETIME, updated_at DATETIME, category_id INT) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"

echo Создаём таблицу advert...
%MYSQL% -u root -p%MYSQL_PASSWORD% enb -e "CREATE TABLE IF NOT EXISTS advert (id INT PRIMARY KEY AUTO_INCREMENT, title VARCHAR(255), description TEXT, price DECIMAL(10,2), company_id INT, category_id INT, user_id INT, phone VARCHAR(20), email VARCHAR(255), address TEXT, status INT DEFAULT 1, views INT DEFAULT 0, created_at DATETIME, updated_at DATETIME, image VARCHAR(255)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"

echo Создаём таблицу categories...
%MYSQL% -u root -p%MYSQL_PASSWORD% enb -e "CREATE TABLE IF NOT EXISTS categories (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), slug VARCHAR(255), parent_id INT, icon VARCHAR(255), sort_order INT DEFAULT 0, status INT DEFAULT 1, created_at DATETIME, updated_at DATETIME) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"

echo Создаём таблицу file...
%MYSQL% -u root -p%MYSQL_PASSWORD% enb -e "CREATE TABLE IF NOT EXISTS file (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), path VARCHAR(255), url VARCHAR(255), type VARCHAR(50), size INT, model VARCHAR(50), model_id INT, created_at DATETIME) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"

echo ✅ Структура таблиц создана
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 3: Импорт данных через DISCARD/IMPORT TABLESPACE
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo ⚠️  ВНИМАНИЕ: Этот метод может не сработать из-за разных версий MySQL/MariaDB
echo.
echo Останавливаем MariaDB...
net stop MariaDB
timeout /t 3 >nul

echo.
echo Копируем файлы таблиц...

:: Копируем только основные таблицы
if exist "%SOURCE_DIR%\user.ibd" (
    echo Копируем user...
    copy /Y "%SOURCE_DIR%\user.ibd" "%TARGET_DIR%\user.ibd"
    copy /Y "%SOURCE_DIR%\user.frm" "%TARGET_DIR%\user.frm"
)

if exist "%SOURCE_DIR%\companies.ibd" (
    echo Копируем companies...
    copy /Y "%SOURCE_DIR%\companies.ibd" "%TARGET_DIR%\companies.ibd"
    copy /Y "%SOURCE_DIR%\companies.frm" "%TARGET_DIR%\companies.frm"
)

if exist "%SOURCE_DIR%\advert.ibd" (
    echo Копируем advert...
    copy /Y "%SOURCE_DIR%\advert.ibd" "%TARGET_DIR%\advert.ibd"
    copy /Y "%SOURCE_DIR%\advert.frm" "%TARGET_DIR%\advert.frm"
)

if exist "%SOURCE_DIR%\categories.ibd" (
    echo Копируем categories...
    copy /Y "%SOURCE_DIR%\categories.ibd" "%TARGET_DIR%\categories.ibd"
    copy /Y "%SOURCE_DIR%\categories.frm" "%TARGET_DIR%\categories.frm"
)

if exist "%SOURCE_DIR%\file.ibd" (
    echo Копируем file...
    copy /Y "%SOURCE_DIR%\file.ibd" "%TARGET_DIR%\file.ibd"
    copy /Y "%SOURCE_DIR%\file.frm" "%TARGET_DIR%\file.frm"
)

echo.
echo Запускаем MariaDB...
net start MariaDB
timeout /t 5 >nul

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 4: Проверка данных
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

%MYSQL% -u root -p%MYSQL_PASSWORD% -e "USE enb; SHOW TABLES;"

echo.
echo Статистика:
%MYSQL% -u root -p%MYSQL_PASSWORD% -e "USE enb; SELECT 'user' as Таблица, COUNT(*) as Записей FROM user UNION ALL SELECT 'companies', COUNT(*) FROM companies UNION ALL SELECT 'advert', COUNT(*) FROM advert UNION ALL SELECT 'categories', COUNT(*) FROM categories UNION ALL SELECT 'file', COUNT(*) FROM file;" 2>nul

if %errorLevel% neq 0 (
    echo.
    echo ⚠️  Метод копирования файлов не сработал
    echo.
    echo Попробуйте альтернативный метод:
    echo   1. Установите MySQL 5.7
    echo   2. Запустите: start_mysql57.bat
    echo   3. Создайте дамп: create_dump_from_enb.bat
    echo.
) else (
    echo.
    echo ╔════════════════════════════════════════════════════════════════╗
    echo ║              ✅ ДАННЫЕ УСПЕШНО ВОССТАНОВЛЕНЫ!                  ║
    echo ╚════════════════════════════════════════════════════════════════╝
    echo.
    echo Теперь можно запустить миграцию:
    echo   cd backend\scripts
    echo   python migrate_data.py
)

echo.
pause
