"""
Миграция магазинов из temp.companies в market.stores
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from config import settings


async def migrate_stores():
    """Мигрировать магазины из temp.companies в market.stores"""
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        print("🏪 Начинаем миграцию магазинов...\n")
        
        # Проверяем сколько уже есть
        result = await session.execute(text("SELECT COUNT(*) FROM market.stores"))
        existing_count = result.scalar()
        print(f"📊 Существующих магазинов: {existing_count}")
        
        # Проверяем сколько в temp
        result = await session.execute(text("SELECT COUNT(*) FROM temp.companies"))
        temp_count = result.scalar()
        print(f"📊 Магазинов в temp.companies: {temp_count}\n")
        
        # Миграция данных
        migrate_query = text("""
            INSERT INTO market.stores (
                name,
                description,
                address,
                phone,
                email,
                working_hours,
                is_active,
                created_at,
                updated_at
            )
            SELECT 
                COALESCE(name, 'Магазин #' || id) as name,
                description,
                COALESCE(address, 'Адрес не указан') as address,
                phone,
                email,
                working_hours,
                CASE 
                    WHEN status = 'active' THEN true
                    ELSE false
                END as is_active,
                COALESCE(created_at, NOW()) as created_at,
                COALESCE(updated_at, NOW()) as updated_at
            FROM temp.companies
            WHERE id IS NOT NULL
            ON CONFLICT DO NOTHING
        """)
        
        result = await session.execute(migrate_query)
        await session.commit()
        
        migrated_count = result.rowcount
        print(f"\n✅ Мигрировано магазинов: {migrated_count}")
        
        # Проверяем результат
        result = await session.execute(text("SELECT COUNT(*) FROM market.stores"))
        final_count = result.scalar()
        print(f"📊 Всего магазинов в market.stores: {final_count}")
        
        # Показываем примеры
        print("\n📋 Примеры мигрированных магазинов:\n")
        result = await session.execute(text("""
            SELECT id, name, address, phone, is_active
            FROM market.stores
            ORDER BY id
            LIMIT 5
        """))
        stores = result.fetchall()
        
        for store in stores:
            active = "✅" if store.is_active else "❌"
            print(f"  {active} {store.name}")
            print(f"     📍 {store.address}")
            if store.phone:
                print(f"     📞 {store.phone}")
            print()
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(migrate_stores())
