"""
Извлечение данных из file.ibd и создание INSERT запросов
"""
import struct
import re

IBD_FILE = r"C:\python\sites_mysql\enb\file.ibd"
OUTPUT_FILE = r"C:\python\edu-na-bazar\file_inserts.sql"

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

def parse_file_data(strings):
    """Парсим данные файлов из строк"""
    files = []
    
    # Паттерны для поиска путей к файлам
    file_pattern = re.compile(r'[a-zA-Z0-9_\-]+\.(jpg|jpeg|png|gif|webp|pdf|doc|docx)', re.IGNORECASE)
    path_pattern = re.compile(r'(/[a-zA-Z0-9_\-/]+\.(jpg|jpeg|png|gif|webp))', re.IGNORECASE)
    
    for s in strings:
        # Пропускаем служебные данные
        if any(x in s.lower() for x in ['mysql', 'innodb', 'table', 'index', 'primary', 'supremum', 'infimum']):
            continue
        
        # Ищем пути к файлам
        path_match = path_pattern.search(s)
        if path_match:
            file_path = path_match.group(1)
            files.append({
                'path': file_path,
                'filename': file_path.split('/')[-1],
                'type': 'image'
            })
            continue
        
        # Ищем имена файлов
        file_match = file_pattern.search(s)
        if file_match:
            filename = file_match.group()
            ext = file_match.group(1).lower()
            file_type = 'image' if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp'] else 'document'
            
            files.append({
                'path': f'/uploads/{filename}',
                'filename': filename,
                'type': file_type
            })
    
    return files

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
            
            # Показываем прогресс каждые 100 страниц
            if page_num % 100 == 0 and page_num > 0:
                print(f"  Обработано {page_num}/{num_pages} страниц...")
    
    return all_strings

def create_insert_statements(files):
    """Создаём INSERT запросы"""
    inserts = []
    
    print(f"\nНайдено файлов: {len(files)}")
    
    for idx, file_data in enumerate(files, 1):
        path = file_data.get('path', f'/uploads/file{idx}.jpg')
        filename = file_data.get('filename', f'file{idx}.jpg')
        file_type = file_data.get('type', 'image')
        
        # Экранируем кавычки
        path_escaped = path.replace("'", "''")
        filename_escaped = filename.replace("'", "''")
        
        # Создаём INSERT
        insert = f"""INSERT INTO file (id, filename, path, type, advert_id, company_id, size, created_at) 
VALUES ({idx}, '{filename_escaped}', '{path_escaped}', '{file_type}', NULL, NULL, 0, UNIX_TIMESTAMP());"""
        inserts.append(insert)
    
    return inserts

def main():
    print("="*80)
    print("ИЗВЛЕЧЕНИЕ ДАННЫХ ИЗ file.ibd")
    print("="*80)
    print()
    
    print(f"Файл: {IBD_FILE}")
    print(f"Размер: {11534336 / 1024 / 1024:.1f} MB")
    print()
    
    all_strings = parse_ibd_file(IBD_FILE)
    
    print(f"\nВсего найдено строк: {len(all_strings)}")
    
    files = parse_file_data(all_strings)
    
    # Удаляем дубликаты по пути
    unique_files = []
    seen_paths = set()
    
    for file_data in files:
        path = file_data.get('path', '')
        
        if path and path not in seen_paths:
            seen_paths.add(path)
            unique_files.append(file_data)
    
    print(f"Уникальных файлов: {len(unique_files)}")
    
    inserts = create_insert_statements(unique_files)
    
    # Сохраняем в файл
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("-- Файлы (фото) извлечённые из file.ibd\n")
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
    
    # Показываем первые 10 записей
    print("Первые 10 файлов:")
    for i, file_data in enumerate(unique_files[:10], 1):
        filename = file_data.get('filename', 'N/A')
        file_type = file_data.get('type', 'N/A')
        print(f"  {i}. {filename} ({file_type})")
    
    print("\n" + "="*80)
    print("ГОТОВО!")
    print("="*80)
    print()
    print("Для импорта в MySQL:")
    print(f"  C:\\mysql57\\bin\\mysql.exe -u root < {OUTPUT_FILE}")
    print()

if __name__ == "__main__":
    main()
