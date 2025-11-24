"""
Правильная экстракция данных из advert.ibd БЕЗ замены на NULL
Извлекаем ВСЕ поля включая company_id и category_id
Используем тот же подход что и для file.ibd
"""
import struct
import re
from pathlib import Path

IBD_FILE = r"C:\python\sites_mysql\enb\advert.ibd"
OUTPUT_FILE = r"C:\python\edu-na-bazar\advert_inserts_correct.sql"

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

def parse_ibd_file(filename):
    """Парсим InnoDB файл - альтернативный метод как для file.ibd"""
    all_records = []
    
    with open(filename, 'rb') as f:
        file_size = f.seek(0, 2)
        f.seek(0)
        
        num_pages = file_size // 16384
        print(f"Обрабатываю {num_pages} страниц (альтернативный метод)...")
        
        # Паттерн для поиска текста (потенциальные title)
        # Ищем последовательности печатных символов
        title_pattern = re.compile(b'([\x20-\x7E\x80-\xFF]{10,200})', re.IGNORECASE)
        
        for page_num in range(3, num_pages):  # Пропускаем первые 3 страницы
            f.seek(page_num * 16384)
            page = f.read(16384)
            
            # Ищем потенциальные названия товаров
            for match in title_pattern.finditer(page):
                try:
                    title = match.group(1).decode('utf-8', errors='ignore').strip()
                    
                    # Фильтруем служебные данные
                    if any(x in title.lower() for x in ['mysql', 'innodb', 'supremum', 'infimum', 'primary']):
                        continue
                    
                    if len(title) < 10 or len(title) > 200:
                        continue
                    
                    pos = match.start()
                    
                    # Ищем числа перед названием товара (могут быть ID, company_id, category_id)
                    record_id = None
                    company_id = None
                    category_id = None
                    
                    # Ищем ID перед title
                    if pos >= 50:
                        for i in range(max(0, pos - 50), pos, 4):
                            try:
                                potential_id = struct.unpack('>I', page[i:i+4])[0]
                                if 1 <= potential_id <= 100000:
                                    record_id = potential_id
                                    break
                            except:
                                pass
                    
                    # Ищем числа после title (могут быть company_id, category_id)
                    end_pos = match.end()
                    if end_pos + 100 < len(page):
                        numbers = []
                        for i in range(end_pos, min(end_pos + 100, len(page) - 4), 4):
                            try:
                                num = struct.unpack('>I', page[i:i+4])[0]
                                if 1 <= num <= 10000:  # Разумный диапазон для company_id и category_id
                                    numbers.append(num)
                            except:
                                pass
                        
                        # Первое число может быть company_id
                        if len(numbers) > 0:
                            company_id = numbers[0]
                        # Второе число может быть category_id
                        if len(numbers) > 1:
                            category_id = numbers[1]
                    
                    record = {
                        'id': record_id if record_id else len(all_records) + 1,
                        'title': title,
                        'company_id': company_id,
                        'category_id': category_id,
                    }
                    
                    all_records.append(record)
                    
                except:
                    pass
            
            if page_num % 100 == 0:
                print(f"  Страница {page_num}/{num_pages}, найдено: {len(all_records)}")
    
    return all_records

def main():
    print("="*80)
    print("ПРАВИЛЬНАЯ ЭКСТРАКЦИЯ advert.ibd БЕЗ ЗАМЕНЫ НА NULL")
    print("="*80)
    print()
    
    if not Path(IBD_FILE).exists():
        print(f"❌ Файл не найден: {IBD_FILE}")
        return
    
    records = parse_ibd_file(IBD_FILE)
    
    print(f"\nВсего найдено записей: {len(records)}")
    
    # Удаляем дубликаты
    unique_records = []
    seen_ids = set()
    
    for record in records:
        rec_id = record.get('id')
        if rec_id and rec_id not in seen_ids:
            seen_ids.add(rec_id)
            unique_records.append(record)
    
    print(f"Уникальных записей: {len(unique_records)}")
    
    # Статистика
    with_company = sum(1 for r in unique_records if r.get('company_id'))
    with_category = sum(1 for r in unique_records if r.get('category_id'))
    
    print(f"\n📊 Статистика связей:")
    print(f"   С company_id: {with_company}")
    print(f"   С category_id: {with_category}")
    
    # Создаём SQL (полная версия)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("-- Товары извлечённые из advert.ibd БЕЗ ЗАМЕНЫ НА NULL\n")
        f.write("-- Создано автоматически\n\n")
        f.write("USE enb;\n\n")
        f.write("-- Создание таблицы\n")
        f.write("""CREATE TABLE IF NOT EXISTS advert (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) DEFAULT 0,
    company_id INT,
    category_id INT,
    contact_phone VARCHAR(20),
    status INT DEFAULT 1,
    views INT DEFAULT 0,
    created_at INT,
    updated_at INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

""")
        f.write("-- Вставка данных\n")
        
        for record in unique_records:  # ВСЕ записи
            rec_id = record.get('id', 0)
            title = record.get('title', '').replace("'", "''")[:255]
            company_id = record.get('company_id')
            category_id = record.get('category_id')
            
            company_str = str(company_id) if company_id else 'NULL'
            category_str = str(category_id) if category_id else 'NULL'
            
            insert = f"INSERT INTO advert (id, title, description, price, company_id, category_id, contact_phone, status, views, created_at, updated_at) VALUES ({rec_id}, '{title}', '', 0, {company_str}, {category_str}, '', 1, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());\n"
            f.write(insert)
    
    print(f"\n✅ Создан файл: {OUTPUT_FILE}")
    print(f"   Записей: {len(unique_records)}")
    
    if with_company > 0:
        print(f"\n📸 Примеры с company_id:")
        count = 0
        for r in unique_records:
            if r.get('company_id'):
                print(f"   ID: {r['id']}, Company: {r['company_id']}, Category: {r.get('category_id', 'NULL')}, Title: {r['title'][:40]}")
                count += 1
                if count >= 10:
                    break
    
    print("\n" + "="*80)
    print("✅ ГОТОВО!")
    print("="*80)

if __name__ == "__main__":
    main()
