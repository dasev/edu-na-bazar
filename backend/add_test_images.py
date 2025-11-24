"""
Добавление тестовых изображений для демонстрации галереи
"""
import psycopg2

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
    print("📸 Добавление дополнительных изображений товарам...")
    
    # Получаем товары с изображениями
    cur.execute("""
        SELECT id, image 
        FROM market.products 
        WHERE image IS NOT NULL 
        LIMIT 10
    """)
    products = cur.fetchall()
    
    added = 0
    for product_id, main_image in products:
        # Добавляем 2-3 дополнительных изображения (копии основного для теста)
        for i in range(2, 4):
            cur.execute("""
                INSERT INTO market.product_images (product_id, image_url, is_primary, sort_order, created_at)
                VALUES (%s, %s, false, %s, NOW())
                ON CONFLICT DO NOTHING
            """, (product_id, main_image, i))
            added += 1
    
    conn.commit()
    print(f"✅ Добавлено {added} дополнительных изображений")
    print("🎉 Готово!")
    
except Exception as e:
    conn.rollback()
    print(f"❌ Ошибка: {e}")
    raise
finally:
    cur.close()
    conn.close()
