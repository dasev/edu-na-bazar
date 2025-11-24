"""
Финальная миграция товаров с правильной обработкой NULL
- Если company_id NULL → создаём дефолтную компанию "Старые данные"
- Если category_id NULL → назначаем категорию "Услуги"
"""
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar"


async def final_migration():
    """Финальная миграция с обработкой NULL"""
    
    print("="*80)
    print("🚀 ФИНАЛЬНАЯ МИГРАЦИЯ ТОВАРОВ")
    print("="*80)
    print()
    
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Шаг 1: Создаём дефолтную компанию для старых данных
        print("🏪 Шаг 1: Создание дефолтной компании...")
        
        result = await session.execute(text("""
            SELECT id FROM market.store_owners WHERE name = 'Старые данные'
        """))
        default_company = result.scalar()
        
        if not default_company:
            result = await session.execute(text("""
                INSERT INTO market.store_owners (
                    owner_id, name, legal_name, inn, address, description, status, created_at, updated_at
                )
                VALUES (
                    1,  -- Привязываем к первому пользователю
                    'Старые данные',
                    'ООО "Старые данные"',
                    '0000000000',
                    'Адрес не указан',
                    'Компания для товаров без привязки из старой системы',
                    'active',
                    NOW(),
                    NOW()
                )
                RETURNING id
            """))
            default_company = result.scalar()
            await session.commit()
            print(f"   ✅ Создана компания ID: {default_company}")
        else:
            print(f"   ✅ Компания уже существует ID: {default_company}")
        
        print()
        
        # Шаг 2: Получаем ID категории "Услуги"
        print("📁 Шаг 2: Получение категории 'Услуги'...")
        
        result = await session.execute(text("""
            SELECT id FROM market.categories WHERE name = 'Услуги'
        """))
        services_category = result.scalar()
        print(f"   ✅ Категория 'Услуги' ID: {services_category}")
        print()
        
        # Шаг 3: Проверяем текущее состояние temp.advert
        print("📊 Шаг 3: Анализ temp.advert...")
        
        result = await session.execute(text("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN company_id IS NOT NULL THEN 1 END) as with_company,
                COUNT(CASE WHEN category_id IS NOT NULL THEN 1 END) as with_category
            FROM temp.advert
        """))
        row = result.first()
        print(f"   Всего товаров: {row[0]}")
        print(f"   С company_id: {row[1]} ({row[1]/row[0]*100:.1f}%)")
        print(f"   С category_id: {row[2]} ({row[2]/row[0]*100:.1f}%)")
        print(f"   Без company_id: {row[0] - row[1]} (будут в 'Старые данные')")
        print(f"   Без category_id: {row[0] - row[2]} (будут в 'Услуги')")
        print()
        
        # Шаг 4: Очищаем старые данные
        print("🗑️ Шаг 4: Очистка старых данных...")
        
        await session.execute(text("DELETE FROM market.product_images"))
        await session.execute(text("DELETE FROM market.products"))
        await session.execute(text("DELETE FROM temp.id_mapping WHERE old_table IN ('advert', 'categories')"))
        await session.commit()
        print("   ✅ Старые данные удалены")
        print()
        
        # Шаг 5: Пересоздаём маппинг категорий
        print("🗺️ Шаг 5: Маппинг категорий...")
        
        # Маппинг категорий уже создан в temp.category_mapping
        # Нужно создать маппинг по ID из temp.categories
        await session.execute(text("""
            INSERT INTO temp.id_mapping (old_table, old_id, new_id)
            SELECT 'categories', tc.id, tcm.market_category_id
            FROM temp.categories tc
            JOIN temp.category_mapping tcm ON tc.name = tcm.temp_category_name
            WHERE tcm.market_category_id IS NOT NULL
        """))
        await session.commit()
        
        result = await session.execute(text("""
            SELECT COUNT(*) FROM temp.id_mapping WHERE old_table = 'categories'
        """))
        count = result.scalar()
        print(f"   ✅ Смаппено категорий: {count}")
        print()
        
        # Шаг 6: Миграция товаров с обработкой NULL
        print("📦 Шаг 6: Миграция товаров...")
        print("   Это займёт несколько минут...")
        
        result = await session.execute(text(f"""
            INSERT INTO market.products (
                name, description, price, category_id, store_owner_id, 
                status, views, created_at, updated_at
            )
            SELECT 
                ta.title,
                COALESCE(ta.description, ''),
                COALESCE(ta.price, 0),
                -- Если category_id NULL или нет в маппинге → Услуги
                COALESCE(
                    (SELECT new_id FROM temp.id_mapping 
                     WHERE old_table = 'categories' AND old_id = ta.category_id),
                    {services_category}
                ),
                -- Если company_id NULL или нет в маппинге → Старые данные
                COALESCE(
                    (SELECT new_id FROM temp.id_mapping 
                     WHERE old_table = 'companies' AND old_id = ta.company_id),
                    {default_company}
                ),
                CASE WHEN ta.status = 1 THEN 'active' ELSE 'inactive' END,
                COALESCE(ta.views, 0),
                TO_TIMESTAMP(ta.created_at),
                TO_TIMESTAMP(ta.updated_at)
            FROM temp.advert ta
            ORDER BY ta.id
        """))
        await session.commit()
        
        result = await session.execute(text("SELECT COUNT(*) FROM market.products"))
        total_products = result.scalar()
        print(f"   ✅ Мигрировано товаров: {total_products}")
        print()
        
        # Шаг 7: Создаём маппинг товаров
        print("🗺️ Шаг 7: Создание маппинга товаров...")
        
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
        
        # Шаг 8: Миграция изображений
        print("🖼️ Шаг 8: Миграция изображений...")
        
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
        
        result = await session.execute(text("SELECT COUNT(*) FROM market.product_images"))
        total_images = result.scalar()
        print(f"   ✅ Загружено изображений: {total_images}")
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
        
        # Шаг 9: Итоговая статистика
        print("="*80)
        print("📊 ИТОГОВАЯ СТАТИСТИКА")
        print("="*80)
        print()
        
        # Товары
        result = await session.execute(text("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN category_id = :services_cat THEN 1 END) as in_services,
                COUNT(CASE WHEN store_owner_id = :default_company THEN 1 END) as in_default_company
            FROM market.products
        """), {"services_cat": services_category, "default_company": default_company})
        row = result.first()
        
        print(f"📦 Товары:")
        print(f"   Всего: {row[0]}")
        print(f"   В категории 'Услуги': {row[1]} ({row[1]/row[0]*100:.1f}%)")
        print(f"   В компании 'Старые данные': {row[2]} ({row[2]/row[0]*100:.1f}%)")
        print()
        
        # Распределение по категориям
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
            print(f"   {row[0]:30} → {row[1]:>6} товаров")
        
        print()
        
        # Распределение по компаниям
        print("🏪 Топ-10 компаний:")
        result = await session.execute(text("""
            SELECT so.name, COUNT(p.id) as count
            FROM market.store_owners so
            LEFT JOIN market.products p ON p.store_owner_id = so.id
            GROUP BY so.id, so.name
            HAVING COUNT(p.id) > 0
            ORDER BY count DESC
            LIMIT 10
        """))
        
        for row in result:
            print(f"   {row[0]:30} → {row[1]:>6} товаров")
        
        print()
        
        # Изображения
        print(f"🖼️ Изображений: {total_images}")
        
        result = await session.execute(text("SELECT COUNT(*) FROM market.store_owners"))
        stores = result.scalar()
        print(f"🏪 Магазинов: {stores}")
        
        result = await session.execute(text("SELECT COUNT(*) FROM config.users"))
        users = result.scalar()
        print(f"👥 Пользователей: {users}")
        
        result = await session.execute(text("SELECT COUNT(*) FROM market.categories"))
        categories = result.scalar()
        print(f"📁 Категорий: {categories}")
    
    await engine.dispose()
    
    print()
    print("="*80)
    print("🎉 МИГРАЦИЯ ЗАВЕРШЕНА УСПЕШНО!")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(final_migration())
