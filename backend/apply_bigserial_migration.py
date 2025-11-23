"""
Применение миграции на BIGSERIAL
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
    
    print("📝 Читаем миграцию...")
    
    with open('migrations/recreate_all_with_bigserial.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    
    print("🔄 Применяем миграцию...")
    
    cur.execute(sql)
    
    print("✅ Миграция применена!")
    
    cur.close()
    conn.close()
    
    print("\n✅ Готово! Все таблицы пересозданы с BIGSERIAL!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
