"""
Проверка структуры таблицы store_owners
"""
import asyncio
import asyncpg
from config import settings

async def check_db():
    """Проверить структуру таблицы"""
    
    # Парсим DATABASE_URL
    db_url = settings.DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://')
    
    # Подключаемся к БД
    conn = await asyncpg.connect(db_url)
    
    try:
        # Проверяем структуру таблицы
        columns = await conn.fetch("""
            SELECT column_name, data_type, udt_name
            FROM information_schema.columns
            WHERE table_name = 'store_owners'
            ORDER BY ordinal_position
        """)
        
        print("📊 Структура таблицы store_owners:\n")
        for col in columns:
            print(f"  {col['column_name']:20} {col['data_type']:20} ({col['udt_name']})")
        
        # Проверяем существование типа store_status
        type_exists = await conn.fetchval("""
            SELECT EXISTS (
                SELECT 1 FROM pg_type WHERE typname = 'store_status'
            )
        """)
        
        print(f"\n🔍 Тип store_status существует: {type_exists}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(check_db())
