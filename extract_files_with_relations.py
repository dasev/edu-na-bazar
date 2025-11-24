"""
Извлечение данных из file.ibd С ПОПЫТКОЙ ВОССТАНОВИТЬ СВЯЗИ
"""
import struct
import re

IBD_FILE = r"C:\python\sites_mysql\enb\file.ibd"
OUTPUT_FILE = r"C:\python\edu-na-bazar\file_inserts_with_relations.sql"

def extract_strings_from_page(page_data):
    """Извлекаем читаемые строки из страницы"""
    strings = []
    current_string = bytearray()
    
    for byte in page_data:
        if 32 <= byte <= 126 or byte >= 128:
            current_string.append(byte)
        else:
            if len(current_string) > 3:
                try:
                    s = current_string.decode('utf-8', errors='ignore')
                    if s.strip():
                        strings.append(s.strip())
                except:
                    pass
            current_string = bytearray()
    
    return strings

def extract_integers_from_page(page_data):
    """Извлекаем целые числа из страницы"""
    integers = []
    
    # Пробуем извлечь 4-байтовые целые числа
    for i in range(0, len(page_data) - 4, 1):
        try:
            # Big-endian
            num = struct.unpack('>I', page_data[i:i+4])[0]
            if 0 < num < 1000000:  # Разумный диапазон для ID
                integers.append(num)
        except:
            pass
    
    return integers

def parse_file_record(strings, integers, start_idx):
    """
    Пытаемся распарсить запись файла
    Структура InnoDB: ID, filename, path, type, advert_id, company_id, size, created_at
    """
    record = {
        'id': None,
        'filename': None,
        'path': None,
        'type': 'image',
        'advert_id': None,
        'company_id': None,
        'size': 0,
        'created_at': None
    }
    
    # Ищем имя файла (с расширением)
    file_pattern = re.compile(r'[a-zA-Z0-9_\-]+\.(jpg|jpeg|png|gif|webp|pdf)', re.IGNORECASE)
    path_pattern = re.compile(r'(/[a-zA-Z0-9_\-/]+\.(jpg|jpeg|png|gif|webp))', re.IGNORECASE)
    
    for s in strings[start_idx:start_idx+10]:  # Смотрим следующие 10 строк
        # Путь к файлу
        path_match = path_pattern.search(s)
        if path_match and not record['path']:
            record['path'] = path_match.group(1)
            record['filename'] = record['path'].split('/')[-1]
        
        # Имя файла
        file_match = file_pattern.search(s)
        if file_match and not record['filename']:
            record['filename'] = file_match.group()
            if not record['path']:
                record['path'] = f'/{record["filename"]}'
    
    return record

def parse_ibd_file_advanced(filename):
    """Парсим InnoDB файл с попыткой извлечь связи"""
    all_records = []
    
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
            
            # Извлекаем строки и числа
            strings = extract_strings_from_page(page)
            integers = extract_integers_from_page(page)
            
            # Ищем записи файлов
            for i, s in enumerate(strings):
                if any(ext in s.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                    record = parse_file_record(strings, integers, i)
                    if record['filename']:
                        # Пытаемся найти ID рядом с записью
                        # В InnoDB данные идут последовательно
                        nearby_integers = integers[:20] if integers else []
                        
                        # Первое число может быть ID записи
                        if nearby_integers:
                            record['id'] = nearby_integers[0]
                            # Следующие числа могут быть advert_id, company_id
                            if len(nearby_integers) > 1:
                                record['advert_id'] = nearby_integers[1] if nearby_integers[1] < 100000 else None
                            if len(nearby_integers) > 2:
                                record['company_id'] = nearby_integers[2] if nearby_integers[2] < 100000 else None
                        
                        all_records.append(record)
            
            if page_num % 100 == 0 and page_num > 0:
                print(f"  Обработано {page_num}/{num_pages} страниц... Найдено записей: {len(all_records)}")
    
    return all_records

def create_insert_statements(records):
    """Создаём INSERT запросы"""
    inserts = []
    
    print(f"\nНайдено записей: {len(records)}")
    
    # Удаляем дубликаты
    unique_records = []
    seen_paths = set()
    
    for record in records:
        path = record.get('path', '')
        if path and path not in seen_paths:
            seen_paths.add(path)
            unique_records.append(record)
    
    print(f"Уникальных записей: {len(unique_records)}")
    
    # Статистика по связям
    with_advert = sum(1 for r in unique_records if r.get('advert_id'))
    with_company = sum(1 for r in unique_records if r.get('company_id'))
    
    print(f"С advert_id: {with_advert}")
    print(f"С company_id: {with_company}")
    
    for idx, record in enumerate(unique_records, 1):
        path = record.get('path', f'/file{idx}.jpg')
        filename = record.get('filename', f'file{idx}.jpg')
        file_type = record.get('type', 'image')
        advert_id = record.get('advert_id', 'NULL')
        company_id = record.get('company_id', 'NULL')
        
        # Экранируем кавычки
        path_escaped = path.replace("'", "''")
        filename_escaped = filename.replace("'", "''")
        
        # Создаём INSERT
        insert = f"""INSERT INTO file (id, filename, path, type, advert_id, company_id, size, created_at) 
VALUES ({idx}, '{filename_escaped}', '{path_escaped}', '{file_type}', {advert_id}, {company_id}, 0, UNIX_TIMESTAMP());"""
        inserts.append(insert)
    
    return inserts

def main():
    print("="*80)
    print("ИЗВЛЕЧЕНИЕ ДАННЫХ ИЗ file.ibd С ПОПЫТКОЙ ВОССТАНОВИТЬ СВЯЗИ")
    print("="*80)
    print()
    
    print(f"Файл: {IBD_FILE}")
    print()
    
    records = parse_ibd_file_advanced(IBD_FILE)
    
    inserts = create_insert_statements(records)
    
    # Сохраняем в файл
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("-- Файлы (фото) извлечённые из file.ibd С ПОПЫТКОЙ ВОССТАНОВИТЬ СВЯЗИ\n")
        f.write("-- Создано автоматически\n\n")
        f.write("USE enb;\n\n")
        f.write("-- Создание таблицы\n")
        f.write("""CREATE TABLE IF NOT EXISTS file (
    id INT PRIMARY KEY AUTO_INCREMENT,
    filename VARCHAR(255) NOT NULL,
    path VARCHAR(500) NOT NULL,
    type VARCHAR(50) DEFAULT 'image',
    advert_id INT,
    company_id INT,
    size INT DEFAULT 0,
    created_at INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

""")
        f.write("-- Вставка данных\n")
        for insert in inserts:
            f.write(insert + "\n")
    
    print(f"\n✅ Создан файл: {OUTPUT_FILE}")
    print(f"   Записей: {len(inserts)}")
    print()
    
    print("="*80)
    print("ГОТОВО!")
    print("="*80)

if __name__ == "__main__":
    main()
