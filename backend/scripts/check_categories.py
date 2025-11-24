"""
Проверка категорий
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

cur.execute("SELECT id, name FROM market.categories ORDER BY id")
categories = cur.fetchall()

print("📊 Категории:\n")
for cat_id, cat_name in categories:
    print(f"  {cat_id}. {cat_name}")

cur.close()
conn.close()
