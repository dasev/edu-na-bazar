"""
Скрипт миграции данных из старой MySQL базы (enb) в новую PostgreSQL базу
"""
import asyncio
import pymysql
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from datetime import datetime
import sys
import os

# Добавляем путь к backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Настройки подключения
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Пустой пароль
    'database': 'enb',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

POSTGRES_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar"


def normalize_phone(phone):
    """Нормализация телефона к формату +7XXXXXXXXXX"""
    if not phone:
        return None
    # Убираем все кроме цифр
    phone = ''.join(filter(str.isdigit, str(phone)))
    # Если начинается с 8, заменяем на 7
    if phone.startswith('8'):
        phone = '7' + phone[1:]
    # Если начинается с 7 и длина 11
    if phone.startswith('7') and len(phone) == 11:
        return '+' + phone
    # Если длина 10, добавляем +7
    if len(phone) == 10:
        return '+7' + phone
    return '+' + phone if phone else None


async def migrate_users(mysql_conn, pg_session):
    """Миграция пользователей"""
    print("\n" + "="*80)
    print("👤 МИГРАЦИЯ ПОЛЬЗОВАТЕЛЕЙ")
    print("="*80)
    
    with mysql_conn.cursor() as cursor:
        cursor.execute("""
            SELECT 
                id,
                username,
                email,
                phone,
                created_at,
                updated_at,
                status
            FROM user
            WHERE status = 10
            ORDER BY id
        """)
        users = cursor.fetchall()
        
        print(f"📊 Найдено {len(users)} активных пользователей")
        
        migrated = 0
        skipped = 0
        errors = 0
        
        for user in users:
            try:
                phone = normalize_phone(user['phone'])
                if not phone:
                    phone = f"+7900{user['id']:07d}"  # Генерируем фейковый телефон
                
                # Проверяем есть ли уже такой пользователь
                result = await pg_session.execute(
                    text("SELECT id FROM config.users WHERE phone = :phone"),
                    {"phone": phone}
                )
                if result.scalar_one_or_none():
                    print(f"⏭️  Пользователь {phone} уже существует")
                    skipped += 1
                    continue
                
                # Вставляем пользователя
                await pg_session.execute(
                    text("""
                        INSERT INTO config.users 
                        (phone, full_name, email, status, created_at, updated_at)
                        VALUES (:phone, :full_name, :email, :status, :created_at, :updated_at)
                    """),
                    {
                        "phone": phone,
                        "full_name": user['username'] or f"Пользователь {user['id']}",
                        "email": user['email'],
                        "status": 'active',
                        "created_at": user['created_at'] or datetime.now(),
                        "updated_at": user['updated_at'] or datetime.now()
                    }
                )
                migrated += 1
                if migrated % 100 == 0:
                    print(f"  ✅ Мигрировано {migrated} пользователей...")
                
            except Exception as e:
                print(f"❌ Ошибка при миграции пользователя {user['id']}: {e}")
                errors += 1
        
        await pg_session.commit()
        print(f"\n✅ Миграция пользователей завершена:")
        print(f"   - Мигрировано: {migrated}")
        print(f"   - Пропущено: {skipped}")
        print(f"   - Ошибок: {errors}")
        
        return migrated


async def migrate_categories(mysql_conn, pg_session):
    """Миграция категорий"""
    print("\n" + "="*80)
    print("📁 МИГРАЦИЯ КАТЕГОРИЙ")
    print("="*80)
    
    with mysql_conn.cursor() as cursor:
        cursor.execute("""
            SELECT 
                id,
                name,
                slug,
                parent_id,
                image
            FROM categories
            ORDER BY id
        """)
        categories = cursor.fetchall()
        
        print(f"📊 Найдено {len(categories)} категорий")
        
        migrated = 0
        skipped = 0
        
        for cat in categories:
            try:
                # Проверяем есть ли уже такая категория
                result = await pg_session.execute(
                    text("SELECT id FROM market.categories WHERE slug = :slug"),
                    {"slug": cat['slug']}
                )
                if result.scalar_one_or_none():
                    print(f"⏭️  Категория {cat['slug']} уже существует")
                    skipped += 1
                    continue
                
                # Вставляем категорию
                await pg_session.execute(
                    text("""
                        INSERT INTO market.categories 
                        (name, slug, image, parent_id)
                        VALUES (:name, :slug, :image, :parent_id)
                    """),
                    {
                        "name": cat['name'],
                        "slug": cat['slug'],
                        "image": cat['image'],
                        "parent_id": cat['parent_id']
                    }
                )
                migrated += 1
                
            except Exception as e:
                print(f"❌ Ошибка при миграции категории {cat['id']}: {e}")
        
        await pg_session.commit()
        print(f"\n✅ Миграция категорий завершена:")
        print(f"   - Мигрировано: {migrated}")
        print(f"   - Пропущено: {skipped}")
        
        return migrated


