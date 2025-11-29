"""
Правильное извлечение данных из file.ibd
Используем структуру InnoDB страниц
"""
import struct
import sys

IBD_FILE = r"C:\python\sites_mysql\enb\file.ibd"
OUTPUT_FILE = r"C:\python\edu-na-bazar\file_data_proper.sql"

# Константы InnoDB
PAGE_SIZE = 16384  # 16KB - стандартный размер страницы
FIL_PAGE_DATA = 38  # Начало данных на странице
PAGE_NEW_SUPREMUM = 112  # Позиция supremum записи

def read_page_header(page_data):
    """Читаем заголовок страницы"""
    if len(page_data) < 38:
        return None
    
    # FIL Header (38 байт)
    checksum = struct.unpack('>I', page_data[0:4])[0]
    page_number = struct.unpack('>I', page_data[4:8])[0]
    prev_page = struct.unpack('>I', page_data[8:12])[0]
    next_page = struct.unpack('>I', page_data[12:16])[0]
    lsn = struct.unpack('>Q', page_data[16:24])[0]
    page_type = struct.unpack('>H', page_data[24:26])[0]
    
    return {
        'page_number': page_number,
        'page_type': page_type,
        'prev_page': prev_page,
        'next_page': next_page
    }

def extract_varchar(data, offset):
    """Извлекаем VARCHAR поле"""
    if offset >= len(data):
        return None, offset
    
    # Читаем длину (1 или 2 байта)
    length = data[offset]
    offset += 1
    
    if length == 0:
        return '', offset
    
    if offset + length > len(data):
        return None, offset
    
    try:
        value = data[offset:offset+length].decode('utf-8', errors='ignore')
        return value, offset + length
    except:
        return None, offset + length

def extract_int(data, offset, size=4):
    """Извлекаем INT поле"""
    if offset + size > len(data):
        return None, offset
    
    if size == 4:
        value = struct.unpack('>I', data[offset:offset+4])[0]
    elif size == 2:
        value = struct.unpack('>H', data[offset:offset+2])[0]
    elif size == 1:
        value = data[offset]
    else:
        return None, offset
    
    return value, offset + size

def parse_record(record_data):
    """
    Парсим одну запись
    Структура таблицы file:
    - id INT (4 байта)
    - filename VARCHAR(255)
    - path VARCHAR(500)
    - type VARCHAR(50)
    - advert_id INT (4 байта)
    - company_id INT (4 байта)
    - size INT (4 байта)
    - created_at INT (4 байта)
    """
    offset = 0
    record = {}
    
    # Пропускаем Record Header (переменная длина)
    # Обычно 5-6 байт для заголовка записи
    offset = 6
    
    # id INT
    record['id'], offset = extract_int(record_data, offset, 4)
    if record['id'] is None:
        return None
    
    # filename VARCHAR(255)
    record['filename'], offset = extract_varchar(record_data, offset)
    if record['filename'] is None:
        return None
    
    # path VARCHAR(500)
    record['path'], offset = extract_varchar(record_data, offset)
    if record['path'] is None:
        return None
    
    # type VARCHAR(50)
    record['type'], offset = extract_varchar(record_data, offset)
    
    # advert_id INT (может быть NULL)
    record['advert_id'], offset = extract_int(record_data, offset, 4)
    
    # company_id INT (может быть NULL)
    record['company_id'], offset = extract_int(record_data, offset, 4)
    
    # size INT
    record['size'], offset = extract_int(record_data, offset, 4)
    
    # created_at INT
    record['created_at'], offset = extract_int(record_data, offset, 4)
    
    return record

def main():
    print(f"📖 Читаем InnoDB файл: {IBD_FILE}")
    print(f"📄 Размер страницы: {PAGE_SIZE} байт\n")
    
    records = []
    
    with open(IBD_FILE, 'rb') as f:
        page_num = 0
        
        while True:
            page_data = f.read(PAGE_SIZE)
            if not page_data or len(page_data) < PAGE_SIZE:
                break
            
            page_num += 1
            
            # Читаем заголовок страницы
            header = read_page_header(page_data)
            if not header:
                continue
            
            # Тип страницы 17855 (0x45BF) = INDEX page (данные)
            if header['page_type'] != 17855:
                continue
            
            # Извлекаем записи из страницы
            # Начинаем с позиции после заголовка
            offset = PAGE_NEW_SUPREMUM
            
            # Читаем записи пока не дойдем до конца страницы
            while offset < PAGE_SIZE - 100:
                try:
                    record_data = page_data[offset:offset+1000]
                    record = parse_record(record_data)
                    
                    if record and record.get('filename'):
                        # Проверяем что это похоже на реальные данные
                        if (record['filename'].endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')) and
                            len(record['filename']) > 10):
                            records.append(record)
                            
                            if len(records) % 100 == 0:
                                print(f"  Найдено записей: {len(records)}")
                    
                    # Переходим к следующей записи
                    offset += 100  # Примерный размер записи
                    
                except Exception as e:
                    offset += 100
                    continue
            
            if page_num % 100 == 0:
                print(f"  Обработано страниц: {page_num}, найдено записей: {len(records)}")
    
    print(f"\n✅ Всего найдено записей: {len(records)}")
    
    # Удаляем дубликаты по filename
    unique_records = {}
    for record in records:
        key = record['filename']
        if key not in unique_records:
            unique_records[key] = record
    
    print(f"📊 Уникальных записей: {len(unique_records)}")
    
    # Генерируем SQL
    print(f"\n📝 Создаём SQL файл: {OUTPUT_FILE}")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("-- Данные извлечённые из file.ibd\n")
        f.write("-- Правильный парсинг структуры InnoDB\n\n")
        
        for record in unique_records.values():
            filename = record['filename'].replace("'", "''")
            path = record.get('path', '').replace("'", "''")
            file_type = record.get('type', 'image')
            
            sql = f"INSERT INTO temp.file (id, filename, path, type, advert_id, company_id) VALUES ("
            sql += f"{record['id']}, "
            sql += f"'{filename}', "
            sql += f"'{path}', "
            sql += f"'{file_type}', "
            sql += f"{record.get('advert_id') if record.get('advert_id') else 'NULL'}, "
            sql += f"{record.get('company_id') if record.get('company_id') else 'NULL'}"
            sql += ");\n"
            
            f.write(sql)
    
    print(f"✅ Готово! Создано {len(unique_records)} INSERT запросов")
    print(f"📁 Файл сохранён: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
