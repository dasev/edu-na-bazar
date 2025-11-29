"""
Admin API endpoints - управление пользователями
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, text
from typing import List, Optional

from database import get_db
from models.user import User
from models.store_owner import StoreOwner
from models.product import Product
from models.order import Order
from api.dependencies import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/api/admin", tags=["admin"])


class UserResponse(BaseModel):
    id: int
    phone: str
    email: Optional[str]
    full_name: str
    address: Optional[str]
    is_active: bool
    is_verified: bool
    is_email_verified: bool = False
    is_phone_verified: bool = False
    is_moderator: bool
    status: str
    created_at: str
    last_login: Optional[str]
    # Статистика
    stores_count: int = 0
    products_count: int = 0
    orders_count: int = 0

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_moderator: Optional[bool] = None
    status: Optional[str] = None


class UserStatsResponse(BaseModel):
    total_users: int
    active_users: int
    verified_users: int
    moderators: int
    total_stores: int
    total_products: int
    total_orders: int


def check_admin(current_user: User):
    """Проверка прав администратора"""
    # TODO: Добавить поле is_admin в модель User
    # Временно проверяем is_moderator
    if not current_user.is_moderator:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен. Требуются права администратора."
        )


class UserListResponse(BaseModel):
    data: List[UserResponse]
    totalCount: int


@router.get("/users", response_model=UserListResponse)
async def get_users(
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    is_moderator: Optional[bool] = None,
    is_active: Optional[bool] = None,
    sort: Optional[str] = None,
    id: Optional[int] = None,
    id_lt: Optional[int] = None,
    id_gt: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получить список пользователей (только для администратора)"""
    check_admin(current_user)
    
    print(f"📋 Получение пользователей, admin={current_user.id}, skip={skip}, limit={limit}")
    
    # Базовый запрос с явным указанием всех столбцов
    query = select(User).options()
    
    # Фильтры
    if search:
        query = query.where(
            (User.phone.ilike(f"%{search}%")) |
            (User.full_name.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%"))
        )
    
    if is_moderator is not None:
        query = query.where(User.is_moderator == is_moderator)
    
    if is_active is not None:
        query = query.where(User.is_active == is_active)
    
    if id is not None:
        query = query.where(User.id == id)
    
    if id_lt is not None:
        query = query.where(User.id < id_lt)
    
    if id_gt is not None:
        query = query.where(User.id > id_gt)
    
    # Подсчет общего количества
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Сортировка
    if sort:
        # Формат: "field,asc" или "field,desc"
        parts = sort.split(',')
        if len(parts) == 2:
            field, direction = parts
            if hasattr(User, field):
                order_column = getattr(User, field)
                if direction == 'desc':
                    query = query.order_by(order_column.desc())
                else:
                    query = query.order_by(order_column.asc())
    else:
        query = query.order_by(User.created_at.desc())
    
    # Получаем пользователей с пагинацией
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()
    
    # Явно обновляем объекты из БД
    for user in users:
        await db.refresh(user)
    
    print(f"  Найдено пользователей: {total}, возвращаем: {len(users)}")
    
    # Добавляем статистику для каждого пользователя
    users_with_stats = []
    for user in users:
        # Подсчет магазинов
        stores_result = await db.execute(
            select(func.count(StoreOwner.id)).where(StoreOwner.owner_id == user.id)
        )
        stores_count = stores_result.scalar() or 0
        
        # Подсчет товаров через магазины
        products_result = await db.execute(
            select(func.count(Product.id)).select_from(Product).join(
                StoreOwner, Product.store_owner_id == StoreOwner.id
            ).where(StoreOwner.owner_id == user.id)
        )
        products_count = products_result.scalar() or 0
        
        # Подсчет заказов
        orders_result = await db.execute(
            select(func.count(Order.id)).where(Order.user_id == user.id)
        )
        orders_count = orders_result.scalar() or 0
        
        # Явно получаем значения из БД через raw SQL
        verification_result = await db.execute(
            text("SELECT is_email_verified, is_phone_verified FROM config.users WHERE id = :user_id"),
            {"user_id": user.id}
        )
        verification_row = verification_result.fetchone()
        is_email_verified = verification_row[0] if verification_row else False
        is_phone_verified = verification_row[1] if verification_row else False
        
        user_dict = {
            "id": user.id,
            "phone": user.phone,
            "email": user.email,
            "full_name": user.full_name,
            "address": user.address,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "is_email_verified": is_email_verified,
            "is_phone_verified": is_phone_verified,
            "is_moderator": user.is_moderator,
            "status": user.status,
            "created_at": user.created_at.isoformat(),
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "stores_count": stores_count,
            "products_count": products_count,
            "orders_count": orders_count
        }
        print(f"  User {user.id}: is_email_verified={is_email_verified}, is_phone_verified={is_phone_verified}")
        users_with_stats.append(user_dict)
    
    result = {
        "data": users_with_stats,
        "totalCount": total
    }
    print(f"  Возвращаем первого пользователя: {users_with_stats[0] if users_with_stats else 'нет пользователей'}")
    return result


@router.get("/stats", response_model=UserStatsResponse)
async def get_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получить общую статистику (только для администратора)"""
    check_admin(current_user)
    
    # Общее количество пользователей
    total_users_result = await db.execute(select(func.count(User.id)))
    total_users = total_users_result.scalar() or 0
    
    # Активные пользователи
    active_users_result = await db.execute(
        select(func.count(User.id)).where(User.is_active == True)
    )
    active_users = active_users_result.scalar() or 0
    
    # Верифицированные пользователи
    verified_users_result = await db.execute(
        select(func.count(User.id)).where(User.is_verified == True)
    )
    verified_users = verified_users_result.scalar() or 0
    
    # Модераторы
    moderators_result = await db.execute(
        select(func.count(User.id)).where(User.is_moderator == True)
    )
    moderators = moderators_result.scalar() or 0
    
    # Общее количество магазинов
    total_stores_result = await db.execute(select(func.count(StoreOwner.id)))
    total_stores = total_stores_result.scalar() or 0
    
    # Общее количество товаров
    total_products_result = await db.execute(select(func.count(Product.id)))
    total_products = total_products_result.scalar() or 0
    
    # Общее количество заказов
    total_orders_result = await db.execute(select(func.count(Order.id)))
    total_orders = total_orders_result.scalar() or 0
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "verified_users": verified_users,
        "moderators": moderators,
        "total_stores": total_stores,
        "total_products": total_products,
        "total_orders": total_orders
    }


@router.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Обновить данные пользователя (только для администратора)"""
    check_admin(current_user)
    
    print(f"✏️ Обновление пользователя {user_id}, admin={current_user.id}")
    
    # Получаем пользователя
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    # Обновляем поля
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    await db.commit()
    await db.refresh(user)
    
    # Получаем статистику
    stores_result = await db.execute(
        select(func.count(StoreOwner.id)).where(StoreOwner.owner_id == user.id)
    )
    stores_count = stores_result.scalar() or 0
    
    products_result = await db.execute(
        select(func.count(Product.id)).select_from(Product).join(
            StoreOwner, Product.store_owner_id == StoreOwner.id
        ).where(StoreOwner.owner_id == user.id)
    )
    products_count = products_result.scalar() or 0
    
    orders_result = await db.execute(
        select(func.count(Order.id)).where(Order.user_id == user.id)
    )
    orders_count = orders_result.scalar() or 0
    
    print(f"✅ Пользователь {user_id} обновлен")
    
    return {
        "id": user.id,
        "phone": user.phone,
        "email": user.email,
        "full_name": user.full_name,
        "address": user.address,
        "is_active": user.is_active,
        "is_verified": user.is_verified,
        "is_moderator": user.is_moderator,
        "status": user.status,
        "created_at": user.created_at.isoformat(),
        "last_login": user.last_login.isoformat() if user.last_login else None,
        "stores_count": stores_count,
        "products_count": products_count,
        "orders_count": orders_count
    }


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Удалить пользователя (только для администратора)"""
    check_admin(current_user)
    
    print(f"🗑️ Удаление пользователя {user_id}, admin={current_user.id}")
    
    # Получаем пользователя
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    # Нельзя удалить самого себя
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя удалить самого себя"
        )
    
    await db.delete(user)
    await db.commit()
    
    print(f"✅ Пользователь {user_id} удален")
    
    return {"message": "Пользователь удален", "user_id": user_id}
