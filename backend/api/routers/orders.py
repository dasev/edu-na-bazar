"""
Orders API router
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from datetime import datetime

from database import get_db
from models.order import Order, OrderItem
from models.product import Product
from models.user import User
from schemas.order import (
    OrderCreate,
    OrderUpdateStatus,
    OrderResponse,
    OrderListResponse,
)
from api.dependencies import get_current_user  # Используем стандартный get_current_user

router = APIRouter()


@router.get("/", response_model=OrderListResponse)
async def get_orders(
    status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить заказы пользователя"""
    try:
        query = select(Order).where(Order.user_id == user.id)
        
        if status:
            query = query.where(Order.status == status)
        
        # Подсчет
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Сортировка и пагинация
        query = query.order_by(Order.created_at.desc()).offset(skip).limit(limit)
        
        result = await db.execute(query)
        orders = result.scalars().all()
        
        # Пока возвращаем без items для отладки
        return OrderListResponse(
            data=orders,
            meta={
                "total": total,
                "skip": skip,
                "limit": limit,
                "page": (skip // limit) + 1 if limit > 0 else 1,
                "pages": (total + limit - 1) // limit if limit > 0 else 1,
            }
        )
    except Exception as e:
        print(f"❌ Ошибка в get_orders: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка получения заказов: {str(e)}")


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить детали заказа"""
    result = await db.execute(
        select(Order).where(Order.id == order_id, Order.user_id == user.id)
    )
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    
    # Загружаем items
    items_result = await db.execute(
        select(OrderItem).where(OrderItem.order_id == order.id)
    )
    order.items = items_result.scalars().all()
    
    return order


@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(
    order_data: OrderCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Создать новый заказ"""
    # Проверяем товары и считаем сумму
    total = 0
    order_items_data = []
    
    for item_data in order_data.items:
        # Получаем товар
        result = await db.execute(
            select(Product).where(Product.id == item_data.product_id)
        )
        product = result.scalar_one_or_none()
        
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Товар {item_data.product_id} не найден"
            )
        
        if not product.in_stock:
            raise HTTPException(
                status_code=400,
                detail=f"Товар {product.name} нет в наличии"
            )
        
        if product.stock_quantity < item_data.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Недостаточно товара {product.name} на складе"
            )
        
        subtotal = float(product.price) * item_data.quantity
        total += subtotal
        
        order_items_data.append({
            "product_id": product.id,
            "product_name": product.name,
            "product_image": product.image,
            "quantity": item_data.quantity,
            "price": product.price,
        })
    
    # Создаем заказ
    order = Order(
        user_id=user.id,
        status="created",
        total=total,
        delivery_address=order_data.delivery_address,
        delivery_time=order_data.delivery_time,
        delivery_comment=order_data.delivery_comment,
        payment_method=order_data.payment_method,
        payment_status="pending",
        contact_phone=order_data.contact_phone,
        contact_name=order_data.contact_name,
        comment=order_data.comment,
    )
    
    db.add(order)
    await db.flush()  # Получаем ID заказа
    
    # Создаем items
    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=order.id,
            **item_data
        )
        db.add(order_item)
        
        # Уменьшаем количество на складе
        result = await db.execute(
            select(Product).where(Product.id == item_data["product_id"])
        )
        product = result.scalar_one()
        product.stock_quantity -= item_data["quantity"]
    
    await db.commit()
    await db.refresh(order)
    
    # Загружаем items
    items_result = await db.execute(
        select(OrderItem).where(OrderItem.order_id == order.id)
    )
    order.items = items_result.scalars().all()
    
    return order


@router.put("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: str,
    status_data: OrderUpdateStatus,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Обновить статус заказа (только для админов в будущем)"""
    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    
    order.status = status_data.status
    
    if status_data.status == "completed":
        order.completed_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(order)
    
    # Загружаем items
    items_result = await db.execute(
        select(OrderItem).where(OrderItem.order_id == order.id)
    )
    order.items = items_result.scalars().all()
    
    return order
