"""
Проверка структуры изображений
"""
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar"


async def check():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        print("="*80)
        print("🖼️ СТРУКТУРА ИЗОБРАЖЕНИЙ")
        print("="*80)
        
        # Проверяем temp.file
        print("\n📁 temp.file:")
        result = await session.execute(text("""
            SELECT id, filename, path, type, advert_id 
            FROM temp.file 
            WHERE type = 'image'
            LIMIT 5
        """))
        
        for row in result:
            print(f"   ID: {row[0]}")
            print(f"   Filename: {row[1]}")
            print(f"   Path: {row[2]}")
            print(f"   Type: {row[3]}")
            print(f"   Advert ID: {row[4]}")
            print()
        
        # Статистика
        result = await session.execute(text("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN advert_id IS NOT NULL THEN 1 END) as with_advert,
                COUNT(CASE WHEN company_id IS NOT NULL THEN 1 END) as with_company
            FROM temp.file
            WHERE type = 'image'
        """))
        
        row = result.first()
        print(f"📊 Статистика:")
        print(f"   Всего изображений: {row[0]}")
        print(f"   С привязкой к товару: {row[1]}")
        print(f"   С привязкой к компании: {row[2]}")
        
        # Проверяем market.product_images
        print(f"\n📁 market.product_images:")
        result = await session.execute(text("""
            SELECT column_name, data_type 
            FROM information_schema.columns
            WHERE table_schema = 'market' AND table_name = 'product_images'
            ORDER BY ordinal_position
        """))
        
        for row in result:
            print(f"   {row[0]:20} {row[1]}")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(check())
