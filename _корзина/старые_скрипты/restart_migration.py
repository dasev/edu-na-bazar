"""
Перезапуск миграции - удаляет схему temp и запускает миграцию заново
"""
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar"


async def drop_temp_schema():
    """Удаляет схему temp"""
    print("🗑️ Удаляем схему temp...")
    
    engine = create_async_engine(DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA IF EXISTS temp CASCADE"))
    
    await engine.dispose()
    
    print("✅ Схема temp удалена")


async def main():
    """Главная функция"""
    print("="*60)
    print("🔄 Перезапуск миграции")
    print("="*60)
    print()
    
    # Удаляем старую схему
    await drop_temp_schema()
    
    print()
    print("="*60)
    print("🚀 Теперь запустите миграцию:")
    print("python scripts\\migrate_to_temp_schema.py")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
