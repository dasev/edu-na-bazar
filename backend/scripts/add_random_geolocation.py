"""
Скрипт для добавления случайной геолокации товарам по всей России
"""
import asyncio
import random
from sqlalchemy import select, update, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import sys
import os

# Добавляем путь к backend для импорта моделей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.product import Product
from config import settings

# Импортируем все модели для правильной инициализации relationships
from models import user, category, store, store_owner, order, cart, product_image, review, geography, message  # noqa


# Границы России (приблизительные)
RUSSIA_BOUNDS = {
    'lat_min': 41.0,   # Южная граница (Дагестан)
    'lat_max': 77.0,   # Северная граница (Арктика)
    'lon_min': 19.0,   # Западная граница (Калининград)
    'lon_max': 180.0,  # Восточная граница (Чукотка)
}

# Крупные города России с координатами (для более реалистичного распределения)
MAJOR_CITIES = [
    {'name': 'Москва', 'lat': 55.7558, 'lon': 37.6173, 'radius': 50},
    {'name': 'Санкт-Петербург', 'lat': 59.9343, 'lon': 30.3351, 'radius': 40},
    {'name': 'Новосибирск', 'lat': 55.0084, 'lon': 82.9357, 'radius': 30},
    {'name': 'Екатеринбург', 'lat': 56.8389, 'lon': 60.6057, 'radius': 30},
    {'name': 'Казань', 'lat': 55.8304, 'lon': 49.0661, 'radius': 25},
    {'name': 'Нижний Новгород', 'lat': 56.2965, 'lon': 43.9361, 'radius': 25},
    {'name': 'Челябинск', 'lat': 55.1644, 'lon': 61.4368, 'radius': 25},
    {'name': 'Самара', 'lat': 53.1959, 'lon': 50.1002, 'radius': 25},
    {'name': 'Омск', 'lat': 54.9885, 'lon': 73.3242, 'radius': 20},
    {'name': 'Ростов-на-Дону', 'lat': 47.2357, 'lon': 39.7015, 'radius': 25},
    {'name': 'Уфа', 'lat': 54.7388, 'lon': 55.9721, 'radius': 25},
    {'name': 'Красноярск', 'lat': 56.0153, 'lon': 92.8932, 'radius': 25},
    {'name': 'Воронеж', 'lat': 51.6720, 'lon': 39.1843, 'radius': 20},
    {'name': 'Пермь', 'lat': 58.0105, 'lon': 56.2502, 'radius': 20},
    {'name': 'Волгоград', 'lat': 48.7080, 'lon': 44.5133, 'radius': 20},
    {'name': 'Краснодар', 'lat': 45.0355, 'lon': 38.9753, 'radius': 25},
    {'name': 'Саратов', 'lat': 51.5924, 'lon': 46.0348, 'radius': 20},
    {'name': 'Тюмень', 'lat': 57.1522, 'lon': 65.5272, 'radius': 20},
    {'name': 'Тольятти', 'lat': 53.5303, 'lon': 49.3461, 'radius': 15},
    {'name': 'Ижевск', 'lat': 56.8498, 'lon': 53.2045, 'radius': 15},
    {'name': 'Барнаул', 'lat': 53.3606, 'lon': 83.7636, 'radius': 15},
    {'name': 'Ульяновск', 'lat': 54.3142, 'lon': 48.4031, 'radius': 15},
    {'name': 'Иркутск', 'lat': 52.2869, 'lon': 104.3050, 'radius': 20},
    {'name': 'Хабаровск', 'lat': 48.4827, 'lon': 135.0838, 'radius': 20},
    {'name': 'Владивосток', 'lat': 43.1155, 'lon': 131.8855, 'radius': 20},
]


