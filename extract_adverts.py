"""
Извлечение данных из advert.ibd и создание INSERT запросов
"""
import struct
import re

IBD_FILE = r"C:\python\sites_mysql\enb\advert.ibd"
OUTPUT_FILE = r"C:\python\edu-na-bazar\advert_inserts.sql"

def extract_strings_from_page(page_data):
    """Извлекаем читаемые строки из страницы"""
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

def parse_advert_data(strings):
    """Парсим данные объявлений из строк"""
    adverts = []
    
    # Паттерны
    price_pattern = re.compile(r'\d+[\.,]?\d*')
    phone_pattern = re.compile(r'[\+]?[0-9]{10,15}')
    
    current_advert = {}
    
    for s in strings:
        # Пропускаем служебные данные
        if any(x in s.lower() for x in ['mysql', 'innodb', 'table', 'index', 'primary', 'supremum', 'infimum']):
            continue
        
        # Если строка похожа на название товара (длина 5-200 символов)
        if 5 <= len(s) <= 200 and 'title' not in current_advert:
            # Проверяем что это не URL и не путь
            if not s.startswith('/') and not s.startswith('http'):
                # Проверяем что это не только цифры
                if not s.isdigit():
                    current_advert['title'] = s
                    continue
        
        # Ищем цену
        if 'price' not in current_advert:
            price_match = price_pattern.search(s)
            if price_match and len(s) < 20:
                try:
                    price = float(price_match.group().replace(',', '.'))
                    if 0 < price < 1000000000:  # Разумная цена
                        current_advert['price'] = price
                except:
                    pass
        
        # Ищем телефон
        if 'phone' not in current_advert:
            phone_match = phone_pattern.search(s)
            if phone_match:
                current_advert['phone'] = phone_match.group()
        
        # Если строка похожа на описание (длина 20-500 символов)
        if 20 <= len(s) <= 500 and 'description' not in current_advert:
            if 'title' in current_advert and s != current_advert['title']:
                current_advert['description'] = s
                # Сохраняем объявление если есть заголовок
                if current_advert:
                    adverts.append(current_advert)
                    current_advert = {}
    
    if current_advert and 'title' in current_advert:
        adverts.append(current_advert)
    
    return adverts

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
            
            # Пропускаем системные страницы
            if page_num < 3:
                continue
            
            # Извлекаем строки
            strings = extract_strings_from_page(page)
            all_strings.extend(strings)
            
            # Показываем прогресс каждые 100 страниц
            if page_num % 100 == 0:
                print(f"  Обработано {page_num}/{num_pages} страниц...")
    
    return all_strings

def create_insert_statements(adverts):
    """Создаём INSERT запросы"""
    inserts = []
    
    print(f"\nНайдено объявлений: {len(adverts)}")
    
    for idx, advert in enumerate(adverts, 1):
        title = advert.get('title', f'Товар {idx}')
        description = advert.get('description', '')
        price = advert.get('price', 0)
        phone = advert.get('phone', '')
        
        # Экранируем кавычки
        title_escaped = title.replace("'", "''")[:255]  # Ограничиваем длину
        description_escaped = description.replace("'", "''")[:1000]
        phone_escaped = phone.replace("'", "''")
        
        # Создаём INSERT
        insert = f"""INSERT INTO advert (id, title, description, price, company_id, category_id, contact_phone, status, views, created_at, updated_at) 
VALUES ({idx}, '{title_escaped}', '{description_escaped}', {price}, NULL, NULL, '{phone_escaped}', 1, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());"""
        inserts.append(insert)
    
    return inserts

def main():
    print("="*80)
    print("ИЗВЛЕЧЕНИЕ ДАННЫХ ИЗ advert.ibd")
    print("="*80)
    print()
    
    print(f"Файл: {IBD_FILE}")
    print(f"Размер: {30408704 / 1024 / 1024:.1f} MB")
    print()
    
    # Парсим файл
    all_strings = parse_ibd_file(IBD_FILE)
    
    print(f"\nВсего найдено строк: {len(all_strings)}")
    
    # Парсим данные объявлений
    adverts = parse_advert_data(all_strings)
    
    # Удаляем дубликаты по заголовку
    unique_adverts = []
    seen_titles = set()
    
    for advert in adverts:
        title = advert.get('title', '')
        
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_adverts.append(advert)
    
    print(f"Уникальных объявлений: {len(unique_adverts)}")
    
    # Создаём INSERT запросы
    inserts = create_insert_statements(unique_adverts)
    
    # Сохраняем в файл
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("-- Объявления (товары) извлечённые из advert.ibd\n")
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
        for insert in inserts:
            f.write(insert + "\n")
    
    print(f"\n✅ Создан файл: {OUTPUT_FILE}")
    print(f"   Записей: {len(inserts)}")
    print()
    
    # Показываем первые 10 записей
    print("Первые 10 объявлений:")
    for i, advert in enumerate(unique_adverts[:10], 1):
        title = advert.get('title', 'N/A')
        price = advert.get('price', 0)
        phone = advert.get('phone', 'N/A')
        print(f"  {i}. {title}")
        print(f"     Цена: {price}, Телефон: {phone}")
    
    print("\n" + "="*80)
    print("ГОТОВО!")
    print("="*80)
    print()
    print("Для импорта в MySQL:")
    print(f"  C:\\mysql57\\bin\\mysql.exe -u root < {OUTPUT_FILE}")
    print()

if __name__ == "__main__":
    main()
