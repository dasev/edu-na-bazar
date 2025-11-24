import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="edu_na_bazar",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

cur.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_schema = 'config' AND table_name = 'users'
    ORDER BY ordinal_position
""")

columns = cur.fetchall()

print("📊 Колонки таблицы config.users:\n")
for col_name, col_type in columns:
    print(f"  {col_name}: {col_type}")

cur.close()
conn.close()
