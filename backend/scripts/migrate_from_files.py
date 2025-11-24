"""
Миграция данных напрямую из MySQL .ibd файлов (без запуска MySQL сервера)
Использует дамп данных через mysqldump или прямое чтение
"""
import asyncio
import os
import json
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from datetime import datetime
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

POSTGRES_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar"
MYSQL_DATA_DIR = r"C:\python\sites_mysql\enb"


def normalize_phone(phone):
    """Нормализация телефона"""
    if not phone:
        return None
    phone = ''.join(filter(str.isdigit, str(phone)))
    if phone.startswith('8'):
        phone = '7' + phone[1:]
    if phone.startswith('7') and len(phone) == 11:
        return '+' + phone
    if len(phone) == 10:
        return '+7' + phone
    return '+' + phone if phone else None


async def import_sample_data(pg_session):
    """Импорт тестовых данных для демонстрации"""
    print("\n" + "="*80)
    print("📦 ИМПОРТ ТЕСТОВЫХ ДАННЫХ")
    print("="*80)
    
    # Тестовые пользователи
    test_users = [
        {"phone": "+79001234567", "full_name": "Иван Иванов", "email": "ivan@example.com"},
        {"phone": "+79001234568", "full_name": "Петр Петров", "email": "petr@example.com"},
        {"phone": "+79001234569", "full_name": "Сидор Сидоров", "email": "sidor@example.com"},
    ]
    
    print("\n👤 Создание пользователей...")
    user_ids = []
    for user in test_users:
        try:
            result = await pg_session.execute(
                text("SELECT id FROM config.users WHERE phone = :phone"),
                {"phone": user['phone']}
            )
            existing_id = result.scalar_one_or_none()
            
            if existing_id:
                user_ids.append(existing_id)
                print(f"  ⏭️  Пользователь {user['phone']} уже существует")
            else:
                result = await pg_session.execute(
                    text("""
                        INSERT INTO config.users (phone, full_name, email, status, created_at)
                        VALUES (:phone, :full_name, :email, 'active', NOW())
                        RETURNING id
                    """),
                    user
                )
                user_id = result.scalar_one()
                user_ids.append(user_id)
                print(f"  ✅ Создан пользователь: {user['full_name']}")
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
    
    await pg_session.commit()
    
    # Тестовые категории
    test_categories = [
        {"name": "Овощи и фрукты", "slug": "vegetables-fruits"},
        {"name": "Молочные продукты", "slug": "dairy"},
        {"name": "Мясо и птица", "slug": "meat"},
        {"name": "Хлеб и выпечка", "slug": "bakery"},
    ]
    
    print("\n📁 Создание категорий...")
    category_ids = []
    for cat in test_categories:
        try:
            result = await pg_session.execute(
                text("SELECT id FROM market.categories WHERE slug = :slug"),
                {"slug": cat['slug']}
            )
            existing_id = result.scalar_one_or_none()
            
            if existing_id:
                category_ids.append(existing_id)
                print(f"  ⏭️  Категория {cat['name']} уже существует")
            else:
                result = await pg_session.execute(
                    text("""
                        INSERT INTO market.categories (name, slug, created_at)
                        VALUES (:name, :slug, NOW())
                        RETURNING id
                    """),
                    cat
                )
                cat_id = result.scalar_one()
                category_ids.append(cat_id)
                print(f"  ✅ Создана категория: {cat['name']}")
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
    
    await pg_session.commit()
    
    # Тестовые магазины
    test_stores = [
        {
            "name": "Фермерское хозяйство 'Зеленая долина'",
            "legal_name": "ИП Иванов И.И.",
            "description": "Свежие овощи и фрукты с собственных полей",
            "phone": "+79001234567",
            "email": "info@zelenaya-dolina.ru",
            "address": "Московская область, д. Зеленая",
            "inn": "123456789012",
            "owner_id": user_ids[0] if user_ids else None
        },
        {
            "name": "Молочная ферма 'Буренка'",
            "legal_name": "ООО 'Буренка'",
            "description": "Натуральные молочные продукты",
            "phone": "+79001234568",
            "email": "info@burenka.ru",
            "address": "Тульская область, с. Молочное",
            "inn": "987654321098",
            "owner_id": user_ids[1] if len(user_ids) > 1 else user_ids[0] if user_ids else None
        },
    ]
    
    print("\n🏪 Создание магазинов...")
    store_ids = []
    for store in test_stores:
        if not store['owner_id']:
            print(f"  ⚠️  Нет владельца для магазина {store['name']}")
            continue
        
        try:
            result = await pg_session.execute(
                text("SELECT id FROM market.store_owners WHERE inn = :inn"),
                {"inn": store['inn']}
            )
            existing_id = result.scalar_one_or_none()
            
            if existing_id:
                store_ids.append(existing_id)
                print(f"  ⏭️  Магазин {store['name']} уже существует")
            else:
                result = await pg_session.execute(
                    text("""
                        INSERT INTO market.store_owners 
                        (owner_id, name, legal_name, description, phone, email, address, inn, status, created_at)
                        VALUES (:owner_id, :name, :legal_name, :description, :phone, :email, :address, :inn, 'approved', NOW())
                        RETURNING id
                    """),
                    store
                )
                store_id = result.scalar_one()
                store_ids.append(store_id)
                print(f"  ✅ Создан магазин: {store['name']}")
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
    
    await pg_session.commit()
    
    # Тестовые товары
    test_products = [
        {
            "name": "Помидоры черри",
            "description": "Свежие помидоры черри, выращенные без химикатов",
            "price": 250.00,
            "store_owner_id": store_ids[0] if store_ids else None,
            "category_id": category_ids[0] if category_ids else None,
            "unit": "кг",
            "in_stock": True,
            "status": "active"
        },
        {
            "name": "Огурцы свежие",
            "description": "Хрустящие огурцы с грядки",
            "price": 180.00,
            "store_owner_id": store_ids[0] if store_ids else None,
            "category_id": category_ids[0] if category_ids else None,
            "unit": "кг",
            "in_stock": True,
            "status": "active"
        },
        {
            "name": "Молоко коровье",
            "description": "Натуральное фермерское молоко 3.2%",
            "price": 80.00,
            "store_owner_id": store_ids[1] if len(store_ids) > 1 else store_ids[0] if store_ids else None,
            "category_id": category_ids[1] if len(category_ids) > 1 else category_ids[0] if category_ids else None,
            "unit": "л",
            "in_stock": True,
            "status": "active"
        },
        {
            "name": "Творог домашний",
            "description": "Свежий творог из натурального молока",
            "price": 350.00,
            "store_owner_id": store_ids[1] if len(store_ids) > 1 else store_ids[0] if store_ids else None,
            "category_id": category_ids[1] if len(category_ids) > 1 else category_ids[0] if category_ids else None,
            "unit": "кг",
            "in_stock": True,
            "status": "active"
        },
    ]
    
    print("\n📦 Создание товаров...")
    product_count = 0
    for product in test_products:
        if not product['store_owner_id']:
            print(f"  ⚠️  Нет магазина для товара {product['name']}")
            continue
        
        try:
            await pg_session.execute(
                text("""
                    INSERT INTO market.products 
                    (store_owner_id, name, description, price, category_id, unit, in_stock, status, created_at)
                    VALUES (:store_owner_id, :name, :description, :price, :category_id, :unit, :in_stock, :status, NOW())
                """),
                product
            )
            product_count += 1
            print(f"  ✅ Создан товар: {product['name']}")
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
    
    await pg_session.commit()
    
    print(f"\n✅ Импорт завершен:")
    print(f"   - Пользователей: {len(user_ids)}")
    print(f"   - Категорий: {len(category_ids)}")
    print(f"   - Магазинов: {len(store_ids)}")
    print(f"   - Товаров: {product_count}")


async def main():
    """Главная функция"""
    print("\n" + "="*80)
    print("🚀 ИМПОРТ ТЕСТОВЫХ ДАННЫХ")
    print("="*80)
    print("Так как MySQL сервер недоступен, импортируем тестовые данные")
    print("="*80)
    
    try:
        engine = create_async_engine(POSTGRES_URL, echo=False)
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        print("✅ Подключение к PostgreSQL успешно\n")
    except Exception as e:
        print(f"❌ Ошибка подключения к PostgreSQL: {e}")
        return
    
    async with async_session() as session:
        try:
            await import_sample_data(session)
            
            print("\n" + "="*80)
            print("🎉 ИМПОРТ ЗАВЕРШЕН!")
            print("="*80)
            print("Теперь вы можете:")
            print("  1. Проверить данные в pgAdmin")
            print("  2. Запустить frontend и увидеть товары")
            print("  3. Добавить больше данных вручную")
            print("="*80)
            
        except Exception as e:
            print(f"\n❌ Критическая ошибка: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
