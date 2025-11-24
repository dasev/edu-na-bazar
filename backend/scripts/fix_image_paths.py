"""
Исправление путей к изображениям в БД
"""
import os
import psycopg2

# Подключение к БД
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="edu_na_bazar",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

# Путь к папке с изображениями
IMAGES_DIR = r"C:\python\edu-na-bazar\backend\uploads\products\original"

# Получаем список реальных файлов
real_files = set()
for filename in os.listdir(IMAGES_DIR):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        real_files.add(filename)

print(f"📁 Найдено файлов в папке: {len(real_files)}\n")

# Получаем текущие пути из БД
print("📊 Текущие пути в market.product_images:")
cur.execute("""
    SELECT id, product_id, image_url 
    FROM market.product_images 
    LIMIT 10
""")

for row in cur.fetchall():
    print(f"   ID: {row[0]}, Product: {row[1]}, URL: {row[2]}")

# Проверяем сколько путей нужно исправить
print("\n🔍 Анализ путей...")
cur.execute("SELECT id, image_url FROM market.product_images")
all_images = cur.fetchall()

need_fix = 0
already_ok = 0
missing_files = 0

for img_id, url in all_images:
    # Извлекаем имя файла из URL
    # URL вида: /uploads/products/original/filename.jpg
    if url:
        filename = os.path.basename(url)
        
        if filename in real_files:
            already_ok += 1
        else:
            # Проверяем есть ли файл с другим расширением
            base_name = os.path.splitext(filename)[0]
            found = False
            for ext in ['.jpg', '.jpeg', '.png', '.gif']:
                if base_name + ext in real_files:
                    need_fix += 1
                    found = True
                    break
            if not found:
                missing_files += 1

print(f"   ✅ Пути корректны: {already_ok}")
print(f"   🔧 Нужно исправить: {need_fix}")
print(f"   ❌ Файлы отсутствуют: {missing_files}")

# Спрашиваем подтверждение
print(f"\n❓ Обновить пути в БД? (y/n): ", end="")
answer = input().strip().lower()

if answer == 'y':
    print("\n🔧 Обновляем пути...")
    updated = 0
    
    cur.execute("SELECT id, image_url FROM market.product_images")
    all_images = cur.fetchall()
    
    for img_id, url in all_images:
        if not url:
            continue
            
        filename = os.path.basename(url)
        base_name = os.path.splitext(filename)[0]
        
        # Ищем файл с любым расширением
        for ext in ['.jpg', '.jpeg', '.png', '.gif']:
            test_filename = base_name + ext
            if test_filename in real_files:
                new_url = f"/uploads/products/original/{test_filename}"
                if new_url != url:
                    cur.execute(
                        "UPDATE market.product_images SET image_url = %s WHERE id = %s",
                        (new_url, img_id)
                    )
                    updated += 1
                break
    
    conn.commit()
    print(f"✅ Обновлено путей: {updated}")
else:
    print("❌ Отменено")

cur.close()
conn.close()
