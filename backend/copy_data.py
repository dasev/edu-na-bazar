"""
Копирование данных из public в config/market
"""
import psycopg2

conn_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'edu_na_bazar',
    'user': 'postgres',
    'password': 'postgres'
}

print("📝 Копирование данных из public в config/market...")

try:
    conn = psycopg2.connect(**conn_params)
    conn.autocommit = True
    cur = conn.cursor()
    
    with open('migrations/copy_data_to_new_schemas.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    
    cur.execute(sql)
    
    # Получаем результаты
    results = cur.fetchall()
    print("\n✅ Данные скопированы!")
    print("\n📊 Статистика:")
    for row in results:
        print(f"  {row[0]}: {row[1]} записей")
    
    cur.close()
    conn.close()
    
    print("\n✅ Готово!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
