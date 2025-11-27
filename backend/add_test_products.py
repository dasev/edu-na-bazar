"""
Скрипт для добавления тестовых товаров во все категории с фотографиями
"""
import asyncio
import random
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models.product import Product
from models.category import Category
from models.store_owner import StoreOwner
import os
import requests
from pathlib import Path

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar"

# Создаем движок
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Тестовые товары по категориям
PRODUCTS_BY_CATEGORY = {
    "Овощи": [
        {"name": "Помидоры свежие", "price": 150, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1546094096-0df4bcaaa337?w=800"},
        {"name": "Огурцы парниковые", "price": 120, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1604977042946-1eecc30f269e?w=800"},
        {"name": "Картофель молодой", "price": 80, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=800"},
        {"name": "Морковь отборная", "price": 70, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=800"},
        {"name": "Свекла столовая", "price": 60, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1590165482129-1b8b27698780?w=800"},
        {"name": "Капуста белокочанная", "price": 50, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?w=800"},
        {"name": "Перец болгарский", "price": 200, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=800"},
        {"name": "Баклажаны", "price": 180, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1659261200833-ec8761558af7?w=800"},
        {"name": "Кабачки", "price": 90, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1597362925123-77861d3fbac7?w=800"},
        {"name": "Лук репчатый", "price": 40, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?w=800"},
    ],
    "Фрукты": [
        {"name": "Яблоки Гала", "price": 180, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=800"},
        {"name": "Бананы", "price": 120, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1603833665858-e61d17a86224?w=800"},
        {"name": "Апельсины", "price": 150, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1547514701-42782101795e?w=800"},
        {"name": "Груши Конференция", "price": 200, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1568909344668-6f14a07b56a0?w=800"},
        {"name": "Виноград кишмиш", "price": 250, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1599819177626-c0d9c3a39b3e?w=800"},
        {"name": "Мандарины", "price": 160, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?w=800"},
        {"name": "Киви", "price": 220, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1585059895524-72359e06133a?w=800"},
        {"name": "Персики", "price": 280, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1629828874514-944d8c50f5ac?w=800"},
        {"name": "Сливы", "price": 190, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1629828874514-944d8c50f5ac?w=800"},
        {"name": "Гранаты", "price": 300, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=800"},
    ],
    "Молочные продукты": [
        {"name": "Молоко 3.2%", "price": 85, "unit": "л", "image_url": "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=800"},
        {"name": "Кефир 2.5%", "price": 80, "unit": "л", "image_url": "https://images.unsplash.com/photo-1623065422902-30a2d299bbe4?w=800"},
        {"name": "Творог 9%", "price": 150, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1628088062854-d1870b4553da?w=800"},
        {"name": "Сметана 20%", "price": 120, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1628088062854-d1870b4553da?w=800"},
        {"name": "Сыр Российский", "price": 450, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=800"},
        {"name": "Масло сливочное 82%", "price": 600, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=800"},
        {"name": "Йогурт натуральный", "price": 95, "unit": "л", "image_url": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=800"},
        {"name": "Ряженка 4%", "price": 75, "unit": "л", "image_url": "https://images.unsplash.com/photo-1623065422902-30a2d299bbe4?w=800"},
        {"name": "Сливки 33%", "price": 180, "unit": "л", "image_url": "https://images.unsplash.com/photo-1628088062854-d1870b4553da?w=800"},
        {"name": "Сырок глазированный", "price": 45, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1571212515416-fca2ce42c9f5?w=800"},
    ],
    "Мясо и птица": [
        {"name": "Куриная грудка", "price": 380, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=800"},
        {"name": "Свинина вырезка", "price": 550, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=800"},
        {"name": "Говядина мраморная", "price": 750, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1603048588665-791ca8aea617?w=800"},
        {"name": "Фарш говяжий", "price": 420, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1603048588665-791ca8aea617?w=800"},
        {"name": "Куриные окорочка", "price": 220, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1587593810167-a84920ea0781?w=800"},
        {"name": "Индейка филе", "price": 480, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=800"},
        {"name": "Колбаса докторская", "price": 350, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1599894380345-d8c0c9e4c5a5?w=800"},
        {"name": "Сосиски молочные", "price": 280, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1612741214270-c0e5c9f8b9d5?w=800"},
        {"name": "Бекон", "price": 520, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1528607929212-2636ec44253e?w=800"},
        {"name": "Крылышки куриные", "price": 250, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1562967916-ca8ed48f87ea?w=800"},
    ],
    "Хлеб и выпечка": [
        {"name": "Хлеб белый", "price": 45, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800"},
        {"name": "Хлеб черный", "price": 50, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1586444248902-2f64eddc13df?w=800"},
        {"name": "Батон нарезной", "price": 40, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?w=800"},
        {"name": "Булочки с маком", "price": 60, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=800"},
        {"name": "Круассаны", "price": 120, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=800"},
        {"name": "Пирожки с капустой", "price": 35, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1608198093002-ad4e005484ec?w=800"},
        {"name": "Торт Наполеон", "price": 450, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1464349095431-e9a21285b5f3?w=800"},
        {"name": "Печенье овсяное", "price": 180, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=800"},
        {"name": "Пряники", "price": 150, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=800"},
        {"name": "Слойки с повидлом", "price": 90, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1509365465985-25d11c17e812?w=800"},
    ],
}

async def download_image(url: str, product_name: str) -> str:
    """Скачать изображение и сохранить локально"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # Создаем директорию если не существует
            upload_dir = Path("backend/uploads/products")
            upload_dir.mkdir(parents=True, exist_ok=True)
            
            # Генерируем имя файла
            import uuid
            filename = f"{uuid.uuid4()}.jpg"
            filepath = upload_dir / filename
            
            # Сохраняем файл
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Скачано изображение для {product_name}: {filename}")
            return f"/uploads/products/{filename}"
        else:
            print(f"❌ Ошибка скачивания для {product_name}: {response.status_code}")
            return ""
    except Exception as e:
        print(f"❌ Ошибка скачивания для {product_name}: {e}")
        return ""

async def add_test_products():
    """Добавить тестовые товары во все категории"""
    async with async_session() as session:
        # Получаем все категории
        result = await session.execute(select(Category))
        categories = result.scalars().all()
        
        # Получаем первый магазин
        result = await session.execute(select(StoreOwner).limit(1))
        store = result.scalar_one_or_none()
        
        if not store:
            print("❌ Нет магазинов в базе данных")
            return
        
        print(f"📦 Добавляем товары в магазин: {store.name}")
        
        added_count = 0
        
        for category in categories:
            print(f"\n📁 Категория: {category.name}")
            
            # Получаем товары для этой категории
            products_data = PRODUCTS_BY_CATEGORY.get(category.name, [])
            
            if not products_data:
                print(f"⚠️ Нет тестовых данных для категории {category.name}")
                continue
            
            for product_data in products_data:
                # Скачиваем изображение
                image_path = await download_image(product_data["image_url"], product_data["name"])
                
                # Создаем товар
                product = Product(
                    store_id=store.id,
                    name=product_data["name"],
                    description=f"Качественный товар - {product_data['name']}. Всегда свежий и по доступной цене!",
                    price=product_data["price"],
                    old_price=int(product_data["price"] * 1.2),  # Старая цена на 20% выше
                    category_id=category.id,
                    in_stock=True,
                    stock_quantity=random.randint(50, 200),
                    unit=product_data["unit"],
                    images=[image_path] if image_path else [],
                    status="active"
                )
                
                session.add(product)
                added_count += 1
                print(f"  ✅ Добавлен: {product_data['name']}")
        
        await session.commit()
        print(f"\n🎉 Всего добавлено товаров: {added_count}")

if __name__ == "__main__":
    print("🚀 Запуск скрипта добавления тестовых товаров...")
    asyncio.run(add_test_products())
    print("✅ Готово!")
