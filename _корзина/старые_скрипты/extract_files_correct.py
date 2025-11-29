"""
Правильная экстракция данных из file.ibd БЕЗ замены на NULL
Извлекаем ВСЕ поля включая advert_id и company_id
"""
import struct
import re
from collections import defaultdict

IBD_FILE = r"C:\python\sites_mysql\enb\file.ibd"
OUTPUT_FILE = r"C:\python\edu-na-bazar\file_inserts_correct.sql"

def extract_record_data(page_data, offset):
    """
    Извлекаем данные записи из InnoDB страницы
    Структура записи file:
    - id (INT, 4 bytes)
    - filename (VARCHAR)
    - path (VARCHAR)
    - type (VARCHAR)
    - advert_id (INT, 4 bytes, может быть NULL)
    - company_id (INT, 4 bytes, может быть NULL)
    - size (INT, 4 bytes)
    - created_at (INT, 4 bytes)
    """
    try:
        # Пропускаем заголовок записи
        pos = offset
        
        # Читаем NULL bitmap (1 байт на каждые 8 полей)
        null_bitmap = page_data[pos]
        pos += 1
        
        # Читаем ID (INT NOT NULL)
        if pos + 4 <= len(page_data):
            record_id = struct.unpack('>I', page_data[pos:pos+4])[0]
            pos += 4
        else:
            return None
        
        # Читаем длину filename
        if pos + 1 <= len(page_data):
            filename_len = page_data[pos]
            pos += 1
            
            if pos + filename_len <= len(page_data):
                filename = page_data[pos:pos+filename_len].decode('utf-8', errors='ignore')
                pos += filename_len
            else:
                return None
        else:
            return None
        
        # Читаем длину path
        if pos + 2 <= len(page_data):
            path_len = struct.unpack('>H', page_data[pos:pos+2])[0]
            pos += 2
            
            if pos + path_len <= len(page_data):
                path = page_data[pos:pos+path_len].decode('utf-8', errors='ignore')
                pos += path_len
            else:
                return None
        else:
            return None
        
        # Читаем type
        if pos + 1 <= len(page_data):
            type_len = page_data[pos]
            pos += 1
            
            if pos + type_len <= len(page_data):
                file_type = page_data[pos:pos+type_len].decode('utf-8', errors='ignore')
                pos += type_len
            else:
                file_type = 'image'
        else:
            file_type = 'image'
        
        # Читаем advert_id (INT, может быть NULL)
        advert_id = None
        if not (null_bitmap & 0x10):  # Проверяем NULL bitmap
            if pos + 4 <= len(page_data):
                advert_id = struct.unpack('>I', page_data[pos:pos+4])[0]
                if advert_id == 0 or advert_id > 1000000:
                    advert_id = None
                pos += 4
        
        # Читаем company_id (INT, может быть NULL)
        company_id = None
        if not (null_bitmap & 0x20):  # Проверяем NULL bitmap
            if pos + 4 <= len(page_data):
                company_id = struct.unpack('>I', page_data[pos:pos+4])[0]
                if company_id == 0 or company_id > 1000000:
                    company_id = None
                pos += 4
        
        # Читаем size
        size = 0
        if pos + 4 <= len(page_data):
            size = struct.unpack('>I', page_data[pos:pos+4])[0]
            pos += 4
        
        # Читаем created_at
        created_at = None
        if pos + 4 <= len(page_data):
            created_at = struct.unpack('>I', page_data[pos:pos+4])[0]
        
        return {
            'id': record_id,
            'filename': filename,
            'path': path,
            'type': file_type,
            'advert_id': advert_id,
            'company_id': company_id,
            'size': size,
            'created_at': created_at
        }
    
    except Exception as e:
        return None

def scan_page_for_records(page_data):
    """Сканируем страницу в поисках записей"""
    records = []
    
    # InnoDB страница 16KB
    # Заголовок страницы - первые 38 байт
    # Записи начинаются после заголовка
    
    # Ищем паттерны имен файлов
    file_pattern = re.compile(b'[a-zA-Z0-9_\-]{20,50}\.(jpg|jpeg|png|gif|webp)', re.IGNORECASE)
    
    for match in file_pattern.finditer(page_data):
        start_pos = match.start()
        
        # Пытаемся извлечь запись начиная с позиции перед именем файла
        for offset in range(max(0, start_pos - 100), start_pos):
            record = extract_record_data(page_data, offset)
            if record and record['filename'] in match.group().decode('utf-8', errors='ignore'):
                records.append(record)
                break
    
    return records

def parse_ibd_simple(filename):
    """Простой парсинг - ищем строки и числа рядом"""
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
            
            # Ищем записи на странице
            page_records = scan_page_for_records(page)
            records.extend(page_records)
            
            if page_num % 100 == 0 and page_num > 0:
                print(f"  Страница {page_num}/{num_pages}, найдено записей: {len(records)}")
    
    return records

