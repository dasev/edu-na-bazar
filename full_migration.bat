@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║          ПОЛНАЯ МИГРАЦИЯ ДАННЫХ ИЗ СТАРОЙ БАЗЫ ENB            ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

:: Проверка Python
where python >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ ERROR: Python не найден
    pause
    exit /b 1
)

:: Проверка MySQL/MariaDB
where mysql >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ ERROR: mysql не найден в PATH
    echo.
    echo Добавьте путь к MariaDB в PATH:
    echo Например: C:\Program Files\MariaDB 12.1\bin
    pause
    exit /b 1
)

echo ✅ Python и MariaDB найдены
echo.

:: ========================================
:: ШАГ 1: ПРОВЕРКА MARIADB
:: ========================================
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 1/4: ПРОВЕРКА ПОДКЛЮЧЕНИЯ К MARIADB
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

mysql -u root -proot -e "SELECT VERSION();" >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ Не удалось подключиться к MariaDB
    echo.
    echo Возможные причины:
    echo 1. MariaDB не запущена - запустите: net start MariaDB
    echo 2. Неверный пароль (сейчас используется: root)
    echo.
    echo Если пароль другой, отредактируйте:
    echo   backend\scripts\migrate_data.py
    echo   Найдите: MYSQL_CONFIG
    echo   Измените: 'password': 'ВАШ_ПАРОЛЬ'
    echo.
    pause
    exit /b 1
)

echo ✅ Подключение к MariaDB успешно
echo.

:: ========================================
:: ШАГ 2: ПРОВЕРКА БАЗЫ ENB
:: ========================================
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 2/4: ПРОВЕРКА БАЗЫ ENB
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

mysql -u root -proot -e "USE enb; SELECT 1;" >nul 2>&1
if %errorLevel% neq 0 (
    echo ⚠️  База данных enb НЕ найдена
    echo.
    
    :: Проверка наличия дампа
    if not exist "enb_export.sql" (
        echo ❌ ERROR: Файл enb_export.sql не найден
        echo.
        echo Положите дамп базы в корень проекта и запустите снова
        pause
        exit /b 1
    )
    
    echo ✅ Файл enb_export.sql найден
    echo.
    echo Восстанавливаем базу данных...
    
    mysql -u root -proot -e "DROP DATABASE IF EXISTS enb; CREATE DATABASE enb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    if %errorLevel% neq 0 (
        echo ❌ Не удалось создать базу
        pause
        exit /b 1
    )
    
    echo Импортируем данные (это может занять несколько минут)...
    mysql -u root -proot enb < enb_export.sql
    if %errorLevel% neq 0 (
        echo ❌ Не удалось импортировать данные
        pause
        exit /b 1
    )
    
    echo ✅ База enb успешно восстановлена
) else (
    echo ✅ База данных enb найдена
)

echo.
echo Статистика таблиц:
mysql -u root -proot -e "USE enb; SELECT 'Users' as Таблица, COUNT(*) as Записей FROM user UNION SELECT 'Companies', COUNT(*) FROM companies UNION SELECT 'Adverts', COUNT(*) FROM advert UNION SELECT 'Categories', COUNT(*) FROM categories;"
echo.

:: ========================================
:: ШАГ 3: УСТАНОВКА ЗАВИСИМОСТЕЙ
:: ========================================
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 3/4: УСТАНОВКА ЗАВИСИМОСТЕЙ
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

cd backend

:: Проверка venv
if not exist "venv\Scripts\activate.bat" (
    echo Создаём виртуальное окружение...
    python -m venv venv
)

echo Активируем venv...
call venv\Scripts\activate.bat

echo Устанавливаем pymysql...
pip install pymysql -q
if %errorLevel% neq 0 (
    echo ❌ Не удалось установить pymysql
    pause
    exit /b 1
)

echo ✅ Зависимости установлены
echo.

:: ========================================
:: ШАГ 4: МИГРАЦИЯ ДАННЫХ
:: ========================================
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ШАГ 4/4: МИГРАЦИЯ ДАННЫХ
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

cd scripts
python migrate_data.py

if %errorLevel% neq 0 (
    echo.
    echo ❌ Миграция завершилась с ошибками
    echo.
    echo Проверьте логи выше для деталей
    pause
    exit /b 1
)

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                  ✅ МИГРАЦИЯ ЗАВЕРШЕНА!                        ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Что дальше:
echo.
echo 1. Запустите backend:
echo    cd backend
echo    uvicorn main:app --reload
echo.
echo 2. Откройте в браузере:
echo    http://localhost:8000/docs
echo.
echo 3. Проверьте данные:
echo    GET /api/products
echo    GET /api/categories
echo.
pause
