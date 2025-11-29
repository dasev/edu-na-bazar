@echo off
echo Copying database files...
echo This requires Administrator privileges!
echo.

:: Check for admin rights
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with Administrator privileges...
    
    echo Stopping MariaDB...
    net stop MariaDB
    
    echo Copying files...
    xcopy "C:\python\sites_mysql\enb" "C:\Program Files\MariaDB 12.1\data\enb" /E /I /Y
    
    echo Starting MariaDB...
    net start MariaDB
    
    echo Done!
    echo.
    echo Checking tables:
    mysql -u root -proot enb -e "SHOW TABLES;"
    
) else (
    echo ERROR: This script requires Administrator privileges!
    echo Please right-click and select "Run as Administrator"
)

pause
