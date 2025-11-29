"""
Извлечение данных из companies.ibd и создание INSERT запросов
"""
import struct
import re

IBD_FILE = r"C:\python\sites_mysql\enb\companies.ibd"
OUTPUT_FILE = r"C:\python\edu-na-bazar\companies_inserts.sql"

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

def parse_company_data(strings):
    """Парсим данные компаний из строк"""
    companies = []
    
    # Паттерны для поиска данных
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    phone_pattern = re.compile(r'[\+]?[0-9]{10,15}')
    
    current_company = {}
    
    for s in strings:
        # Пропускаем служебные данные
        if any(x in s.lower() for x in ['mysql', 'innodb', 'table', 'index', 'primary', 'supremum', 'infimum']):
            continue
        
        # Ищем email
        email_match = email_pattern.search(s)
        if email_match:
            if current_company:
                companies.append(current_company)
            current_company = {'email': email_match.group()}
            continue
        
        # Ищем телефон
        phone_match = phone_pattern.search(s)
        if phone_match and 'phone' not in current_company:
            current_company['phone'] = phone_match.group()
            continue
        
        # Если строка похожа на название компании (длина 5-100 символов)
        if 5 <= len(s) <= 100 and 'name' not in current_company:
            # Проверяем что это не URL и не путь
            if not s.startswith('/') and not s.startswith('http'):
                current_company['name'] = s
    
    if current_company:
        companies.append(current_company)
    
    return companies

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
    
    return all_strings

def create_insert_statements(companies):
    """Создаём INSERT запросы"""
    inserts = []
    
    print(f"\nНайдено компаний: {len(companies)}")
    
    for idx, company in enumerate(companies, 1):
        name = company.get('name', f'Company {idx}')
        email = company.get('email', '')
        phone = company.get('phone', '')
        
        # Экранируем кавычки
        name_escaped = name.replace("'", "''")
        email_escaped = email.replace("'", "''")
        phone_escaped = phone.replace("'", "''")
        
        # Создаём INSERT
        insert = f"""INSERT INTO companies (id, name, description, user_id, phone, email, address, logo, status, created_at, updated_at, category_id) 
VALUES ({idx}, '{name_escaped}', NULL, NULL, '{phone_escaped}', '{email_escaped}', NULL, NULL, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);"""
        inserts.append(insert)
    
    return inserts

def main():
    print("="*80)
    print("ИЗВЛЕЧЕНИЕ ДАННЫХ ИЗ companies.ibd")
    print("="*80)
    print()
    
    print(f"Файл: {IBD_FILE}")
    print()
    
    # Парсим файл
    all_strings = parse_ibd_file(IBD_FILE)
    
    print(f"\nВсего найдено строк: {len(all_strings)}")
    
    # Парсим данные компаний
    companies = parse_company_data(all_strings)
    
    # Удаляем дубликаты по email
    unique_companies = []
    seen_emails = set()
    seen_names = set()
    
    for company in companies:
        email = company.get('email', '')
        name = company.get('name', '')
        
        if email and email not in seen_emails:
            seen_emails.add(email)
            unique_companies.append(company)
        elif name and name not in seen_names and not email:
            seen_names.add(name)
            unique_companies.append(company)
    
    print(f"Уникальных компаний: {len(unique_companies)}")
    
    # Создаём INSERT запросы
    inserts = create_insert_statements(unique_companies)
    
    # Сохраняем в файл
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("-- Компании извлечённые из companies.ibd\n")
        f.write("-- Создано автоматически\n\n")
        f.write("USE enb;\n\n")
        f.write("-- Создание таблицы\n")
        f.write("""CREATE TABLE IF NOT EXISTS companies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    user_id INT,
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    logo VARCHAR(255),
    status INT DEFAULT 1,
    created_at INT,
    updated_at INT,
    category_id INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

""")
        f.write("-- Вставка данных\n")
        for insert in inserts:
            f.write(insert + "\n")
    
    print(f"\n✅ Создан файл: {OUTPUT_FILE}")
    print(f"   Записей: {len(inserts)}")
    print()
    
    # Показываем первые 10 записей
    print("Первые 10 компаний:")
    for i, company in enumerate(unique_companies[:10], 1):
        name = company.get('name', 'N/A')
        email = company.get('email', 'N/A')
        phone = company.get('phone', 'N/A')
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
