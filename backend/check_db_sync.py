"""
Проверка структуры таблицы store_owners (синхронная версия)
"""
import psycopg2

# Параметры подключения
conn_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'edu_na_bazar',
    'user': 'postgres',
    'password': 'postgres'
}

try:
    # Подключаемся к БД
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    
    # Проверяем структуру таблицы
    cur.execute("""
        SELECT column_name, data_type, udt_name
        FROM information_schema.columns
        WHERE table_name = 'store_owners'
        ORDER BY ordinal_position
    """)
    
    columns = cur.fetchall()
    
    print("📊 Структура таблицы store_owners:\n")
    for col in columns:
        print(f"  {col[0]:20} {col[1]:20} ({col[2]})")
    
    # Проверяем существование типа store_status
    cur.execute("""
        SELECT EXISTS (
            SELECT 1 FROM pg_type WHERE typname = 'store_status'
        )
    """)
    
    type_exists = cur.fetchone()[0]
    print(f"\n🔍 Тип store_status существует: {type_exists}")
    
    cur.close()
    conn.close()
    
    print("\n✅ Готово!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
