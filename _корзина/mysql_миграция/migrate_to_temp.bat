@echo off
chcp 65001 >nul
echo ============================================
echo 🚀 Миграция данных в схему temp
echo ============================================
echo.

cd backend

echo 📦 Активируем виртуальное окружение...
call venv\Scripts\activate.bat

echo.
echo 🔄 Запускаем миграцию...
python scripts\migrate_to_temp_schema.py

echo.
echo ============================================
echo ✅ Готово!
echo ============================================
echo.
echo 📊 Проверьте данные в PostgreSQL:
echo    SELECT schemaname, tablename FROM pg_tables WHERE schemaname = 'temp';
echo.
pause
