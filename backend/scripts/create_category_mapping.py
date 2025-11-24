"""
Создание таблицы маппинга категорий temp → market
"""
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar"


# Маппинг категорий: temp.categories.name → market.categories.name
CATEGORY_MAPPING = {
    # Овощи и фрукты
    "/frukty-yagody/": "Овощи и фрукты",
    "/griby/": "Овощи и фрукты",
    "/dekorativnye-kultury/": "Овощи и фрукты",
    "/maslichnye-kultury/": "Овощи и фрукты",
    "/kormovye-korneplody/": "Овощи и фрукты",
    
    # Мясо, птица, рыба
    "/korma-dlya-ryb/": "Мясо, птица, рыба",
    
    # Зерно
    "/krupy/": "Зерно",
    "/krakhmalo-patochnaya-produktsiya/": "Зерно",
    
    # Мед
    "/med-produkty-pchelovodstva/": "Мед",
    
    # Готовые продукты
    "/bakaleya/": "Готовые продукты",
    "/konservy/": "Готовые продукты",
    "/konditerskie-izdeliya/\"4": "Готовые продукты",
    "/makaronnye-izdeliya/": "Готовые продукты",
    "/chay-kofe-kakao/": "Готовые продукты",
    "/bezalkogolnye-napitki-soki/\"<": "Готовые продукты",
    "/maslozhirovaya-produktsiya/": "Готовые продукты",
    
    # Корма и добавки
    "/kombikorma/": "Корма и добавки",
    "/kormovye-dobavki/": "Корма и добавки",
    "/kormovye-drozhzhi/": "Корма и добавки",
    "/korma-ekstrudirovannye/": "Корма и добавки",
    "/barda/": "Корма и добавки",
    "/bioudobrenie/": "Корма и добавки",
    
    # Агротовары и удобрения
    "/agrotovary/": "Агротовары и удобрения",
    "/biopreparaty/": "Агротовары и удобрения",
    "/khelatnye-mikroudobreniya/": "Агротовары и удобрения",
    "/grunty/": "Агротовары и удобрения",
    "/dezinfitsiruyushhie-sredstva/": "Агротовары и удобрения",
    
    # Оборудование и техника
    "/arenda-spetstekhniki/": "Оборудование и техника",
    "/avtomobilnyy-skh-transport/": "Оборудование и техника",
    "/kormouborochnaya-tekhnika/": "Оборудование и техника",
    "/mini-tekhnika/": "Оборудование и техника",
    "/emkostnoe-oborudovanie/2X": "Оборудование и техника",
    "/fasovochnoe-i-upakovochnoe-oborudovanie/": "Оборудование и техника",
    "/khlebopekarnoe-i-konditerskoe-oborudovanie/": "Оборудование и техника",
    "/kholodilnoe-oborudovanie/": "Оборудование и техника",
    "/moechnoe-i-sanitarno-gigienicheskoe-oborudovanie/": "Оборудование и техника",
    "/markirovochnoe-i-etiketirovochnoe-oborudovanie/": "Оборудование и техника",
    
    # Услуги
    "/agroturizm/": "Услуги",
    "/aviakhimraboty/": "Услуги",
    "/gruzoperevozki/": "Услуги",
    "/inform-agentstva/": "Услуги",
    "/investitsii-skh/+J": "Услуги",
}


async def create_mapping():
    """Создаёт таблицу маппинга категорий"""
    
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        print("="*80)
        print("🗺️ СОЗДАНИЕ ТАБЛИЦЫ МАППИНГА КАТЕГОРИЙ")
        print("="*80)
        
        # Создаём таблицу маппинга
        print("\n📋 Создаём таблицу temp.category_mapping...")
        await session.execute(text("""
            CREATE TABLE IF NOT EXISTS temp.category_mapping (
                temp_category_name VARCHAR(255) PRIMARY KEY,
                market_category_name VARCHAR(255) NOT NULL,
                market_category_id BIGINT
            )
        """))
        
        # Очищаем таблицу
        await session.execute(text("TRUNCATE TABLE temp.category_mapping"))
        await session.commit()
        print("✅ Таблица создана")
        
        # Заполняем маппинг
        print(f"\n📥 Заполняем маппинг ({len(CATEGORY_MAPPING)} категорий)...")
        
        mapped_count = 0
        for temp_name, market_name in CATEGORY_MAPPING.items():
            # Получаем ID категории из market
            result = await session.execute(text("""
                SELECT id FROM market.categories WHERE name = :name
            """), {"name": market_name})
            
            market_id = result.scalar()
            
            if market_id:
                await session.execute(text("""
                    INSERT INTO temp.category_mapping (temp_category_name, market_category_name, market_category_id)
                    VALUES (:temp_name, :market_name, :market_id)
                    ON CONFLICT (temp_category_name) DO UPDATE
                    SET market_category_name = :market_name, market_category_id = :market_id
                """), {
                    "temp_name": temp_name,
                    "market_name": market_name,
                    "market_id": market_id
                })
                mapped_count += 1
            else:
                print(f"   ⚠️  Категория '{market_name}' не найдена в market.categories")
        
        await session.commit()
        print(f"✅ Смаппено {mapped_count} категорий")
        
        # Показываем результат
        print("\n📊 Маппинг по категориям:")
        result = await session.execute(text("""
            SELECT market_category_name, COUNT(*) as count
            FROM temp.category_mapping
            GROUP BY market_category_name
            ORDER BY count DESC
        """))
        
        for row in result:
            print(f"   {row[0]:30} ← {row[1]:2} категорий из temp")
        
        # Проверяем сколько товаров будет смаппено
        print("\n📦 Проверка товаров:")
        result = await session.execute(text("""
            SELECT COUNT(DISTINCT ta.id) as total_adverts,
                   COUNT(DISTINCT CASE WHEN tcm.market_category_id IS NOT NULL THEN ta.id END) as mapped_adverts
            FROM temp.advert ta
            LEFT JOIN temp.categories tc ON tc.id = ta.category_id
            LEFT JOIN temp.category_mapping tcm ON tcm.temp_category_name = tc.name
        """))
        
        row = result.first()
        if row:
            total = row[0]
            mapped = row[1]
            percent = (mapped / total * 100) if total > 0 else 0
            print(f"   Всего товаров: {total}")
            print(f"   Будет смаппено: {mapped} ({percent:.1f}%)")
            print(f"   Без категории: {total - mapped}")
        
        print("\n" + "="*80)
        print("✅ МАППИНГ СОЗДАН!")
        print("="*80)
        print("\n💡 Теперь можно запустить миграцию с учётом маппинга")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_mapping())
