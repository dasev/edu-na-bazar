"""
Проверка таблиц в схеме public
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
    cur = conn.cursor()
    
    # Таблицы в public
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """)
    
    public_tables = cur.fetchall()
    
    print("📊 Таблицы в схеме public:\n")
    for table in public_tables:
        print(f"  - {table[0]}")
    
    # Таблицы в config
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'config' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """)
    
    config_tables = cur.fetchall()
    
    print("\n📊 Таблицы в схеме config:\n")
    for table in config_tables:
        print(f"  - {table[0]}")
    
    # Таблицы в market
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'market' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """)
    
    market_tables = cur.fetchall()
    
    print("\n📊 Таблицы в схеме market:\n")
    for table in market_tables:
        print(f"  - {table[0]}")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
