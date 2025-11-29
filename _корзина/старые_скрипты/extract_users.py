"""
Извлечение данных из user.ibd и создание INSERT запросов
"""
import struct
import re

IBD_FILE = r"C:\python\sites_mysql\enb\user.ibd"
OUTPUT_FILE = r"C:\python\edu-na-bazar\user_inserts.sql"

def extract_strings_from_page(page_data):
    """Извлекаем читаемые строки из страницы"""
    strings = []
    current_string = bytearray()
    
    for byte in page_data:
        if 32 <= byte <= 126 or byte >= 128:  # Печатные символы + UTF-8
            current_string.append(byte)
        else:
            if len(current_string) > 2:  # Минимум 3 символа
                try:
                    s = current_string.decode('utf-8', errors='ignore')
                    if s.strip():
                        strings.append(s.strip())
                except:
                    pass
            current_string = bytearray()
    
    return strings

def parse_user_data(strings):
    """Парсим данные пользователей из строк"""
    users = []
    
    # Паттерны для поиска данных
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    phone_pattern = re.compile(r'[\+]?[0-9]{10,15}')
    
    current_user = {}
    
    for s in strings:
        # Пропускаем служебные данные
        if any(x in s.lower() for x in ['mysql', 'innodb', 'table', 'index', 'primary', 'supremum', 'infimum']):
            continue
        
        # Ищем email
        email_match = email_pattern.search(s)
        if email_match:
            email = email_match.group()
            # Если уже есть пользователь, сохраняем его
            if current_user and 'email' in current_user:
                users.append(current_user)
            current_user = {'email': email}
            continue
        
        # Ищем телефон
        phone_match = phone_pattern.search(s)
        if phone_match and 'phone' not in current_user:
            current_user['phone'] = phone_match.group()
            continue
        
        # Если строка похожа на имя (длина 2-50 символов, не URL)
        if 2 <= len(s) <= 50 and 'name' not in current_user:
            if not s.startswith('/') and not s.startswith('http') and '@' not in s:
                # Проверяем что это не число
                if not s.isdigit():
                    current_user['name'] = s
    
    if current_user:
        users.append(current_user)
    
    return users

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

def create_insert_statements(users):
    """Создаём INSERT запросы"""
    inserts = []
    
    print(f"\nНайдено пользователей: {len(users)}")
    
    for idx, user in enumerate(users, 1):
        name = user.get('name', f'User{idx}')
        email = user.get('email', f'user{idx}@example.com')
        phone = user.get('phone', '')
        
        # Экранируем кавычки
        name_escaped = name.replace("'", "''")
        email_escaped = email.replace("'", "''")
        phone_escaped = phone.replace("'", "''")
        
        # Создаём INSERT
        # Пароль не мигрируем (будет NULL или пустой хеш)
        insert = f"""INSERT INTO user (id, name, email, phone, password_hash, role, status, created_at, updated_at, last_login) 
VALUES ({idx}, '{name_escaped}', '{email_escaped}', '{phone_escaped}', NULL, 'user', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), NULL);"""
        inserts.append(insert)
    
    return inserts

def main():
    print("="*80)
    print("ИЗВЛЕЧЕНИЕ ДАННЫХ ИЗ user.ibd")
    print("="*80)
    print()
    
    print(f"Файл: {IBD_FILE}")
    print()
    
    # Парсим файл
    all_strings = parse_ibd_file(IBD_FILE)
    
    print(f"\nВсего найдено строк: {len(all_strings)}")
    
    # Парсим данные пользователей
    users = parse_user_data(all_strings)
    
    # Удаляем дубликаты по email
    unique_users = []
    seen_emails = set()
    
    for user in users:
        email = user.get('email', '')
        
        if email and email not in seen_emails:
            seen_emails.add(email)
            unique_users.append(user)
    
    print(f"Уникальных пользователей: {len(unique_users)}")
    
    # Создаём INSERT запросы
    inserts = create_insert_statements(unique_users)
    
    # Сохраняем в файл
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("-- Пользователи извлечённые из user.ibd\n")
        f.write("-- Создано автоматически\n")
        f.write("-- ВАЖНО: Пароли не мигрируются! Пользователям нужно будет сбросить пароли.\n\n")
        f.write("USE enb;\n\n")
        f.write("-- Создание таблицы\n")
        f.write("""CREATE TABLE IF NOT EXISTS user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    password_hash VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user',
    status INT DEFAULT 1,
    created_at INT,
    updated_at INT,
    last_login INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

""")
        f.write("-- Вставка данных\n")
        for insert in inserts:
            f.write(insert + "\n")
    
    print(f"\n✅ Создан файл: {OUTPUT_FILE}")
    print(f"   Записей: {len(inserts)}")
    print()
    
    # Показываем первые 10 записей
    print("Первые 10 пользователей:")
    for i, user in enumerate(unique_users[:10], 1):
        name = user.get('name', 'N/A')
        email = user.get('email', 'N/A')
        phone = user.get('phone', 'N/A')
        print(f"  {i}. {name}")
        print(f"     Email: {email}, Phone: {phone}")
    
    print("\n" + "="*80)
    print("ГОТОВО!")
    print("="*80)
    print()
    print("⚠️  ВАЖНО: Пароли не мигрируются!")
    print("   Пользователям нужно будет сбросить пароли через функцию восстановления.")
    print()
    print("Для импорта в MySQL:")
    print(f"  C:\\mysql57\\bin\\mysql.exe -u root < {OUTPUT_FILE}")
    print()

if __name__ == "__main__":
    main()
