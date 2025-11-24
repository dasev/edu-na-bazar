"""
Тест API товара
"""
import requests
import json

# Проверяем несколько товаров с изображениями
product_ids = [14178, 14187, 14192, 98110]

for product_id in product_ids:
    url = f"http://localhost:8000/api/products/{product_id}"
    
    print(f"\n{'='*80}")
    print(f"Товар ID: {product_id}")
    print(f"URL: {url}")
    print('='*80)
    
    try:
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"Name: {data.get('name', '')[:80]}")
            print(f"Image: {data.get('image')}")
            print(f"Images count: {len(data.get('images', []))}")
            
            if data.get('images'):
                print("\nImages:")
                for i, img in enumerate(data.get('images', [])[:5]):
                    print(f"  {i+1}. {img.get('image_url')}")
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

print(f"\n{'='*80}")
