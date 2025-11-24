"""
Добавление изображений к товарам первой категории
Используем Picsum Photos (надёжный источник placeholder изображений)
"""
import psycopg2
import requests
import hashlib
from pathlib import Path
import time

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="edu_na_bazar",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

# Директория для изображений
IMAGES_DIR = Path(r"C:\python\edu-na-bazar\backend\uploads\products\original")
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Получаем товары первой категории без изображений
cur.execute("""
    SELECT id, name 
    FROM market.products 
    WHERE category_id = 1 
    AND (image IS NULL OR image = '')
    ORDER BY id
    LIMIT 100
""")

products = cur.fetchall()

print(f"📦 Найдено товаров без изображений: {len(products)}\n")

# Список URL изображений овощей и фруктов
# Используем Lorem Picsum - надёжный сервис placeholder изображений
VEGETABLE_IMAGES = [
    "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=800&h=600&fit=crop",  # Tomatoes
    "https://images.unsplash.com/photo-1449300079323-02e209d9d3a6?w=800&h=600&fit=crop",  # Cucumbers
    "https://images.unsplash.com/photo-1518013431117-eb1465fa5752?w=800&h=600&fit=crop",  # Potatoes
    "https://images.unsplash.com/photo-1447175008436-054170c2e979?w=800&h=600&fit=crop",  # Carrots
    "https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?w=800&h=600&fit=crop",  # Cabbage
    "https://images.unsplash.com/photo-1587735243615-c03f25aaff15?w=800&h=600&fit=crop",  # Beets
    "https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?w=800&h=600&fit=crop",  # Onions
    "https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=800&h=600&fit=crop",  # Bell peppers
    "https://images.unsplash.com/photo-1570913149827-d2ac84ab3f9a?w=800&h=600&fit=crop",  # Apples
    "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=800&h=600&fit=crop",  # Pears
    "https://images.unsplash.com/photo-1601493700631-2b16ec4b4716?w=800&h=600&fit=crop",  # Grapes
    "https://images.unsplash.com/photo-1587049352846-4a222e784720?w=800&h=600&fit=crop",  # Watermelon
    "https://images.unsplash.com/photo-1464454709131-ffd692591ee5?w=800&h=600&fit=crop",  # Strawberries
    "https://images.unsplash.com/photo-1577003833154-a7e6d12c2a8c?w=800&h=600&fit=crop",  # Raspberries
    "https://images.unsplash.com/photo-1528821128474-27f963b062bf?w=800&h=600&fit=crop",  # Lettuce
]

def download_image(url, filename):
    """Скачиваем изображение с retry"""
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            print(f"    📥 Загрузка изображения (попытка {attempt + 1})...", end=" ")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                filepath = IMAGES_DIR / filename
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print("✅")
                return f"/uploads/products/original/{filename}"
            else:
                print(f"❌ Статус: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            
        if attempt < max_retries - 1:
            time.sleep(2)  # Пауза перед повтором
    
    return None

total_updated = 0

for i, (product_id, product_name) in enumerate(products):
    print(f"\n{i+1}. Товар: {product_name[:50]}... (ID: {product_id})")
    
    # Выбираем изображение по кругу
    image_url = VEGETABLE_IMAGES[i % len(VEGETABLE_IMAGES)]
    
    # Генерируем уникальное имя файла
    unique_string = f"{product_id}_{i}_{product_name}"
    hash_name = hashlib.md5(unique_string.encode()).hexdigest()
    filename = f"{hash_name}.jpg"
    
    # Скачиваем изображение
    image_path = download_image(image_url, filename)
    
    if image_path:
        try:
            # Обновляем товар
            cur.execute("""
                UPDATE market.products 
                SET image = %s 
                WHERE id = %s
            """, (image_path, product_id))
            
            # Добавляем в product_images
            cur.execute("""
                INSERT INTO market.product_images 
                (product_id, image_url, sort_order)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (product_id, image_path, 0))
            
            total_updated += 1
            
            if total_updated % 10 == 0:
                conn.commit()
                print(f"\n  💾 Сохранено {total_updated} товаров")
                
        except Exception as e:
            print(f"    ❌ Ошибка БД: {e}")
            conn.rollback()
    
    # Небольшая пауза чтобы не перегружать сервер
    time.sleep(0.5)

conn.commit()

print(f"\n\n🎉 ГОТОВО!")
print(f"  ✅ Обновлено товаров: {total_updated}")
print(f"  📁 Изображения сохранены в: {IMAGES_DIR}")

# Проверяем результат
cur.execute("""
    SELECT COUNT(*) 
    FROM market.products 
    WHERE category_id = 1 
    AND image IS NOT NULL 
    AND image != ''
""")

count_with_images = cur.fetchone()[0]

print(f"  📊 Товаров с изображениями в категории 1: {count_with_images}")

cur.close()
conn.close()
