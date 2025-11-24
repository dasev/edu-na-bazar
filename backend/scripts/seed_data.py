"""
Скрипт для заполнения БД тестовыми данными
"""
import asyncio
from decimal import Decimal
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from geoalchemy2.elements import WKTElement

from config import settings
from models.category import Category
from models.product import Product
from models.store import Store


# Категории
CATEGORIES = [
    {"name": "Агротовары и удобрения", "slug": "agro", "icon": "🌱", "sort_order": 1},
    {"name": "Готовые продукты", "slug": "ready-food", "icon": "🥫", "sort_order": 2},
    {"name": "Зерно", "slug": "grain", "icon": "🌾", "sort_order": 3},
    {"name": "Корма и добавки", "slug": "feed", "icon": "🌽", "sort_order": 4},
    {"name": "Мед", "slug": "honey", "icon": "🍯", "sort_order": 5},
    {"name": "Молочные продукты", "slug": "dairy", "icon": "🥛", "sort_order": 6},
    {"name": "Мясо, птица, рыба", "slug": "meat", "icon": "🥩", "sort_order": 7},
    {"name": "Оборудование и техника", "slug": "equipment", "icon": "🚜", "sort_order": 8},
    {"name": "Овощи и фрукты", "slug": "vegetables-fruits", "icon": "🥬", "sort_order": 9},
    {"name": "Услуги", "slug": "services", "icon": "⚙️", "sort_order": 10},
    {"name": "Яйца", "slug": "eggs", "icon": "🥚", "sort_order": 11},
    {"name": "Саженцы и семена", "slug": "seedlings", "icon": "🌿", "sort_order": 12},
]


