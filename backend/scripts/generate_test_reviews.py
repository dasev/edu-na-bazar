"""
Генерация тестовых отзывов и вопросов
"""
import psycopg2
import random
from datetime import datetime, timedelta

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="edu_na_bazar",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

# Получаем товары из категории 1
cur.execute("SELECT id, name FROM market.products WHERE category_id = 1 LIMIT 12")
products = cur.fetchall()

# Получаем пользователей
cur.execute("SELECT id, COALESCE(full_name, email) as name FROM config.users LIMIT 10")
users = cur.fetchall()

if not users:
    print("⚠️ Нет пользователей! Создаю тестового...")
    cur.execute("""
        INSERT INTO config.users (email, full_name)
        VALUES ('test@example.com', 'Тестовый Пользователь')
        RETURNING id, full_name
    """)
    users = [cur.fetchone()]
    conn.commit()

print(f"📦 Товаров: {len(products)}")
print(f"👥 Пользователей: {len(users)}\n")

# Шаблоны отзывов
REVIEW_TEMPLATES = [
    {
        'rating': 5,
        'title': 'Отличный товар!',
        'comment': 'Всё целое пока ещё не использовал. По ходу дела дополню отзыв',
        'advantages': 'Свежий, качественный, быстрая доставка',
        'disadvantages': None
    },
    {
        'rating': 5,
        'title': 'Всё нормально',
        'comment': 'Товар соответствует описанию. Доволен покупкой.',
        'advantages': 'Хорошее качество, адекватная цена',
        'disadvantages': 'Не обнаружил'
    },
    {
        'rating': 4,
        'title': 'Хорошо',
        'comment': 'В целом доволен. Есть небольшие замечания, но в целом рекомендую.',
        'advantages': 'Качество хорошее, свежий',
        'disadvantages': 'Упаковка могла бы быть лучше'
    },
    {
        'rating': 5,
        'title': 'Рекомендую!',
        'comment': 'Покупаю уже не первый раз. Всегда свежее и вкусное. Спасибо продавцу!',
        'advantages': 'Отличное качество, вкусно, свежее',
        'disadvantages': None
    },
    {
        'rating': 4,
        'title': 'Неплохо',
        'comment': 'Товар нормальный, но ожидал большего за эту цену.',
        'advantages': 'Качество приемлемое',
        'disadvantages': 'Цена немного завышена'
    },
    {
        'rating': 5,
        'title': 'Супер!',
        'comment': 'Очень доволен покупкой! Всё свежее, качественное. Буду заказывать ещё.',
        'advantages': 'Отличное качество, быстрая доставка, свежий товар',
        'disadvantages': 'Не нашёл'
    },
]

# Шаблоны вопросов
QUESTION_TEMPLATES = [
    'Какой срок годности?',
    'Есть ли в наличии?',
    'Можно ли заказать оптом?',
    'Откуда привезли?',
    'Какая упаковка?',
    'Доставка включена в цену?',
]

total_reviews = 0
total_questions = 0

for product_id, product_name in products:
    print(f"📝 {product_name}")
    
    # Генерируем 2-5 отзывов на товар
    num_reviews = random.randint(2, 5)
    
    for _ in range(num_reviews):
        user_id, username = random.choice(users)
        template = random.choice(REVIEW_TEMPLATES)
        
        # Случайная дата за последние 30 дней
        days_ago = random.randint(1, 30)
        created_at = datetime.now() - timedelta(days=days_ago)
        
        try:
            cur.execute("""
                INSERT INTO market.product_reviews 
                (product_id, user_id, rating, title, comment, advantages, disadvantages, 
                 is_verified_purchase, helpful_count, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                product_id,
                user_id,
                template['rating'],
                template['title'],
                template['comment'],
                template['advantages'],
                template['disadvantages'],
                random.choice([True, False]),
                random.randint(0, 15),
                created_at
            ))
            total_reviews += 1
        except Exception as e:
            print(f"  ⚠️ Ошибка отзыва: {e}")
    
    # Генерируем 1-2 вопроса
    num_questions = random.randint(1, 2)
    
    for _ in range(num_questions):
        user_id, username = random.choice(users)
        question_text = random.choice(QUESTION_TEMPLATES)
        
        days_ago = random.randint(1, 20)
        created_at = datetime.now() - timedelta(days=days_ago)
        
        try:
            cur.execute("""
                INSERT INTO market.product_questions 
                (product_id, user_id, question_text, is_anonymous, created_at)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (
                product_id,
                user_id,
                question_text,
                random.choice([True, False]),
                created_at
            ))
            
            question_id = cur.fetchone()[0]
            total_questions += 1
            
            # Добавляем ответ с вероятностью 70%
            if random.random() < 0.7:
                answer_user_id, answer_username = random.choice(users)
                answer_text = "Спасибо за вопрос! Уточните у продавца."
                
                cur.execute("""
                    INSERT INTO market.question_answers 
                    (question_id, user_id, answer_text, is_seller, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    question_id,
                    answer_user_id,
                    answer_text,
                    False,
                    created_at + timedelta(hours=random.randint(1, 48))
                ))
                
        except Exception as e:
            print(f"  ⚠️ Ошибка вопроса: {e}")
    
    print(f"  ✅ Отзывов: {num_reviews}, Вопросов: {num_questions}")

conn.commit()

print(f"\n🎉 ГОТОВО!")
print(f"  📝 Всего отзывов: {total_reviews}")
print(f"  ❓ Всего вопросов: {total_questions}")

cur.close()
conn.close()
