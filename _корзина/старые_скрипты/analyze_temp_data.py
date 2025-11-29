"""
Анализ данных в схеме temp для маппинга на основные таблицы
"""
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar"


async def analyze_temp_schema():
    """Анализирует структуру и данные в схеме temp"""
    
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        print("="*80)
        print("📊 АНАЛИЗ ДАННЫХ В СХЕМЕ TEMP")
        print("="*80)
        print()
        
        # 1. Список таблиц и количество записей
        print("1️⃣ ТАБЛИЦЫ И КОЛИЧЕСТВО ЗАПИСЕЙ:")
        print("-"*80)
        
        tables = ['seller', 'categories', 'companies', 'sub_categories', 
                  'user', 'review', 'file', 'advert']
        
        for table in tables:
            try:
                result = await session.execute(text(f"SELECT COUNT(*) FROM temp.{table}"))
                count = result.scalar()
                print(f"   temp.{table:20} → {count:>6} записей")
            except Exception as e:
                print(f"   temp.{table:20} → ❌ Ошибка: {e}")
        
        print()
        
        # 2. Структура temp.categories
        print("2️⃣ СТРУКТУРА temp.categories:")
        print("-"*80)
        result = await session.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'temp' AND table_name = 'categories'
            ORDER BY ordinal_position
        """))
        for row in result:
            print(f"   {row[0]:20} {row[1]:15} {'NULL' if row[2] == 'YES' else 'NOT NULL'}")
        
        # Примеры данных
        result = await session.execute(text("SELECT * FROM temp.categories LIMIT 3"))
        print("\n   Примеры данных:")
        for row in result:
            print(f"   ID: {row[0]}, Name: {row[1]}, Parent: {row[2]}")
        
        print()
        
        # 3. Структура temp.companies
        print("3️⃣ СТРУКТУРА temp.companies:")
        print("-"*80)
        result = await session.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'temp' AND table_name = 'companies'
            ORDER BY ordinal_position
        """))
        for row in result:
            print(f"   {row[0]:20} {row[1]:15} {'NULL' if row[2] == 'YES' else 'NOT NULL'}")
        
        # Примеры данных
        result = await session.execute(text("SELECT id, name, phone, email, address FROM temp.companies LIMIT 3"))
        print("\n   Примеры данных:")
        for row in result:
            print(f"   ID: {row[0]}, Name: {row[1][:30]}, Phone: {row[2]}, Email: {row[3][:30]}")
        
        print()
        
        # 4. Структура temp.user
        print("4️⃣ СТРУКТУРА temp.user:")
        print("-"*80)
        result = await session.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'temp' AND table_name = 'user'
            ORDER BY ordinal_position
        """))
        for row in result:
            print(f"   {row[0]:20} {row[1]:15} {'NULL' if row[2] == 'YES' else 'NOT NULL'}")
        
        # Примеры данных
        result = await session.execute(text("SELECT id, name, email, phone FROM temp.user LIMIT 3"))
        print("\n   Примеры данных:")
        for row in result:
            print(f"   ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Phone: {row[3]}")
        
        print()
        
        # 5. Структура temp.advert
        print("5️⃣ СТРУКТУРА temp.advert:")
        print("-"*80)
        result = await session.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'temp' AND table_name = 'advert'
            ORDER BY ordinal_position
        """))
        for row in result:
            print(f"   {row[0]:20} {row[1]:15} {'NULL' if row[2] == 'YES' else 'NOT NULL'}")
        
        # Примеры данных
        result = await session.execute(text("""
            SELECT id, name, price, category_id, company_id 
            FROM temp.advert 
            WHERE name IS NOT NULL 
            LIMIT 3
        """))
        print("\n   Примеры данных:")
        for row in result:
            print(f"   ID: {row[0]}, Name: {row[1][:40] if row[1] else 'NULL'}, Price: {row[2]}, Cat: {row[3]}, Company: {row[4]}")
        
        print()
        
        # 6. Структура temp.file
        print("6️⃣ СТРУКТУРА temp.file:")
        print("-"*80)
        result = await session.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'temp' AND table_name = 'file'
            ORDER BY ordinal_position
        """))
        for row in result:
            print(f"   {row[0]:20} {row[1]:15} {'NULL' if row[2] == 'YES' else 'NOT NULL'}")
        
        # Примеры данных
        result = await session.execute(text("SELECT id, filename, filepath FROM temp.file LIMIT 3"))
        print("\n   Примеры данных:")
        for row in result:
            print(f"   ID: {row[0]}, File: {row[1][:50] if row[1] else 'NULL'}")
        
        print()
        
        # 7. Анализ связей
        print("7️⃣ АНАЛИЗ СВЯЗЕЙ:")
        print("-"*80)
        
        # Категории с подкатегориями
        result = await session.execute(text("""
            SELECT COUNT(*) 
            FROM temp.categories 
            WHERE parent_id IS NOT NULL
        """))
        subcats = result.scalar()
        print(f"   Подкатегорий (с parent_id): {subcats}")
        
        # Объявления с категориями
        result = await session.execute(text("""
            SELECT COUNT(*) 
            FROM temp.advert 
            WHERE category_id IS NOT NULL
        """))
        adverts_with_cat = result.scalar()
        print(f"   Объявлений с категорией: {adverts_with_cat}")
        
        # Объявления с компаниями
        result = await session.execute(text("""
            SELECT COUNT(*) 
            FROM temp.advert 
            WHERE company_id IS NOT NULL
        """))
        adverts_with_company = result.scalar()
        print(f"   Объявлений с компанией: {adverts_with_company}")
        
        # Пользователи с email
        result = await session.execute(text("""
            SELECT COUNT(*) 
            FROM temp.user 
            WHERE email IS NOT NULL AND email != ''
        """))
        users_with_email = result.scalar()
        print(f"   Пользователей с email: {users_with_email}")
        
        # Пользователи с телефоном
        result = await session.execute(text("""
            SELECT COUNT(*) 
            FROM temp.user 
            WHERE phone IS NOT NULL AND phone != ''
        """))
        users_with_phone = result.scalar()
        print(f"   Пользователей с телефоном: {users_with_phone}")
        
        print()
        print("="*80)
        print("✅ АНАЛИЗ ЗАВЕРШЕН")
        print("="*80)
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(analyze_temp_schema())
