@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║     ВОССТАНОВЛЕНИЕ ТАБЛИЦЫ COMPANIES (ИСПРАВЛЕННАЯ ВЕРСИЯ)     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

set MYSQL57_BIN=C:\mysql57\bin
set SOURCE_IBD=C:\python\sites_mysql\enb\companies.ibd
set SOURCE_FRM=C:\python\sites_mysql\enb\companies.frm
set NEW_DATA_DIR=C:\mysql57_data

echo ✅ Файлы найдены
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ИНСТРУКЦИЯ ДЛЯ РУЧНОГО ВОССТАНОВЛЕНИЯ:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo Из-за конфликта клиентов MySQL/MariaDB, выполните команды вручную:
echo.
echo 1. Откройте НОВОЕ окно PowerShell от АДМИНИСТРАТОРА
echo.
echo 2. Выполните:
echo.
echo    cd C:\mysql57\bin
echo    .\mysqld.exe --datadir=C:\mysql57_data --console
echo.
echo 3. Дождитесь: "ready for connections"
echo.
echo 4. Откройте ЕЩЁ ОДНО окно PowerShell
echo.
echo 5. Выполните:
echo.
echo    cd C:\mysql57\bin
echo    .\mysql.exe -u root --protocol=TCP
echo.
echo 6. В MySQL консоли выполните:
echo.
echo    CREATE DATABASE enb;
echo    USE enb;
echo    CREATE TABLE companies (
echo        id INT PRIMARY KEY AUTO_INCREMENT,
echo        name VARCHAR(255),
echo        description TEXT,
echo        user_id INT,
echo        phone VARCHAR(20),
echo        email VARCHAR(255),
echo        address TEXT,
echo        logo VARCHAR(255),
echo        status INT,
echo        created_at INT,
echo        updated_at INT,
echo        category_id INT
echo    ) ENGINE=InnoDB ROW_FORMAT=COMPACT;
echo.
echo    ALTER TABLE companies DISCARD TABLESPACE;
echo    exit
echo.
echo 7. Остановите MySQL (Ctrl+C в первом окне)
echo.
echo 8. Скопируйте файл:
echo.
echo    copy C:\python\sites_mysql\enb\companies.ibd C:\mysql57_data\enb\companies.ibd
echo    copy C:\python\sites_mysql\enb\companies.frm C:\mysql57_data\enb\companies.frm
echo.
echo 9. Запустите MySQL снова (шаг 2)
echo.
echo 10. В MySQL консоли:
echo.
echo    USE enb;
echo    ALTER TABLE companies IMPORT TABLESPACE;
echo    SELECT COUNT(*) FROM companies;
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║              ГОТОВО! Данные восстановлены!                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
pause
