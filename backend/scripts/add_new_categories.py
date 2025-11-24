"""
Добавление 4 новых категорий в проект
"""
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar"


async def add_categories():
    """Добавляет 4 новые категории"""
    
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        print("="*80)
        print("➕ ДОБАВЛЕНИЕ 4 НОВЫХ КАТЕГОРИЙ")
        print("="*80)
        
        # Проверяем текущие категории
        result = await session.execute(text("""
            SELECT id, name FROM market.categories ORDER BY id
        """))
        current = result.fetchall()
        print(f"\n📊 Текущие категории ({len(current)}):")
        for row in current:
            print(f"   {row[0]:3} | {row[1]}")
        
        # Добавляем новые категории
        new_categories = [
            ("Корма и добавки", "Комбикорма, кормовые добавки, барда, биоудобрения"),
            ("Агротовары и удобрения", "Биопрепараты, грунты, микроудобрения, дезинфицирующие средства"),
            ("Оборудование и техника", "Спецтехника, производственное оборудование, мини-техника"),
            ("Услуги", "Агротуризм, грузоперевозки, авиахимработы, консультации")
        ]
        
        print(f"\n➕ Добавляем новые категории:")
        
        for name, description in new_categories:
            # Проверяем, не существует ли уже
            result = await session.execute(text("""
                SELECT id FROM market.categories WHERE name = :name
            """), {"name": name})
            
            if result.first():
                print(f"   ⚠️  {name} - уже существует")
            else:
                await session.execute(text("""
                    INSERT INTO market.categories (name, description, parent_id, created_at, updated_at)
                    VALUES (:name, :description, NULL, NOW(), NOW())
                """), {"name": name, "description": description})
                print(f"   ✅ {name}")
        
        await session.commit()
        
        # Показываем итоговый список
        result = await session.execute(text("""
            SELECT id, name FROM market.categories ORDER BY id
        """))
        final = result.fetchall()
        
        print(f"\n📊 Итоговые категории ({len(final)}):")
        for row in final:
            print(f"   {row[0]:3} | {row[1]}")
        
        print("\n" + "="*80)
        print("✅ КАТЕГОРИИ ДОБАВЛЕНЫ!")
        print("="*80)
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(add_categories())
