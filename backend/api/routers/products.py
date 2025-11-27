"""
Products API router with full CRUD
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional
from decimal import Decimal

from database import get_db
from models.product import Product
from schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse,
)

router = APIRouter()


@router.get("/", response_model=ProductListResponse)
async def get_products(
    category_id: Optional[int] = Query(None),
    store_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    in_stock: Optional[bool] = Query(None),
    with_images: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список товаров с фильтрацией и пагинацией
    
    - **category_id**: Фильтр по категории
    - **store_id**: Фильтр по магазину
    - **min_price, max_price**: Диапазон цен
    - **min_rating**: Минимальный рейтинг
    - **in_stock**: Только в наличии
    - **search**: Поиск по названию
    - **sort_by**: Сортировка (price, rating, created_at, name)
    - **sort_order**: Порядок (asc, desc)
    - **skip, limit**: Пагинация
    """
    
    # Базовый запрос - только активные товары для каталога
    query = select(Product).where(Product.status == "active")
    
    # Фильтры
    if category_id:
        query = query.where(Product.category_id == category_id)
    
    if store_id:
        query = query.where(Product.store_owner_id == store_id)
    
    if min_price is not None:
        query = query.where(Product.price >= min_price)
    
    if max_price is not None:
        query = query.where(Product.price <= max_price)
    
    if in_stock is not None:
        query = query.where(Product.in_stock == in_stock)
    
    if with_images is not None and with_images:
        query = query.where(Product.image.isnot(None))
        query = query.where(Product.image != '')
    
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            or_(
                Product.name.ilike(search_pattern),
                Product.description.ilike(search_pattern)
            )
        )
    
    # Подсчет общего количества
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Сортировка
    sort_column = getattr(Product, sort_by)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    # Пагинация
    query = query.offset(skip).limit(limit)
    
    # Выполнение запроса
    result = await db.execute(query)
    products = result.scalars().all()
    
    return ProductListResponse(
        data=products,
        meta={
            "total": total,
            "skip": skip,
            "limit": limit,
            "page": (skip // limit) + 1 if limit > 0 else 1,
            "pages": (total + limit - 1) // limit if limit > 0 else 1,
        }
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """Получить товар по ID с изображениями"""
    from models.product_image import ProductImage
    from sqlalchemy.orm import selectinload
    
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.images))
        .where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    return product


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    """Создать новый товар"""
    # Проверка уникальности slug
    result = await db.execute(
        select(Product).where(Product.slug == product_data.slug)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Товар с таким slug уже существует")
    
    product = Product(**product_data.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    
    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Обновить товар"""
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    # Обновляем только переданные поля
    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    await db.commit()
    await db.refresh(product)
    
    return product


@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """Удалить товар"""
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    await db.delete(product)
    await db.commit()
    
    return None


@router.get("/map/geojson")
async def get_products_geojson(
    category_id: Optional[int] = Query(None),
    store_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    min_rating: Optional[float] = Query(None),
    in_stock: Optional[bool] = Query(None),
    limit: int = Query(1000, ge=1, le=5000),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить товары в формате GeoJSON для отображения на карте
    
    Возвращает только товары с координатами
    """
    from sqlalchemy.orm import selectinload
    from models.category import Category
    
    # Базовый запрос - только товары с координатами
    query = select(Product).options(selectinload(Product.category))
    query = query.where(Product.latitude.isnot(None))
    query = query.where(Product.longitude.isnot(None))
    
    # Фильтры
    if category_id:
        query = query.where(Product.category_id == category_id)
    
    if store_id:
        query = query.where(Product.store_owner_id == store_id)
    
    if min_price is not None:
        query = query.where(Product.price >= min_price)
    
    if max_price is not None:
        query = query.where(Product.price <= max_price)
    
    if min_rating is not None:
        query = query.where(Product.rating >= min_rating)
    
    if in_stock is not None:
        query = query.where(Product.in_stock == in_stock)
    
    # Ограничение
    query = query.limit(limit)
    
    # Выполнение запроса
    result = await db.execute(query)
    products = result.scalars().all()
    
    # Формируем GeoJSON
    features = []
    for product in products:
        # Собираем все изображения товара
        images = []
        if product.image:
            images.append(product.image)
        # Добавляем дополнительные изображения из связанной таблицы
        if hasattr(product, 'images') and product.images:
            for img in product.images:
                if img.image_url and img.image_url not in images:
                    images.append(img.image_url)
        
        import json
        
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [product.longitude, product.latitude]
            },
            "properties": {
                "id": product.id,
                "name": product.name,
                "price": float(product.price),
                "image": product.image,
                "images": json.dumps(images),  # Сериализуем в JSON строку
                "category_id": product.category_id,
                "category_name": product.category.name if product.category else None,
                "category_icon": product.category.image if product.category else "📦",
                "in_stock": product.in_stock,
                "rating": float(product.rating) if product.rating else 0,
            }
        })
    
    return {
        "type": "FeatureCollection",
        "features": features
    }
