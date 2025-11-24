@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║         ШАГ 3: КОПИРОВАНИЕ ФАЙЛОВ                             ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo ⚠️  ВАЖНО: Остановите MySQL 5.7!
echo    Перейдите в окно где запущен MySQL 5.7
echo    Нажмите Ctrl+C
echo.
pause

echo.
echo Копируем файлы...

if not exist "C:\mysql57_data\enb" mkdir "C:\mysql57_data\enb"

copy /Y "C:\python\sites_mysql\enb\companies.ibd" "C:\mysql57_data\enb\companies.ibd"
copy /Y "C:\python\sites_mysql\enb\companies.frm" "C:\mysql57_data\enb\companies.frm"

echo ✅ Файлы скопированы
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║    ГОТОВО! Запустите MySQL 5.7 снова (step1_start_mysql57.bat)║
echo ║    Затем переходите к шагу 4                                  ║
echo ╚════════════════════════════════════════════════════════════════╝
pause
