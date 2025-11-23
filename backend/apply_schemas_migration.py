"""
Применение миграции со схемами config и market
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
    
    with open('migrations/create_schemas_and_tables.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    
    print("🔄 Применяем миграцию...")
    print("   - Создаем схемы config и market")
    print("   - Создаем таблицы с BIGSERIAL")
    
    cur.execute(sql)
    
    print("\n✅ Миграция применена!")
    print("\n📊 Созданные схемы:")
    print("   - config: пользователи и настройки")
    print("   - market: товары, магазины, корзины")
    
    cur.close()
    conn.close()
    
    print("\n✅ Готово!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
