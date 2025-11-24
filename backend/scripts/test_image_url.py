"""
Тест доступности изображений
"""
import requests

# Проверяем доступность изображения
url = "http://localhost:8000/uploads/products/original/whMZVFzw9X4FDzJmv7frU8IpXfYSvvcQ.png"

print(f"🔍 Проверка URL: {url}\n")

try:
    response = requests.head(url, timeout=5)
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        print("\n✅ Изображение доступно!")
    else:
        print(f"\n❌ Ошибка: {response.status_code}")
        
        # Пробуем GET запрос
        response = requests.get(url, timeout=5)
        print(f"\nGET Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}")
        print(f"Content-Length: {len(response.content)} bytes")
        
except Exception as e:
    print(f"❌ Ошибка: {e}")
