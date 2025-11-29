@echo off
echo ========================================
echo ВНИМАНИЕ: MySQL 5.7 НЕ НУЖЕН!
echo ========================================
echo.
echo У вас уже установлена MariaDB 12.1, которая полностью
echo совместима со старой базой данных enb.
echo.
echo ========================================
echo ПРАВИЛЬНЫЙ СПОСОБ МИГРАЦИИ:
echo ========================================
echo.
echo 1. Проверьте MariaDB:
echo    test_mariadb_connection.bat
echo.
echo 2. Восстановите базу enb (если нужно):
echo    restore_old_database.bat
echo.
echo 3. Запустите миграцию:
echo    cd backend\scripts
echo    python migrate_data.py
echo.
echo ========================================
echo ПОДРОБНАЯ ИНСТРУКЦИЯ:
echo ========================================
echo.
echo Откройте файл: MIGRATE_NOW.txt
echo Или: MIGRATION_README.md
echo.
pause
exit /b 0

:: ========================================
:: СТАРЫЙ КОД (НЕ ИСПОЛЬЗУЕТСЯ)
:: ========================================
:: Check if MySQL 5.7 exists
if not exist "C:\mysql57\bin\mysqld.exe" (
    echo ERROR: MySQL 5.7 not found at C:\mysql57
    echo.
    echo Please install MySQL 5.7 first:
    echo 1. Download from: https://downloads.mysql.com/archives/community/
    echo 2. Extract to C:\mysql57
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)

:: Stop MariaDB if running
echo Stopping MariaDB...
net stop MariaDB 2>nul
if %errorLevel% == 0 (
    echo MariaDB stopped
) else (
    echo MariaDB not running or already stopped
)
echo.

:: Start MySQL 5.7
echo Starting MySQL 5.7...
echo Data directory: C:\python\sites_mysql
echo.
echo Press Ctrl+C to stop MySQL 5.7
echo.

cd /d C:\mysql57\bin
mysqld.exe --datadir=C:\python\sites_mysql --console

pause
