"""
Наполнение категорий: Молочные продукты и Яйца
"""
import psycopg2
import requests
import hashlib
from pathlib import Path
import time
import random

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

# Товары с изображениями
PRODUCTS = [
    # Категория 3: Молочные продукты
    {
        'category_id': 3,
        'name': 'Молоко фермерское 3.2%',
        'description': 'Свежее фермерское молоко от здоровых коров. Натуральное, без добавок. Жирность 3.2%.',
        'price': 89.90,
        'unit': 'л',
        'images': [
            'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=800&h=600&fit=crop&q=80',
            'https://images.unsplash.com/photo-1563636619-e9143da7973b?w=800&h=600&fit=crop&q=80',
        ]
    },
    {
        'category_id': 3,
        'name': 'Творог домашний 9%',
        'description': 'Свежий творог из натурального молока. Нежная консистенция, богат кальцием.',
        'price': 249.90,
        'unit': 'кг',
        'images': [
            'https://images.unsplash.com/photo-1628088062854-d1870b4553da?w=800&h=600&fit=crop&q=80',
            'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=800&h=600&fit=crop&q=80',
        ]
    },
    {
        'category_id': 3,
        'name': 'Сметана 20% домашняя',
        'description': 'Густая сметана из натуральных сливок. Без загустителей.',
        'price': 189.90,
        'unit': 'кг',
        'images': [
            'https://images.unsplash.com/photo-1571212515416-fef01fc43637?w=800&h=600&fit=crop&q=80',
        ]
    },
    {
        'category_id': 3,
        'name': 'Сыр фермерский твердый',
        'description': 'Натуральный сыр из коровьего молока. Выдержанный, с насыщенным вкусом.',
        'price': 599.90,
        'unit': 'кг',
        'images': [
            'https://images.unsplash.com/photo-1452195100486-9cc805987862?w=800&h=600&fit=crop&q=80',
            'https://images.unsplash.com/photo-1618164436241-4473940d1f5c?w=800&h=600&fit=crop&q=80',
        ]
    },
    {
        'category_id': 3,
        'name': 'Масло сливочное 82.5%',
        'description': 'Натуральное сливочное масло высшего сорта. Из свежих сливок.',
        'price': 449.90,
        'unit': 'кг',
        'images': [
            'https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=800&h=600&fit=crop&q=80',
        ]
    },
    {
        'category_id': 3,
        'name': 'Кефир 2.5% натуральный',
        'description': 'Свежий кефир на живой закваске. Полезен для пищеварения.',
        'price': 79.90,
        'unit': 'л',
        'images': [
            'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=800&h=600&fit=crop&q=80',
        ]
    },
    
    # Категория 11: Яйца
    {
        'category_id': 11,
        'name': 'Яйца куриные С0 домашние',
        'description': 'Свежие яйца от кур свободного выгула. Крупные, с ярким желтком.',
        'price': 129.90,
        'unit': '10 шт',
        'images': [
            'https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=800&h=600&fit=crop&q=80',
            'https://images.unsplash.com/photo-1506976785307-8732e854ad03?w=800&h=600&fit=crop&q=80',
        ]
    },
    {
        'category_id': 11,
        'name': 'Яйца куриные С1 фермерские',
        'description': 'Яйца первой категории от домашних кур. Свежие, вкусные.',
        'price': 99.90,
        'unit': '10 шт',
        'images': [
            'https://images.unsplash.com/photo-1518569656558-1f25e69d93d7?w=800&h=600&fit=crop&q=80',
        ]
    },
    {
        'category_id': 11,
        'name': 'Яйца перепелиные диетические',
        'description': 'Свежие перепелиные яйца. Очень полезные, богаты витаминами.',
        'price': 189.90,
        'unit': '20 шт',
        'images': [
            'https://images.unsplash.com/photo-1587486937773-5c82f5d29e3e?w=800&h=600&fit=crop&q=80',
            'https://images.unsplash.com/photo-1599873494936-4b7d2c6e5f5a?w=800&h=600&fit=crop&q=80',
        ]
    },
    {
        'category_id': 11,
        'name': 'Яйца утиные крупные',
        'description': 'Домашние утиные яйца. Крупнее куриных, с богатым вкусом.',
        'price': 159.90,
        'unit': '6 шт',
        'images': [
            'https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=800&h=600&fit=crop&q=80',
        ]
    },
]

def download_image(url, filename):
    """Скачиваем изображение"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            filepath = IMAGES_DIR / filename
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return f"/uploads/products/original/{filename}"
        else:
            print(f"      ⚠️ {response.status_code}")
    except Exception as e:
        print(f"      ❌ {e}")
    return None

print("📦 Наполнение категорий: Молочные продукты и Яйца\n")

total_products = 0
total_images = 0

for i, product_data in enumerate(PRODUCTS):
    print(f"{i+1}. {product_data['name']}")
    
    rating = round(random.uniform(4.3, 5.0), 1)
    reviews_count = random.randint(20, 180)
    
    try:
        cur.execute("""
            INSERT INTO market.products 
            (name, description, price, category_id, rating, reviews_count, in_stock, unit)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            product_data['name'],
            product_data['description'],
            product_data['price'],
            product_data['category_id'],
            rating,
            reviews_count,
            True,
            product_data['unit']
        ))
        
        product_id = cur.fetchone()[0]
        total_products += 1
        
        for img_index, image_url in enumerate(product_data['images']):
            print(f"   📥 {img_index + 1}/{len(product_data['images'])}...", end=" ")
            
            unique_string = f"{product_id}_{img_index}_{product_data['name']}"
            hash_name = hashlib.md5(unique_string.encode()).hexdigest()
            filename = f"prod_{hash_name}.jpg"
            
            image_path = download_image(image_url, filename)
            
            if image_path:
                print("✅")
                
                if img_index == 0:
                    cur.execute("UPDATE market.products SET image = %s WHERE id = %s", 
                              (image_path, product_id))
                
                cur.execute("""
                    INSERT INTO market.product_images 
                    (product_id, image_url, is_main, sort_order)
                    VALUES (%s, %s, %s, %s)
                """, (product_id, image_path, img_index == 0, img_index))
                
                total_images += 1
            else:
                print("❌")
            
            time.sleep(0.3)
        
        conn.commit()
        print()
        
    except Exception as e:
        print(f"   ❌ {e}")
        conn.rollback()

print(f"\n🎉 ГОТОВО!")
print(f"  ✅ Товаров: {total_products}")
print(f"  🖼️ Изображений: {total_images}")

cur.close()
conn.close()
