@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║              ЗАПУСК ТОЛЬКО MySQL 5.7                           ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Шаг 1: Остановка MariaDB
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

net stop MariaDB 2>nul
if %errorLevel% equ 0 (
    echo ✅ MariaDB остановлена
) else (
    echo ⚠️  MariaDB не запущена
)

timeout /t 3 >nul

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Шаг 2: Запуск MySQL 5.7
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

if not exist "C:\mysql57\bin\mysqld.exe" (
    echo ❌ MySQL 5.7 не найден в C:\mysql57\bin
    pause
    exit /b 1
)

echo Запускаем MySQL 5.7 с данными из C:\python\sites_mysql...
echo.
echo ⚠️  ВАЖНО: Не закрывайте это окно!
echo.
echo Ждите сообщение: "ready for connections"
echo.

cd C:\mysql57\bin
.\mysqld.exe --datadir=C:\python\sites_mysql --console
