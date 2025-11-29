@echo off
echo ========================================
echo Восстановление старой базы enb в MariaDB
echo ========================================
echo.

:: Проверка наличия MariaDB
where mysql >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: MariaDB/MySQL не найден в PATH
    echo Добавьте путь к MariaDB в переменную PATH
    echo Например: C:\Program Files\MariaDB 12.1\bin
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

echo [1/3] Создание базы данных enb...
mysql -u root -p -e "DROP DATABASE IF EXISTS enb; CREATE DATABASE enb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
if %errorLevel% neq 0 (
    echo ERROR: Не удалось создать базу данных
    pause
    exit /b 1
)
echo ✅ База данных создана

echo.
echo [2/3] Восстановление данных из дампа...
echo Это может занять несколько минут...
mysql -u root -p enb < enb_export.sql
if %errorLevel% neq 0 (
    echo ERROR: Не удалось восстановить данные
    pause
    exit /b 1
)
echo ✅ Данные восстановлены

echo.
echo [3/3] Проверка данных...
mysql -u root -p -e "USE enb; SELECT 'Users:' as Table_Name, COUNT(*) as Count FROM user UNION SELECT 'Companies:', COUNT(*) FROM companies UNION SELECT 'Adverts:', COUNT(*) FROM advert UNION SELECT 'Categories:', COUNT(*) FROM categories;"

echo.
echo ========================================
echo ✅ База enb успешно восстановлена!
echo ========================================
echo.
echo Теперь можно запустить миграцию:
echo   cd backend\scripts
echo   python migrate_data.py
echo.
pause
