@echo off
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║              ШАГ 1: ЗАПУСК MySQL 5.7                           ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo Останавливаем MariaDB...
net stop MariaDB 2>nul

echo.
echo Запускаем MySQL 5.7...
echo ⚠️  НЕ ЗАКРЫВАЙТЕ ЭТО ОКНО!
echo.

cd C:\mysql57\bin
.\mysqld.exe --datadir=C:\mysql57_data --console
