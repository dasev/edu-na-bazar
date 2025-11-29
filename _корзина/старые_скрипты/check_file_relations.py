"""
Проверка связей в temp.file
"""
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar"


async def check():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        print("="*80)
        print("🔍 ПРОВЕРКА СВЯЗЕЙ В temp.file")
        print("="*80)
        
        # Общая статистика
        result = await session.execute(text("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN advert_id IS NOT NULL THEN 1 END) as with_advert,
                COUNT(CASE WHEN company_id IS NOT NULL THEN 1 END) as with_company,
                COUNT(CASE WHEN advert_id IS NULL AND company_id IS NULL THEN 1 END) as without_links
            FROM temp.file
            WHERE type = 'image'
        """))
        
        row = result.first()
        print(f"\n📊 Статистика изображений:")
        print(f"   Всего изображений: {row[0]}")
        print(f"   С advert_id: {row[1]}")
        print(f"   С company_id: {row[2]}")
        print(f"   Без связей: {row[3]}")
        
        # Примеры с advert_id
        if row[1] > 0:
            print(f"\n✅ Найдены изображения с advert_id!")
            result = await session.execute(text("""
                SELECT id, filename, advert_id, company_id
                FROM temp.file
                WHERE type = 'image' AND advert_id IS NOT NULL
                LIMIT 10
            """))
            
            print(f"\n📸 Примеры:")
            for r in result:
                print(f"   ID: {r[0]}, File: {r[1][:50]}, Advert: {r[2]}, Company: {r[3]}")
        
        # Примеры с company_id
        if row[2] > 0:
            print(f"\n✅ Найдены изображения с company_id!")
            result = await session.execute(text("""
                SELECT id, filename, advert_id, company_id
                FROM temp.file
                WHERE type = 'image' AND company_id IS NOT NULL
                LIMIT 10
            """))
            
            print(f"\n🏢 Примеры:")
            for r in result:
                print(f"   ID: {r[0]}, File: {r[1][:50]}, Advert: {r[2]}, Company: {r[3]}")
        
        # Проверяем есть ли отдельная таблица связей
        print(f"\n🔍 Проверяем другие таблицы...")
        result = await session.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'temp' 
            AND table_name LIKE '%file%' OR table_name LIKE '%image%' OR table_name LIKE '%photo%'
        """))
        
        tables = result.fetchall()
        if tables:
            print(f"\n📋 Найденные таблицы:")
            for t in tables:
                print(f"   - {t[0]}")
        else:
            print(f"\n⚠️ Других таблиц с изображениями не найдено")
    
    await engine.dispose()
    
    print("\n" + "="*80)
    if row[1] == 0 and row[2] == 0:
        print("❌ СВЯЗИ НЕ НАЙДЕНЫ")
        print("="*80)
        print("\n💡 Вывод:")
        print("   - В temp.file все advert_id и company_id = NULL")
        print("   - Связи между фото и товарами потеряны")
        print("   - Нужно использовать ручную корректировку через temp.image_mapping")
    else:
        print("✅ СВЯЗИ НАЙДЕНЫ!")
        print("="*80)


if __name__ == "__main__":
    asyncio.run(check())
