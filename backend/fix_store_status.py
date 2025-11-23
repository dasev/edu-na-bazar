"""
Создание типа store_status напрямую в БД
"""
import asyncio
import asyncpg
from config import settings

async def fix_store_status():
    """Создать тип store_status если его нет"""
    
    # Парсим DATABASE_URL
    db_url = settings.DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://')
    
    # Подключаемся к БД
    conn = await asyncpg.connect(db_url)
    
    try:
        # Проверяем существует ли тип
        result = await conn.fetchval("""
            SELECT EXISTS (
                SELECT 1 FROM pg_type WHERE typname = 'store_status'
            )
        """)
        
        if result:
            print("✅ Тип store_status уже существует")
        else:
            print("⚠️ Тип store_status не найден, создаем...")
            
            # Создаем тип
            await conn.execute("""
                CREATE TYPE store_status AS ENUM ('pending', 'active', 'suspended', 'rejected')
            """)
            
            print("✅ Тип store_status создан!")
        
        # Проверяем существует ли таблица
        result = await conn.fetchval("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name = 'store_owners'
            )
        """)
        
        if result:
            print("✅ Таблица store_owners существует")
        else:
            print("⚠️ Таблица store_owners не найдена, создаем...")
            
            # Создаем таблицу
            await conn.execute("""
                CREATE TABLE store_owners (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    inn VARCHAR(12) NOT NULL UNIQUE,
                    kpp VARCHAR(9),
                    ogrn VARCHAR(15),
                    name VARCHAR(500) NOT NULL,
                    legal_name VARCHAR(1000) NOT NULL,
                    address TEXT NOT NULL,
                    phone VARCHAR(20),
                    email VARCHAR(255),
                    description TEXT,
                    logo VARCHAR(500),
                    banner VARCHAR(500),
                    status store_status NOT NULL DEFAULT 'pending',
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Создаем индексы
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_store_owners_owner_id ON store_owners(owner_id)
            """)
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_store_owners_inn ON store_owners(inn)
            """)
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_store_owners_status ON store_owners(status)
            """)
            
            print("✅ Таблица store_owners создана!")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(fix_store_status())
