@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║         ШАГ 4: ИМПОРТ ДАННЫХ                                  ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

cd C:\mysql57\bin

echo Импортируем tablespace...
.\mysql.exe -u root --protocol=TCP enb -e "ALTER TABLE companies IMPORT TABLESPACE;"

if %errorLevel% neq 0 (
    echo ❌ Ошибка импорта
    pause
    exit /b 1
)

echo ✅ Tablespace импортирован!
echo.

echo Проверяем данные...
.\mysql.exe -u root --protocol=TCP enb -e "SELECT COUNT(*) as 'Всего записей' FROM companies;"

echo.
.\mysql.exe -u root --protocol=TCP enb -e "SELECT id, name, phone, email FROM companies LIMIT 5;"

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║         ✅ ДАННЫЕ УСПЕШНО ВОССТАНОВЛЕНЫ!                       ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Теперь можно создать дамп:
echo   step5_create_dump.bat
echo.
pause
