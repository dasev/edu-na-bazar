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
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    min_rating: Optional[float] = Query(None),
    in_stock: Optional[bool] = Query(None),
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
    - **min_price, max_price**: Диапазон цен
    - **min_rating**: Минимальный рейтинг
    - **in_stock**: Только в наличии
    - **search**: Поиск по названию
    - **sort_by**: Сортировка (price, rating, created_at, name)
    - **sort_order**: Порядок (asc, desc)
    - **skip, limit**: Пагинация
    """
    
    # Базовый запрос
    query = select(Product)
    
    # Фильтры
    if category_id:
        query = query.where(Product.category_id == category_id)
    
    if min_price is not None:
        query = query.where(Product.price >= min_price)
    
    if max_price is not None:
        query = query.where(Product.price <= max_price)
    
    if min_rating is not None:
        query = query.where(Product.rating >= min_rating)
    
    if in_stock is not None:
        query = query.where(Product.in_stock == in_stock)
    
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
async def get_product(product_id: str, db: AsyncSession = Depends(get_db)):
    """Получить товар по ID"""
    result = await db.execute(
        select(Product).where(Product.id == product_id)
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
    product_id: str,
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
async def delete_product(product_id: str, db: AsyncSession = Depends(get_db)):
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
