@echo off
chcp 65001 >nul
echo.
echo ========================================
echo Восстановление базы enb в MariaDB
echo ========================================
echo.

set MYSQL_PATH="C:\Program Files\MariaDB 12.1\bin\mysql.exe"

:: Проверка наличия mysql
if not exist %MYSQL_PATH% (
    echo ERROR: MySQL не найден
    pause
    exit /b 1
)

:: Проверка наличия дампа
if not exist "enb_export.sql" (
    echo ERROR: Файл enb_export.sql не найден
    pause
    exit /b 1
)

echo ✅ MySQL найден
echo ✅ Дамп найден
echo.

:: Запрос пароля
set /p MYSQL_PASSWORD="Введите пароль root для MariaDB (обычно: root): "
if "%MYSQL_PASSWORD%"=="" set MYSQL_PASSWORD=root

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 1/3: Проверка базы данных
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

%MYSQL_PATH% -u root -p%MYSQL_PASSWORD% -e "SHOW DATABASES LIKE 'enb';" 2>nul | findstr "enb" >nul

if %errorLevel% equ 0 (
    echo ⚠️  База enb уже существует
    echo.
    choice /C YN /M "Удалить существующую базу и создать заново? (Y/N)"
    if errorlevel 2 goto SKIP_CREATE
    if errorlevel 1 goto DROP_DB
) else (
    goto CREATE_DB
)

:DROP_DB
echo.
echo Удаление существующей базы...
%MYSQL_PATH% -u root -p%MYSQL_PASSWORD% -e "DROP DATABASE IF EXISTS enb;"
if %errorLevel% neq 0 (
    echo ⚠️  Не удалось удалить базу стандартным способом
    echo Пробуем альтернативный метод...
    
    :: Останавливаем MariaDB
    echo Останавливаем MariaDB...
    net stop MariaDB 2>nul
    timeout /t 3 >nul
    
    :: Удаляем папку базы данных
    if exist "C:\Program Files\MariaDB 12.1\data\enb" (
        echo Удаляем папку базы данных...
        rd /s /q "C:\Program Files\MariaDB 12.1\data\enb"
    )
    
    :: Запускаем MariaDB
    echo Запускаем MariaDB...
    net start MariaDB
    timeout /t 5 >nul
)

:CREATE_DB
echo.
echo Создание базы данных enb...
%MYSQL_PATH% -u root -p%MYSQL_PASSWORD% -e "CREATE DATABASE IF NOT EXISTS enb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

if %errorLevel% neq 0 (
    echo ❌ Ошибка создания базы
    pause
    exit /b 1
)

echo ✅ База данных готова
echo.

:SKIP_CREATE
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 2/3: Импорт данных
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo Импортируем данные (это может занять несколько минут)...
echo.

%MYSQL_PATH% -u root -p%MYSQL_PASSWORD% enb < enb_export.sql 2>import_errors.log

if %errorLevel% neq 0 (
    echo ⚠️  Импорт завершился с предупреждениями
    echo Проверьте файл import_errors.log для деталей
    echo.
    echo Продолжаем проверку данных...
) else (
    echo ✅ Данные импортированы
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 3/3: Проверка данных
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

%MYSQL_PATH% -u root -p%MYSQL_PASSWORD% -e "USE enb; SELECT 'Users' as Таблица, COUNT(*) as Записей FROM user UNION SELECT 'Companies', COUNT(*) FROM companies UNION SELECT 'Adverts', COUNT(*) FROM advert UNION SELECT 'Categories', COUNT(*) FROM categories UNION SELECT 'Files', COUNT(*) FROM file;" 2>nul

if %errorLevel% neq 0 (
    echo ⚠️  Не удалось получить статистику
    echo Возможно, таблицы еще не созданы
    echo.
    echo Проверьте вручную:
    echo   mysql -u root -p
    echo   USE enb;
    echo   SHOW TABLES;
) else (
    echo.
    echo ╔════════════════════════════════════════════════════════════════╗
    echo ║              ✅ БАЗА ENB УСПЕШНО ВОССТАНОВЛЕНА!                ║
    echo ╚════════════════════════════════════════════════════════════════╝
)

echo.
echo Следующий шаг - миграция в PostgreSQL:
echo.
echo   cd backend\scripts
echo   python migrate_data.py
echo.
pause
