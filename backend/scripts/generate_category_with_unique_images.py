"""
Генерация товаров для категории "Овощи и фрукты" с уникальными изображениями
По 2-3 фото на каждый товар
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

# Сначала удалим тестовые товары из категории 1
print("🗑️ Удаляем старые тестовые товары...")
cur.execute("""
    DELETE FROM market.products 
    WHERE category_id = 1 
    AND id > 102602
""")
conn.commit()
print(f"✅ Удалено\n")

# Товары с конкретными изображениями
PRODUCTS_WITH_IMAGES = [
    {
        'name': 'Помидоры черри свежие',
        'description': 'Сладкие помидоры черри с собственной теплицы. Идеальны для салатов и закусок. Выращены без химикатов.',
        'price': 189.90,
        'unit': 'кг',
        'images': [
            'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=800&h=600&fit=crop&q=80',
            'https://images.unsplash.com/photo-1561136594-7f68413baa99?w=800&h=600&fit=crop&q=80',
            'https://images.unsplash.com/photo-1607305387299-a3d9611cd469?w=800&h=600&fit=crop&q=80',
        ]
    },
    {
        'name': 'Помидоры сливка красные',
        'description': 'Мясистые томаты сорта "Сливка". Отлично подходят для консервации и свежих салатов. Сочные и ароматные.',
        'price': 149.90,
        'unit': 'кг',
        'images': [
            'https://images.unsplash.com/photo-1546470427-227a2e2e5b6e?w=800&h=600&fit=crop&q=80',
            'https://images.unsplash.com/photo-1582284540020-8acbe03f4924?w=800&h=600&fit=crop&q=80',
        ]
    },
    {
        'name': 'Огурцы грунтовые хрустящие',
        'description': 'Свежие грунтовые огурцы без горечи. Выращены в открытом грунте. Идеальны для засолки и салатов.',
        'price': 129.90,
        'unit': 'кг',
        'images': [
            'https://images.unsplash.com/photo-1604977042946-1eecc30f269e?w=800&h=600&fit=crop&q=80',
            'https://images.unsplash.com/photo-1568584711271-e90e6a4f5a0d?w=800&h=600&fit=crop&q=80',
            'https://images.unsplash.com/photo-1589927986089-35812388d1f4?w=800&h=600&fit=crop&q=80',
        ]
    },
    {
        'name': 'Картофель молодой',
        'description': 'Молодой картофель с тонкой кожурой. Рассыпчатый и вкусный. Отлично подходит для варки и запекания.',
        'price': 59.90,
        'unit': 'кг',
        'images': [
            'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=800&h=600&fit=crop&q=80',
            'https://images.unsplash.com/photo-1596097635780-36c0c6c3c8b6?w=800&h=600&fit=crop&q=80',
        ]
    },
    {
        'name': 'Морковь сочная оранжевая',
        'description': 'Сладкая морковь ярко-оранжевого цвета. Богата витаминами. Отлично хранится всю зиму.',
        'price': 69.90,
        'unit': 'кг',
        'images': [
            'https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=800&h=600&fit=crop&q=80',
            'https://images.unsplash.com/photo-1447175008436-054170c2e979?w=800&h=600&fit=crop&q=80',
            'https://images.unsplash.com/photo-1582515073490-39981397c445?w=800&h=600&fit=crop&q=80',
        ]
    },
    {
        'name': 'Капуста белокочанная',
        'description': 'Свежая капуста с хрустящими листьями. Плотные кочаны. Идеальна для квашения и борща.',
        'price': 39.90,
        'unit': 'кг',
        'images': [
            'https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?w=800&h=600&fit=crop&q=80',
            'https://images.unsplash.com/photo-1556801712-76c8eb07bbc9?w=800&h=600&fit=crop&q=80',
        ]
    },
    {
        'name': 'Свекла столовая',
        'description': 'Сладкая свекла насыщенного бордового цвета. Без прожилок. Отлично варится, сочная.',
        'price': 49.90,
        'unit': 'кг',
        'images': [
            'https://images.unsplash.com/photo-1587735243615-c03f25aaff15?w=800&h=600&fit=crop&q=80',
            'https://images.unsplash.com/photo-1590165482129-1b8b27698780?w=800&h=600&fit=crop&q=80',
        ]
    },
    {
        'name': 'Лук репчатый золотистый',
        'description': 'Острый лук золотистого цвета. Долго хранится. Отлично подходит для любых блюд.',
        'price': 44.90,
        'unit': 'кг',
        'images': [
            'https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?w=800&h=600&fit=crop&q=80',
            'https://images.unsplash.com/photo-1508747703725-719777637510?w=800&h=600&fit=crop&q=80',
        ]
    },
    {
        'name': 'Перец болгарский микс',
        'description': 'Сладкий перец разных цветов: красный, желтый, зеленый. Толстые стенки. Очень сочный и ароматный.',
        'price': 249.90,
        'unit': 'кг',
        'images': [
            'https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=800&h=600&fit=crop&q=80',
            'https://images.unsplash.com/photo-1525607551316-4a8e16d1f9ba?w=800&h=600&fit=crop&q=80',
            'https://images.unsplash.com/photo-1601493700631-2b16ec4b4716?w=800&h=600&fit=crop&q=80',
        ]
    },
    {
        'name': 'Яблоки Антоновка',
        'description': 'Кисло-сладкие яблоки сорта Антоновка. Ароматные, хрустящие. Отлично подходят для пирогов и компотов.',
        'price': 89.90,
        'unit': 'кг',
        'images': [
            'https://images.unsplash.com/photo-1570913149827-d2ac84ab3f9a?w=800&h=600&fit=crop&q=80',
            'https://images.unsplash.com/photo-1619546813926-a78fa6372cd2?w=800&h=600&fit=crop&q=80',
        ]
    },
    {
        'name': 'Груши Конференция',
        'description': 'Сладкие груши с нежной мякотью. Сочные и ароматные. Тают во рту.',
        'price': 159.90,
        'unit': 'кг',
        'images': [
            'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=800&h=600&fit=crop&q=80',
            'https://images.unsplash.com/photo-1574856344991-aaa31b6f4ce3?w=800&h=600&fit=crop&q=80',
        ]
    },
    {
        'name': 'Виноград кишмиш',
        'description': 'Сладкий виноград без косточек. Крупные ягоды. Идеален для еды и сушки.',
        'price': 279.90,
        'unit': 'кг',
        'images': [
            'https://images.unsplash.com/photo-1601493700631-2b16ec4b4716?w=800&h=600&fit=crop&q=80',
            'https://images.unsplash.com/photo-1596363505729-4190a9506133?w=800&h=600&fit=crop&q=80',
        ]
    },
]

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
        else:
            print(f"      ⚠️ Статус: {response.status_code}")
    except Exception as e:
        print(f"      ❌ Ошибка: {e}")
    
    return None

print("📦 Генерация товаров с уникальными изображениями\n")

total_products = 0
total_images = 0

for i, product_data in enumerate(PRODUCTS_WITH_IMAGES):
    print(f"{i+1}. {product_data['name']}")
    
    # Генерируем рейтинг
    rating = round(random.uniform(4.2, 5.0), 1)
    reviews_count = random.randint(15, 150)
    
    # Вставляем товар
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
            1,  # category_id = 1 (Овощи и фрукты)
            rating,
            reviews_count,
            True,
            product_data['unit']
        ))
        
        product_id = cur.fetchone()[0]
        total_products += 1
        
        # Скачиваем изображения
        for img_index, image_url in enumerate(product_data['images']):
            print(f"   📥 Фото {img_index + 1}/{len(product_data['images'])}...", end=" ")
            
            # Генерируем уникальное имя файла
            unique_string = f"{product_id}_{img_index}_{product_data['name']}"
            hash_name = hashlib.md5(unique_string.encode()).hexdigest()
            filename = f"prod_{hash_name}.jpg"
            
            image_path = download_image(image_url, filename)
            
            if image_path:
                print("✅")
                
                # Первое изображение - главное
                if img_index == 0:
                    cur.execute("""
                        UPDATE market.products 
                        SET image = %s 
                        WHERE id = %s
                    """, (image_path, product_id))
                
                # Добавляем в product_images
                cur.execute("""
                    INSERT INTO market.product_images 
                    (product_id, image_url, is_main, sort_order)
                    VALUES (%s, %s, %s, %s)
                """, (product_id, image_path, img_index == 0, img_index))
                
                total_images += 1
            else:
                print("❌")
            
            time.sleep(0.3)  # Пауза между запросами
        
        conn.commit()
        print()
        
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        conn.rollback()
        continue

print(f"\n🎉 ГОТОВО!")
print(f"  ✅ Создано товаров: {total_products}")
print(f"  🖼️ Загружено изображений: {total_images}")
print(f"  📊 Среднее фото на товар: {total_images / total_products if total_products > 0 else 0:.1f}")

cur.close()
conn.close()
