"""
Анализ категорий: текущие vs temp
"""
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar"


async def analyze():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        print("="*80)
        print("📊 ТЕКУЩИЕ КАТЕГОРИИ В ПРОЕКТЕ (market.categories)")
        print("="*80)
        
        result = await session.execute(text("""
            SELECT id, name, description, parent_id 
            FROM market.categories 
            ORDER BY id
        """))
        
        current_cats = result.fetchall()
        if current_cats:
            for row in current_cats:
                parent = f"Parent: {row[3]}" if row[3] else "Корневая"
                print(f"ID: {row[0]:3} | {row[1]:40} | {parent}")
        else:
            print("⚠️ Категорий пока нет")
        
        print(f"\n📊 Всего текущих категорий: {len(current_cats)}")
        
        print("\n" + "="*80)
        print("📊 КАТЕГОРИИ ИЗ TEMP (temp.categories)")
        print("="*80)
        
        result = await session.execute(text("""
            SELECT id, name, parent_id 
            FROM temp.categories 
            ORDER BY name
            LIMIT 50
        """))
        
        temp_cats = result.fetchall()
        print(f"\nПоказываю первые 50 из {len(temp_cats)} категорий:\n")
        
        for row in temp_cats:
            parent = f"Parent: {row[2]}" if row[2] else "Корневая"
            print(f"{row[1]:50} | {parent}")
        
        # Получаем полный список
        result = await session.execute(text("""
            SELECT name FROM temp.categories 
            WHERE parent_id IS NULL
            ORDER BY name
        """))
        
        all_temp = result.fetchall()
        print(f"\n📊 Всего категорий в temp: {len(all_temp)}")
        print(f"📊 Корневых категорий: {len([c for c in temp_cats if not c[2]])}")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(analyze())
