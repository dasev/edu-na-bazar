"""
Проверка что возвращает API для товаров
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

print("📦 Проверка товаров с изображениями:\n")

cur.execute("""
    SELECT id, name, image, price
    FROM market.products 
    WHERE image IS NOT NULL AND image != ''
    LIMIT 10
""")

for row in cur.fetchall():
    print(f"ID: {row[0]}")
    print(f"Name: {row[1][:80]}")
    print(f"Image: {row[2]}")
    print(f"Price: {row[3]}")
    print()

cur.close()
conn.close()
