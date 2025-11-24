"""
Проверка связи товаров и изображений
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

print("🔍 Анализ связи товаров и изображений:\n")

# Сколько уникальных товаров в product_images
cur.execute("""
    SELECT COUNT(DISTINCT product_id) 
    FROM market.product_images
""")
unique_products = cur.fetchone()[0]
print(f"📊 Уникальных товаров в product_images: {unique_products}")

# Сколько всего товаров
cur.execute("SELECT COUNT(*) FROM market.products")
total_products = cur.fetchone()[0]
print(f"📊 Всего товаров в products: {total_products}")

# Проверяем диапазон ID товаров
cur.execute("SELECT MIN(id), MAX(id) FROM market.products")
min_id, max_id = cur.fetchone()
print(f"📊 Диапазон ID товаров: {min_id} - {max_id}")

# Проверяем диапазон product_id в product_images
cur.execute("SELECT MIN(product_id), MAX(product_id) FROM market.product_images")
min_pid, max_pid = cur.fetchone()
print(f"📊 Диапазон product_id в images: {min_pid} - {max_pid}")

# Проверяем есть ли товары с этими ID
cur.execute("""
    SELECT COUNT(*) 
    FROM market.products 
    WHERE id BETWEEN %s AND %s
""", (min_pid, max_pid))
products_in_range = cur.fetchone()[0]
print(f"📊 Товаров в диапазоне {min_pid}-{max_pid}: {products_in_range}")

# Проверяем сколько изображений не привязаны к существующим товарам
cur.execute("""
    SELECT COUNT(*) 
    FROM market.product_images pi
    LEFT JOIN market.products p ON pi.product_id = p.id
    WHERE p.id IS NULL
""")
orphaned = cur.fetchone()[0]
print(f"⚠️  Изображений без товаров: {orphaned}")

cur.close()
conn.close()
