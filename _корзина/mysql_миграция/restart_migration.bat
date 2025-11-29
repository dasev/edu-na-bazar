@echo off
chcp 65001 >nul
echo ============================================
echo 🔄 Перезапуск миграции в схему temp
echo ============================================
echo.

cd backend

echo 📦 Активируем виртуальное окружение...
call venv\Scripts\activate.bat

echo.
echo 🗑️ Удаляем старую схему temp...
python -c "import asyncio; from sqlalchemy import text; from sqlalchemy.ext.asyncio import create_async_engine; async def drop(): engine = create_async_engine('postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar'); async with engine.begin() as conn: await conn.execute(text('DROP SCHEMA IF EXISTS temp CASCADE')); print('✅ Схема temp удалена'); await engine.dispose(); asyncio.run(drop())"

echo.
echo 🔄 Запускаем миграцию заново...
python scripts\migrate_to_temp_schema.py

echo.
echo ============================================
echo ✅ Готово!
echo ============================================
pause