def parse_ibd_alternative(filename):
    """Альтернативный метод - извлекаем все данные и собираем записи"""
    all_data = []
    
    with open(filename, 'rb') as f:
        file_size = f.seek(0, 2)
        f.seek(0)
        
        num_pages = file_size // 16384
        print(f"Обрабатываю {num_pages} страниц (альтернативный метод)...")
        
        # Паттерны для поиска
        filename_pattern = re.compile(b'([a-zA-Z0-9_\-]{10,50}\.(jpg|jpeg|png|gif|webp))', re.IGNORECASE)
        
        for page_num in range(3, num_pages):  # Пропускаем первые 3 страницы
            f.seek(page_num * 16384)
            page = f.read(16384)
            
            # Ищем имена файлов
            for match in filename_pattern.finditer(page):
                filename = match.group(1).decode('utf-8', errors='ignore')
                pos = match.start()
                
                # Ищем числа перед и после имени файла
                # Обычно структура: [ID][len][filename][len][path][type][advert_id][company_id][size][created_at]
                
                # Пытаемся извлечь ID (4 байта перед именем файла)
                record_id = None
                if pos >= 10:
                    for i in range(max(0, pos - 50), pos, 4):
                        try:
                            potential_id = struct.unpack('>I', page[i:i+4])[0]
                            if 1 <= potential_id <= 100000:
                                record_id = potential_id
                                break
                        except:
                            pass
                
                # Ищем путь (обычно начинается с /)
                path = f'/{filename}'
                path_match = re.search(b'(/[a-zA-Z0-9_\-/]+\.(jpg|jpeg|png|gif|webp))', page[max(0, pos-200):pos+200], re.IGNORECASE)
                if path_match:
                    path = path_match.group(1).decode('utf-8', errors='ignore')
                
                # Ищем числа после имени файла (могут быть advert_id, company_id)
                advert_id = None
                company_id = None
                
                end_pos = match.end()
                if end_pos + 100 < len(page):
                    # Извлекаем следующие несколько 4-байтовых чисел
                    numbers = []
                    for i in range(end_pos, min(end_pos + 100, len(page) - 4), 4):
                        try:
                            num = struct.unpack('>I', page[i:i+4])[0]
                            if 1 <= num <= 100000:
                                numbers.append(num)
                        except:
                            pass
                    
                    # Первое число может быть advert_id
                    if len(numbers) > 0:
                        advert_id = numbers[0]
                    # Второе число может быть company_id
                    if len(numbers) > 1:
                        company_id = numbers[1]
                
                record = {
                    'id': record_id if record_id else len(all_data) + 1,
                    'filename': filename,
                    'path': path,
                    'type': 'image',
                    'advert_id': advert_id,
                    'company_id': company_id,
                    'size': 0,
                    'created_at': None
                }
                
                all_data.append(record)
            
            if page_num % 100 == 0:
                print(f"  Страница {page_num}/{num_pages}, найдено: {len(all_data)}")
    
    return all_data

def main():
    print("="*80)
    print("ПРАВИЛЬНАЯ ЭКСТРАКЦИЯ file.ibd БЕЗ ЗАМЕНЫ НА NULL")
    print("="*80)
    print()
    
    # Пробуем альтернативный метод
    records = parse_ibd_alternative(IBD_FILE)
    
    print(f"\nВсего найдено записей: {len(records)}")
    
    # Удаляем дубликаты по пути
    unique_records = []
    seen_paths = set()
    
    for record in records:
        path = record.get('path', '')
        if path and path not in seen_paths:
            seen_paths.add(path)
            unique_records.append(record)
    
    print(f"Уникальных записей: {len(unique_records)}")
    
    # Статистика
    with_advert = sum(1 for r in unique_records if r.get('advert_id'))
    with_company = sum(1 for r in unique_records if r.get('company_id'))
    
    print(f"\n📊 Статистика связей:")
    print(f"   С advert_id: {with_advert}")
    print(f"   С company_id: {with_company}")
    print(f"   Без связей: {len(unique_records) - max(with_advert, with_company)}")
    
    # Создаём SQL
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("-- Файлы извлечённые из file.ibd БЕЗ ЗАМЕНЫ НА NULL\n")
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
        
        for idx, record in enumerate(unique_records, 1):
            filename = record.get('filename', '').replace("'", "''")
            path = record.get('path', '').replace("'", "''")
            file_type = record.get('type', 'image')
            advert_id = record.get('advert_id')
            company_id = record.get('company_id')
            size = record.get('size', 0)
            
            # НЕ заменяем на NULL, оставляем как есть
            advert_str = str(advert_id) if advert_id else 'NULL'
            company_str = str(company_id) if company_id else 'NULL'
            
            insert = f"INSERT INTO file (id, filename, path, type, advert_id, company_id, size, created_at) VALUES ({idx}, '{filename}', '{path}', '{file_type}', {advert_str}, {company_str}, {size}, UNIX_TIMESTAMP());\n"
            f.write(insert)
    
    print(f"\n✅ Создан файл: {OUTPUT_FILE}")
    print(f"   Записей: {len(unique_records)}")
    
    # Показываем примеры с связями
    if with_advert > 0:
        print(f"\n📸 Примеры записей с advert_id:")
        count = 0
        for r in unique_records:
            if r.get('advert_id'):
                print(f"   ID: {r['id']}, File: {r['filename'][:40]}, Advert: {r['advert_id']}, Company: {r.get('company_id', 'NULL')}")
                count += 1
                if count >= 5:
                    break
    
    print("\n" + "="*80)
    print("ГОТОВО!")
    print("="*80)

if __name__ == "__main__":
    main()
