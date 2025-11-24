"""
Извлечение данных из file.ibd с правильной обработкой advert_id
Избегаем дублирования записей
"""
import struct
import re
from collections import defaultdict

IBD_FILE = r"C:\python\sites_mysql\enb\file.ibd"
OUTPUT_FILE = r"C:\python\edu-na-bazar\file_inserts_v2.sql"

# Для отслеживания уникальных записей
seen_files = set()
files_by_advert = defaultdict(list)

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
    
    if len(current_string) > 3:
        try:
            s = current_string.decode('utf-8', errors='ignore')
            if s.strip():
                strings.append(s.strip())
        except:
            pass
    
    return strings

def parse_file_record(data_chunk):
    """
    Парсим одну запись файла
    Структура: id, filename, path, type, advert_id, company_id
    """
    # Ищем паттерны
    filename_pattern = re.compile(r'([a-zA-Z0-9_\-]{20,})\.(jpg|jpeg|png|gif|webp)', re.IGNORECASE)
    path_pattern = re.compile(r'(/[a-zA-Z0-9_\-/]+\.(jpg|jpeg|png|gif|webp))', re.IGNORECASE)
    number_pattern = re.compile(r'\b(\d+)\b')
    
    filename_match = filename_pattern.search(data_chunk)
    path_match = path_pattern.search(data_chunk)
    
    if not (filename_match or path_match):
        return None
    
    # Извлекаем данные
    filename = filename_match.group(0) if filename_match else None
    path = path_match.group(1) if path_match else None
    
    if not filename and path:
        filename = path.split('/')[-1]
    if not path and filename:
        path = f"/{filename}"
    
    # Ищем числа (потенциальные ID)
    numbers = number_pattern.findall(data_chunk)
    
    # Первое число - обычно ID записи
    # Последние числа - advert_id или company_id
    record_id = None
    advert_id = None
    company_id = None
    
    if numbers:
        # Фильтруем слишком большие числа (не ID)
        valid_numbers = [int(n) for n in numbers if len(n) <= 10 and int(n) < 1000000]
        
        if valid_numbers:
            record_id = valid_numbers[0] if len(valid_numbers) > 0 else None
            advert_id = valid_numbers[-1] if len(valid_numbers) > 1 else None
            company_id = valid_numbers[-2] if len(valid_numbers) > 2 else None
    
    return {
        'id': record_id,
        'filename': filename,
        'path': path,
        'type': 'image',
        'advert_id': advert_id,
        'company_id': company_id
    }

def main():
    print(f"📖 Читаем файл: {IBD_FILE}")
    
    with open(IBD_FILE, 'rb') as f:
        # Читаем файл страницами (16KB - стандартный размер страницы InnoDB)
        page_size = 16384
        page_num = 0
        total_records = 0
        
        while True:
            page_data = f.read(page_size)
            if not page_data:
                break
            
            page_num += 1
            
            # Извлекаем строки
            strings = extract_strings_from_page(page_data)
            
            # Объединяем строки в блоки данных
            data_chunk = ' '.join(strings)
            
            # Парсим записи
            if data_chunk:
                record = parse_file_record(data_chunk)
                if record and record['filename']:
                    # Создаём уникальный ключ
                    key = (record['filename'], record['path'])
                    
                    # Проверяем дубликаты
                    if key not in seen_files:
                        seen_files.add(key)
                        
                        # Группируем по advert_id
                        if record['advert_id']:
                            files_by_advert[record['advert_id']].append(record)
                        else:
                            files_by_advert[0].append(record)
                        
                        total_records += 1
            
            if page_num % 1000 == 0:
                print(f"  Обработано страниц: {page_num}, найдено уникальных файлов: {total_records}")
    
    print(f"\n✅ Всего найдено уникальных файлов: {total_records}")
    print(f"📊 Файлов с advert_id: {sum(1 for k in files_by_advert.keys() if k > 0)}")
    print(f"📊 Файлов без advert_id: {len(files_by_advert.get(0, []))}")
    
    # Генерируем SQL
    print(f"\n📝 Создаём SQL файл: {OUTPUT_FILE}")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("-- Импорт файлов из file.ibd\n")
        f.write("-- Уникальные записи без дублирования\n\n")
        
        insert_count = 0
        
        for advert_id in sorted(files_by_advert.keys()):
            files = files_by_advert[advert_id]
            
            if advert_id > 0:
                f.write(f"\n-- Файлы для advert_id = {advert_id} ({len(files)} шт)\n")
            else:
                f.write(f"\n-- Файлы без advert_id ({len(files)} шт)\n")
            
            for record in files:
                filename = record['filename'].replace("'", "''")
                path = record['path'].replace("'", "''") if record['path'] else ''
                
                sql = f"INSERT INTO temp.file (filename, path, type, advert_id, company_id) VALUES ("
                sql += f"'{filename}', "
                sql += f"'{path}', "
                sql += f"'image', "
                sql += f"{record['advert_id'] if record['advert_id'] else 'NULL'}, "
                sql += f"{record['company_id'] if record['company_id'] else 'NULL'}"
                sql += ");\n"
                
                f.write(sql)
                insert_count += 1
        
        f.write(f"\n-- Всего INSERT запросов: {insert_count}\n")
    
    print(f"✅ Готово! Создано {insert_count} INSERT запросов")
    print(f"📁 Файл сохранён: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
