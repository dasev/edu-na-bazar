"""
Изменение колонки status на VARCHAR
"""
import asyncio
import asyncpg
from config import settings

async def fix_status_column():
    """Изменить колонку status на VARCHAR"""
    
    # Парсим DATABASE_URL
    db_url = settings.DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://')
    
    # Подключаемся к БД
    conn = await asyncpg.connect(db_url)
    
    try:
        print("🔧 Изменяем колонку status на VARCHAR...")
        
        # Изменяем тип колонки
        await conn.execute("""
            ALTER TABLE store_owners 
            ALTER COLUMN status TYPE VARCHAR(20) USING status::text
        """)
        
        print("✅ Колонка status изменена на VARCHAR(20)!")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(fix_status_column())
