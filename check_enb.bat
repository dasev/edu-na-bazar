@echo off
chcp 65001 >nul
echo.
echo ========================================
echo Проверка базы данных enb
echo ========================================
echo.

set MYSQL="C:\Program Files\MariaDB 12.1\bin\mysql.exe"

set /p MYSQL_PASSWORD="Введите пароль root (обычно: root): "
if "%MYSQL_PASSWORD%"=="" set MYSQL_PASSWORD=root

echo.
echo Таблицы в базе enb:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
%MYSQL% -u root -p%MYSQL_PASSWORD% -e "USE enb; SHOW TABLES;"

echo.
echo Статистика по таблицам:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
%MYSQL% -u root -p%MYSQL_PASSWORD% -e "USE enb; SELECT 'user' as Таблица, COUNT(*) as Записей FROM user UNION ALL SELECT 'companies', COUNT(*) FROM companies UNION ALL SELECT 'advert', COUNT(*) FROM advert UNION ALL SELECT 'categories', COUNT(*) FROM categories UNION ALL SELECT 'file', COUNT(*) FROM file;"

echo.
pause
