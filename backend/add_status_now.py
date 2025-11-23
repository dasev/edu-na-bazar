"""
Добавить колонку status в таблицу store_owners
"""
import psycopg2

conn_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'edu_na_bazar',
    'user': 'postgres',
    'password': 'postgres'
}

try:
    conn = psycopg2.connect(**conn_params)
    conn.autocommit = True
    cur = conn.cursor()
    
    print("📝 Добавляем колонку status...")
    
    cur.execute("""
        ALTER TABLE store_owners 
        ADD COLUMN IF NOT EXISTS status VARCHAR(20) NOT NULL DEFAULT 'pending'
    """)
    
    print("✅ Колонка status добавлена!")
    
    print("📝 Создаем индекс...")
    
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_store_owners_status ON store_owners(status)
    """)
    
    print("✅ Индекс создан!")
    
    cur.close()
    conn.close()
    
    print("\n✅ Готово!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
