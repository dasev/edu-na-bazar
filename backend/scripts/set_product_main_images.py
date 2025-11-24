"""
Установка главного изображения для товаров из product_images
"""
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="edu_na_bazar",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

print("🖼️ Установка главных изображений для товаров...\n")

# Обновляем поле image в products первым изображением из product_images
# Убираем условие (p.image IS NULL OR p.image = '') чтобы обновить ВСЕ товары
update_query = """
UPDATE market.products p
SET image = pi.image_url
FROM (
    SELECT DISTINCT ON (product_id) 
        product_id, 
        image_url
    FROM market.product_images
    WHERE image_url IS NOT NULL
    ORDER BY product_id, id
) pi
WHERE p.id = pi.product_id
"""

cur.execute(update_query)
updated = cur.rowcount
conn.commit()

print(f"✅ Обновлено товаров: {updated}")

# Проверяем результат
cur.execute("""
    SELECT COUNT(*) 
    FROM market.products 
    WHERE image IS NOT NULL AND image != ''
""")
with_images = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM market.products")
total = cur.fetchone()[0]

print(f"📊 Товаров с изображениями: {with_images} из {total}")

# Показываем примеры
print("\n📋 Примеры товаров с изображениями:")
cur.execute("""
    SELECT id, name, image 
    FROM market.products 
    WHERE image IS NOT NULL AND image != ''
    LIMIT 5
""")

for row in cur.fetchall():
    print(f"   {row[0]}: {row[1][:50]}...")
    print(f"      {row[2]}")

cur.close()
conn.close()

print("\n✅ Готово!")
