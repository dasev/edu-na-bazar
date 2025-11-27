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
        from sqlalchemy.orm import selectinload
        
        query = select(Order).where(Order.user_id == user.id).options(selectinload(Order.items))
        
        if status:
            query = query.where(Order.status == status)
        
        # Подсчет
        count_query = select(func.count()).select_from(
            select(Order).where(Order.user_id == user.id).subquery()
        )
        if status:
            count_query = select(func.count()).select_from(
                select(Order).where(Order.user_id == user.id, Order.status == status).subquery()
            )
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Сортировка и пагинация
        query = query.order_by(Order.created_at.desc()).offset(skip).limit(limit)
        
        result = await db.execute(query)
        orders = result.scalars().all()
        
        # Преобразуем в словари с загрузкой информации о товарах
        orders_data = []
        for order in orders:
            # Загружаем товары для items
            items_with_products = []
            for item in order.items:
                # Получаем товар
                from models.product import Product
                product_result = await db.execute(
                    select(Product).where(Product.id == item.product_id)
                )
                product = product_result.scalar_one_or_none()
                
                items_with_products.append({
                    "id": item.id,
                    "order_id": item.order_id,
                    "product_id": item.product_id,
                    "product_name": product.name if product else f"Товар {item.product_id}",
                    "product_image": product.image if product else None,
                    "quantity": item.quantity,
                    "price": float(item.price),
                    "subtotal": item.subtotal,
                    "created_at": item.created_at,
                })
            
            orders_data.append({
                "id": order.id,
                "user_id": order.user_id,
                "store_id": order.store_id,
                "status": order.status,
                "total_amount": float(order.total_amount),
                "delivery_address": order.delivery_address,
                "delivery_phone": order.delivery_phone,
                "payment_method": order.payment_method,
                "notes": order.notes,
                "created_at": order.created_at,
                "updated_at": order.updated_at,
                "items": items_with_products
            })
        
        return OrderListResponse(
            data=orders_data,
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
    order_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить детали заказа"""
    from sqlalchemy.orm import selectinload
    
    result = await db.execute(
        select(Order)
        .where(Order.id == order_id, Order.user_id == user.id)
        .options(selectinload(Order.items))
    )
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    
    # Преобразуем в словарь
    order_dict = {
        "id": order.id,
        "user_id": order.user_id,
        "store_id": order.store_id,
        "status": order.status,
        "total_amount": float(order.total_amount),
        "delivery_address": order.delivery_address,
        "delivery_phone": order.delivery_phone,
        "payment_method": order.payment_method,
        "notes": order.notes,
        "created_at": order.created_at,
        "updated_at": order.updated_at,
        "items": [
            {
                "id": item.id,
                "order_id": item.order_id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": float(item.price),
                "subtotal": item.subtotal,
                "created_at": item.created_at,
            }
            for item in order.items
        ]
    }
    
    return order_dict


@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(
    order_data: OrderCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Создать новый заказ"""
    try:
        print(f"📝 Creating order for user {user.id}")
        print(f"Order data: {order_data}")
        
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
            
            subtotal = float(product.price) * item_data.quantity
            total += subtotal
            
            order_items_data.append({
                "product_id": product.id,
                "quantity": item_data.quantity,
                "price": product.price,
            })
        
        # Создаем заказ
        order = Order(
            user_id=user.id,
            status="created",
            total_amount=total,
            delivery_address=order_data.delivery_address,
            delivery_phone=order_data.contact_phone,
            payment_method=order_data.payment_method,
            notes=order_data.comment,
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
        
        await db.commit()
        
        # Загружаем заказ заново с items
        from sqlalchemy.orm import selectinload
        result = await db.execute(
            select(Order)
            .where(Order.id == order.id)
            .options(selectinload(Order.items))
        )
        order_with_items = result.scalar_one()
        
        # Преобразуем в словарь чтобы избежать проблем с сессией
        order_dict = {
            "id": order_with_items.id,
            "user_id": order_with_items.user_id,
            "store_id": order_with_items.store_id,
            "status": order_with_items.status,
            "total_amount": float(order_with_items.total_amount),
            "delivery_address": order_with_items.delivery_address,
            "delivery_phone": order_with_items.delivery_phone,
            "payment_method": order_with_items.payment_method,
            "notes": order_with_items.notes,
            "created_at": order_with_items.created_at,
            "updated_at": order_with_items.updated_at,
            "items": [
                {
                    "id": item.id,
                    "order_id": item.order_id,
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": float(item.price),
                    "subtotal": item.subtotal,
                    "created_at": item.created_at,
                }
                for item in order_with_items.items
            ]
        }
        
        print(f"✅ Order created: {order_dict['id']}")
        return order_dict
    except Exception as e:
        print(f"❌ Error creating order: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка создания заказа: {str(e)}")


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
