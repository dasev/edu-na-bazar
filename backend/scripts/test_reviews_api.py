"""
Тест API отзывов
"""
import requests

BASE_URL = "http://localhost:8000"

# Проверяем статистику отзывов для товара
product_id = 102703  # ID товара из категории 1

print(f"🔍 Проверка API отзывов для товара {product_id}\n")

# 1. Статистика
print("1. Статистика отзывов:")
try:
    response = requests.get(f"{BASE_URL}/api/reviews/product/{product_id}/stats")
    print(f"   Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Всего отзывов: {data['total_reviews']}")
        print(f"   ⭐ Средний рейтинг: {data['average_rating']}")
        print(f"   📊 Распределение: {data['rating_distribution']}")
    else:
        print(f"   ❌ Ошибка: {response.text}")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

print()

# 2. Список отзывов
print("2. Список отзывов:")
try:
    response = requests.get(f"{BASE_URL}/api/reviews/product/{product_id}")
    print(f"   Статус: {response.status_code}")
    if response.status_code == 200:
        reviews = response.json()
        print(f"   ✅ Получено отзывов: {len(reviews)}")
        if reviews:
            print(f"   Первый отзыв: {reviews[0]['comment'][:50]}...")
    else:
        print(f"   ❌ Ошибка: {response.text}")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

print()

# 3. Вопросы
print("3. Вопросы о товаре:")
try:
    response = requests.get(f"{BASE_URL}/api/reviews/questions/product/{product_id}")
    print(f"   Статус: {response.status_code}")
    if response.status_code == 200:
        questions = response.json()
        print(f"   ✅ Получено вопросов: {len(questions)}")
        if questions:
            print(f"   Первый вопрос: {questions[0]['question_text']}")
    else:
        print(f"   ❌ Ошибка: {response.text}")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

print()

# 4. Проверяем что отзывы есть в БД
print("4. Проверка БД:")
import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="edu_na_bazar",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM market.product_reviews")
    total = cur.fetchone()[0]
    print(f"   ✅ Всего отзывов в БД: {total}")
    
    cur.execute("SELECT COUNT(*) FROM market.product_questions")
    total_q = cur.fetchone()[0]
    print(f"   ✅ Всего вопросов в БД: {total_q}")
    
    cur.close()
    conn.close()
except Exception as e:
    print(f"   ❌ Ошибка БД: {e}")
