@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║              ПРОВЕРКА MySQL 5.7 И ДАННЫХ                       ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

set MYSQL57=C:\mysql57\bin\mysql.exe

if not exist "%MYSQL57%" (
    echo ❌ MySQL 5.7 не найден по пути: %MYSQL57%
    pause
    exit /b 1
)

echo ✅ MySQL 5.7 найден
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Проверка подключения...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

%MYSQL57% -u root -e "SELECT VERSION() as MySQL_Version, NOW() as Current_Time;"

if %errorLevel% neq 0 (
    echo.
    echo ❌ Не удалось подключиться к MySQL 5.7
    echo.
    echo Проверьте что MySQL 5.7 запущен:
    echo   C:\mysql57\bin\mysqld.exe --datadir=C:\python\sites_mysql --console
    pause
    exit /b 1
)

echo.
echo ✅ Подключение успешно!
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Проверка базы данных enb...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

%MYSQL57% -u root -e "SHOW DATABASES LIKE 'enb';"

echo.
echo Таблицы в базе enb:
%MYSQL57% -u root -e "USE enb; SHOW TABLES;"

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Статистика данных:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

%MYSQL57% -u root -e "USE enb; SELECT 'user' as Таблица, COUNT(*) as Записей FROM user UNION ALL SELECT 'companies', COUNT(*) FROM companies UNION ALL SELECT 'advert', COUNT(*) FROM advert UNION ALL SELECT 'categories', COUNT(*) FROM categories UNION ALL SELECT 'file', COUNT(*) FROM file UNION ALL SELECT 'messages', COUNT(*) FROM messages UNION ALL SELECT 'review', COUNT(*) FROM review;"

if %errorLevel% neq 0 (
    echo.
    echo ⚠️  Не удалось получить статистику
) else (
    echo.
    echo ╔════════════════════════════════════════════════════════════════╗
    echo ║              ✅ ДАННЫЕ УСПЕШНО ПРОЧИТАНЫ!                      ║
    echo ╚════════════════════════════════════════════════════════════════╝
    echo.
    echo Следующий шаг - создать дамп:
    echo.
    echo   C:\mysql57\bin\mysqldump.exe -u root --skip-lock-tables --complete-insert --single-transaction enb ^> enb_real_dump.sql
    echo.
)

pause
