@echo off
chcp 65001 >nul
echo.
echo ========================================
echo Создание дампа базы enb
echo ========================================
echo.

set MYSQL="C:\Program Files\MariaDB 12.1\bin\mysql.exe"
set MYSQLDUMP="C:\Program Files\MariaDB 12.1\bin\mysqldump.exe"

set /p MYSQL_PASSWORD="Введите пароль root (обычно: root): "
if "%MYSQL_PASSWORD%"=="" set MYSQL_PASSWORD=root

echo.
echo Проверка наличия базы enb...
%MYSQL% -u root -p%MYSQL_PASSWORD% -e "SHOW DATABASES LIKE 'enb';" 2>nul | findstr "enb" >nul

if %errorLevel% neq 0 (
    echo ❌ База данных enb не найдена в MariaDB
    echo.
    echo Возможные варианты:
    echo 1. База находится в другом месте (MySQL 5.7 в C:\python\sites_mysql)
    echo 2. База еще не создана
    echo.
    pause
    exit /b 1
)

echo ✅ База enb найдена
echo.

echo Проверка таблиц...
%MYSQL% -u root -p%MYSQL_PASSWORD% -e "USE enb; SHOW TABLES;"

echo.
echo Создание дампа...
%MYSQLDUMP% -u root -p%MYSQL_PASSWORD% --skip-lock-tables --complete-insert enb > enb_full_dump.sql

if %errorLevel% neq 0 (
    echo ❌ Ошибка создания дампа
    pause
    exit /b 1
)

echo ✅ Дамп создан: enb_full_dump.sql
echo.

:: Проверка размера
for %%A in (enb_full_dump.sql) do echo Размер файла: %%~zA байт

echo.
pause
