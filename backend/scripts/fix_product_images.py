"""
Исправление изображений товаров - привязка правильных фото
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

# Маппинг: ключевое слово -> конкретное изображение из уже загруженных
# Сначала посмотрим какие изображения у нас есть

cur.execute("""
    SELECT p.id, p.name, p.image
    FROM market.products p
    WHERE p.category_id = 1 
    AND p.image IS NOT NULL
    ORDER BY p.id
    LIMIT 20
""")

products = cur.fetchall()

print("📋 Примеры товаров с изображениями:\n")
for pid, name, image in products:
    print(f"  {pid}: {name[:40]}... -> {image}")

print("\n💡 Рекомендация:")
print("Лучше использовать готовые изображения из датасетов или")
print("загрузить свои фотографии в /uploads/products/original/")
print("\nНапример:")
print("  - tomato.jpg, cucumber.jpg, potato.jpg и т.д.")
print("  - Затем привязать их к товарам по ключевым словам")

cur.close()
conn.close()
