@echo off
echo Starting MySQL server...
cd /d C:\mysql\bin
start mysqld.exe --datadir=C:\python\sites_mysql --console
echo MySQL server started!
pause
