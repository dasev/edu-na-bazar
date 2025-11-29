"""
Анализ структуры старой MySQL базы enb
Сравнение с новой структурой PostgreSQL
"""
import pymysql

# Подключение к MySQL
try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='enb',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    print("✅ Подключение к MySQL успешно\n")
    
    with connection.cursor() as cursor:
        # Анализ таблицы advert (объявления -> products)
        print("=" * 80)
        print("📦 ТАБЛИЦА: advert (объявления) -> products")
        print("=" * 80)
        cursor.execute("DESCRIBE advert")
        advert_fields = cursor.fetchall()
        for field in advert_fields:
            print(f"  {field['Field']:30} {field['Type']:20} {field['Null']:5} {field['Key']:5} {field['Default']}")
        
        cursor.execute("SELECT COUNT(*) as count FROM advert")
        count = cursor.fetchone()
        print(f"\n📊 Всего записей: {count['count']}\n")
        
        # Анализ таблицы companies (компании -> store_owners)
        print("=" * 80)
        print("🏪 ТАБЛИЦА: companies (компании) -> store_owners")
        print("=" * 80)
        cursor.execute("DESCRIBE companies")
        companies_fields = cursor.fetchall()
        for field in companies_fields:
            print(f"  {field['Field']:30} {field['Type']:20} {field['Null']:5} {field['Key']:5} {field['Default']}")
        
        cursor.execute("SELECT COUNT(*) as count FROM companies")
        count = cursor.fetchone()
        print(f"\n📊 Всего записей: {count['count']}\n")
        
        # Анализ таблицы user (пользователи -> users)
        print("=" * 80)
        print("👤 ТАБЛИЦА: user (пользователи) -> users")
        print("=" * 80)
        cursor.execute("DESCRIBE user")
        user_fields = cursor.fetchall()
        for field in user_fields:
            print(f"  {field['Field']:30} {field['Type']:20} {field['Null']:5} {field['Key']:5} {field['Default']}")
        
        cursor.execute("SELECT COUNT(*) as count FROM user WHERE status = 10")
        count = cursor.fetchone()
        print(f"\n📊 Активных пользователей: {count['count']}\n")
        
        # Анализ таблицы file (файлы -> product_images)
        print("=" * 80)
        print("🖼️  ТАБЛИЦА: file (файлы) -> product_images")
        print("=" * 80)
        cursor.execute("DESCRIBE file")
        file_fields = cursor.fetchall()
        for field in file_fields:
            print(f"  {field['Field']:30} {field['Type']:20} {field['Null']:5} {field['Key']:5} {field['Default']}")
        
        cursor.execute("SELECT COUNT(*) as count FROM file")
        count = cursor.fetchone()
        print(f"\n📊 Всего файлов: {count['count']}\n")
        
        # Анализ таблицы categories
        print("=" * 80)
        print("📁 ТАБЛИЦА: categories -> categories")
        print("=" * 80)
        cursor.execute("DESCRIBE categories")
        categories_fields = cursor.fetchall()
        for field in categories_fields:
            print(f"  {field['Field']:30} {field['Type']:20} {field['Null']:5} {field['Key']:5} {field['Default']}")
        
        cursor.execute("SELECT COUNT(*) as count FROM categories")
        count = cursor.fetchone()
        print(f"\n📊 Всего категорий: {count['count']}\n")
        
        # Примеры данных
        print("=" * 80)
        print("📋 ПРИМЕРЫ ДАННЫХ")
        print("=" * 80)
        
        print("\n🏪 Пример компании:")
        cursor.execute("SELECT * FROM companies LIMIT 1")
        company = cursor.fetchone()
        if company:
            for key, value in company.items():
                print(f"  {key:30} = {value}")
        
        print("\n📦 Пример объявления:")
        cursor.execute("SELECT * FROM advert LIMIT 1")
        advert = cursor.fetchone()
        if advert:
            for key, value in advert.items():
                print(f"  {key:30} = {value}")
        
        print("\n👤 Пример пользователя:")
        cursor.execute("SELECT * FROM user WHERE status = 10 LIMIT 1")
        user = cursor.fetchone()
        if user:
            for key, value in user.items():
                print(f"  {key:30} = {value}")
        
        print("\n🖼️  Пример файла:")
        cursor.execute("SELECT * FROM file LIMIT 1")
        file = cursor.fetchone()
        if file:
            for key, value in file.items():
                print(f"  {key:30} = {value}")
    
    connection.close()
    print("\n✅ Анализ завершен")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    print("\n💡 Убедитесь что:")
    print("  1. MySQL сервер запущен")
    print("  2. База данных 'enb' существует")
    print("  3. Пароль root правильный (по умолчанию пустой)")
