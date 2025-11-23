"""
Проверка данных в разных схемах
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
    
    # Проверяем users в public
    cur.execute("SELECT COUNT(*) FROM public.users")
    public_users = cur.fetchone()[0]
    print(f"📊 public.users: {public_users} записей")
    
    # Проверяем users в config
    cur.execute("SELECT COUNT(*) FROM config.users")
    config_users = cur.fetchone()[0]
    print(f"📊 config.users: {config_users} записей")
    
    # Проверяем products в public
    cur.execute("SELECT COUNT(*) FROM public.products")
    public_products = cur.fetchone()[0]
    print(f"📊 public.products: {public_products} записей")
    
    # Проверяем products в market
    cur.execute("SELECT COUNT(*) FROM market.products")
    market_products = cur.fetchone()[0]
    print(f"📊 market.products: {market_products} записей")
    
    # Проверяем categories в public
    cur.execute("SELECT COUNT(*) FROM public.categories")
    public_categories = cur.fetchone()[0]
    print(f"📊 public.categories: {public_categories} записей")
    
    # Проверяем categories в market
    cur.execute("SELECT COUNT(*) FROM market.categories")
    market_categories = cur.fetchone()[0]
    print(f"📊 market.categories: {market_categories} записей")
    
    print("\n💡 Нужно скопировать данные из public в config/market!")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
