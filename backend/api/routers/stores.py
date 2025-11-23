"""
Stores API router (GIS)
"""
from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from typing import List
from geoalchemy2.functions import ST_Distance, ST_DWithin, ST_MakePoint, ST_AsGeoJSON
from geoalchemy2.elements import WKTElement

from database import get_db
from models.store import Store
from schemas.store import (
    StoreCreate,
    StoreUpdate,
    StoreResponse,
    StoreWithDistance,
    LocationResponse,
)

router = APIRouter()


def store_to_response(store: Store) -> dict:
    """Преобразовать Store в dict для response"""
    # Получаем координаты из PostGIS POINT
    location_data = {
        "type": "Point",
        "coordinates": [0, 0]  # Default
    }
    
    if store.location:
        # location хранится как WKB, нужно извлечь координаты
        # В реальном запросе используем ST_AsGeoJSON
        pass
    
    return {
        "id": str(store.id),
        "name": store.name,
        "address": store.address,
        "phone": store.phone,
        "email": store.email,
        "working_hours": store.working_hours,
        "description": store.description,
        "location": location_data,
        "image": store.image,
        "is_active": store.is_active,
        "created_at": store.created_at,
        "updated_at": store.updated_at,
    }


@router.get("/", response_model=List[StoreResponse])
async def get_stores(db: AsyncSession = Depends(get_db)):
    """Получить все магазины"""
    # Используем ST_AsGeoJSON для получения координат в JSON формате
    query = select(
        Store,
        func.ST_X(Store.location).label('longitude'),
        func.ST_Y(Store.location).label('latitude')
    )
    
    result = await db.execute(query)
    rows = result.all()
    
    stores = []
    for row in rows:
        store = row[0]
        lon = row[1]
        lat = row[2]
        
        store_dict = {
            "id": str(store.id),
            "name": store.name,
            "address": store.address,
            "phone": store.phone,
            "email": store.email,
            "working_hours": store.working_hours,
            "description": store.description,
            "location": {
                "type": "Point",
                "coordinates": [float(lon) if lon else 0, float(lat) if lat else 0]
            },
            "image": store.image,
            "is_active": store.is_active,
            "created_at": store.created_at,
            "updated_at": store.updated_at,
        }
        stores.append(store_dict)
    
    return stores


