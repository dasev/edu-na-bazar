"""
Проверка изображений - синхронная версия
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

print("="*80)
print("🖼️ ПРОВЕРКА ИЗОБРАЖЕНИЙ")
print("="*80)

# Проверяем temp.file
print("\n📁 temp.file - примеры:")
cur.execute("""
    SELECT id, filename, path, type, advert_id 
    FROM temp.file 
    LIMIT 5
""")

for row in cur.fetchall():
    print(f"   ID: {row[0]}, Filename: {row[1]}, Path: {row[2]}, Type: {row[3]}, Advert: {row[4]}")

# Статистика
print("\n📊 Статистика temp.file:")
cur.execute("SELECT COUNT(*) FROM temp.file")
total = cur.fetchone()[0]
print(f"   Всего записей: {total}")

cur.execute("SELECT COUNT(*) FROM temp.file WHERE type = 'image'")
images = cur.fetchone()[0]
print(f"   Изображений: {images}")

# Проверяем market.products
print("\n📦 market.products - изображения:")
cur.execute("""
    SELECT id, name, image 
    FROM market.products 
    WHERE image IS NOT NULL 
    LIMIT 5
""")

for row in cur.fetchall():
    print(f"   ID: {row[0]}, Name: {row[1]}, Image: {row[2]}")

# Проверяем market.product_images
print("\n🖼️ market.product_images:")
cur.execute("SELECT COUNT(*) FROM market.product_images")
count = cur.fetchone()[0]
print(f"   Всего записей: {count}")

if count > 0:
    cur.execute("SELECT id, product_id, image_url FROM market.product_images LIMIT 5")
    for row in cur.fetchall():
        print(f"   ID: {row[0]}, Product: {row[1]}, URL: {row[2]}")

cur.close()
conn.close()

print("\n✅ Готово!")
