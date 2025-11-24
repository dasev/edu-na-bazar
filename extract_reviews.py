"""
Извлечение данных из review.ibd и создание INSERT запросов
"""
import struct
import re

IBD_FILE = r"C:\python\sites_mysql\enb\review.ibd"
OUTPUT_FILE = r"C:\python\edu-na-bazar\review_inserts.sql"

def extract_strings_from_page(page_data):
    """Извлекаем читаемые строки из страницы"""
    strings = []
    current_string = bytearray()
    
    for byte in page_data:
        if 32 <= byte <= 126 or byte >= 128:  # Печатные символы + UTF-8
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

def parse_review_data(strings):
    """Парсим данные отзывов из строк"""
    reviews = []
    
    current_review = {}
    
    for s in strings:
        # Пропускаем служебные данные
        if any(x in s.lower() for x in ['mysql', 'innodb', 'table', 'index', 'primary', 'supremum', 'infimum']):
            continue
        
        # Если строка похожа на текст отзыва (длина 10-500 символов)
        if 10 <= len(s) <= 500:
            if not s.startswith('/') and not s.startswith('http'):
                if not s.isdigit():
                    current_review['text'] = s
                    # Сохраняем отзыв
                    if current_review:
                        reviews.append(current_review)
                        current_review = {}
    
    if current_review:
        reviews.append(current_review)
    
    return reviews

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

def create_insert_statements(reviews):
    """Создаём INSERT запросы"""
    inserts = []
    
    print(f"\nНайдено отзывов: {len(reviews)}")
    
    for idx, review in enumerate(reviews, 1):
        text = review.get('text', f'Отзыв {idx}')
        
        # Экранируем кавычки
        text_escaped = text.replace("'", "''")[:1000]
        
        # Создаём INSERT
        insert = f"""INSERT INTO review (id, company_id, user_id, rating, text, status, created_at, updated_at) 
VALUES ({idx}, NULL, NULL, 5, '{text_escaped}', 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());"""
        inserts.append(insert)
    
    return inserts

def main():
    print("="*80)
    print("ИЗВЛЕЧЕНИЕ ДАННЫХ ИЗ review.ibd")
    print("="*80)
    print()
    
    print(f"Файл: {IBD_FILE}")
    print()
    
    all_strings = parse_ibd_file(IBD_FILE)
    
    print(f"\nВсего найдено строк: {len(all_strings)}")
    
    reviews = parse_review_data(all_strings)
    
    # Удаляем дубликаты
    unique_reviews = []
    seen_texts = set()
    
    for review in reviews:
        text = review.get('text', '')
        
        if text and text not in seen_texts:
            seen_texts.add(text)
            unique_reviews.append(review)
    
    print(f"Уникальных отзывов: {len(unique_reviews)}")
    
    inserts = create_insert_statements(unique_reviews)
    
    # Сохраняем в файл
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("-- Отзывы извлечённые из review.ibd\n")
        f.write("-- Создано автоматически\n\n")
        f.write("USE enb;\n\n")
        f.write("-- Создание таблицы\n")
        f.write("""CREATE TABLE IF NOT EXISTS review (
    id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT,
    user_id INT,
    rating INT DEFAULT 5,
    text TEXT,
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
    
    # Показываем первые 5 записей
    print("Первые 5 отзывов:")
    for i, review in enumerate(unique_reviews[:5], 1):
        text = review.get('text', 'N/A')[:100]
        print(f"  {i}. {text}...")
    
    print("\n" + "="*80)
    print("ГОТОВО!")
    print("="*80)
    print()
    print("Для импорта в MySQL:")
    print(f"  C:\\mysql57\\bin\\mysql.exe -u root < {OUTPUT_FILE}")
    print()

if __name__ == "__main__":
    main()
