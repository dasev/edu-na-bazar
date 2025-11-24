@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║         ИМПОРТ ВСЕХ ДАННЫХ В MySQL 5.7                        ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

set MYSQL=C:\mysql57\bin\mysql.exe

echo Проверка подключения к MySQL...
%MYSQL% -u root --protocol=TCP -e "SELECT VERSION();" >nul 2>&1

if %errorLevel% neq 0 (
    echo ❌ MySQL не запущен!
    echo.
    echo Запустите MySQL 5.7:
    echo   C:\mysql57\bin\mysqld.exe --datadir=C:\mysql57_data_new
    pause
    exit /b 1
)

echo ✅ MySQL доступен
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Импорт категорий (333 записи)...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

%MYSQL% -u root --protocol=TCP < categories_inserts.sql

if %errorLevel% neq 0 (
    echo ❌ Ошибка импорта категорий
) else (
    echo ✅ Категории импортированы
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Импорт подкатегорий (501 запись)...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

%MYSQL% -u root --protocol=TCP < sub_categories_inserts.sql

if %errorLevel% neq 0 (
    echo ❌ Ошибка импорта подкатегорий
) else (
    echo ✅ Подкатегории импортированы
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Импорт компаний (689 записей)...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

%MYSQL% -u root --protocol=TCP < companies_inserts.sql

if %errorLevel% neq 0 (
    echo ❌ Ошибка импорта компаний
) else (
    echo ✅ Компании импортированы
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Импорт пользователей (2582 записи)...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

%MYSQL% -u root --protocol=TCP < user_inserts.sql

if %errorLevel% neq 0 (
    echo ❌ Ошибка импорта пользователей
) else (
    echo ✅ Пользователи импортированы
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Импорт объявлений/товаров (15799 записей)...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

%MYSQL% -u root --protocol=TCP < advert_inserts.sql

if %errorLevel% neq 0 (
    echo ❌ Ошибка импорта объявлений
) else (
    echo ✅ Объявления импортированы
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Импорт отзывов (19 записей)...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

%MYSQL% -u root --protocol=TCP < review_inserts.sql

if %errorLevel% neq 0 (
    echo ❌ Ошибка импорта отзывов
) else (
    echo ✅ Отзывы импортированы
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Импорт файлов/фото (9765 записей)...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

%MYSQL% -u root --protocol=TCP < file_inserts.sql

if %errorLevel% neq 0 (
    echo ❌ Ошибка импорта файлов
) else (
    echo ✅ Файлы импортированы
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Проверка данных...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

%MYSQL% -u root --protocol=TCP -e "USE enb; SELECT 'categories' as Таблица, COUNT(*) as Записей FROM categories UNION ALL SELECT 'sub_categories', COUNT(*) FROM sub_categories UNION ALL SELECT 'companies', COUNT(*) FROM companies UNION ALL SELECT 'user', COUNT(*) FROM user UNION ALL SELECT 'advert', COUNT(*) FROM advert UNION ALL SELECT 'review', COUNT(*) FROM review UNION ALL SELECT 'file', COUNT(*) FROM file;"

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║              ✅ ИМПОРТ ЗАВЕРШЁН!                               ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Следующий шаг - миграция в PostgreSQL:
echo   cd backend\scripts
echo   python migrate_data.py
echo.
pause
