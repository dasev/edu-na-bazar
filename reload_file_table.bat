@echo off
chcp 65001 >nul
echo ============================================
echo 🔄 ПЕРЕЗАГРУЗКА ТАБЛИЦЫ file С СВЯЗЯМИ
echo ============================================
echo.
echo Найдено связей:
echo   - С advert_id: 4,095 (42%%)
echo   - С company_id: 3,999 (41%%)
echo.
pause
echo.

cd backend

echo 📦 Активируем виртуальное окружение...
call venv\Scripts\activate.bat

echo.
echo 🗑️ Удаляем старую таблицу temp.file...
python -c "import asyncio; from sqlalchemy import text; from sqlalchemy.ext.asyncio import create_async_engine; async def drop(): engine = create_async_engine('postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar'); async with engine.begin() as conn: await conn.execute(text('DROP TABLE IF EXISTS temp.file CASCADE')); print('✅ Таблица temp.file удалена'); await engine.dispose(); asyncio.run(drop())"

echo.
echo 📥 Загружаем новую таблицу с связями...
python ..\migrate_to_temp_schema.py

echo.
echo ============================================
echo ✅ Готово!
echo ============================================
echo.
echo 📊 Проверьте связи:
echo    SELECT COUNT(*) as total,
echo           COUNT(CASE WHEN advert_id IS NOT NULL THEN 1 END) as with_advert
echo    FROM temp.file;
echo.
pause
