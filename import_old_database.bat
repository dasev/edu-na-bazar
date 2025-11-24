@echo off
echo Creating database enb...
mysql -u root -proot -e "CREATE DATABASE IF NOT EXISTS enb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

echo.
echo Database created! Now you need to:
echo 1. Copy files from C:\python\sites_mysql\enb to MariaDB data directory
echo 2. Or use mysqldump to export/import data
echo.
echo To find MariaDB data directory, run:
mysql -u root -proot -e "SELECT @@datadir;"
echo.
pause
