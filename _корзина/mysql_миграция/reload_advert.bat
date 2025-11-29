@echo off
chcp 65001 >nul
echo ============================================
echo 🔄 ПЕРЕЗАГРУЗКА temp.advert СО СВЯЗЯМИ
echo ============================================
echo.
echo Найдено связей:
echo   - С company_id: 8,787 (9.5%%)
echo   - С category_id: 4,877 (5.3%%)
echo.
pause

cd backend
call venv\Scripts\activate.bat

echo.
echo 🗑️ Удаляем старую таблицу...
python -c "import asyncio; from sqlalchemy import text; from sqlalchemy.ext.asyncio import create_async_engine; async def drop(): engine = create_async_engine('postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar'); async with engine.begin() as conn: await conn.execute(text('DROP TABLE IF EXISTS temp.advert CASCADE')); print('✅ Удалено'); await engine.dispose(); asyncio.run(drop())"

echo.
echo 📥 Загружаем новую таблицу со связями...
echo Это займёт несколько минут (92,456 записей)...
python scripts\migrate_to_temp_schema.py

echo.
echo ============================================
echo ✅ Готово!
echo ============================================
pause
