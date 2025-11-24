@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║     ИМПОРТ ТАБЛИЦ ИЗ .IBD ФАЙЛОВ ПО ОДНОЙ ТАБЛИЦЕ             ║
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

echo ✅ Исходная папка найдена: %SOURCE_DIR%
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
echo ШАГ 2: Импорт таблиц по одной
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo Останавливаем MariaDB для копирования файлов...
net stop MariaDB
timeout /t 3 >nul

echo.
echo Создаём папку базы данных...
if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Копируем файлы таблиц...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

:: Копируем db.opt
if exist "%SOURCE_DIR%\db.opt" (
    echo   db.opt
    copy /Y "%SOURCE_DIR%\db.opt" "%TARGET_DIR%\db.opt" >nul
)

:: Таблица user
echo.
echo [1/5] Таблица user...
if exist "%SOURCE_DIR%\user.ibd" (
    copy /Y "%SOURCE_DIR%\user.frm" "%TARGET_DIR%\user.frm" >nul
    copy /Y "%SOURCE_DIR%\user.ibd" "%TARGET_DIR%\user.ibd" >nul
    echo   ✅ user скопирована (9.4 MB)
) else (
    echo   ⚠️  user.ibd не найден
)

:: Таблица companies
echo.
echo [2/5] Таблица companies...
if exist "%SOURCE_DIR%\companies.ibd" (
    copy /Y "%SOURCE_DIR%\companies.frm" "%TARGET_DIR%\companies.frm" >nul
    copy /Y "%SOURCE_DIR%\companies.ibd" "%TARGET_DIR%\companies.ibd" >nul
    echo   ✅ companies скопирована (79.7 MB)
) else (
    echo   ⚠️  companies.ibd не найден
)

:: Таблица advert
echo.
echo [3/5] Таблица advert...
if exist "%SOURCE_DIR%\advert.ibd" (
    copy /Y "%SOURCE_DIR%\advert.frm" "%TARGET_DIR%\advert.frm" >nul
    copy /Y "%SOURCE_DIR%\advert.ibd" "%TARGET_DIR%\advert.ibd" >nul
    echo   ✅ advert скопирована (30.4 MB)
) else (
    echo   ⚠️  advert.ibd не найден
)

:: Таблица categories
echo.
echo [4/5] Таблица categories...
if exist "%SOURCE_DIR%\categories.ibd" (
    copy /Y "%SOURCE_DIR%\categories.frm" "%TARGET_DIR%\categories.frm" >nul
    copy /Y "%SOURCE_DIR%\categories.ibd" "%TARGET_DIR%\categories.ibd" >nul
    echo   ✅ categories скопирована (98 KB)
) else (
    echo   ⚠️  categories.ibd не найден
)

:: Таблица file
echo.
echo [5/5] Таблица file...
if exist "%SOURCE_DIR%\file.ibd" (
    copy /Y "%SOURCE_DIR%\file.frm" "%TARGET_DIR%\file.frm" >nul
    copy /Y "%SOURCE_DIR%\file.ibd" "%TARGET_DIR%\file.ibd" >nul
    echo   ✅ file скопирована (11.5 MB)
) else (
    echo   ⚠️  file.ibd не найден
)

:: Дополнительные таблицы (если нужны)
echo.
echo Копируем дополнительные таблицы...

if exist "%SOURCE_DIR%\messages.ibd" (
    copy /Y "%SOURCE_DIR%\messages.frm" "%TARGET_DIR%\messages.frm" >nul
    copy /Y "%SOURCE_DIR%\messages.ibd" "%TARGET_DIR%\messages.ibd" >nul
    echo   ✅ messages
)

if exist "%SOURCE_DIR%\review.ibd" (
    copy /Y "%SOURCE_DIR%\review.frm" "%TARGET_DIR%\review.frm" >nul
    copy /Y "%SOURCE_DIR%\review.ibd" "%TARGET_DIR%\review.ibd" >nul
    echo   ✅ review
)

if exist "%SOURCE_DIR%\city.ibd" (
    copy /Y "%SOURCE_DIR%\city.frm" "%TARGET_DIR%\city.frm" >nul
    copy /Y "%SOURCE_DIR%\city.ibd" "%TARGET_DIR%\city.ibd" >nul
    echo   ✅ city
)

if exist "%SOURCE_DIR%\region.ibd" (
    copy /Y "%SOURCE_DIR%\region.frm" "%TARGET_DIR%\region.frm" >nul
    copy /Y "%SOURCE_DIR%\region.ibd" "%TARGET_DIR%\region.ibd" >nul
    echo   ✅ region
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 3: Запуск MariaDB
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo Запускаем MariaDB...
net start MariaDB
timeout /t 5 >nul

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 4: Проверка данных
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo Таблицы в базе enb:
%MYSQL% -u root -p%MYSQL_PASSWORD% -e "USE enb; SHOW TABLES;" 2>nul

echo.
echo Статистика по таблицам:
%MYSQL% -u root -p%MYSQL_PASSWORD% -e "USE enb; SELECT 'user' as Таблица, COUNT(*) as Записей FROM user UNION ALL SELECT 'companies', COUNT(*) FROM companies UNION ALL SELECT 'advert', COUNT(*) FROM advert UNION ALL SELECT 'categories', COUNT(*) FROM categories UNION ALL SELECT 'file', COUNT(*) FROM file;" 2>check_errors.log

if %errorLevel% neq 0 (
    echo.
    echo ⚠️  Не удалось получить статистику
    echo.
    echo Возможные причины:
    echo 1. Несовместимость версий MySQL/MariaDB
    echo 2. Повреждённые файлы таблиц
    echo 3. Неправильный формат .frm файлов
    echo.
    echo Ошибки сохранены в: check_errors.log
    echo.
    echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    echo РЕКОМЕНДАЦИЯ: Используйте MySQL 5.7
    echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    echo.
    echo Файлы .ibd созданы в старой версии MySQL и несовместимы
    echo с MariaDB 12.1.
    echo.
    echo Решение:
    echo 1. Скачайте MySQL 5.7.44 ZIP
    echo 2. Запустите: C:\mysql57\bin\mysqld.exe --datadir=C:\python\sites_mysql
    echo 3. Создайте дамп: mysqldump -u root enb ^> enb_real_dump.sql
    echo 4. Импортируйте в MariaDB
    echo.
    echo Подробная инструкция: ПРОСТОЕ_РЕШЕНИЕ.md
    echo.
) else (
    echo.
    echo ╔════════════════════════════════════════════════════════════════╗
    echo ║              ✅ ТАБЛИЦЫ УСПЕШНО ИМПОРТИРОВАНЫ!                 ║
    echo ╚════════════════════════════════════════════════════════════════╝
    echo.
    echo Следующий шаг - миграция в PostgreSQL:
    echo.
    echo   cd backend\scripts
    echo   python migrate_data.py
    echo.
)

pause
