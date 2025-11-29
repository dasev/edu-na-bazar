"""
Экспорт данных из temp.file в SQL файл
Используем данные которые уже в БД (9,753 записей)
"""
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="edu_na_bazar",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

OUTPUT_FILE = r"C:\python\edu-na-bazar\file_from_db.sql"

print("📊 Экспорт данных из temp.file...\n")

# Получаем все данные
cur.execute("""
    SELECT id, filename, path, type, advert_id, company_id
    FROM temp.file
    ORDER BY id
""")

records = cur.fetchall()

print(f"✅ Найдено записей: {len(records)}")

# Статистика
cur.execute("SELECT COUNT(*) FROM temp.file WHERE advert_id IS NOT NULL")
with_advert = cur.fetchone()[0]

cur.execute("SELECT COUNT(DISTINCT advert_id) FROM temp.file WHERE advert_id IS NOT NULL")
unique_advert = cur.fetchone()[0]

print(f"📊 С advert_id: {with_advert}")
print(f"📊 Уникальных advert_id: {unique_advert}")

# Генерируем SQL
print(f"\n📝 Создаём SQL файл: {OUTPUT_FILE}")

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write("-- Экспорт данных из temp.file\n")
    f.write(f"-- Всего записей: {len(records)}\n")
    f.write(f"-- С advert_id: {with_advert}\n")
    f.write(f"-- Уникальных advert_id: {unique_advert}\n\n")
    
    for record in records:
        id_val, filename, path, file_type, advert_id, company_id = record
        
        # Экранируем кавычки
        filename = filename.replace("'", "''") if filename else ''
        path = path.replace("'", "''") if path else ''
        file_type = file_type.replace("'", "''") if file_type else 'image'
        
        sql = f"INSERT INTO temp.file (id, filename, path, type, advert_id, company_id) VALUES ("
        sql += f"{id_val}, "
        sql += f"'{filename}', "
        sql += f"'{path}', "
        sql += f"'{file_type}', "
        sql += f"{advert_id if advert_id else 'NULL'}, "
        sql += f"{company_id if company_id else 'NULL'}"
        sql += ");\n"
        
        f.write(sql)

print(f"✅ Готово! Создано {len(records)} INSERT запросов")
print(f"📁 Файл сохранён: {OUTPUT_FILE}")

cur.close()
conn.close()
