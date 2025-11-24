"""
Применение миграции геолокации и добавление координат товарам
"""
import psycopg2
import random

# Подключение к БД
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="edu_na_bazar",
    user="postgres",
    password="postgres"
)
conn.autocommit = False
cur = conn.cursor()

try:
    print("🚀 Применение миграции геолокации...")
    
    # Читаем и выполняем миграцию
    with open('migrations/versions/007_add_product_geolocation.sql', 'r', encoding='utf-8') as f:
        migration_sql = f.read()
        cur.execute(migration_sql)
    
    print("✅ Миграция применена")
    
    # Добавляем случайные координаты товарам в Москве
    print("\n📍 Добавление координат товарам...")
    
    # Центр Москвы: 55.7558, 37.6173
    # Радиус ~10км
    cur.execute("SELECT id FROM market.products WHERE latitude IS NULL LIMIT 1000")
    products = cur.fetchall()
    
    updated = 0
    for (product_id,) in products:
        # Случайные координаты в радиусе 10км от центра Москвы
        lat = 55.7558 + random.uniform(-0.1, 0.1)  # ~11км
        lng = 37.6173 + random.uniform(-0.15, 0.15)  # ~11км
        
        cur.execute("""
            UPDATE market.products 
            SET 
                latitude = %s,
                longitude = %s,
                geo_location = ST_SetSRID(ST_MakePoint(%s, %s), 4326)
            WHERE id = %s
        """, (lat, lng, lng, lat, product_id))
        
        updated += 1
        if updated % 100 == 0:
            print(f"  ✅ Обновлено {updated} товаров...")
    
    conn.commit()
    print(f"\n✅ Всего обновлено товаров: {updated}")
    print("🎉 Готово!")
    
except Exception as e:
    conn.rollback()
    print(f"❌ Ошибка: {e}")
    raise
finally:
    cur.close()
    conn.close()
