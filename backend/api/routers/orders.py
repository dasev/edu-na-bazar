"""
Orders API router
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from datetime import datetime
import asyncio

from database import get_db
from models.order import Order, OrderItem
from models.product import Product
from models.product_image import ProductImage
from models.user import User
from models.store_owner import StoreOwner
from schemas.order import (
    OrderCreate,
    OrderUpdateStatus,
    OrderResponse,
    OrderListResponse,
)
from api.dependencies import get_current_user  # Используем стандартный get_current_user
from services.email_service import email_service

router = APIRouter()


async def send_order_created_emails(order_dict: dict, user_data: dict):
    """Отправка email уведомлений при создании заказа"""
    # Создаем новую сессию БД для асинхронной задачи
    from database import AsyncSessionLocal
    
    async with AsyncSessionLocal() as db:
        try:
            print(f"📧 Начинаем отправку email для заказа #{order_dict['id']}")
            print(f"   Пользователь: {user_data['full_name']}, Email: {user_data['email']}")
            
            # Получаем товары для email
            items_data = []
            store_id = None
            
            for item in order_dict['items']:
                result = await db.execute(
                    select(Product).where(Product.id == item['product_id'])
                )
                product = result.scalar_one_or_none()
                if product:
                    items_data.append({
                        'name': product.name,
                        'quantity': item['quantity'],
                        'unit': product.unit,
                        'price': item['price']
                    })
                    if not store_id and product.store_owner_id:
                        store_id = product.store_owner_id
            
            print(f"   Товаров в заказе: {len(items_data)}, Store ID: {store_id}")
            
            # Данные для шаблона
            email_data = {
                'order_id': order_dict['id'],
                'customer_name': user_data['full_name'] or 'Покупатель',
                'customer_phone': order_dict['delivery_phone'],
                'store_name': 'Магазин',  # Заполним ниже
                'created_at': order_dict['created_at'].strftime('%d.%m.%Y %H:%M'),
                'delivery_address': order_dict['delivery_address'],
                'items': items_data,
                'total_amount': order_dict['total_amount']
            }
            
            # Отправляем покупателю
            if user_data['email']:
                print(f"   📨 Отправляем письмо покупателю: {user_data['email']}")
                await email_service.send_order_created(user_data['email'], email_data)
            else:
                print(f"   ⚠️ У пользователя нет email, пропускаем отправку покупателю")
            
            # Отправляем магазину
            if store_id:
                result = await db.execute(
                    select(StoreOwner).where(StoreOwner.id == store_id)
                )
                store = result.scalar_one_or_none()
                if store:
                    email_data['store_name'] = store.store_name
                    print(f"   Магазин: {store.store_name}, Email: {store.email}")
                    if store.email:
                        print(f"   📨 Отправляем письмо магазину: {store.email}")
                        await email_service.send_new_order_to_store(store.email, email_data)
                    else:
                        print(f"   ⚠️ У магазина нет email, пропускаем отправку")
                else:
                    print(f"   ⚠️ Магазин не найден")
            else:
                print(f"   ⚠️ Store ID не определен")
        except Exception as e:
            print(f"❌ Ошибка отправки email: {e}")
            import traceback
            traceback.print_exc()


async def send_order_status_email(order: Order, user: User, db: AsyncSession):
    """Отправка email при изменении статуса заказа"""
    try:
        if not user.email:
            return
        
        # Получаем товары
        items_data = []
        store_name = 'Магазин'
        store_address = None
        store_phone = None
        
        for item in order.items:
            result = await db.execute(
                select(Product).where(Product.id == item.product_id)
            )
            product = result.scalar_one_or_none()
            if product:
                items_data.append({
                    'name': product.name,
                    'quantity': item.quantity,
                    'unit': product.unit,
                    'price': float(item.price)
                })
                # Получаем информацию о магазине
                if product.store_owner_id:
                    store_result = await db.execute(
                        select(StoreOwner).where(StoreOwner.id == product.store_owner_id)
                    )
                    store = store_result.scalar_one_or_none()
                    if store:
                        store_name = store.store_name
                        store_address = store.address
                        store_phone = store.phone
        
        email_data = {
            'order_id': order.id,
            'customer_name': user.full_name or 'Покупатель',
            'store_name': store_name,
            'store_address': store_address,
            'store_phone': store_phone,
            'total_amount': float(order.total_amount),
            'items': items_data
        }
        
        # Отправляем соответствующее уведомление
        if order.status == 'paid':
            await email_service.send_order_confirmed(user.email, email_data)
        elif order.status == 'delivering':
            await email_service.send_order_ready(user.email, email_data)
        elif order.status == 'completed':
            await email_service.send_order_completed(user.email, email_data)
        elif order.status == 'cancelled':
            await email_service.send_order_cancelled(user.email, email_data)
    except Exception as e:
        print(f"❌ Ошибка отправки email при изменении статуса: {e}")


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
        print(f"📦 Всего заказов для обработки: {len(orders)}")
        orders_data = []
        for order in orders:
            print(f"📋 Обрабатываем заказ #{order.id}, items: {len(order.items)}")
            # Загружаем товары для items
            items_with_products = []
            for item in order.items:
                try:
                    # Получаем товар с изображениями (lazy="selectin" в модели)
                    product_result = await db.execute(
                        select(Product).where(Product.id == item.product_id)
                    )
                    product = product_result.scalar_one_or_none()
                    
                    # Получаем первое изображение или основное изображение
                    product_image = None
                    product_name = f"Товар {item.product_id}"
                    
                    if product:
                        product_name = product.name
                        print(f"🔍 Товар {item.product_id}: {product.name}, images count: {len(product.images) if product.images else 0}")
                        
                        if product.images and len(product.images) > 0:
                            # Берем первое изображение из массива
                            product_image = product.images[0].image_url
                            print(f"   📸 Изображение: {product_image}")
                        elif product.image:
                            # Fallback на старое поле image
                            product_image = product.image
                            print(f"   📸 Fallback изображение: {product_image}")
                        else:
                            print(f"   ⚠️ Нет изображений")
                    
                    items_with_products.append({
                        "id": item.id,
                        "order_id": item.order_id,
                        "product_id": item.product_id,
                        "product_name": product_name,
                        "product_image": product_image,
                        "quantity": item.quantity,
                        "price": float(item.price),
                        "subtotal": item.subtotal,
                        "created_at": item.created_at,
                    })
                except Exception as e:
                    print(f"❌ Ошибка загрузки товара {item.product_id}: {e}")
                    import traceback
                    traceback.print_exc()
                    # Добавляем базовую информацию
                    items_with_products.append({
                        "id": item.id,
                        "order_id": item.order_id,
                        "product_id": item.product_id,
                        "product_name": f"Товар {item.product_id}",
                        "product_image": None,
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
    
    # Загружаем информацию о товарах
    items_with_products = []
    for item in order.items:
        product_result = await db.execute(
            select(Product).where(Product.id == item.product_id)
        )
        product = product_result.scalar_one_or_none()
        
        # Получаем первое изображение из массива
        product_image = None
        if product:
            if product.images and len(product.images) > 0:
                product_image = product.images[0].image_url
            elif product.image:
                product_image = product.image
        
        print(f"📦 Товар {item.product_id}: name={product.name if product else 'N/A'}, image={product_image}")
        
        items_with_products.append({
            "id": item.id,
            "order_id": item.order_id,
            "product_id": item.product_id,
            "product_name": product.name if product else f"Товар {item.product_id}",
            "product_image": product_image,
            "quantity": item.quantity,
            "price": float(item.price),
            "subtotal": item.subtotal,
            "created_at": item.created_at,
        })
    
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
        "items": items_with_products
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
        
        # Подготавливаем данные пользователя для email (чтобы избежать DetachedInstanceError)
        user_data = {
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name
        }
        
        # Отправляем email уведомления асинхронно (не блокируем ответ)
        asyncio.create_task(send_order_created_emails(order_dict, user_data))
        
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
    
    old_status = order.status
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
    
    # Отправляем email если статус изменился
    if old_status != status_data.status:
        # Получаем пользователя
        user_result = await db.execute(
            select(User).where(User.id == order.user_id)
        )
        order_user = user_result.scalar_one_or_none()
        if order_user:
            asyncio.create_task(send_order_status_email(order, order_user, db))
    
    return order
