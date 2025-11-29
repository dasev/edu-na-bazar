@echo off
chcp 65001 >nul
echo ============================================
echo 🔄 ПЕРЕЗАГРУЗКА temp.file СО СВЯЗЯМИ
echo ============================================
echo.

cd backend
call venv\Scripts\activate.bat

echo 🗑️ Удаляем старую таблицу...
python -c "import asyncio; from sqlalchemy import text; from sqlalchemy.ext.asyncio import create_async_engine; async def drop(): engine = create_async_engine('postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar'); async with engine.begin() as conn: await conn.execute(text('DROP TABLE IF EXISTS temp.file CASCADE')); print('✅ Удалено'); await engine.dispose(); asyncio.run(drop())"

echo.
echo 📥 Загружаем новую таблицу...
python scripts\migrate_to_temp_schema.py

echo.
echo ============================================
echo ✅ Готово!
echo ============================================
pause
