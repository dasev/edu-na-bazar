"""
Добавление недостающих таблиц
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
    
    with open('migrations/add_missing_tables.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    
    print("🔄 Добавляем недостающие таблицы...")
    print("   - config.sms_codes")
    print("   - market.orders")
    print("   - market.order_items")
    print("   - market.stores")
    
    cur.execute(sql)
    
    print("\n✅ Таблицы добавлены!")
    
    cur.close()
    conn.close()
    
    print("\n✅ Готово!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
