"""
Копирование изображений в uploads/products/original
"""
import os
import shutil
from pathlib import Path

# Пути
SOURCE_DIR = r"C:\python\downloaded_images"
TARGET_DIR = r"C:\python\edu-na-bazar\backend\uploads\products\original"

# Создаём целевую директорию
os.makedirs(TARGET_DIR, exist_ok=True)

print("📁 Копирование изображений...")
print(f"   Из: {SOURCE_DIR}")
print(f"   В:  {TARGET_DIR}\n")

# Счётчики
copied = 0
skipped = 0
errors = 0

# Копируем все файлы
for filename in os.listdir(SOURCE_DIR):
    source_path = os.path.join(SOURCE_DIR, filename)
    
    # Пропускаем директории
    if os.path.isdir(source_path):
        continue
    
    # Пропускаем не-изображения
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        skipped += 1
        continue
    
    target_path = os.path.join(TARGET_DIR, filename)
    
    try:
        shutil.copy2(source_path, target_path)
        copied += 1
        if copied % 100 == 0:
            print(f"   Скопировано: {copied}")
    except Exception as e:
        errors += 1
        print(f"   ❌ Ошибка при копировании {filename}: {e}")

print(f"\n✅ Готово!")
print(f"   Скопировано: {copied}")
print(f"   Пропущено: {skipped}")
print(f"   Ошибок: {errors}")
