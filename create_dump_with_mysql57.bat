@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║         СОЗДАНИЕ ДАМПА БАЗЫ ENB ЧЕРЕЗ MySQL 5.7               ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

set MYSQL57_BIN=C:\mysql57\bin
set DATA_DIR=C:\python\sites_mysql
set DUMP_FILE=enb_real_dump.sql

:: Проверка MySQL 5.7
if not exist "%MYSQL57_BIN%\mysqld.exe" (
    echo ❌ MySQL 5.7 не найден в %MYSQL57_BIN%
    pause
    exit /b 1
)

echo ✅ MySQL 5.7 найден
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 1: Остановка MariaDB
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo Останавливаем MariaDB...
net stop MariaDB 2>nul
if %errorLevel% equ 0 (
    echo ✅ MariaDB остановлена
) else (
    echo ⚠️  MariaDB не запущена или уже остановлена
)

timeout /t 3 >nul

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 2: Запуск MySQL 5.7
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo Запускаем MySQL 5.7 с данными из %DATA_DIR%...
echo.
echo ⚠️  ВАЖНО: Оставьте это окно открытым!
echo.

start "MySQL 5.7 Server" /MIN "%MYSQL57_BIN%\mysqld.exe" --datadir=%DATA_DIR% --console

echo Ждём запуска MySQL 5.7 (10 секунд)...
timeout /t 10 >nul

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 3: Проверка подключения
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

"%MYSQL57_BIN%\mysql.exe" -u root -e "SELECT VERSION() as MySQL_Version;"

if %errorLevel% neq 0 (
    echo.
    echo ❌ Не удалось подключиться к MySQL 5.7
    echo.
    echo Останавливаем MySQL 5.7...
    taskkill /F /IM mysqld.exe >nul 2>&1
    echo.
    echo Запускаем MariaDB обратно...
    net start MariaDB
    pause
    exit /b 1
)

echo ✅ Подключение успешно!
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 4: Проверка данных
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo Таблицы в базе enb:
"%MYSQL57_BIN%\mysql.exe" -u root -e "USE enb; SHOW TABLES;"

echo.
echo Статистика:
"%MYSQL57_BIN%\mysql.exe" -u root -e "USE enb; SELECT 'user' as Таблица, COUNT(*) as Записей FROM user UNION ALL SELECT 'companies', COUNT(*) FROM companies UNION ALL SELECT 'advert', COUNT(*) FROM advert UNION ALL SELECT 'categories', COUNT(*) FROM categories UNION ALL SELECT 'file', COUNT(*) FROM file;"

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 5: Создание дампа
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo Создаём дамп базы enb...
echo Это может занять несколько минут...
echo.

"%MYSQL57_BIN%\mysqldump.exe" -u root --skip-lock-tables --complete-insert --single-transaction enb > %DUMP_FILE%

if %errorLevel% neq 0 (
    echo ❌ Ошибка создания дампа
) else (
    echo ✅ Дамп создан: %DUMP_FILE%
    echo.
    
    :: Проверка размера
    for %%A in (%DUMP_FILE%) do (
        set size=%%~zA
        set /a size_mb=%%~zA/1024/1024
    )
    
    echo Размер файла: !size_mb! MB
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 6: Остановка MySQL 5.7
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo Останавливаем MySQL 5.7...
taskkill /F /IM mysqld.exe >nul 2>&1
timeout /t 2 >nul
echo ✅ MySQL 5.7 остановлен

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 7: Запуск MariaDB
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo Запускаем MariaDB...
net start MariaDB
echo ✅ MariaDB запущена

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║              ✅ ДАМП УСПЕШНО СОЗДАН!                           ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Файл: %DUMP_FILE%
echo.
echo Следующий шаг - импорт в MariaDB:
echo.
echo   "C:\Program Files\MariaDB 12.1\bin\mysql.exe" -u root -proot -e "DROP DATABASE IF EXISTS enb; CREATE DATABASE enb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
echo   "C:\Program Files\MariaDB 12.1\bin\mysql.exe" -u root -proot enb ^< %DUMP_FILE%
echo.
echo Или запустите:
echo   .\import_dump_to_mariadb.bat
echo.
pause
