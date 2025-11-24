"""
Проверка отзывов в БД
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

print("📊 Проверка данных отзывов:\n")

# Отзывы
cur.execute("SELECT COUNT(*) FROM market.product_reviews")
total_reviews = cur.fetchone()[0]
print(f"✅ Всего отзывов: {total_reviews}")

# Вопросы
cur.execute("SELECT COUNT(*) FROM market.product_questions")
total_questions = cur.fetchone()[0]
print(f"✅ Всего вопросов: {total_questions}")

# Ответы
cur.execute("SELECT COUNT(*) FROM market.question_answers")
total_answers = cur.fetchone()[0]
print(f"✅ Всего ответов: {total_answers}")

print("\n📝 Примеры отзывов:")
cur.execute("""
    SELECT pr.id, pr.product_id, pr.rating, pr.comment, p.name
    FROM market.product_reviews pr
    JOIN market.products p ON p.id = pr.product_id
    LIMIT 3
""")

for review_id, product_id, rating, comment, product_name in cur.fetchall():
    print(f"\n  ID: {review_id}")
    print(f"  Товар: {product_name} (ID: {product_id})")
    print(f"  Рейтинг: {rating} ⭐")
    print(f"  Комментарий: {comment[:60]}...")

print("\n❓ Примеры вопросов:")
cur.execute("""
    SELECT pq.id, pq.product_id, pq.question_text, p.name
    FROM market.product_questions pq
    JOIN market.products p ON p.id = pq.product_id
    LIMIT 3
""")

for q_id, product_id, question, product_name in cur.fetchall():
    print(f"\n  ID: {q_id}")
    print(f"  Товар: {product_name} (ID: {product_id})")
    print(f"  Вопрос: {question}")

cur.close()
conn.close()
