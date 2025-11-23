"""
Cart API router
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from decimal import Decimal

from database import get_db
from models.cart import CartItem
from models.product import Product
from models.user import User
from schemas.cart import (
    CartItemCreate,
    CartItemUpdate,
    CartResponse,
)
from services.jwt_service import JWTService

router = APIRouter()


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Получить текущего пользователя из токена"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Требуется авторизация")
    
    # Извлекаем токен из заголовка "Bearer <token>"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(status_code=401, detail="Неверная схема авторизации")
    except ValueError:
        raise HTTPException(status_code=401, detail="Неверный формат токена")
    
    user_id = JWTService.get_user_id_from_token(token)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Неверный токен")
    
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    return user


@router.get("/", response_model=CartResponse)
async def get_cart(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить корзину пользователя"""
    # Получаем все товары в корзине
    result = await db.execute(
        select(CartItem, Product)
        .join(Product, CartItem.product_id == Product.id)
        .where(CartItem.user_id == user.id)
    )
    rows = result.all()
    
    items = []
    total = Decimal(0)
    
    for cart_item, product in rows:
        subtotal = product.price * cart_item.quantity
        total += subtotal
        
        items.append({
            "id": str(cart_item.id),
            "product_id": str(cart_item.product_id),
            "quantity": cart_item.quantity,
            "created_at": cart_item.created_at,
            "updated_at": cart_item.updated_at,
            "product_name": product.name,
            "product_price": product.price,
            "product_image": product.image,
            "product_in_stock": product.in_stock,
            "subtotal": subtotal,
        })
    
    return CartResponse(
        items=items,
        total=total,
        items_count=len(items)
    )


@router.post("/items", status_code=201)
async def add_to_cart(
    item_data: CartItemCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Добавить товар в корзину"""
    # Проверяем существование товара
    result = await db.execute(
        select(Product).where(Product.id == item_data.product_id)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    if not product.in_stock:
        raise HTTPException(status_code=400, detail="Товар нет в наличии")
    
    # Проверяем, есть ли уже этот товар в корзине
    result = await db.execute(
        select(CartItem).where(
            CartItem.user_id == user.id,
            CartItem.product_id == item_data.product_id
        )
    )
    existing_item = result.scalar_one_or_none()
    
    if existing_item:
        # Увеличиваем количество
        existing_item.quantity += item_data.quantity
        await db.commit()
        await db.refresh(existing_item)
        return {"message": "Количество обновлено", "item_id": str(existing_item.id)}
    else:
        # Создаем новый item
        cart_item = CartItem(
            user_id=user.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity
        )
        db.add(cart_item)
        await db.commit()
        await db.refresh(cart_item)
        return {"message": "Товар добавлен в корзину", "item_id": str(cart_item.id)}


@router.put("/items/{item_id}")
async def update_cart_item(
    item_id: str,
    item_data: CartItemUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Обновить количество товара в корзине"""
    result = await db.execute(
        select(CartItem).where(
            CartItem.id == item_id,
            CartItem.user_id == user.id
        )
    )
    cart_item = result.scalar_one_or_none()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Товар в корзине не найден")
    
    cart_item.quantity = item_data.quantity
    await db.commit()
    await db.refresh(cart_item)
    
    return {"message": "Количество обновлено"}


@router.delete("/items/{item_id}", status_code=204)
async def remove_from_cart(
    item_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Удалить товар из корзины"""
    result = await db.execute(
        select(CartItem).where(
            CartItem.id == item_id,
            CartItem.user_id == user.id
        )
    )
    cart_item = result.scalar_one_or_none()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Товар в корзине не найден")
    
    await db.delete(cart_item)
    await db.commit()
    
    return None


@router.delete("/", status_code=204)
async def clear_cart(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Очистить корзину"""
    result = await db.execute(
        select(CartItem).where(CartItem.user_id == user.id)
    )
    cart_items = result.scalars().all()
    
    for item in cart_items:
        await db.delete(item)
    
    await db.commit()
    
    return None
