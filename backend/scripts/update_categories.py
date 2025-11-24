"""
Обновление иконок категорий и добавление новых
БЕЗ УДАЛЕНИЯ существующих данных!
"""
import asyncio
import sys
from pathlib import Path

# Добавляем путь к backend
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from config import settings


async def update_categories():
    """Обновить иконки категорий"""
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        print("🎨 Обновляем иконки категорий...\n")
        
        # Обновляем иконки для существующих категорий
        updates = [
            ("🌱", "%гротовар%", "%удобрени%"),
            ("🥫", "%отов%продукт%", None),
            ("🌾", "%ерн%", None),
            ("🌽", "%орм%", "%добав%"),
            ("🍯", "%ед%", None),
            ("🥛", "%олочн%", None),
            ("🥩", "%ясо%", "%птиц%"),
            ("🚜", "%борудован%", "%техник%"),
            ("🥬", "%вощ%", "%рукт%"),
            ("⚙️", "%слуг%", None),
        ]
        
        for icon, pattern1, pattern2 in updates:
            if pattern2:
                query = text("""
                    UPDATE market.categories 
                    SET image = :icon 
                    WHERE name ILIKE :pattern1 OR name ILIKE :pattern2
                """)
                result = await session.execute(query, {"icon": icon, "pattern1": pattern1, "pattern2": pattern2})
            else:
                query = text("""
                    UPDATE market.categories 
                    SET image = :icon 
                    WHERE name ILIKE :pattern1
                """)
                result = await session.execute(query, {"icon": icon, "pattern1": pattern1})
            
            if result.rowcount > 0:
                print(f"  ✅ Обновлено {result.rowcount} категорий с иконкой {icon}")
        
        await session.commit()
        
        print("\n📁 Добавляем новые категории...\n")
        
        # Добавляем новые категории
        new_categories = [
            ("Яйца", "🥚"),
            ("Саженцы и семена", "🌿"),
        ]
        
        for name, icon in new_categories:
            # Проверяем существование
            check_query = text("SELECT COUNT(*) FROM market.categories WHERE name = :name")
            result = await session.execute(check_query, {"name": name})
            count = result.scalar()
            
            if count == 0:
                insert_query = text("""
                    INSERT INTO market.categories (name, image, created_at, updated_at)
                    VALUES (:name, :image, NOW(), NOW())
                """)
                await session.execute(insert_query, {
                    "name": name,
                    "image": icon
                })
                print(f"  ✅ Добавлена категория: {icon} {name}")
            else:
                print(f"  ⏭️  Категория '{name}' уже существует")
        
        await session.commit()
        
        print("\n📊 Текущие категории:\n")
        
        # Показываем все категории
        query = text("""
            SELECT id, name, image 
            FROM market.categories 
            ORDER BY id
        """)
        result = await session.execute(query)
        categories = result.fetchall()
        
        for cat in categories:
            icon = cat.image if cat.image else "❓"
            print(f"  {icon} {cat.name}")
        
        print(f"\n✅ Всего категорий: {len(categories)}")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(update_categories())
