@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║     ВОССТАНОВЛЕНИЕ ТАБЛИЦЫ COMPANIES В ЧИСТЫЙ MySQL 5.7        ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

set MYSQL57=C:\mysql57
set SOURCE_IBD=C:\python\sites_mysql\enb\companies.ibd
set SOURCE_FRM=C:\python\sites_mysql\enb\companies.frm
set NEW_DATA_DIR=C:\mysql57_data

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Шаг 1: Проверка файлов
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

if not exist "%SOURCE_IBD%" (
    echo ❌ Файл companies.ibd не найден
    pause
    exit /b 1
)

if not exist "%SOURCE_FRM%" (
    echo ❌ Файл companies.frm не найден
    pause
    exit /b 1
)

echo ✅ Файлы найдены:
echo    companies.ibd - 79.7 MB
echo    companies.frm - 2.3 KB
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Шаг 2: Создание чистой директории данных для MySQL 5.7
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

if exist "%NEW_DATA_DIR%" (
    echo Папка %NEW_DATA_DIR% уже существует
    choice /C YN /M "Удалить и создать заново?"
    if errorlevel 2 goto SKIP_INIT
    rd /s /q "%NEW_DATA_DIR%"
)

echo Инициализируем новую базу данных MySQL 5.7...
cd %MYSQL57%\bin
.\mysqld.exe --initialize-insecure --datadir=%NEW_DATA_DIR% --console

if %errorLevel% neq 0 (
    echo ❌ Ошибка инициализации
    pause
    exit /b 1
)

echo ✅ Чистая база данных создана
echo.

:SKIP_INIT
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Шаг 3: Запуск MySQL 5.7 с новой базой
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo Останавливаем MariaDB...
net stop MariaDB 2>nul
timeout /t 2 >nul

echo.
echo Запускаем MySQL 5.7...
start "MySQL 5.7" /MIN .\mysqld.exe --datadir=%NEW_DATA_DIR% --console

echo Ждём запуска (10 секунд)...
timeout /t 10 >nul

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Шаг 4: Создание базы данных enb
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

.\mysql.exe -u root --skip-ssl -e "CREATE DATABASE IF NOT EXISTS enb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

if %errorLevel% neq 0 (
    echo ❌ Не удалось создать базу
    pause
    exit /b 1
)

echo ✅ База enb создана
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Шаг 5: Создание структуры таблицы companies
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

.\mysql.exe -u root --skip-ssl enb -e "CREATE TABLE companies (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), description TEXT, user_id INT, phone VARCHAR(20), email VARCHAR(255), address TEXT, logo VARCHAR(255), status INT, created_at INT, updated_at INT, category_id INT) ENGINE=InnoDB ROW_FORMAT=COMPACT;"

echo ✅ Структура таблицы создана
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Шаг 6: Отключение tablespace
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

.\mysql.exe -u root --skip-ssl enb -e "ALTER TABLE companies DISCARD TABLESPACE;"

echo ✅ Tablespace отключен
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Шаг 7: Копирование .ibd файла
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo Останавливаем MySQL 5.7...
taskkill /F /IM mysqld.exe >nul 2>&1
timeout /t 3 >nul

echo Копируем companies.ibd...
copy /Y "%SOURCE_IBD%" "%NEW_DATA_DIR%\enb\companies.ibd"
copy /Y "%SOURCE_FRM%" "%NEW_DATA_DIR%\enb\companies.frm"

echo ✅ Файлы скопированы
echo.

echo Запускаем MySQL 5.7 снова...
start "MySQL 5.7" /MIN .\mysqld.exe --datadir=%NEW_DATA_DIR% --console
timeout /t 10 >nul

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Шаг 8: Импорт tablespace
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

.\mysql.exe -u root --skip-ssl enb -e "ALTER TABLE companies IMPORT TABLESPACE;"

if %errorLevel% neq 0 (
    echo ❌ Ошибка импорта tablespace
    echo.
    echo Возможные причины:
    echo 1. Файл .ibd повреждён
    echo 2. Несовместимость версий
    echo 3. Неправильная структура таблицы
    pause
    exit /b 1
)

echo ✅ Tablespace импортирован!
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Шаг 9: Проверка данных
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

.\mysql.exe -u root --skip-ssl enb -e "SELECT COUNT(*) as 'Всего записей' FROM companies; SELECT * FROM companies LIMIT 3;"

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║              ✅ ТАБЛИЦА COMPANIES ВОССТАНОВЛЕНА!               ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Теперь можно создать дамп:
echo.
echo   .\mysqldump.exe -u root --skip-ssl enb companies ^> companies_dump.sql
echo.
pause