def generate_random_coordinates_near_city(city: dict) -> tuple[float, float]:
    """
    Генерирует случайные координаты вокруг города
    
    Args:
        city: Словарь с данными города (lat, lon, radius)
        
    Returns:
        Кортеж (latitude, longitude)
    """
    # Радиус в градусах (примерно 1 градус = 111 км)
    radius_deg = city['radius'] / 111.0
    
    # Случайное смещение от центра города
    lat_offset = random.uniform(-radius_deg, radius_deg)
    lon_offset = random.uniform(-radius_deg, radius_deg)
    
    latitude = city['lat'] + lat_offset
    longitude = city['lon'] + lon_offset
    
    # Округляем до 6 знаков после запятой
    return round(latitude, 6), round(longitude, 6)


def generate_random_coordinates_russia() -> tuple[float, float]:
    """
    Генерирует случайные координаты в пределах России
    
    Returns:
        Кортеж (latitude, longitude)
    """
    latitude = random.uniform(RUSSIA_BOUNDS['lat_min'], RUSSIA_BOUNDS['lat_max'])
    longitude = random.uniform(RUSSIA_BOUNDS['lon_min'], RUSSIA_BOUNDS['lon_max'])
    
    # Округляем до 6 знаков после запятой
    return round(latitude, 6), round(longitude, 6)


async def add_geolocation_to_products():
    """Добавляет геолокацию товарам, у которых её нет"""
    
    # Создаем async engine
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
    )
    
    # Создаем async session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        try:
            # Получаем товары без геолокации
            result = await session.execute(
                select(Product).where(Product.latitude.is_(None))
            )
            products_without_geo = result.scalars().all()
            
            print(f"📊 Найдено товаров без геолокации: {len(products_without_geo)}")
            
            if not products_without_geo:
                print("✅ Все товары уже имеют геолокацию!")
                return
            
            # Распределяем товары:
            # 70% - вокруг крупных городов
            # 30% - случайно по России
            city_products_count = int(len(products_without_geo) * 0.7)
            
            updated_count = 0
            
            # Обновляем товары вокруг городов
            for i, product in enumerate(products_without_geo[:city_products_count]):
                city = random.choice(MAJOR_CITIES)
                latitude, longitude = generate_random_coordinates_near_city(city)
                
                product.latitude = latitude
                product.longitude = longitude
                # PostGIS POINT: ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
                product.geo_location = f'SRID=4326;POINT({longitude} {latitude})'
                
                updated_count += 1
                
                if (i + 1) % 10 == 0:
                    print(f"  ✓ Обновлено {i + 1}/{city_products_count} товаров вокруг городов...")
            
            print(f"✅ Обновлено {city_products_count} товаров вокруг городов")
            
            # Обновляем остальные товары случайно по России
            random_count = 0
            for i, product in enumerate(products_without_geo[city_products_count:]):
                latitude, longitude = generate_random_coordinates_russia()
                
                product.latitude = latitude
                product.longitude = longitude
                product.geo_location = f'SRID=4326;POINT({longitude} {latitude})'
                
                random_count += 1
                updated_count += 1
            
            print(f"✅ Обновлено {random_count} товаров случайно по России")
            
            # Сохраняем изменения
            await session.commit()
            
            print(f"\n🎉 Всего обновлено товаров: {updated_count}")
            
            # Проверяем результат
            result = await session.execute(
                select(Product).where(Product.latitude.is_not(None))
            )
            products_with_geo = result.scalars().all()
            
            print(f"📊 Товаров с геолокацией: {len(products_with_geo)}")
            
            # Показываем примеры
            print("\n📍 Примеры добавленных координат:")
            for product in products_without_geo[:5]:
                print(f"  • {product.name[:50]}: ({product.latitude}, {product.longitude})")
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            await session.rollback()
            raise
        finally:
            await engine.dispose()


if __name__ == "__main__":
    print("🚀 Запуск скрипта добавления геолокации...")
    print(f"📍 Распределение: 70% вокруг {len(MAJOR_CITIES)} крупных городов, 30% случайно по РФ\n")
    
    asyncio.run(add_geolocation_to_products())
    
    print("\n✅ Готово!")
