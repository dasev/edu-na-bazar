"""
Миграция данных из схемы temp в основные таблицы проекта
С сохранением ссылочной целостности и всех связей
"""
import asyncio
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar"


class DataMigrator:
    """Класс для миграции данных с сохранением связей"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = None
        self.session_maker = None
        
        # Статистика миграции
        self.stats = {
            'categories': {'migrated': 0, 'errors': 0},
            'users': {'migrated': 0, 'errors': 0},
            'store_owners': {'migrated': 0, 'errors': 0},
            'products': {'migrated': 0, 'errors': 0},
            'product_images': {'migrated': 0, 'errors': 0},
            'reviews': {'migrated': 0, 'errors': 0},
        }
    
    async def init(self):
        """Инициализация подключения"""
        self.engine = create_async_engine(self.database_url, echo=False)
        self.session_maker = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
    
    async def close(self):
        """Закрытие подключения"""
        if self.engine:
            await self.engine.dispose()
    
    async def create_mapping_table(self, session: AsyncSession):
        """Создаёт таблицу для маппинга старых ID на новые"""
        print("📋 Создаём таблицу маппинга ID...")
        
        await session.execute(text("""
            CREATE TABLE IF NOT EXISTS temp.id_mapping (
                old_table VARCHAR(50) NOT NULL,
                old_id INTEGER NOT NULL,
                new_id BIGINT NOT NULL,
                PRIMARY KEY (old_table, old_id)
            )
        """))
        
        # Очищаем таблицу если она уже существует
        await session.execute(text("TRUNCATE TABLE temp.id_mapping"))
        await session.commit()
        
        print("✅ Таблица маппинга создана")
    
    async def migrate_categories(self, session: AsyncSession):
        """
        Фаза 1: Миграция категорий с использованием маппинга
        temp.categories → market.categories (через temp.category_mapping)
        """
        print("\n" + "="*80)
        print("📁 ФАЗА 1: Маппинг категорий")
        print("="*80)
        
        try:
            # Используем готовый маппинг из temp.category_mapping
            # Сохраняем маппинг категорий в temp.id_mapping
            await session.execute(text("""
                INSERT INTO temp.id_mapping (old_table, old_id, new_id)
                SELECT 'categories', tc.id, tcm.market_category_id
                FROM temp.categories tc
                JOIN temp.category_mapping tcm ON tcm.temp_category_name = tc.name
                WHERE tcm.market_category_id IS NOT NULL
                ON CONFLICT (old_table, old_id) DO UPDATE
                SET new_id = EXCLUDED.new_id
            """))
            await session.commit()
            
            # Подсчитываем смаппенные категории
            result = await session.execute(text("""
                SELECT COUNT(*) FROM temp.id_mapping WHERE old_table = 'categories'
            """))
            count = result.scalar()
            self.stats['categories']['migrated'] = count
            
            print(f"✅ Смаппено категорий: {count}")
            
            # Показываем распределение по категориям
            result = await session.execute(text("""
                SELECT mc.name, COUNT(im.old_id) as count
                FROM temp.id_mapping im
                JOIN market.categories mc ON mc.id = im.new_id
                WHERE im.old_table = 'categories'
                GROUP BY mc.id, mc.name
                ORDER BY count DESC
            """))
            
            print(f"\n📊 Распределение по категориям:")
            for row in result:
                print(f"   {row[0]:30} ← {row[1]:2} категорий из temp")
            
            print(f"\n📊 Итого смаппено категорий: {self.stats['categories']['migrated']}")
            
        except Exception as e:
            self.stats['categories']['errors'] += 1
            print(f"❌ Ошибка маппинга категорий: {e}")
            await session.rollback()
    
    async def migrate_users(self, session: AsyncSession):
        """
        Фаза 2: Миграция пользователей
        temp.user → config.users
        """
        print("\n" + "="*80)
        print("👥 ФАЗА 2: Миграция пользователей")
        print("="*80)
        
        try:
            # Вставляем пользователей
            result = await session.execute(text("""
                INSERT INTO config.users (phone, email, full_name, is_active, status, created_at, updated_at, last_login)
                SELECT 
                    -- Если телефона нет, генерируем уникальный
                    CASE 
                        WHEN phone IS NOT NULL AND phone != '' THEN phone
                        ELSE 'temp_' || id || '@migrated.local'
                    END as phone,
                    NULLIF(email, '') as email,
                    name as full_name,
                    (status = 1) as is_active,
                    CASE WHEN status = 1 THEN 'active' ELSE 'blocked' END as status,
                    TO_TIMESTAMP(created_at) as created_at,
                    TO_TIMESTAMP(updated_at) as updated_at,
                    CASE WHEN last_login IS NOT NULL THEN TO_TIMESTAMP(last_login) ELSE NULL END as last_login
                FROM temp.user
                WHERE email IS NOT NULL
                ON CONFLICT (phone) DO NOTHING
                RETURNING id
            """))
            
            count = len(result.fetchall())
            self.stats['users']['migrated'] = count
            await session.commit()
            print(f"✅ Пользователи: {count}")
            
            # Сохраняем маппинг пользователей
            await session.execute(text("""
                INSERT INTO temp.id_mapping (old_table, old_id, new_id)
                SELECT 'user', tu.id, cu.id
                FROM temp.user tu
                JOIN config.users cu ON tu.email = cu.email
                WHERE tu.email IS NOT NULL
            """))
            await session.commit()
            
            print(f"📊 Итого пользователей: {self.stats['users']['migrated']}")
            
        except Exception as e:
            self.stats['users']['errors'] += 1
            print(f"❌ Ошибка миграции пользователей: {e}")
            await session.rollback()
    
    async def migrate_store_owners(self, session: AsyncSession):
        """
        Фаза 3: Миграция магазинов (компаний → store_owners)
        temp.companies → market.store_owners
        Связь: store_owner → user (owner_id)
        """
        print("\n" + "="*80)
        print("🏪 ФАЗА 3: Миграция магазинов")
        print("="*80)
        
        try:
            # Вставляем магазины с привязкой к пользователям
            result = await session.execute(text("""
                INSERT INTO market.store_owners (
                    owner_id, inn, name, legal_name, address, phone, email, 
                    description, logo, category_id, status, created_at, updated_at
                )
                SELECT 
                    -- Связываем с пользователем если есть user_id
                    COALESCE(user_map.new_id, (SELECT id FROM config.users LIMIT 1)) as owner_id,
                    -- Генерируем ИНН если нет
                    COALESCE(NULLIF(tc.phone, ''), 'MIGR' || tc.id) as inn,
                    tc.name,
                    tc.name as legal_name,
                    COALESCE(tc.address, 'Адрес не указан') as address,
                    NULLIF(tc.phone, '') as phone,
                    NULLIF(tc.email, '') as email,
                    tc.description,
                    tc.logo,
                    cat_map.new_id as category_id,
                    CASE WHEN tc.status = 1 THEN 'active' ELSE 'pending' END as status,
                    TO_TIMESTAMP(tc.created_at) as created_at,
                    TO_TIMESTAMP(tc.updated_at) as updated_at
                FROM temp.companies tc
                LEFT JOIN temp.id_mapping user_map ON user_map.old_table = 'user' AND user_map.old_id = tc.user_id
                LEFT JOIN temp.id_mapping cat_map ON cat_map.old_table = 'categories' AND cat_map.old_id = tc.category_id
                WHERE tc.name IS NOT NULL
                ON CONFLICT (inn) DO NOTHING
                RETURNING id
            """))
            
            count = len(result.fetchall())
            self.stats['store_owners']['migrated'] = count
            await session.commit()
            print(f"✅ Магазины: {count}")
            
            # Сохраняем маппинг магазинов
            await session.execute(text("""
                INSERT INTO temp.id_mapping (old_table, old_id, new_id)
                SELECT 'companies', tc.id, mso.id
                FROM temp.companies tc
                JOIN market.store_owners mso ON tc.name = mso.name
                WHERE tc.name IS NOT NULL
            """))
            await session.commit()
            
            print(f"📊 Итого магазинов: {self.stats['store_owners']['migrated']}")
            
        except Exception as e:
            self.stats['store_owners']['errors'] += 1
            print(f"❌ Ошибка миграции магазинов: {e}")
            await session.rollback()
    
    async def migrate_products(self, session: AsyncSession):
        """
        Фаза 4: Миграция товаров
        temp.advert → market.products
        Связи: product → category, product → store_owner
        """
        print("\n" + "="*80)
        print("📦 ФАЗА 4: Миграция товаров")
        print("="*80)
        
        try:
            # Вставляем товары со всеми связями
            result = await session.execute(text("""
                INSERT INTO market.products (
                    name, description, price, category_id, store_owner_id,
                    in_stock, views, status, created_at, updated_at
                )
                SELECT 
                    ta.title as name,
                    ta.description,
                    COALESCE(ta.price, 0)::DOUBLE PRECISION as price,
                    cat_map.new_id as category_id,
                    store_map.new_id as store_owner_id,
                    (ta.status = 1) as in_stock,
                    COALESCE(ta.views, 0) as views,
                    CASE WHEN ta.status = 1 THEN 'active' ELSE 'archived' END as status,
                    TO_TIMESTAMP(ta.created_at) as created_at,
                    TO_TIMESTAMP(ta.updated_at) as updated_at
                FROM temp.advert ta
                LEFT JOIN temp.id_mapping cat_map ON cat_map.old_table = 'categories' AND cat_map.old_id = ta.category_id
                LEFT JOIN temp.id_mapping store_map ON store_map.old_table = 'companies' AND store_map.old_id = ta.company_id
                WHERE ta.title IS NOT NULL
                RETURNING id
            """))
            
            count = len(result.fetchall())
            self.stats['products']['migrated'] = count
            await session.commit()
            print(f"✅ Товары: {count}")
            
            # Сохраняем маппинг товаров
            await session.execute(text("""
                INSERT INTO temp.id_mapping (old_table, old_id, new_id)
                SELECT 'advert', ta.id, mp.id
                FROM temp.advert ta
                JOIN market.products mp ON ta.title = mp.name
                    AND TO_TIMESTAMP(ta.created_at) = mp.created_at
                WHERE ta.title IS NOT NULL
                LIMIT 14139
            """))
            await session.commit()
            
            print(f"📊 Итого товаров: {self.stats['products']['migrated']}")
            
        except Exception as e:
            self.stats['products']['errors'] += 1
            print(f"❌ Ошибка миграции товаров: {e}")
            await session.rollback()
    
    async def migrate_product_images(self, session: AsyncSession):
        """
        Фаза 5: Миграция изображений товаров
        temp.file → market.product_images
        Связь: product_image → product
        Сохраняем old_id для ручной корректировки
        """
        print("\n" + "="*80)
        print("🖼️ ФАЗА 5: Миграция изображений")
        print("="*80)
        
        try:
            # Проверяем есть ли изображения с привязкой к товарам
            result = await session.execute(text("""
                SELECT COUNT(*) 
                FROM temp.file tf
                JOIN temp.id_mapping prod_map ON prod_map.old_table = 'advert' AND prod_map.old_id = tf.advert_id
                WHERE tf.type = 'image' AND tf.advert_id IS NOT NULL
            """))
            
            images_with_products = result.scalar()
            
            if images_with_products > 0:
                # Вставляем изображения с привязкой к товарам
                result = await session.execute(text("""
                    INSERT INTO market.product_images (product_id, image_url, old_id, sort_order, created_at)
                    SELECT 
                        prod_map.new_id as product_id,
                        '/uploads/products/original' || tf.path as image_url,
                        tf.id as old_id,
                        0 as sort_order,
                        TO_TIMESTAMP(tf.created_at) as created_at
                    FROM temp.file tf
                    JOIN temp.id_mapping prod_map ON prod_map.old_table = 'advert' AND prod_map.old_id = tf.advert_id
                    WHERE tf.type = 'image' AND tf.advert_id IS NOT NULL
                    RETURNING id
                """))
                
                count = len(result.fetchall())
                self.stats['product_images']['migrated'] = count
                await session.commit()
                print(f"✅ Изображения с привязкой: {count}")
            else:
                print(f"⚠️ Изображения не привязаны к товарам в temp.file")
                print(f"   Назначаем плейсхолдеры...")
                
                # Назначаем плейсхолдер каждому товару
                result = await session.execute(text("""
                    INSERT INTO market.product_images (product_id, image_url, old_id, sort_order, created_at)
                    SELECT 
                        p.id as product_id,
                        '/uploads/products/placeholder.jpg' as image_url,
                        NULL as old_id,
                        0 as sort_order,
                        NOW() as created_at
                    FROM market.products p
                    WHERE NOT EXISTS (
                        SELECT 1 FROM market.product_images pi WHERE pi.product_id = p.id
                    )
                    RETURNING id
                """))
                
                count = len(result.fetchall())
                self.stats['product_images']['migrated'] = count
                await session.commit()
                print(f"✅ Плейсхолдеры: {count}")
            
            # Обновляем маппинг изображений
            await session.execute(text("""
                UPDATE temp.image_mapping im
                SET new_image_id = pi.id,
                    new_product_id = pi.product_id
                FROM market.product_images pi
                WHERE pi.old_id = im.old_file_id
            """))
            await session.commit()
            
            print(f"📊 Итого изображений: {self.stats['product_images']['migrated']}")
            print(f"💡 Используйте temp.image_mapping для ручной корректировки")
            
        except Exception as e:
            self.stats['product_images']['errors'] += 1
            print(f"❌ Ошибка миграции изображений: {e}")
            await session.rollback()
    
    async def migrate_reviews(self, session: AsyncSession):
        """
        Фаза 6: Миграция отзывов
        temp.review → market.reviews
        Связи: review → product, review → user
        """
        print("\n" + "="*80)
        print("⭐ ФАЗА 6: Миграция отзывов")
        print("="*80)
        
        try:
            # Вставляем отзывы с привязкой к товарам и пользователям
            result = await session.execute(text("""
                INSERT INTO market.reviews (product_id, user_id, rating, comment, created_at, updated_at)
                SELECT 
                    -- Связываем с первым товаром компании
                    (SELECT mp.id FROM market.products mp 
                     JOIN temp.id_mapping store_map ON store_map.new_id = mp.store_owner_id 
                     WHERE store_map.old_table = 'companies' AND store_map.old_id = tr.company_id 
                     LIMIT 1) as product_id,
                    user_map.new_id as user_id,
                    tr.rating,
                    tr.text as comment,
                    TO_TIMESTAMP(tr.created_at) as created_at,
                    TO_TIMESTAMP(tr.updated_at) as updated_at
                FROM temp.review tr
                LEFT JOIN temp.id_mapping user_map ON user_map.old_table = 'user' AND user_map.old_id = tr.user_id
                WHERE tr.text IS NOT NULL 
                    AND tr.company_id IS NOT NULL
                    AND EXISTS (
                        SELECT 1 FROM market.products mp 
                        JOIN temp.id_mapping store_map ON store_map.new_id = mp.store_owner_id 
                        WHERE store_map.old_table = 'companies' AND store_map.old_id = tr.company_id
                    )
                RETURNING id
            """))
            
            count = len(result.fetchall())
            self.stats['reviews']['migrated'] = count
            await session.commit()
            print(f"✅ Отзывы: {count}")
            
            print(f"📊 Итого отзывов: {self.stats['reviews']['migrated']}")
            
        except Exception as e:
            self.stats['reviews']['errors'] += 1
            print(f"❌ Ошибка миграции отзывов: {e}")
            await session.rollback()
    
    async def verify_integrity(self, session: AsyncSession):
        """Проверка ссылочной целостности"""
        print("\n" + "="*80)
        print("🔍 ПРОВЕРКА ССЫЛОЧНОЙ ЦЕЛОСТНОСТИ")
        print("="*80)
        
        # Проверяем товары без категорий
        result = await session.execute(text("""
            SELECT COUNT(*) FROM market.products WHERE category_id IS NULL
        """))
        no_category = result.scalar()
        print(f"⚠️ Товаров без категории: {no_category}")
        
        # Проверяем товары без магазина
        result = await session.execute(text("""
            SELECT COUNT(*) FROM market.products WHERE store_owner_id IS NULL
        """))
        no_store = result.scalar()
        print(f"⚠️ Товаров без магазина: {no_store}")
        
        # Проверяем магазины без владельца
        result = await session.execute(text("""
            SELECT COUNT(*) FROM market.store_owners WHERE owner_id IS NULL
        """))
        no_owner = result.scalar()
        print(f"⚠️ Магазинов без владельца: {no_owner}")
        
        # Проверяем изображения без товара
        result = await session.execute(text("""
            SELECT COUNT(*) FROM market.product_images 
            WHERE product_id NOT IN (SELECT id FROM market.products)
        """))
        orphan_images = result.scalar()
        print(f"⚠️ Изображений без товара: {orphan_images}")
        
        # Статистика по связям
        result = await session.execute(text("""
            SELECT 
                COUNT(DISTINCT p.id) as products_with_category,
                COUNT(DISTINCT p.store_owner_id) as unique_stores,
                COUNT(DISTINCT p.category_id) as unique_categories
            FROM market.products p
            WHERE p.category_id IS NOT NULL
        """))
        row = result.first()
        print(f"\n✅ Товаров с категорией: {row[0]}")
        print(f"✅ Уникальных магазинов: {row[1]}")
        print(f"✅ Уникальных категорий: {row[2]}")
    
    async def print_statistics(self):
        """Вывод итоговой статистики"""
        print("\n" + "="*80)
        print("📊 ИТОГОВАЯ СТАТИСТИКА МИГРАЦИИ")
        print("="*80)
        
        total_migrated = sum(s['migrated'] for s in self.stats.values())
        total_errors = sum(s['errors'] for s in self.stats.values())
        
        for table, stats in self.stats.items():
            status = "✅" if stats['errors'] == 0 else "⚠️"
            print(f"{status} {table:20} → {stats['migrated']:>6} записей | Ошибок: {stats['errors']}")
        
        print(f"\n{'='*80}")
        print(f"📈 ВСЕГО МИГРИРОВАНО: {total_migrated} записей")
        print(f"❌ ВСЕГО ОШИБОК: {total_errors}")
        print(f"{'='*80}")
    
    async def run(self):
        """Запуск полной миграции"""
        print("="*80)
        print("🚀 МИГРАЦИЯ ДАННЫХ ИЗ TEMP В ОСНОВНЫЕ ТАБЛИЦЫ")
        print("="*80)
        print(f"📅 Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔗 БД: {self.database_url}")
        print("="*80)
        
        await self.init()
        
        async with self.session_maker() as session:
            # Создаём таблицу маппинга
            await self.create_mapping_table(session)
            
            # Фаза 1: Категории (без зависимостей)
            await self.migrate_categories(session)
            
            # Фаза 2: Пользователи (без зависимостей)
            await self.migrate_users(session)
            
            # Фаза 3: Магазины (зависят от пользователей и категорий)
            await self.migrate_store_owners(session)
            
            # Фаза 4: Товары (зависят от категорий и магазинов)
            await self.migrate_products(session)
            
            # Фаза 5: Изображения (зависят от товаров)
            await self.migrate_product_images(session)
            
            # Фаза 6: Отзывы (зависят от товаров и пользователей)
            await self.migrate_reviews(session)
            
            # Проверка целостности
            await self.verify_integrity(session)
        
        # Итоговая статистика
        await self.print_statistics()
        
        await self.close()
        
        print("\n" + "="*80)
        print("🎉 МИГРАЦИЯ ЗАВЕРШЕНА!")
        print("="*80)


async def main():
    """Главная функция"""
    migrator = DataMigrator(DATABASE_URL)
    await migrator.run()


if __name__ == "__main__":
    asyncio.run(main())