async def migrate_companies(mysql_conn, pg_session):
    """Миграция компаний (магазинов)"""
    print("\n" + "="*80)
    print("🏪 МИГРАЦИЯ МАГАЗИНОВ")
    print("="*80)
    
    with mysql_conn.cursor() as cursor:
        cursor.execute("""
            SELECT 
                c.id,
                c.name,
                c.description,
                c.user_id,
                c.phone,
                c.email,
                c.address,
                c.logo,
                c.created_at,
                c.updated_at,
                c.status
            FROM companies c
            WHERE c.status = 1
            ORDER BY c.id
        """)
        companies = cursor.fetchall()
        
        print(f"📊 Найдено {len(companies)} активных магазинов")
        
        migrated = 0
        skipped = 0
        errors = 0
        
        for comp in companies:
            try:
                # Находим пользователя в новой базе
                phone = normalize_phone(comp.get('phone'))
                if not phone and comp['user_id']:
                    # Ищем по user_id из старой базы
                    cursor.execute("SELECT phone FROM user WHERE id = %s", (comp['user_id'],))
                    user_row = cursor.fetchone()
                    if user_row:
                        phone = normalize_phone(user_row['phone'])
                
                if not phone:
                    phone = f"+7900{comp['id']:07d}"
                
                result = await pg_session.execute(
                    text("SELECT id FROM config.users WHERE phone = :phone"),
                    {"phone": phone}
                )
                user_id = result.scalar_one_or_none()
                
                if not user_id:
                    print(f"⚠️  Пользователь не найден для магазина {comp['name']}, пропускаем")
                    skipped += 1
                    continue
                
                # Проверяем есть ли уже такой магазин
                result = await pg_session.execute(
                    text("SELECT id FROM market.store_owners WHERE name = :name AND owner_id = :owner_id"),
                    {"name": comp['name'], "owner_id": user_id}
                )
                if result.scalar_one_or_none():
                    print(f"⏭️  Магазин {comp['name']} уже существует")
                    skipped += 1
                    continue
                
                # Вставляем магазин
                await pg_session.execute(
                    text("""
                        INSERT INTO market.store_owners 
                        (owner_id, name, legal_name, description, phone, email, address, logo, 
                         inn, status, created_at, updated_at)
                        VALUES (:owner_id, :name, :legal_name, :description, :phone, :email, :address, :logo,
                                :inn, :status, :created_at, :updated_at)
                    """),
                    {
                        "owner_id": user_id,
                        "name": comp['name'],
                        "legal_name": comp['name'],  # Используем то же имя
                        "description": comp['description'],
                        "phone": comp['phone'],
                        "email": comp['email'],
                        "address": comp['address'] or 'Не указан',
                        "logo": comp['logo'],
                        "inn": f"{comp['id']:012d}",  # Генерируем ИНН из ID
                        "status": 'approved',
                        "created_at": comp['created_at'] or datetime.now(),
                        "updated_at": comp['updated_at'] or datetime.now()
                    }
                )
                migrated += 1
                if migrated % 50 == 0:
                    print(f"  ✅ Мигрировано {migrated} магазинов...")
                
            except Exception as e:
                print(f"❌ Ошибка при миграции магазина {comp['id']}: {e}")
                errors += 1
        
        await pg_session.commit()
        print(f"\n✅ Миграция магазинов завершена:")
        print(f"   - Мигрировано: {migrated}")
        print(f"   - Пропущено: {skipped}")
        print(f"   - Ошибок: {errors}")
        
        return migrated


