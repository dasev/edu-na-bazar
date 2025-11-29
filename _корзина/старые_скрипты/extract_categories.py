"""
Извлечение данных из categories.ibd и создание INSERT запросов
"""
import struct
import re

IBD_FILE = r"C:\python\sites_mysql\enb\categories.ibd"
OUTPUT_FILE = r"C:\python\edu-na-bazar\categories_inserts.sql"

def extract_strings_from_page(page_data):
    """Извлекаем читаемые строки из страницы"""
    # Ищем текстовые данные (ASCII и UTF-8)
    strings = []
    current_string = bytearray()
    
    for byte in page_data:
        if 32 <= byte <= 126 or byte >= 128:  # Печатные символы + UTF-8
            current_string.append(byte)
        else:
            if len(current_string) > 3:  # Минимум 4 символа
                try:
                    s = current_string.decode('utf-8', errors='ignore')
                    if s.strip():
                        strings.append(s.strip())
                except:
                    pass
            current_string = bytearray()
    
    return strings

def parse_ibd_file(filename):
    """Парсим InnoDB файл и извлекаем данные"""
    records = []
    
    with open(filename, 'rb') as f:
        file_size = f.seek(0, 2)
        f.seek(0)
        
        num_pages = file_size // 16384
        print(f"Обрабатываю {num_pages} страниц...")
        
        for page_num in range(num_pages):
            f.seek(page_num * 16384)
            page = f.read(16384)
            
            # Пропускаем системные страницы
            if page_num < 3:
                continue
            
            # Извлекаем строки
            strings = extract_strings_from_page(page)
            
            # Ищем паттерны категорий (id, name, parent_id)
            for i, s in enumerate(strings):
                # Если строка похожа на название категории
                if len(s) > 2 and len(s) < 100:
                    # Проверяем что это не служебная информация
                    if not any(x in s.lower() for x in ['mysql', 'innodb', 'table', 'index', 'primary']):
                        records.append(s)
        
    return records

def create_insert_statements(records):
    """Создаём INSERT запросы"""
    inserts = []
    
    # Уникальные записи
    unique_records = list(set(records))
    unique_records.sort()
    
    print(f"\nНайдено уникальных записей: {len(unique_records)}")
    
    for idx, name in enumerate(unique_records, 1):
        # Экранируем кавычки
        name_escaped = name.replace("'", "''")
        
        # Создаём INSERT
        insert = f"INSERT INTO categories (id, name, parent_id, created_at, updated_at) VALUES ({idx}, '{name_escaped}', NULL, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());"
        inserts.append(insert)
    
    return inserts

def main():
    print("="*80)
    print("ИЗВЛЕЧЕНИЕ ДАННЫХ ИЗ categories.ibd")
    print("="*80)
    print()
    
    print(f"Файл: {IBD_FILE}")
    print()
    
    # Парсим файл
    records = parse_ibd_file(IBD_FILE)
    
    print(f"\nВсего найдено записей: {len(records)}")
    
    # Создаём INSERT запросы
    inserts = create_insert_statements(records)
    
    # Сохраняем в файл
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("-- Категории извлечённые из categories.ibd\n")
        f.write("-- Создано автоматически\n\n")
        f.write("USE enb;\n\n")
        f.write("-- Создание таблицы\n")
        f.write("""CREATE TABLE IF NOT EXISTS categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    parent_id INT DEFAULT NULL,
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
    
    # Показываем первые 10 записей
    print("Первые 10 категорий:")
    for i, insert in enumerate(inserts[:10], 1):
        # Извлекаем название из INSERT
        match = re.search(r"VALUES \(\d+, '([^']+)'", insert)
        if match:
            print(f"  {i}. {match.group(1)}")
    
    print("\n" + "="*80)
    print("ГОТОВО!")
    print("="*80)
    print()
    print("Для импорта в MySQL:")
    print(f"  C:\\mysql57\\bin\\mysql.exe -u root enb < {OUTPUT_FILE}")
    print()

if __name__ == "__main__":
    main()
