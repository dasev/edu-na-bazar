"""
Настройка структуры для изображений
"""
import asyncio
from pathlib import Path
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar"


async def setup_images():
    """Настраивает структуру для изображений"""
    
    print("="*80)
    print("🖼️ НАСТРОЙКА СТРУКТУРЫ ДЛЯ ИЗОБРАЖЕНИЙ")
    print("="*80)
    
    # Шаг 1: Создание каталогов
    print("\n📁 Шаг 1: Создание каталогов...")
    
    directories = [
        Path("uploads/products/original"),
        Path("uploads/products/thumbnails"),
        Path("uploads/products/optimized"),
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}")
    
    # Создаём плейсхолдер
    placeholder = Path("uploads/products/placeholder.jpg")
    if not placeholder.exists():
        # Создаём пустой файл-плейсхолдер
        placeholder.touch()
        print(f"   ✅ {placeholder} (плейсхолдер)")
    
    # Шаг 2: Обновление БД
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        print("\n📊 Шаг 2: Обновление структуры БД...")
        
        # Добавляем поле old_id в product_images
        try:
            await session.execute(text("""
                ALTER TABLE market.product_images 
                ADD COLUMN IF NOT EXISTS old_id INTEGER
            """))
            await session.commit()
            print("   ✅ Добавлено поле old_id в market.product_images")
        except Exception as e:
            print(f"   ⚠️ Поле old_id уже существует или ошибка: {e}")
            await session.rollback()
        
        # Создаём индекс
        try:
            await session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_product_images_old_id 
                ON market.product_images(old_id)
            """))
            await session.commit()
            print("   ✅ Создан индекс idx_product_images_old_id")
        except Exception as e:
            print(f"   ⚠️ Индекс уже существует: {e}")
            await session.rollback()
        
        # Шаг 3: Создание таблицы маппинга
        print("\n🗺️ Шаг 3: Создание таблицы маппинга...")
        
        await session.execute(text("""
            CREATE TABLE IF NOT EXISTS temp.image_mapping (
                old_file_id INTEGER PRIMARY KEY,
                old_filename VARCHAR(255),
                old_path VARCHAR(255),
                new_product_id BIGINT,
                new_image_id BIGINT,
                is_correct BOOLEAN DEFAULT FALSE,
                notes TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """))
        await session.commit()
        print("   ✅ Таблица temp.image_mapping создана")
        
        # Заполняем маппинг из temp.file
        await session.execute(text("""
            INSERT INTO temp.image_mapping (old_file_id, old_filename, old_path)
            SELECT id, filename, path
            FROM temp.file
            WHERE type = 'image'
            ON CONFLICT (old_file_id) DO NOTHING
        """))
        await session.commit()
        
        result = await session.execute(text("""
            SELECT COUNT(*) FROM temp.image_mapping
        """))
        count = result.scalar()
        print(f"   ✅ Добавлено {count} записей в маппинг")
        
        # Шаг 4: Статистика
        print("\n📊 Статистика:")
        
        result = await session.execute(text("""
            SELECT COUNT(*) FROM temp.file WHERE type = 'image'
        """))
        total_images = result.scalar()
        print(f"   Всего изображений в temp.file: {total_images}")
        
        result = await session.execute(text("""
            SELECT COUNT(*) FROM market.products
        """))
        total_products = result.scalar()
        print(f"   Всего товаров: {total_products}")
        
        result = await session.execute(text("""
            SELECT COUNT(*) FROM market.product_images
        """))
        current_images = result.scalar()
        print(f"   Текущих изображений товаров: {current_images}")
    
    await engine.dispose()
    
    print("\n" + "="*80)
    print("✅ НАСТРОЙКА ЗАВЕРШЕНА!")
    print("="*80)
    print("\n📝 Что сделано:")
    print("   1. Созданы каталоги для изображений")
    print("   2. Добавлено поле old_id в product_images")
    print("   3. Создана таблица temp.image_mapping")
    print("   4. Заполнен маппинг из temp.file")
    print("\n💡 Следующие шаги:")
    print("   1. Скопировать файлы в uploads/products/original/")
    print("   2. Запустить миграцию товаров")
    print("   3. Вручную назначить изображения через SQL")
    print("\n📋 Пример SQL для назначения изображения:")
    print("""
   UPDATE market.product_images 
   SET image_url = '/uploads/products/original/filename.jpg',
       old_id = 123
   WHERE product_id = 456;
    """)


if __name__ == "__main__":
    asyncio.run(setup_images())
