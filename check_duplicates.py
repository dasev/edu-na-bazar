"""
Проверка дубликатов advert_id в file_inserts_correct.sql
"""
import re
from collections import Counter

# Читаем файл
with open('file_inserts_correct.sql', 'r', encoding='utf-8') as f:
    content = f.read()

# Извлекаем все advert_id (формат: 'image', 11, NULL)
pattern = r"'image', (\d+), "
advert_ids = re.findall(pattern, content)

print(f"📊 Всего записей с advert_id: {len(advert_ids)}")

# Считаем повторения
counter = Counter(advert_ids)

# Находим дубликаты
duplicates = {k: v for k, v in counter.items() if v > 1}

if duplicates:
    print(f"\n⚠️ Найдено дубликатов: {len(duplicates)}")
    print(f"📋 Топ-10 самых частых advert_id:\n")
    
    for advert_id, count in sorted(duplicates.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   advert_id = {advert_id}: {count} раз")
    
    print(f"\n📊 Статистика:")
    print(f"   Уникальных advert_id: {len(counter)}")
    print(f"   Всего записей: {len(advert_ids)}")
    print(f"   Дубликатов: {sum(v - 1 for v in duplicates.values())}")
else:
    print("\n✅ Дубликатов не найдено!")
