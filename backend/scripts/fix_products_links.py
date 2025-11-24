"""
Исправление связей товаров с магазинами через temp.advert
"""
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar"


async def fix_links():
    """Исправляет связи товаров"""
    
    print("="*80)
    print("🔗 ИСПРАВЛЕНИЕ СВЯЗЕЙ ТОВАРОВ")
    print("="*80)
    print()
    
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Создаём маппинг товаров temp.advert → market.products
        print("🗺️ Создаём маппинг товаров...")
        
        await session.execute(text("""
            DELETE FROM temp.id_mapping WHERE old_table = 'advert'
        """))
        await session.commit()
        
        # Маппим по порядку создания (самый надёжный способ)
        await session.execute(text("""
            WITH temp_ordered AS (
                SELECT id, ROW_NUMBER() OVER (ORDER BY id) as rn
                FROM temp.advert
            ),
            market_ordered AS (
                SELECT id, ROW_NUMBER() OVER (ORDER BY id) as rn
                FROM market.products
            )
            INSERT INTO temp.id_mapping (old_table, old_id, new_id)
            SELECT 'advert', t.id, m.id
            FROM temp_ordered t
            JOIN market_ordered m ON m.rn = t.rn
        """))
        await session.commit()
        
        result = await session.execute(text("""
            SELECT COUNT(*) FROM temp.id_mapping WHERE old_table = 'advert'
        """))
        count = result.scalar()
        print(f"   ✅ Смаппено товаров: {count}")
        print()
        
        # Обновляем store_owner_id через маппинг
        print("🏪 Обновляем связи с магазинами...")
        
        result = await session.execute(text("""
            UPDATE market.products p
            SET store_owner_id = store_map.new_id
            FROM temp.id_mapping prod_map
            JOIN temp.advert ta ON ta.id = prod_map.old_id
            JOIN temp.id_mapping store_map ON store_map.old_table = 'companies' 
                AND store_map.old_id = ta.company_id
            WHERE p.id = prod_map.new_id
              AND prod_map.old_table = 'advert'
              AND ta.company_id IS NOT NULL
        """))
        await session.commit()
        
        result = await session.execute(text("""
            SELECT COUNT(*) FROM market.products WHERE store_owner_id IS NOT NULL
        """))
        count = result.scalar()
        print(f"   ✅ Товаров с магазином: {count}")
        print()
        
        # Обновляем category_id через маппинг
        print("📁 Обновляем связи с категориями...")
        
        result = await session.execute(text("""
            UPDATE market.products p
            SET category_id = cat_map.new_id
            FROM temp.id_mapping prod_map
            JOIN temp.advert ta ON ta.id = prod_map.old_id
            JOIN temp.id_mapping cat_map ON cat_map.old_table = 'categories' 
                AND cat_map.old_id = ta.category_id
            WHERE p.id = prod_map.new_id
              AND prod_map.old_table = 'advert'
              AND ta.category_id IS NOT NULL
              AND p.category_id = 6  -- Обновляем только дефолтные
        """))
        await session.commit()
        
        result = await session.execute(text("""
            SELECT COUNT(*) FROM market.products WHERE category_id != 6
        """))
        count = result.scalar()
        print(f"   ✅ Товаров с правильной категорией: {count}")
        print()
        
        # Перезагружаем изображения
        print("🖼️ Перезагружаем изображения...")
        
        await session.execute(text("DELETE FROM market.product_images"))
        await session.commit()
        
        result = await session.execute(text("""
            INSERT INTO market.product_images (product_id, image_url, old_id, sort_order, created_at)
            SELECT 
                prod_map.new_id as product_id,
                '/uploads/products/original' || tf.path as image_url,
                tf.id as old_id,
                0 as sort_order,
                TO_TIMESTAMP(tf.created_at) as created_at
            FROM temp.file tf
            JOIN temp.id_mapping prod_map ON prod_map.old_table = 'advert' 
                AND prod_map.old_id = tf.advert_id
            WHERE tf.type = 'image' 
              AND tf.advert_id IS NOT NULL
        """))
        await session.commit()
        
        result = await session.execute(text("""
            SELECT COUNT(*) FROM market.product_images
        """))
        count = result.scalar()
        print(f"   ✅ Загружено изображений: {count}")
        print()
        
        # Обновляем image_mapping
        await session.execute(text("""
            UPDATE temp.image_mapping im
            SET new_image_id = pi.id,
                new_product_id = pi.product_id
            FROM market.product_images pi
            WHERE pi.old_id = im.old_file_id
        """))
        await session.commit()
        
        # Итоговая статистика
        print("📊 ИТОГОВАЯ СТАТИСТИКА:")
        print("="*80)
        
        result = await session.execute(text("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN category_id IS NOT NULL THEN 1 END) as with_category,
                COUNT(CASE WHEN store_owner_id IS NOT NULL THEN 1 END) as with_store
            FROM market.products
        """))
        row = result.first()
        print(f"📦 Товары:")
        print(f"   Всего: {row[0]}")
        print(f"   С категорией: {row[1]} ({row[1]/row[0]*100:.1f}%)")
        print(f"   С магазином: {row[2]} ({row[2]/row[0]*100:.1f}%)")
        print()
        
        result = await session.execute(text("SELECT COUNT(*) FROM market.product_images"))
        images = result.scalar()
        print(f"🖼️ Изображений: {images}")
        
        result = await session.execute(text("SELECT COUNT(*) FROM market.store_owners"))
        stores = result.scalar()
        print(f"🏪 Магазинов: {stores}")
        
        result = await session.execute(text("SELECT COUNT(*) FROM config.users"))
        users = result.scalar()
        print(f"👥 Пользователей: {users}")
        print()
        
        # Топ категорий
        print("📊 Топ-10 категорий:")
        result = await session.execute(text("""
            SELECT c.name, COUNT(p.id) as count
            FROM market.categories c
            LEFT JOIN market.products p ON p.category_id = c.id
            GROUP BY c.id, c.name
            HAVING COUNT(p.id) > 0
            ORDER BY count DESC
            LIMIT 10
        """))
        
        for row in result:
            print(f"   {row[0]:30} → {row[1]:>5} товаров")
    
    await engine.dispose()
    
    print()
    print("="*80)
    print("✅ ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(fix_links())
