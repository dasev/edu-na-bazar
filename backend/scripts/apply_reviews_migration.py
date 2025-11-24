"""
Применение миграции для отзывов и вопросов
"""
import psycopg2
from pathlib import Path

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="edu_na_bazar",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

# Читаем SQL файл
migration_file = Path(__file__).parent.parent / "migrations" / "create_reviews_and_questions.sql"

print("📝 Применение миграции для отзывов и вопросов...")

with open(migration_file, 'r', encoding='utf-8') as f:
    sql = f.read()
    
try:
    cur.execute(sql)
    conn.commit()
    print("✅ Миграция успешно применена!")
    
    # Проверяем созданные таблицы
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'market' 
        AND table_name LIKE '%review%' OR table_name LIKE '%question%'
        ORDER BY table_name
    """)
    
    tables = cur.fetchall()
    print(f"\n📊 Создано таблиц: {len(tables)}")
    for table in tables:
        print(f"  ✓ {table[0]}")
        
except Exception as e:
    print(f"❌ Ошибка: {e}")
    conn.rollback()

cur.close()
conn.close()
