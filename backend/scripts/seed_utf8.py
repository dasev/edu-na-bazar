"""
Скрипт для заполнения БД тестовыми данными с правильной кодировкой UTF-8
"""
import asyncio
import sys
from decimal import Decimal
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text

# Устанавливаем UTF-8 для вывода
sys.stdout.reconfigure(encoding='utf-8')

# Настройка путей
sys.path.insert(0, 'C:\\python\\edu-na-bazar\\backend')

from config import settings

async def seed_database():
    """Заполнить БД тестовыми данными"""
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        print("🌱 Очищаем старые данные...")
        
        # Очищаем таблицы
        await session.execute(text("TRUNCATE TABLE cart_items, order_items, orders, products, categories, stores CASCADE"))
        await session.commit()
        
        print("📁 Создаем категории...")
        
        # Категории
        categories = [
            ("11111111-1111-1111-1111-111111111111", "Фрукты", "fruits", "🍎", 1),
            ("22222222-2222-2222-2222-222222222222", "Овощи", "vegetables", "🥕", 2),
            ("33333333-3333-3333-3333-333333333333", "Молочные продукты", "dairy", "🥛", 3),
            ("44444444-4444-4444-4444-444444444444", "Мясо и птица", "meat", "🍖", 4),
            ("55555555-5555-5555-5555-555555555555", "Зерно и крупы", "grains", "🌾", 5),
            ("66666666-6666-6666-6666-666666666666", "Яйца и мёд", "eggs-honey", "🥚", 6),
        ]
        
        for cat_id, name, slug, icon, sort_order in categories:
            await session.execute(
                text("INSERT INTO categories (id, name, slug, icon, sort_order) VALUES (:id, :name, :slug, :icon, :sort_order)"),
                {"id": cat_id, "name": name, "slug": slug, "icon": icon, "sort_order": sort_order}
            )
            print(f"  ✅ {name}")
        
        await session.commit()
        
        print("\n🛒 Создаем товары...")
        
        # Товары
        products = [
            ("a1111111-1111-1111-1111-111111111111", "Яблоки Гренни Смит", "Свежие зеленые яблоки", 120.00, 150.00, "11111111-1111-1111-1111-111111111111", "https://placehold.co/300x300/e8f5e9/2e7d32?text=🍎", 4.5, "шт"),
            ("a2222222-2222-2222-2222-222222222222", "Бананы", "Спелые бананы из Эквадора", 80.00, None, "11111111-1111-1111-1111-111111111111", "https://placehold.co/300x300/fff9c4/f57f17?text=🍌", 4.8, "кг"),
            ("a3333333-3333-3333-3333-333333333333", "Апельсины", "Сочные апельсины", 100.00, None, "11111111-1111-1111-1111-111111111111", "https://placehold.co/300x300/ffe0b2/e65100?text=🍊", 4.6, "кг"),
            ("b1111111-1111-1111-1111-111111111111", "Помидоры", "Свежие томаты", 90.00, None, "22222222-2222-2222-2222-222222222222", "https://placehold.co/300x300/ffebee/c62828?text=🍅", 4.4, "кг"),
            ("b2222222-2222-2222-2222-222222222222", "Огурцы", "Хрустящие огурцы", 70.00, None, "22222222-2222-2222-2222-222222222222", "https://placehold.co/300x300/e8f5e9/388e3c?text=🥒", 4.3, "кг"),
            ("c1111111-1111-1111-1111-111111111111", "Молоко 3.2%", "Свежее молоко", 65.00, None, "33333333-3333-3333-3333-333333333333", "https://placehold.co/300x300/e3f2fd/1976d2?text=🥛", 4.7, "л"),
            ("c2222222-2222-2222-2222-222222222222", "Творог 5%", "Домашний творог", 110.00, None, "33333333-3333-3333-3333-333333333333", "https://placehold.co/300x300/fff3e0/f57c00?text=🧀", 4.6, "кг"),
            ("d1111111-1111-1111-1111-111111111111", "Куриная грудка", "Охлажденная грудка", 280.00, 320.00, "44444444-4444-4444-4444-444444444444", "https://placehold.co/300x300/fce4ec/c2185b?text=🍗", 4.8, "кг"),
            ("e1111111-1111-1111-1111-111111111111", "Гречка зеленая", "Органическая зеленая гречка", 180.00, 220.00, "55555555-5555-5555-5555-555555555555", "https://placehold.co/300x300/e8f5e9/558b2f?text=🌾", 4.7, "кг"),
            ("e2222222-2222-2222-2222-222222222222", "Пшеница", "Пшеница твердых сортов", 35.00, None, "55555555-5555-5555-5555-555555555555", "https://placehold.co/300x300/fff8e1/f9a825?text=🌾", 4.5, "кг"),
            ("f1111111-1111-1111-1111-111111111111", "Яйца куриные С0", "Свежие домашние яйца", 95.00, 110.00, "66666666-6666-6666-6666-666666666666", "https://placehold.co/300x300/fff8e1/f57f17?text=🥚", 4.9, "десяток"),
            ("f2222222-2222-2222-2222-222222222222", "Мёд цветочный", "Натуральный мёд с пасеки", 450.00, None, "66666666-6666-6666-6666-666666666666", "https://placehold.co/300x300/fff3e0/ff6f00?text=🍯", 5.0, "кг"),
        ]
        
        for prod_id, name, desc, price, old_price, cat_id, image, rating, unit in products:
            await session.execute(
                text("""
                    INSERT INTO products (id, name, description, price, old_price, category_id, image, rating, in_stock, unit)
                    VALUES (:id, :name, :desc, :price, :old_price, :cat_id, :image, :rating, true, :unit)
                """),
                {
                    "id": prod_id, "name": name, "desc": desc, "price": price,
                    "old_price": old_price, "cat_id": cat_id, "image": image,
                    "rating": rating, "unit": unit
                }
            )
            print(f"  ✅ {name}")
        
        await session.commit()
        
        print("\n🏪 Создаем магазины...")
        
        # Магазины
        stores = [
            ("f1111111-1111-1111-1111-111111111111", "Базар Центральный", "ул. Ленина, 1", "+7 (999) 123-45-67", 37.6173, 55.7558),
            ("f2222222-2222-2222-2222-222222222222", "Базар Южный", "ул. Мира, 10", "+7 (999) 234-56-78", 37.6273, 55.7458),
            ("f3333333-3333-3333-3333-333333333333", "Базар Северный", "пр. Победы, 5", "+7 (999) 345-67-89", 37.6073, 55.7658),
        ]
        
        for store_id, name, address, phone, lon, lat in stores:
            await session.execute(
                text("""
                    INSERT INTO stores (id, name, address, phone, location, is_active)
                    VALUES (:id, :name, :address, :phone, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326), true)
                """),
                {"id": store_id, "name": name, "address": address, "phone": phone, "lon": lon, "lat": lat}
            )
            print(f"  ✅ {name}")
        
        await session.commit()
        
        print("\n🎉 Заполнение БД завершено успешно!")
        print(f"  📊 Категорий: {len(categories)}")
        print(f"  🛒 Товаров: {len(products)}")
        print(f"  🏪 Магазинов: {len(stores)}")
        print("\n📦 Категории:")
        for _, name, _, icon, _ in categories:
            print(f"  {icon} {name}")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_database())
