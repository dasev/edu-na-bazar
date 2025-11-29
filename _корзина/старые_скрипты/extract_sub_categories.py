"""
Извлечение данных из sub_categories.ibd и создание INSERT запросов
"""
import struct
import re

IBD_FILE = r"C:\python\sites_mysql\enb\sub_categories.ibd"
OUTPUT_FILE = r"C:\python\edu-na-bazar\sub_categories_inserts.sql"

def extract_strings_from_page(page_data):
    """Извлекаем читаемые строки из страницы"""
    strings = []
    current_string = bytearray()
    
    for byte in page_data:
        if 32 <= byte <= 126 or byte >= 128:  # Печатные символы + UTF-8
            current_string.append(byte)
        else:
            if len(current_string) > 2:
                try:
                    s = current_string.decode('utf-8', errors='ignore')
                    if s.strip():
                        strings.append(s.strip())
                except:
                    pass
            current_string = bytearray()
    
    return strings

def parse_sub_category_data(strings):
    """Парсим данные подкатегорий из строк"""
    sub_categories = []
    
    for s in strings:
        # Пропускаем служебные данные
        if any(x in s.lower() for x in ['mysql', 'innodb', 'table', 'index', 'primary', 'supremum', 'infimum']):
            continue
        
        # Если строка похожа на название подкатегории (длина 3-200 символов)
        if 3 <= len(s) <= 200:
            # Проверяем что это не только цифры
            if not s.isdigit():
                sub_categories.append({'name': s})
    
    return sub_categories

def parse_ibd_file(filename):
    """Парсим InnoDB файл и извлекаем данные"""
    all_strings = []
    
    with open(filename, 'rb') as f:
        file_size = f.seek(0, 2)
        f.seek(0)
        
        num_pages = file_size // 16384
        print(f"Обрабатываю {num_pages} страниц...")
        
        for page_num in range(num_pages):
            f.seek(page_num * 16384)
            page = f.read(16384)
            
            if page_num < 3:
                continue
            
            strings = extract_strings_from_page(page)
            all_strings.extend(strings)
    
    return all_strings

def create_insert_statements(sub_categories):
    """Создаём INSERT запросы"""
    inserts = []
    
    print(f"\nНайдено подкатегорий: {len(sub_categories)}")
    
    for idx, sub_cat in enumerate(sub_categories, 1):
        name = sub_cat.get('name', f'Подкатегория {idx}')
        
        # Экранируем кавычки
        name_escaped = name.replace("'", "''")
        
        # Создаём INSERT
        insert = f"""INSERT INTO sub_categories (id, name, category_id, created_at, updated_at) 
VALUES ({idx}, '{name_escaped}', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());"""
        inserts.append(insert)
    
    return inserts

def main():
    print("="*80)
    print("ИЗВЛЕЧЕНИЕ ДАННЫХ ИЗ sub_categories.ibd")
    print("="*80)
    print()
    
    print(f"Файл: {IBD_FILE}")
    print()
    
    all_strings = parse_ibd_file(IBD_FILE)
    
    print(f"\nВсего найдено строк: {len(all_strings)}")
    
    sub_categories = parse_sub_category_data(all_strings)
    
    # Удаляем дубликаты
    unique_sub_categories = []
    seen_names = set()
    
    for sub_cat in sub_categories:
        name = sub_cat.get('name', '')
        
        if name and name not in seen_names:
            seen_names.add(name)
            unique_sub_categories.append(sub_cat)
    
    print(f"Уникальных подкатегорий: {len(unique_sub_categories)}")
    
    inserts = create_insert_statements(unique_sub_categories)
    
    # Сохраняем в файл
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("-- Подкатегории извлечённые из sub_categories.ibd\n")
        f.write("-- Создано автоматически\n\n")
        f.write("USE enb;\n\n")
        f.write("-- Создание таблицы\n")
        f.write("""CREATE TABLE IF NOT EXISTS sub_categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    category_id INT,
    created_at INT,
    updated_at INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

""")
        f.write("-- Вставка данных\n")
        for insert in inserts:
            f.write(insert + "\n")
    
    print(f"\n✅ Создан файл: {OUTPUT_FILE}")
    print(f"   Записей: {len(inserts)}")
    print()
    
    # Показываем первые 15 записей
    print("Первые 15 подкатегорий:")
    for i, sub_cat in enumerate(unique_sub_categories[:15], 1):
        name = sub_cat.get('name', 'N/A')
        print(f"  {i}. {name}")
    
    print("\n" + "="*80)
    print("ГОТОВО!")
    print("="*80)
    print()
    print("Для импорта в MySQL:")
    print(f"  C:\\mysql57\\bin\\mysql.exe -u root < {OUTPUT_FILE}")
    print()

if __name__ == "__main__":
    main()
