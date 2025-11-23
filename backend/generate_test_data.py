"""
Генерация тестовых данных в схемы config и market
"""
import psycopg2
from datetime import datetime

conn_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'edu_na_bazar',
    'user': 'postgres',
    'password': 'postgres'
}

print("📝 Генерация тестовых данных...")

try:
    conn = psycopg2.connect(**conn_params)
    conn.autocommit = True
    cur = conn.cursor()
    
    # Создаем тестового пользователя
    print("👤 Создаем пользователя...")
    cur.execute("""
        INSERT INTO config.users (email, phone, full_name, address, is_active, is_verified, created_at, updated_at)
        VALUES ('test@example.com', '+79991234567', 'Тестовый Пользователь', 'Москва, ул. Тестовая, д. 1', true, true, NOW(), NOW())
        ON CONFLICT (email) DO NOTHING
        RETURNING id
    """)
    result = cur.fetchone()
    if result:
        user_id = result[0]
        print(f"✅ Пользователь создан (ID: {user_id})")
    else:
        cur.execute("SELECT id FROM config.users WHERE email = 'test@example.com'")
        user_id = cur.fetchone()[0]
        print(f"✅ Пользователь уже существует (ID: {user_id})")
    
    # Создаем категории
    print("\n📁 Создаем категории...")
    categories = [
        ('Фрукты', 'Свежие фрукты'),
        ('Овощи', 'Свежие овощи'),
        ('Молочные продукты', 'Молоко, сыр, йогурты'),
        ('Мясо', 'Свежее мясо и птица'),
        ('Хлеб', 'Хлебобулочные изделия'),
    ]
    
    category_ids = []
    for name, desc in categories:
        cur.execute("""
            INSERT INTO market.categories (name, description, created_at, updated_at)
            VALUES (%s, %s, NOW(), NOW())
            ON CONFLICT (name) DO UPDATE SET description = EXCLUDED.description
            RETURNING id
        """, (name, desc))
        cat_id = cur.fetchone()[0]
        category_ids.append(cat_id)
        print(f"  ✅ {name} (ID: {cat_id})")
    
    # Создаем товары
    print("\n🛒 Создаем товары...")
    products = [
        ('Яблоки', 'Свежие яблоки Гренни Смит', 89.90, category_ids[0]),
        ('Бананы', 'Спелые бананы из Эквадора', 69.90, category_ids[0]),
        ('Апельсины', 'Сочные апельсины', 99.90, category_ids[0]),
        ('Помидоры', 'Свежие помидоры', 149.90, category_ids[1]),
        ('Огурцы', 'Хрустящие огурцы', 119.90, category_ids[1]),
        ('Молоко', 'Молоко 3.2%', 79.90, category_ids[2]),
        ('Сыр', 'Российский сыр', 399.90, category_ids[2]),
        ('Курица', 'Куриная грудка', 299.90, category_ids[3]),
        ('Хлеб', 'Белый хлеб', 45.90, category_ids[4]),
        ('Батон', 'Нарезной батон', 39.90, category_ids[4]),
    ]
    
    for name, desc, price, cat_id in products:
        cur.execute("""
            INSERT INTO market.products (name, description, price, category_id, in_stock, created_at, updated_at)
            VALUES (%s, %s, %s, %s, true, NOW(), NOW())
            RETURNING id
        """, (name, desc, price, cat_id))
        prod_id = cur.fetchone()[0]
        print(f"  ✅ {name} - {price}₽ (ID: {prod_id})")
    
    # Статистика
    print("\n📊 Статистика:")
    cur.execute("SELECT COUNT(*) FROM config.users")
    print(f"  👤 Пользователей: {cur.fetchone()[0]}")
    
    cur.execute("SELECT COUNT(*) FROM market.categories")
    print(f"  📁 Категорий: {cur.fetchone()[0]}")
    
    cur.execute("SELECT COUNT(*) FROM market.products")
    print(f"  🛒 Товаров: {cur.fetchone()[0]}")
    
    cur.close()
    conn.close()
    
    print("\n✅ Готово! Тестовые данные созданы!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
