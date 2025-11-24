"""
Добавление специфичных изображений для каждого типа товара
Используем прямые ссылки на конкретные изображения
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

IMAGES_DIR = Path(r"C:\python\edu-na-bazar\backend\uploads\products\original")
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Конкретные изображения для каждого типа товара
SPECIFIC_IMAGES = {
    'помидор': [
        'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=800&h=600&fit=crop',  # Cherry tomatoes
        'https://images.unsplash.com/photo-1546470427-227a2e2e5b6e?w=800&h=600&fit=crop',  # Red tomatoes
        'https://images.unsplash.com/photo-1582284540020-8acbe03f4924?w=800&h=600&fit=crop',  # Tomatoes on vine
    ],
    'огурец': [
        'https://images.unsplash.com/photo-1604977042946-1eecc30f269e?w=800&h=600&fit=crop',  # Cucumbers
        'https://images.unsplash.com/photo-1568584711271-e90e6a4f5a0d?w=800&h=600&fit=crop',  # Fresh cucumbers
    ],
    'картофель': [
        'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=800&h=600&fit=crop',  # Potatoes
        'https://images.unsplash.com/photo-1596097635780-36c0c6c3c8b6?w=800&h=600&fit=crop',  # Fresh potatoes
    ],
    'морковь': [
        'https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=800&h=600&fit=crop',  # Carrots
        'https://images.unsplash.com/photo-1447175008436-054170c2e979?w=800&h=600&fit=crop',  # Fresh carrots
    ],
    'капуста': [
        'https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?w=800&h=600&fit=crop',  # Cabbage
        'https://images.unsplash.com/photo-1556801712-76c8eb07bbc9?w=800&h=600&fit=crop',  # Green cabbage
    ],
    'свекла': [
        'https://images.unsplash.com/photo-1587735243615-c03f25aaff15?w=800&h=600&fit=crop',  # Beets
        'https://images.unsplash.com/photo-1590165482129-1b8b27698780?w=800&h=600&fit=crop',  # Red beets
    ],
    'лук': [
        'https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?w=800&h=600&fit=crop',  # Onions
        'https://images.unsplash.com/photo-1508747703725-719777637510?w=800&h=600&fit=crop',  # Red onions
    ],
    'перец': [
        'https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=800&h=600&fit=crop',  # Bell peppers
        'https://images.unsplash.com/photo-1525607551316-4a8e16d1f9ba?w=800&h=600&fit=crop',  # Colorful peppers
    ],
}

def find_image_for_product(product_name):
    """Находим подходящее изображение для товара"""
    product_name_lower = product_name.lower()
    
    for keyword, images in SPECIFIC_IMAGES.items():
        if keyword in product_name_lower:
            # Возвращаем случайное изображение из списка
            import random
            return random.choice(images)
    
    return None

def download_image(url, filename):
    """Скачиваем изображение"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            filepath = IMAGES_DIR / filename
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return f"/uploads/products/original/{filename}"
    except Exception as e:
        print(f"    ❌ Ошибка загрузки: {e}")
    
    return None

# Получаем товары категории 1 с изображениями (чтобы заменить неправильные)
cur.execute("""
    SELECT p.id, p.name, p.image
    FROM market.products p
    WHERE p.category_id = 1 
    AND p.image IS NOT NULL
    ORDER BY p.id
    LIMIT 100
""")

products = cur.fetchall()

print(f"📦 Найдено товаров для обновления: {len(products)}\n")

total_updated = 0

for i, (product_id, product_name, old_image) in enumerate(products):
    print(f"{i+1}. {product_name[:50]}...")
    
    # Находим подходящее изображение
    image_url = find_image_for_product(product_name)
    
    if not image_url:
        print(f"    ⚠️ Нет подходящего изображения")
        continue
    
    # Генерируем имя файла
    unique_string = f"{product_id}_{product_name}"
    hash_name = hashlib.md5(unique_string.encode()).hexdigest()
    filename = f"specific_{hash_name}.jpg"
    
    # Скачиваем
    print(f"    📥 Загрузка...", end=" ")
    image_path = download_image(image_url, filename)
    
    if image_path:
        print("✅")
        try:
            # Обновляем товар
            cur.execute("""
                UPDATE market.products 
                SET image = %s 
                WHERE id = %s
            """, (image_path, product_id))
            
            # Удаляем старые изображения из product_images
            cur.execute("""
                DELETE FROM market.product_images 
                WHERE product_id = %s
            """, (product_id,))
            
            # Добавляем новое
            cur.execute("""
                INSERT INTO market.product_images 
                (product_id, image_url, is_main, sort_order)
                VALUES (%s, %s, %s, %s)
            """, (product_id, image_path, True, 0))
            
            total_updated += 1
            
            if total_updated % 10 == 0:
                conn.commit()
                print(f"\n  💾 Обновлено: {total_updated}")
                
        except Exception as e:
            print(f"    ❌ Ошибка БД: {e}")
            conn.rollback()
    else:
        print("❌")
    
    time.sleep(0.3)

conn.commit()

print(f"\n\n🎉 ГОТОВО!")
print(f"  ✅ Обновлено товаров: {total_updated}")

cur.close()
conn.close()