# Товары (будут привязаны к категориям)
PRODUCTS = [
    # Фрукты
    {
        "name": "Яблоки Голден",
        "slug": "apples-golden",
        "description": "Сладкие и сочные яблоки сорта Голден. Идеальны для детей и взрослых.",
        "price": Decimal("89.90"),
        "old_price": Decimal("120.00"),
        "image": "https://via.placeholder.com/300x300?text=Apples",
        "category_slug": "vegetables-fruits",
        "rating": Decimal("4.8"),
        "reviews_count": 156,
        "in_stock": True,
        "stock_quantity": 500,
        "unit": "кг",
    },
    {
        "name": "Бананы",
        "slug": "bananas",
        "description": "Спелые бананы из Эквадора. Богаты калием и витаминами.",
        "price": Decimal("69.90"),
        "image": "https://via.placeholder.com/300x300?text=Bananas",
        "category_slug": "vegetables-fruits",
        "rating": Decimal("4.7"),
        "reviews_count": 203,
        "in_stock": True,
        "stock_quantity": 300,
        "unit": "кг",
    },
    {
        "name": "Апельсины",
        "slug": "oranges",
        "description": "Сочные апельсины из Марокко. Отличный источник витамина C.",
        "price": Decimal("99.90"),
        "old_price": Decimal("129.90"),
        "image": "https://via.placeholder.com/300x300?text=Oranges",
        "category_slug": "vegetables-fruits",
        "rating": Decimal("4.9"),
        "reviews_count": 178,
        "in_stock": True,
        "stock_quantity": 250,
        "unit": "кг",
    },
    # Овощи
    {
        "name": "Помидоры",
        "slug": "tomatoes",
        "description": "Свежие помидоры. Выращены без пестицидов.",
        "price": Decimal("149.90"),
        "image": "https://via.placeholder.com/300x300?text=Tomatoes",
        "category_slug": "vegetables-fruits",
        "rating": Decimal("4.6"),
        "reviews_count": 134,
        "in_stock": True,
        "stock_quantity": 200,
        "unit": "кг",
    },
    {
        "name": "Огурцы",
        "slug": "cucumbers",
        "description": "Хрустящие огурцы. Идеальны для салатов.",
        "price": Decimal("89.90"),
        "image": "https://via.placeholder.com/300x300?text=Cucumbers",
        "category_slug": "vegetables-fruits",
        "rating": Decimal("4.5"),
        "reviews_count": 98,
        "in_stock": True,
        "stock_quantity": 180,
        "unit": "кг",
    },
    {
        "name": "Морковь",
        "slug": "carrots",
        "description": "Сладкая морковь. Богата бета-каротином.",
        "price": Decimal("59.90"),
        "old_price": Decimal("79.90"),
        "image": "https://via.placeholder.com/300x300?text=Carrots",
        "category_slug": "vegetables-fruits",
        "rating": Decimal("4.7"),
        "reviews_count": 112,
        "in_stock": True,
        "stock_quantity": 300,
        "unit": "кг",
    },
    # Молочные продукты
    {
        "name": "Молоко 3.2%",
        "slug": "milk-3-2",
        "description": "Свежее пастеризованное молоко. Срок годности 5 дней.",
        "price": Decimal("79.90"),
        "image": "https://via.placeholder.com/300x300?text=Milk",
        "category_slug": "dairy",
        "rating": Decimal("4.8"),
        "reviews_count": 245,
        "in_stock": True,
        "stock_quantity": 150,
        "unit": "л",
    },
    {
        "name": "Творог 9%",
        "slug": "cottage-cheese-9",
        "description": "Натуральный творог. Без добавок и консервантов.",
        "price": Decimal("129.90"),
        "old_price": Decimal("159.90"),
        "image": "https://via.placeholder.com/300x300?text=Cottage+Cheese",
        "category_slug": "dairy",
        "rating": Decimal("4.9"),
        "reviews_count": 189,
        "in_stock": True,
        "stock_quantity": 100,
        "unit": "кг",
    },
    {
        "name": "Сметана 20%",
        "slug": "sour-cream-20",
        "description": "Густая сметана. Отлично подходит для заправки салатов.",
        "price": Decimal("99.90"),
        "image": "https://via.placeholder.com/300x300?text=Sour+Cream",
        "category_slug": "dairy",
        "rating": Decimal("4.7"),
        "reviews_count": 156,
        "in_stock": True,
        "stock_quantity": 120,
        "unit": "кг",
    },
    # Мясо и птица
    {
        "name": "Куриная грудка",
        "slug": "chicken-breast",
        "description": "Охлажденная куриная грудка. Без кожи и костей.",
        "price": Decimal("299.90"),
        "image": "https://via.placeholder.com/300x300?text=Chicken+Breast",
        "category_slug": "meat",
        "rating": Decimal("4.8"),
        "reviews_count": 167,
        "in_stock": True,
        "stock_quantity": 80,
        "unit": "кг",
    },
    {
        "name": "Говядина",
        "slug": "beef",
        "description": "Охлажденная говядина. Мраморная, для стейков.",
        "price": Decimal("599.90"),
        "old_price": Decimal("699.90"),
        "image": "https://via.placeholder.com/300x300?text=Beef",
        "category_slug": "meat",
        "rating": Decimal("4.9"),
        "reviews_count": 134,
        "in_stock": True,
        "stock_quantity": 50,
        "unit": "кг",
    },
    # Хлеб и выпечка
    {
        "name": "Хлеб белый",
        "slug": "white-bread",
        "description": "Свежий белый хлеб. Выпечка сегодня.",
        "price": Decimal("39.90"),
        "image": "https://via.placeholder.com/300x300?text=White+Bread",
        "category_slug": "ready-food",
        "rating": Decimal("4.6"),
        "reviews_count": 234,
        "in_stock": True,
        "stock_quantity": 200,
        "unit": "шт",
    },
    {
        "name": "Круассан",
        "slug": "croissant",
        "description": "Французский круассан. Слоеное тесто с маслом.",
        "price": Decimal("59.90"),
        "old_price": Decimal("79.90"),
        "image": "https://via.placeholder.com/300x300?text=Croissant",
        "category_slug": "ready-food",
        "rating": Decimal("4.9"),
        "reviews_count": 178,
        "in_stock": True,
        "stock_quantity": 150,
        "unit": "шт",
    },
    # Напитки
    {
        "name": "Сок апельсиновый",
        "slug": "orange-juice",
        "description": "100% натуральный апельсиновый сок. Без сахара.",
        "price": Decimal("149.90"),
        "image": "https://via.placeholder.com/300x300?text=Orange+Juice",
        "category_slug": "ready-food",
        "rating": Decimal("4.8"),
        "reviews_count": 156,
        "in_stock": True,
        "stock_quantity": 100,
        "unit": "л",
    },
    {
        "name": "Вода минеральная",
        "slug": "mineral-water",
        "description": "Газированная минеральная вода. Источник природных минералов.",
        "price": Decimal("49.90"),
        "image": "https://via.placeholder.com/300x300?text=Mineral+Water",
        "category_slug": "ready-food",
        "rating": Decimal("4.7"),
        "reviews_count": 289,
        "in_stock": True,
        "stock_quantity": 300,
        "unit": "л",
    },
    # Мед
    {
        "name": "Мед цветочный",
        "slug": "flower-honey",
        "description": "Натуральный цветочный мед. Собран в экологически чистых районах.",
        "price": Decimal("599.90"),
        "old_price": Decimal("699.90"),
        "image": "https://via.placeholder.com/300x300?text=Honey",
        "category_slug": "honey",
        "rating": Decimal("4.9"),
        "reviews_count": 234,
        "in_stock": True,
        "stock_quantity": 80,
        "unit": "кг",
    },
    # Яйца
    {
        "name": "Яйца куриные С0",
        "slug": "chicken-eggs-c0",
        "description": "Свежие куриные яйца категории С0. От домашних кур.",
        "price": Decimal("89.90"),
        "image": "https://via.placeholder.com/300x300?text=Eggs",
        "category_slug": "eggs",
        "rating": Decimal("4.8"),
        "reviews_count": 167,
        "in_stock": True,
        "stock_quantity": 200,
        "unit": "десяток",
    },
    # Саженцы и семена
    {
        "name": "Семена томатов",
        "slug": "tomato-seeds",
        "description": "Семена томатов сорта 'Бычье сердце'. Высокая урожайность.",
        "price": Decimal("49.90"),
        "image": "https://via.placeholder.com/300x300?text=Seeds",
        "category_slug": "seedlings",
        "rating": Decimal("4.7"),
        "reviews_count": 89,
        "in_stock": True,
        "stock_quantity": 150,
        "unit": "пакет",
    },
    {
        "name": "Саженцы яблони",
        "slug": "apple-seedlings",
        "description": "Саженцы яблони сорта 'Антоновка'. 2-летние.",
        "price": Decimal("399.90"),
        "old_price": Decimal("499.90"),
        "image": "https://via.placeholder.com/300x300?text=Seedlings",
        "category_slug": "seedlings",
        "rating": Decimal("4.9"),
        "reviews_count": 56,
        "in_stock": True,
        "stock_quantity": 50,
        "unit": "шт",
    },
    # Агротовары и удобрения
    {
        "name": "Удобрение органическое",
        "slug": "organic-fertilizer",
        "description": "Органическое удобрение для овощей и фруктов. Экологически чистое.",
        "price": Decimal("299.90"),
        "image": "https://via.placeholder.com/300x300?text=Fertilizer",
        "category_slug": "agro",
        "rating": Decimal("4.6"),
        "reviews_count": 78,
        "in_stock": True,
        "stock_quantity": 100,
        "unit": "кг",
    },
    # Корма и добавки
    {
        "name": "Комбикорм для кур",
        "slug": "chicken-feed",
        "description": "Сбалансированный комбикорм для кур-несушек.",
        "price": Decimal("899.90"),
        "image": "https://via.placeholder.com/300x300?text=Feed",
        "category_slug": "feed",
        "rating": Decimal("4.7"),
        "reviews_count": 123,
        "in_stock": True,
        "stock_quantity": 200,
        "unit": "мешок 25кг",
    },
    # Зерно
    {
        "name": "Пшеница продовольственная",
        "slug": "wheat",
        "description": "Пшеница 3 класса. Для производства муки и круп.",
        "price": Decimal("15.90"),
        "image": "https://via.placeholder.com/300x300?text=Wheat",
        "category_slug": "grain",
        "rating": Decimal("4.5"),
        "reviews_count": 45,
        "in_stock": True,
        "stock_quantity": 1000,
        "unit": "кг",
    },
]