@router.get("/nearby", response_model=List[StoreWithDistance])
async def get_nearby_stores(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lon: float = Query(..., description="Longitude", ge=-180, le=180),
    radius_km: float = Query(5, description="Radius in kilometers", ge=0.1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить ближайшие магазины (PostGIS запрос)
    
    Использует ST_DWithin для поиска магазинов в радиусе
    """
    # Создаем точку из координат пользователя
    # ST_MakePoint(longitude, latitude)
    # ST_DWithin работает в метрах для geography
    radius_meters = radius_km * 1000
    
    # Запрос с расстоянием
    query = select(
        Store,
        func.ST_X(Store.location).label('longitude'),
        func.ST_Y(Store.location).label('latitude'),
        func.ST_Distance(
            func.ST_Transform(Store.location, 4326),
            func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)
        ).label('distance_meters')
    ).where(
        func.ST_DWithin(
            func.cast(Store.location, 'geography'),
            func.cast(func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326), 'geography'),
            radius_meters
        )
    ).order_by(text('distance_meters'))
    
    result = await db.execute(query)
    rows = result.all()
    
    stores = []
    for row in rows:
        store = row[0]
        store_lon = row[1]
        store_lat = row[2]
        distance_m = row[3]
        
        store_dict = {
            "id": str(store.id),
            "name": store.name,
            "address": store.address,
            "phone": store.phone,
            "email": store.email,
            "working_hours": store.working_hours,
            "description": store.description,
            "location": {
                "type": "Point",
                "coordinates": [float(store_lon) if store_lon else 0, float(store_lat) if store_lat else 0]
            },
            "image": store.image,
            "is_active": store.is_active,
            "created_at": store.created_at,
            "updated_at": store.updated_at,
            "distance_km": round(float(distance_m) / 1000, 2) if distance_m else 0
        }
        stores.append(store_dict)
    
    return stores


@router.get("/{store_id}", response_model=StoreResponse)
async def get_store(store_id: str, db: AsyncSession = Depends(get_db)):
    """Получить магазин по ID"""
    query = select(
        Store,
        func.ST_X(Store.location).label('longitude'),
        func.ST_Y(Store.location).label('latitude')
    ).where(Store.id == store_id)
    
    result = await db.execute(query)
    row = result.first()
    
    if not row:
        raise HTTPException(status_code=404, detail="Магазин не найден")
    
    store = row[0]
    lon = row[1]
    lat = row[2]
    
    return {
        "id": str(store.id),
        "name": store.name,
        "address": store.address,
        "phone": store.phone,
        "email": store.email,
        "working_hours": store.working_hours,
        "description": store.description,
        "location": {
            "type": "Point",
            "coordinates": [float(lon) if lon else 0, float(lat) if lat else 0]
        },
        "image": store.image,
        "is_active": store.is_active,
        "created_at": store.created_at,
        "updated_at": store.updated_at,
    }


@router.post("/", response_model=StoreResponse, status_code=201)
async def create_store(
    store_data: StoreCreate,
    db: AsyncSession = Depends(get_db)
):
    """Создать новый магазин"""
    # Создаем POINT из координат
    # ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
    point_wkt = f"POINT({store_data.longitude} {store_data.latitude})"
    
    store = Store(
        name=store_data.name,
        address=store_data.address,
        phone=store_data.phone,
        email=store_data.email,
        working_hours=store_data.working_hours,
        description=store_data.description,
        location=WKTElement(point_wkt, srid=4326),
        image=store_data.image,
        is_active=store_data.is_active,
    )
    
    db.add(store)
    await db.commit()
    await db.refresh(store)
    
    # Получаем координаты обратно
    query = select(
        Store,
        func.ST_X(Store.location).label('longitude'),
        func.ST_Y(Store.location).label('latitude')
    ).where(Store.id == store.id)
    
    result = await db.execute(query)
    row = result.first()
    
    store = row[0]
    lon = row[1]
    lat = row[2]
    
    return {
        "id": str(store.id),
        "name": store.name,
        "address": store.address,
        "phone": store.phone,
        "email": store.email,
        "working_hours": store.working_hours,
        "description": store.description,
        "location": {
            "type": "Point",
            "coordinates": [float(lon), float(lat)]
        },
        "image": store.image,
        "is_active": store.is_active,
        "created_at": store.created_at,
        "updated_at": store.updated_at,
    }


@router.put("/{store_id}", response_model=StoreResponse)
async def update_store(
    store_id: str,
    store_data: StoreUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Обновить магазин"""
    result = await db.execute(
        select(Store).where(Store.id == store_id)
    )
    store = result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(status_code=404, detail="Магазин не найден")
    
    # Обновляем поля
    update_data = store_data.model_dump(exclude_unset=True, exclude={'latitude', 'longitude'})
    for field, value in update_data.items():
        setattr(store, field, value)
    
    # Обновляем координаты если переданы
    if store_data.latitude is not None and store_data.longitude is not None:
        point_wkt = f"POINT({store_data.longitude} {store_data.latitude})"
        store.location = WKTElement(point_wkt, srid=4326)
    
    await db.commit()
    await db.refresh(store)
    
    # Получаем координаты
    query = select(
        Store,
        func.ST_X(Store.location).label('longitude'),
        func.ST_Y(Store.location).label('latitude')
    ).where(Store.id == store.id)
    
    result = await db.execute(query)
    row = result.first()
    
    store = row[0]
    lon = row[1]
    lat = row[2]
    
    return {
        "id": str(store.id),
        "name": store.name,
        "address": store.address,
        "phone": store.phone,
        "email": store.email,
        "working_hours": store.working_hours,
        "description": store.description,
        "location": {
            "type": "Point",
            "coordinates": [float(lon), float(lat)]
        },
        "image": store.image,
        "is_active": store.is_active,
        "created_at": store.created_at,
        "updated_at": store.updated_at,
    }


@router.delete("/{store_id}", status_code=204)
async def delete_store(store_id: str, db: AsyncSession = Depends(get_db)):
    """Удалить магазин"""
    result = await db.execute(
        select(Store).where(Store.id == store_id)
    )
    store = result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(status_code=404, detail="Магазин не найден")
    
    await db.delete(store)
    await db.commit()
    
    return None
