@echo off
echo ========================================
echo Проверка подключения к MariaDB
echo ========================================
echo.

:: Проверка наличия mysql в PATH
where mysql >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ ERROR: mysql не найден в PATH
    echo.
    echo Добавьте путь к MariaDB в переменную PATH:
    echo 1. Найдите папку с MariaDB (обычно C:\Program Files\MariaDB 12.1\bin)
    echo 2. Добавьте в PATH через Системные переменные
    echo.
    echo Или используйте полный путь:
    echo "C:\Program Files\MariaDB 12.1\bin\mysql.exe" -u root -p
    pause
    exit /b 1
)

echo ✅ mysql найден в PATH
echo.

:: Проверка подключения
echo Попытка подключения к MariaDB...
echo (Введите пароль root, обычно: root)
echo.

mysql -u root -p -e "SELECT VERSION() as MariaDB_Version, DATABASE() as Current_DB;"

if %errorLevel% neq 0 (
    echo.
    echo ❌ Не удалось подключиться к MariaDB
    echo.
    echo Возможные причины:
    echo 1. MariaDB не запущена - запустите: net start MariaDB
    echo 2. Неверный пароль
    echo 3. Пользователь root не существует
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ Подключение успешно!
echo ========================================
echo.

:: Проверка базы enb
echo Проверка наличия базы enb...
mysql -u root -p -e "SHOW DATABASES LIKE 'enb';" | findstr "enb" >nul

if %errorLevel% equ 0 (
    echo ✅ База данных enb найдена
    echo.
    echo Статистика таблиц:
    mysql -u root -p -e "USE enb; SELECT table_name as 'Таблица', table_rows as 'Строк', ROUND(data_length/1024/1024, 2) as 'Размер_MB' FROM information_schema.tables WHERE table_schema='enb' ORDER BY data_length DESC LIMIT 10;"
) else (
    echo ⚠️  База данных enb НЕ найдена
    echo.
    echo Запустите restore_old_database.bat для восстановления
)

echo.
pause
