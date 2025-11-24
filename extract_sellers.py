"""
Извлечение данных из seller.ibd и создание INSERT запросов
"""
import struct
import re

IBD_FILE = r"C:\python\sites_mysql\enb\seller.ibd"
OUTPUT_FILE = r"C:\python\edu-na-bazar\seller_inserts.sql"

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

def parse_seller_data(strings):
    """Парсим данные продавцов из строк"""
    sellers = []
    
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    phone_pattern = re.compile(r'[\+]?[0-9]{10,15}')
    
    current_seller = {}
    
    for s in strings:
        # Пропускаем служебные данные
        if any(x in s.lower() for x in ['mysql', 'innodb', 'table', 'index', 'primary', 'supremum', 'infimum']):
            continue
        
        # Ищем email
        email_match = email_pattern.search(s)
        if email_match:
            if current_seller and 'email' in current_seller:
                sellers.append(current_seller)
            current_seller = {'email': email_match.group()}
            continue
        
        # Ищем телефон
        phone_match = phone_pattern.search(s)
        if phone_match and 'phone' not in current_seller:
            current_seller['phone'] = phone_match.group()
            continue
        
        # Если строка похожа на имя продавца (длина 3-100 символов)
        if 3 <= len(s) <= 100 and 'name' not in current_seller:
            if not s.startswith('/') and not s.startswith('http'):
                if not s.isdigit():
                    current_seller['name'] = s
    
    if current_seller:
        sellers.append(current_seller)
    
    return sellers

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

def create_insert_statements(sellers):
    """Создаём INSERT запросы"""
    inserts = []
    
    print(f"\nНайдено продавцов: {len(sellers)}")
    
    for idx, seller in enumerate(sellers, 1):
        name = seller.get('name', f'Продавец {idx}')
        email = seller.get('email', '')
        phone = seller.get('phone', '')
        
        # Экранируем кавычки
        name_escaped = name.replace("'", "''")
        email_escaped = email.replace("'", "''")
        phone_escaped = phone.replace("'", "''")
        
        # Создаём INSERT
        insert = f"""INSERT INTO seller (id, name, email, phone, user_id, company_id, status, created_at, updated_at) 
VALUES ({idx}, '{name_escaped}', '{email_escaped}', '{phone_escaped}', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());"""
        inserts.append(insert)
    
    return inserts

def main():
    print("="*80)
    print("ИЗВЛЕЧЕНИЕ ДАННЫХ ИЗ seller.ibd")
    print("="*80)
    print()
    
    print(f"Файл: {IBD_FILE}")
    print()
    
    all_strings = parse_ibd_file(IBD_FILE)
    
    print(f"\nВсего найдено строк: {len(all_strings)}")
    
    sellers = parse_seller_data(all_strings)
    
    # Удаляем дубликаты по email
    unique_sellers = []
    seen_emails = set()
    
    for seller in sellers:
        email = seller.get('email', '')
        
        if email and email not in seen_emails:
            seen_emails.add(email)
            unique_sellers.append(seller)
    
    print(f"Уникальных продавцов: {len(unique_sellers)}")
    
    inserts = create_insert_statements(unique_sellers)
    
    # Сохраняем в файл
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("-- Продавцы извлечённые из seller.ibd\n")
        f.write("-- Создано автоматически\n\n")
        f.write("USE enb;\n\n")
        f.write("-- Создание таблицы\n")
        f.write("""CREATE TABLE IF NOT EXISTS seller (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    user_id INT,
    company_id INT,
    status INT DEFAULT 1,
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
    print("Первые 10 продавцов:")
    for i, seller in enumerate(unique_sellers[:10], 1):
        name = seller.get('name', 'N/A')
        email = seller.get('email', 'N/A')
        phone = seller.get('phone', 'N/A')
        print(f"  {i}. {name}")
        print(f"     Email: {email}, Phone: {phone}")
    
    print("\n" + "="*80)
    print("ГОТОВО!")
    print("="*80)
    print()
    print("Для импорта в MySQL:")
    print(f"  C:\\mysql57\\bin\\mysql.exe -u root < {OUTPUT_FILE}")
    print()

if __name__ == "__main__":
    main()
