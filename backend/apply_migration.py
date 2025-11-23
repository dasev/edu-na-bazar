"""
Применение SQL миграций
"""
import asyncio
import asyncpg
from config import settings

async def apply_migration():
    """Применить миграцию create_store_owners.sql"""
    
    # Парсим DATABASE_URL
    db_url = settings.DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://')
    
    # Читаем SQL файл
    with open('migrations/create_store_owners.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    
    # Подключаемся к БД
    conn = await asyncpg.connect(db_url)
    
    try:
        # Выполняем миграцию
        await conn.execute(sql)
        print("✅ Миграция create_store_owners.sql успешно применена!")
    except Exception as e:
        print(f"❌ Ошибка применения миграции: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(apply_migration())