async def migrate_products(mysql_conn, pg_session):
    """Миграция товаров (объявлений)"""
    print("\n" + "="*80)
    print("📦 МИГРАЦИЯ ТОВАРОВ")
    print("="*80)
    
    with mysql_conn.cursor() as cursor:
        cursor.execute("""
            SELECT 
                a.id,
                a.title as name,
                a.description,
                a.price,
                a.company_id,
                a.category_id,
                a.image,
                a.views,
                a.address as location,
                a.created_at,
                a.updated_at,
                a.status
            FROM advert a
            WHERE a.status = 1
            ORDER BY a.id
            LIMIT 1000
        """)
        products = cursor.fetchall()
        
        print(f"📊 Найдено {len(products)} активных товаров")
        
        migrated = 0
        skipped = 0
        errors = 0
        
        for prod in products:
            try:
                # Находим магазин в новой базе
                if not prod['company_id']:
                    skipped += 1
                    continue
                
                # Ищем компанию по старому ID
                cursor.execute("SELECT name FROM companies WHERE id = %s", (prod['company_id'],))
                comp_row = cursor.fetchone()
                if not comp_row:
                    skipped += 1
                    continue
                
                result = await pg_session.execute(
                    text("SELECT id FROM market.store_owners WHERE name = :name LIMIT 1"),
                    {"name": comp_row['name']}
                )
                store_id = result.scalar_one_or_none()
                
                if not store_id:
                    skipped += 1
                    continue
                
                # Вставляем товар
                await pg_session.execute(
                    text("""
                        INSERT INTO market.products 
                        (store_owner_id, name, description, price, image, category_id, 
                         views, location, status, in_stock, created_at, updated_at)
                        VALUES (:store_owner_id, :name, :description, :price, :image, :category_id,
                                :views, :location, :status, :in_stock, :created_at, :updated_at)
                    """),
                    {
                        "store_owner_id": store_id,
                        "name": prod['name'] or 'Без названия',
                        "description": prod['description'],
                        "price": float(prod['price']) if prod['price'] else 0,
                        "image": prod['image'],
                        "category_id": prod['category_id'],
                        "views": prod.get('views', 0) or 0,
                        "location": prod.get('location'),
                        "status": 'active',
                        "in_stock": True,
                        "created_at": prod['created_at'] or datetime.now(),
                        "updated_at": prod['updated_at'] or datetime.now()
                    }
                )
                migrated += 1
                if migrated % 100 == 0:
                    print(f"  ✅ Мигрировано {migrated} товаров...")
                
            except Exception as e:
                print(f"❌ Ошибка при миграции товара {prod['id']}: {e}")
                errors += 1
        
        await pg_session.commit()
        print(f"\n✅ Миграция товаров завершена:")
        print(f"   - Мигрировано: {migrated}")
        print(f"   - Пропущено: {skipped}")
        print(f"   - Ошибок: {errors}")
        
        return migrated


async def main():
    """Главная функция миграции"""
    print("\n" + "="*80)
    print("🚀 ЗАПУСК МИГРАЦИИ ДАННЫХ")
    print("="*80)
    print(f"MySQL: {MYSQL_CONFIG['host']}/{MYSQL_CONFIG['database']}")
    print(f"PostgreSQL: {POSTGRES_URL}")
    print("="*80)
    
    # Подключение к MySQL
    try:
        mysql_conn = pymysql.connect(**MYSQL_CONFIG)
        print("✅ Подключение к MySQL успешно")
    except Exception as e:
        print(f"❌ Ошибка подключения к MySQL: {e}")
        print("\n💡 Убедитесь что:")
        print("  1. MySQL сервер запущен")
        print("  2. База данных 'enb' существует")
        print("  3. Пароль root правильный")
        return
    
    # Подключение к PostgreSQL
    try:
        engine = create_async_engine(POSTGRES_URL, echo=False)
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        print("✅ Подключение к PostgreSQL успешно\n")
    except Exception as e:
        print(f"❌ Ошибка подключения к PostgreSQL: {e}")
        mysql_conn.close()
        return
    
    # Миграция
    async with async_session() as session:
        try:
            # 1. Пользователи
            users_count = await migrate_users(mysql_conn, session)
            
            # 2. Категории
            categories_count = await migrate_categories(mysql_conn, session)
            
            # 3. Магазины
            stores_count = await migrate_companies(mysql_conn, session)
            
            # 4. Товары
            products_count = await migrate_products(mysql_conn, session)
            
            # Итоги
            print("\n" + "="*80)
            print("🎉 МИГРАЦИЯ ЗАВЕРШЕНА!")
            print("="*80)
            print(f"👤 Пользователей: {users_count}")
            print(f"📁 Категорий: {categories_count}")
            print(f"🏪 Магазинов: {stores_count}")
            print(f"📦 Товаров: {products_count}")
            print("="*80)
            
        except Exception as e:
            print(f"\n❌ Критическая ошибка: {e}")
            import traceback
            traceback.print_exc()
        finally:
            mysql_conn.close()
            await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
