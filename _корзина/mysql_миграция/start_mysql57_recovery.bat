@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║         ЗАПУСК MySQL 5.7 В РЕЖИМЕ ВОССТАНОВЛЕНИЯ               ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo Останавливаем MariaDB...
net stop MariaDB 2>nul
timeout /t 2 >nul

echo.
echo Запускаем MySQL 5.7 с параметрами восстановления...
echo.
echo ⚠️  Не закрывайте это окно!
echo.

cd C:\mysql57\bin
.\mysqld.exe --datadir=C:\python\sites_mysql --innodb-force-recovery=1 --console

pause
