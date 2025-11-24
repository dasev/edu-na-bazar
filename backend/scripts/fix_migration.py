"""
Исправление проблем после миграции
"""
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar"


async def fix_migration():
    """Исправляет проблемы после миграции"""
    
    print("="*80)
    print("🔧 ИСПРАВЛЕНИЕ ПРОБЛЕМ МИГРАЦИИ")
    print("="*80)
    print()
    
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Проверяем текущее состояние
        print("📊 Текущее состояние:")
        
        result = await session.execute(text("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN category_id IS NULL THEN 1 END) as without_category,
                COUNT(CASE WHEN store_owner_id IS NULL THEN 1 END) as without_store
            FROM market.products
        """))
        row = result.first()
        print(f"   Товаров всего: {row[0]}")
        print(f"   Без категории: {row[1]}")
        print(f"   Без магазина: {row[2]}")
        print()
        
        # Шаг 1: Очистка дубликатов в id_mapping
        print("🗑️ Шаг 1: Очистка дубликатов в маппинге...")
        
        await session.execute(text("""
            DELETE FROM temp.id_mapping 
            WHERE old_table = 'companies'
        """))
        await session.commit()
        print("   ✅ Дубликаты удалены")
        print()
        
        # Шаг 2: Пересоздание маппинга магазинов
        print("🗺️ Шаг 2: Пересоздание маппинга магазинов...")
        
        await session.execute(text("""
            INSERT INTO temp.id_mapping (old_table, old_id, new_id)
            SELECT DISTINCT ON (tc.id) 'companies', tc.id, mso.id
            FROM temp.companies tc
            JOIN market.store_owners mso ON tc.name = mso.name
            WHERE tc.name IS NOT NULL
            ORDER BY tc.id, mso.id
        """))
        await session.commit()
        
        result = await session.execute(text("""
            SELECT COUNT(*) FROM temp.id_mapping WHERE old_table = 'companies'
        """))
        count = result.scalar()
        print(f"   ✅ Смаппено магазинов: {count}")
        print()
        
        # Шаг 3: Обновление товаров - привязка к магазинам
        print("🏪 Шаг 3: Привязка товаров к магазинам...")
        
        result = await session.execute(text("""
            UPDATE market.products p
            SET store_owner_id = map.new_id
            FROM temp.advert ta
            JOIN temp.id_mapping map ON map.old_table = 'companies' AND map.old_id = ta.company_id
            WHERE p.name = ta.title
              AND TO_TIMESTAMP(ta.created_at) = p.created_at
              AND p.store_owner_id IS NULL
        """))
        await session.commit()
        
        result = await session.execute(text("""
            SELECT COUNT(*) FROM market.products WHERE store_owner_id IS NOT NULL
        """))
        count = result.scalar()
        print(f"   ✅ Товаров с магазином: {count}")
        print()
        
        # Шаг 4: Обновление товаров - привязка к категориям
        print("📁 Шаг 4: Привязка товаров к категориям...")
        
        result = await session.execute(text("""
            UPDATE market.products p
            SET category_id = map.new_id
            FROM temp.advert ta
            JOIN temp.id_mapping map ON map.old_table = 'categories' AND map.old_id = ta.category_id
            WHERE p.name = ta.title
              AND TO_TIMESTAMP(ta.created_at) = p.created_at
              AND p.category_id IS NULL
        """))
        await session.commit()
        
        result = await session.execute(text("""
            SELECT COUNT(*) FROM market.products WHERE category_id IS NOT NULL
        """))
        count = result.scalar()
        print(f"   ✅ Товаров с категорией: {count}")
        print()
        
        # Шаг 5: Назначение дефолтной категории остальным
        print("📦 Шаг 5: Назначение дефолтной категории...")
        
        result = await session.execute(text("""
            UPDATE market.products
            SET category_id = 6  -- Готовые продукты
            WHERE category_id IS NULL
        """))
        await session.commit()
        
        result = await session.execute(text("""
            SELECT COUNT(*) FROM market.products WHERE category_id = 6
        """))
        count = result.scalar()
        print(f"   ✅ Товаров в категории 'Готовые продукты': {count}")
        print()
        
        # Шаг 6: Перезагрузка изображений с правильными связями
        print("🖼️ Шаг 6: Перезагрузка изображений...")
        
        # Удаляем старые изображения
        await session.execute(text("DELETE FROM market.product_images"))
        await session.commit()
        
        # Загружаем изображения с правильными связями
        result = await session.execute(text("""
            INSERT INTO market.product_images (product_id, image_url, old_id, sort_order, created_at)
            SELECT 
                p.id as product_id,
                '/uploads/products/original' || tf.path as image_url,
                tf.id as old_id,
                0 as sort_order,
                TO_TIMESTAMP(tf.created_at) as created_at
            FROM temp.file tf
            JOIN temp.advert ta ON ta.id = tf.advert_id
            JOIN market.products p ON p.name = ta.title 
                AND TO_TIMESTAMP(ta.created_at) = p.created_at
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
        
        # Обновляем маппинг изображений
        await session.execute(text("""
            UPDATE temp.image_mapping im
            SET new_image_id = pi.id,
                new_product_id = pi.product_id
            FROM market.product_images pi
            WHERE pi.old_id = im.old_file_id
        """))
        await session.commit()
        
        # Шаг 7: Итоговая проверка
        print("📊 Итоговая проверка:")
        
        result = await session.execute(text("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN category_id IS NOT NULL THEN 1 END) as with_category,
                COUNT(CASE WHEN store_owner_id IS NOT NULL THEN 1 END) as with_store
            FROM market.products
        """))
        row = result.first()
        print(f"   Товаров всего: {row[0]}")
        print(f"   С категорией: {row[1]} ({row[1]/row[0]*100:.1f}%)")
        print(f"   С магазином: {row[2]} ({row[2]/row[0]*100:.1f}%)")
        
        result = await session.execute(text("""
            SELECT COUNT(*) FROM market.product_images
        """))
        images = result.scalar()
        print(f"   Изображений: {images}")
        
        result = await session.execute(text("""
            SELECT COUNT(*) FROM market.store_owners
        """))
        stores = result.scalar()
        print(f"   Магазинов: {stores}")
        
        result = await session.execute(text("""
            SELECT COUNT(*) FROM config.users
        """))
        users = result.scalar()
        print(f"   Пользователей: {users}")
        
        # Статистика по категориям
        print(f"\n📊 Распределение товаров по категориям:")
        result = await session.execute(text("""
            SELECT c.name, COUNT(p.id) as count
            FROM market.categories c
            LEFT JOIN market.products p ON p.category_id = c.id
            GROUP BY c.id, c.name
            HAVING COUNT(p.id) > 0
            ORDER BY count DESC
        """))
        
        for row in result:
            print(f"   {row[0]:30} → {row[1]:>5} товаров")
    
    await engine.dispose()
    
    print()
    print("="*80)
    print("✅ ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(fix_migration())
