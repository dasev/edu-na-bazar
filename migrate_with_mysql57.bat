@echo off
echo ========================================
echo Full Migration Process with MySQL 5.7
echo ========================================
echo.

:: Check MySQL 5.7
if not exist "C:\mysql57\bin\mysqld.exe" (
    echo ERROR: MySQL 5.7 not found!
    echo Please follow INSTALL_MYSQL57.md first
    pause
    exit /b 1
)

:: Stop MariaDB
echo [1/5] Stopping MariaDB...
net stop MariaDB 2>nul
timeout /t 2 >nul

:: Start MySQL 5.7 in background
echo [2/5] Starting MySQL 5.7...
start /B C:\mysql57\bin\mysqld.exe --datadir=C:\python\sites_mysql
timeout /t 5 >nul

:: Test connection
echo [3/5] Testing connection...
C:\mysql57\bin\mysql.exe -u root -e "USE enb; SELECT COUNT(*) FROM user;" >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Cannot connect to MySQL 5.7 or database 'enb' not found
    echo Please check that MySQL 5.7 is running
    pause
    exit /b 1
)
echo Connection OK!

:: Show statistics
echo [4/5] Database statistics:
C:\mysql57\bin\mysql.exe -u root -e "USE enb; SELECT 'Users:' as Table_Name, COUNT(*) as Count FROM user UNION SELECT 'Companies:', COUNT(*) FROM companies UNION SELECT 'Adverts:', COUNT(*) FROM advert UNION SELECT 'Categories:', COUNT(*) FROM categories;"

:: Run migration
echo.
echo [5/5] Running migration script...
cd /d C:\python\edu-na-bazar\backend\scripts
python migrate_data.py

:: Stop MySQL 5.7
echo.
echo Stopping MySQL 5.7...
taskkill /F /IM mysqld.exe >nul 2>&1

:: Restart MariaDB
echo Restarting MariaDB...
net start MariaDB

echo.
echo ========================================
echo Migration completed!
echo ========================================
pause
