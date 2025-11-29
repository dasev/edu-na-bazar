@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║         СОЗДАНИЕ ДАМПА БАЗЫ ENB (УПРОЩЁННЫЙ СПОСОБ)           ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

set MYSQL57=C:\mysql57\bin
set DUMP_FILE=enb_real_dump.sql

echo Проверка MySQL 5.7...
if not exist "%MYSQL57%\mysqld.exe" (
    echo ❌ MySQL 5.7 не найден
    pause
    exit /b 1
)
echo ✅ MySQL 5.7 найден
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ИНСТРУКЦИЯ:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 1. Откройте НОВОЕ окно PowerShell от АДМИНИСТРАТОРА
echo.
echo 2. Выполните команды:
echo.
echo    cd C:\mysql57\bin
echo    .\mysqld.exe --datadir=C:\python\sites_mysql --console
echo.
echo 3. Дождитесь сообщения: "ready for connections"
echo.
echo 4. Вернитесь в ЭТО окно и нажмите любую клавишу
echo.
pause

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Проверка подключения к MySQL 5.7...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

"%MYSQL57%\mysql.exe" -u root --skip-ssl --default-auth=mysql_native_password -e "SELECT VERSION();"

if %errorLevel% neq 0 (
    echo.
    echo ❌ Не удалось подключиться
    echo.
    echo Убедитесь что MySQL 5.7 запущен!
    pause
    exit /b 1
)

echo ✅ Подключение успешно!
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Проверка данных...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

"%MYSQL57%\mysql.exe" -u root --skip-ssl --default-auth=mysql_native_password -e "USE enb; SHOW TABLES;"

echo.
echo Статистика:
"%MYSQL57%\mysql.exe" -u root --skip-ssl --default-auth=mysql_native_password -e "USE enb; SELECT 'user' as Таблица, COUNT(*) as Записей FROM user UNION ALL SELECT 'companies', COUNT(*) FROM companies UNION ALL SELECT 'advert', COUNT(*) FROM advert UNION ALL SELECT 'categories', COUNT(*) FROM categories UNION ALL SELECT 'file', COUNT(*) FROM file;"

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Создание дампа...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo Создаём дамп базы enb (это может занять несколько минут)...

"%MYSQL57%\mysqldump.exe" -u root --skip-ssl --default-auth=mysql_native_password --skip-lock-tables --complete-insert --single-transaction enb > %DUMP_FILE%

if %errorLevel% neq 0 (
    echo ❌ Ошибка создания дампа
    pause
    exit /b 1
)

echo ✅ Дамп создан!
echo.

:: Проверка размера
for %%A in (%DUMP_FILE%) do (
    set /a size_mb=%%~zA/1024/1024
    echo Файл: %DUMP_FILE%
    echo Размер: !size_mb! MB
)

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║              ✅ ДАМП УСПЕШНО СОЗДАН!                           ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo СЛЕДУЮЩИЕ ШАГИ:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 1. Остановите MySQL 5.7 (в другом окне нажмите Ctrl+C)
echo.
echo 2. Импортируйте дамп в MariaDB:
echo    .\import_dump_to_mariadb.bat
echo.
echo 3. Запустите миграцию в PostgreSQL:
echo    cd backend\scripts
echo    python migrate_data.py
echo.
pause