# Магазины (с координатами Москвы)
STORES = [
    {
        "name": "Еду на базар - Центр",
        "address": "г. Москва, ул. Тверская, д. 10",
        "phone": "+7 (495) 123-45-67",
        "email": "center@edu-na-bazar.ru",
        "working_hours": "8:00 - 23:00",
        "description": "Наш главный магазин в центре Москвы",
        "latitude": 55.7558,
        "longitude": 37.6173,
        "is_active": "true",
    },
    {
        "name": "Еду на базар - Юго-Запад",
        "address": "г. Москва, ул. Профсоюзная, д. 45",
        "phone": "+7 (495) 234-56-78",
        "email": "southwest@edu-na-bazar.ru",
        "working_hours": "9:00 - 22:00",
        "description": "Магазин в спальном районе",
        "latitude": 55.6617,
        "longitude": 37.5167,
        "is_active": "true",
    },
    {
        "name": "Еду на базар - Север",
        "address": "г. Москва, Дмитровское шоссе, д. 89",
        "phone": "+7 (495) 345-67-89",
        "email": "north@edu-na-bazar.ru",
        "working_hours": "8:00 - 22:00",
        "description": "Магазин на севере Москвы",
        "latitude": 55.8719,
        "longitude": 37.6561,
        "is_active": "true",
    },
]


async def seed_database():
    """Заполнить БД тестовыми данными"""
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        print("🌱 Начинаем заполнение БД тестовыми данными...\n")
        
        # 1. Создаем категории
        print("📁 Создаем категории...")
        categories_map = {}
        for cat_data in CATEGORIES:
            category = Category(**cat_data)
            session.add(category)
            await session.flush()
            categories_map[cat_data["slug"]] = category.id
            print(f"  ✅ {cat_data['name']}")
        
        await session.commit()
        print(f"\n✅ Создано {len(CATEGORIES)} категорий\n")
        
        # 2. Создаем товары
        print("🛒 Создаем товары...")
        for prod_data in PRODUCTS:
            category_slug = prod_data.pop("category_slug")
            category_id = categories_map[category_slug]
            
            product = Product(
                **prod_data,
                category_id=category_id
            )
            session.add(product)
            print(f"  ✅ {prod_data['name']}")
        
        await session.commit()
        print(f"\n✅ Создано {len(PRODUCTS)} товаров\n")
        
        # 3. Создаем магазины
        print("🏪 Создаем магазины...")
        for store_data in STORES:
            lat = store_data.pop("latitude")
            lon = store_data.pop("longitude")
            
            # Создаем POINT из координат
            point_wkt = f"POINT({lon} {lat})"
            
            store = Store(
                **store_data,
                location=WKTElement(point_wkt, srid=4326)
            )
            session.add(store)
            print(f"  ✅ {store_data['name']}")
        
        await session.commit()
        print(f"\n✅ Создано {len(STORES)} магазинов\n")
        
        print("🎉 Заполнение БД завершено успешно!")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_database())
