@echo off
chcp 65001 >nul
echo.
echo Проверка таблицы companies...
echo.

set MYSQL="C:\Program Files\MariaDB 12.1\bin\mysql.exe"

%MYSQL% -u root -proot -e "USE enb; SELECT COUNT(*) as 'Всего записей' FROM companies; SELECT * FROM companies LIMIT 3;"

if %errorLevel% neq 0 (
    echo.
    echo ❌ Ошибка чтения данных из таблицы companies
    echo.
    echo Причина: Файлы .ibd из MySQL 5.7 несовместимы с MariaDB 12.1
    echo.
    echo Решение: Используйте MySQL 5.7 для создания дампа
    echo См. файл: ФИНАЛЬНОЕ_РЕШЕНИЕ.md
) else (
    echo.
    echo ✅ Данные успешно прочитаны!
)

echo.
pause
