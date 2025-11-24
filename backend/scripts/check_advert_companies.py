"""
Проверка связей в temp.advert
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
        print("🔍 ПРОВЕРКА СВЯЗЕЙ В temp.advert")
        print("="*80)
        print()
        
        result = await session.execute(text("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN company_id IS NOT NULL THEN 1 END) as with_company,
                COUNT(CASE WHEN category_id IS NOT NULL THEN 1 END) as with_category
            FROM temp.advert
        """))
        row = result.first()
        print(f"📊 Статистика temp.advert:")
        print(f"   Всего товаров: {row[0]}")
        print(f"   С company_id: {row[1]} ({row[1]/row[0]*100:.1f}%)")
        print(f"   С category_id: {row[2]} ({row[2]/row[0]*100:.1f}%)")
        print()
        
        if row[1] > 0:
            print("📸 Примеры товаров с company_id:")
            result = await session.execute(text("""
                SELECT id, title, company_id, category_id
                FROM temp.advert
                WHERE company_id IS NOT NULL
                LIMIT 10
            """))
            
            for r in result:
                print(f"   ID: {r[0]:5}, Company: {r[2]:4}, Category: {r[3]:4}, Title: {r[1][:40]}")
        
        print()
        print("🗺️ Проверка маппинга:")
        
        result = await session.execute(text("""
            SELECT COUNT(*) FROM temp.id_mapping WHERE old_table = 'companies'
        """))
        companies_mapped = result.scalar()
        print(f"   Смаппено companies: {companies_mapped}")
        
        result = await session.execute(text("""
            SELECT COUNT(*) FROM temp.id_mapping WHERE old_table = 'categories'
        """))
        categories_mapped = result.scalar()
        print(f"   Смаппено categories: {categories_mapped}")
        
        result = await session.execute(text("""
            SELECT COUNT(*) FROM temp.id_mapping WHERE old_table = 'advert'
        """))
        adverts_mapped = result.scalar()
        print(f"   Смаппено adverts: {adverts_mapped}")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(check())
