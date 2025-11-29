"""
Analytics API endpoints - аналитика и статистика
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, text
from datetime import datetime, timedelta
from typing import List

from database import get_db
from models.user import User
from models.store_owner import StoreOwner
from models.product import Product
from models.order import Order
from models.cart import CartItem
from api.dependencies import get_current_user
from pydantic import BaseModel


router = APIRouter(prefix="/api/analytics", tags=["analytics"])


class DailyStats(BaseModel):
    date: str
    products: int
    stores: int
    orders: int
    users: int


class AnalyticsResponse(BaseModel):
    # Общая статистика
    total_products: int
    total_stores: int
    total_orders: int
    total_users: int
    
    # Статистика за последние 30 дней
    daily_stats: List[DailyStats]
    
    # Топ категорий
    top_categories: List[dict]


class FinancialStats(BaseModel):
    date: str
    revenue: float
    orders_count: int
    avg_order_value: float


class FinancialAnalyticsResponse(BaseModel):
    total_revenue: float
    avg_order_value: float
    daily_stats: List[FinancialStats]
    top_products_by_revenue: List[dict]
    revenue_by_category: List[dict]


class UserActivityStats(BaseModel):
    date: str
    new_users: int
    active_users: int
    orders_made: int


class UserActivityResponse(BaseModel):
    total_users: int
    active_today: int
    new_this_month: int
    retention_rate: float
    daily_stats: List[UserActivityStats]
    users_by_registration_source: List[dict]
    top_active_users: List[dict]


class ConversionStats(BaseModel):
    date: str
    views: int
    cart_adds: int
    orders: int
    conversion_rate: float


class ConversionResponse(BaseModel):
    total_views: int
    total_cart_adds: int
    total_orders: int
    overall_conversion_rate: float
    cart_to_order_rate: float
    abandoned_carts: int
    daily_stats: List[ConversionStats]
    conversion_by_category: List[dict]
    # Новые метрики
    product_clicks: int
    add_to_cart_clicks: int
    checkout_starts: int
    avg_time_to_purchase: float  # в минутах
    abandoned_cart_value: float  # средняя сумма брошенной корзины


class ProductAnalyticsResponse(BaseModel):
    top_products_by_conversion: List[dict]  # Топ товаров по конверсии
    worst_products_by_conversion: List[dict]  # Худшие по конверсии
    locomotive_products: List[dict]  # Товары-локомотивы
    cross_sell_pairs: List[dict]  # Пары товаров для cross-sell


class GeoAnalyticsResponse(BaseModel):
    conversion_by_city: List[dict]  # Конверсия по городам
    orders_by_city: List[dict]  # Заказы по городам
    revenue_by_city: List[dict]  # Выручка по городам
    top_cities: List[dict]  # Топ городов


@router.get("/financial", response_model=FinancialAnalyticsResponse)
async def get_financial_analytics(
    days: int = 30,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получить финансовую аналитику"""
    
    print(f"💰 Запрос финансовой аналитики от пользователя {current_user.id}")
    
    # Общая выручка
    total_revenue_result = await db.execute(
        select(func.sum(Order.total_amount)).where(Order.status != 'cancelled')
    )
    total_revenue = float(total_revenue_result.scalar() or 0)
    
    # Средний чек
    avg_order_result = await db.execute(
        select(func.avg(Order.total_amount)).where(Order.status != 'cancelled')
    )
    avg_order_value = float(avg_order_result.scalar() or 0)
    
    # Статистика по дням
    daily_stats = []
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        next_date = current_date + timedelta(days=1)
        
        # Выручка за день
        revenue_result = await db.execute(
            select(func.sum(Order.total_amount)).where(
                and_(
                    Order.created_at >= current_date,
                    Order.created_at < next_date,
                    Order.status != 'cancelled'
                )
            )
        )
        revenue = float(revenue_result.scalar() or 0)
        
        # Количество заказов
        orders_result = await db.execute(
            select(func.count(Order.id)).where(
                and_(
                    Order.created_at >= current_date,
                    Order.created_at < next_date,
                    Order.status != 'cancelled'
                )
            )
        )
        orders_count = orders_result.scalar() or 0
        
        # Средний чек за день
        avg_value = revenue / orders_count if orders_count > 0 else 0
        
        daily_stats.append(FinancialStats(
            date=current_date.isoformat(),
            revenue=revenue,
            orders_count=orders_count,
            avg_order_value=avg_value
        ))
    
    # Топ товаров по выручке
    top_products_result = await db.execute(
        text("""
            SELECT p.name, SUM(oi.price * oi.quantity) as revenue
            FROM market.order_items oi
            JOIN market.products p ON p.id = oi.product_id
            JOIN market.orders o ON o.id = oi.order_id
            WHERE o.status != 'cancelled'
            GROUP BY p.id, p.name
            ORDER BY revenue DESC
            LIMIT 10
        """)
    )
    top_products = [
        {"name": row[0], "revenue": float(row[1])}
        for row in top_products_result.fetchall()
    ]
    
    # Выручка по категориям
    revenue_by_category_result = await db.execute(
        text("""
            SELECT c.name, SUM(oi.price * oi.quantity) as revenue
            FROM market.order_items oi
            JOIN market.products p ON p.id = oi.product_id
            JOIN market.categories c ON c.id = p.category_id
            JOIN market.orders o ON o.id = oi.order_id
            WHERE o.status != 'cancelled'
            GROUP BY c.id, c.name
            ORDER BY revenue DESC
            LIMIT 10
        """)
    )
    revenue_by_category = [
        {"name": row[0], "revenue": float(row[1])}
        for row in revenue_by_category_result.fetchall()
    ]
    
    return {
        "total_revenue": total_revenue,
        "avg_order_value": avg_order_value,
        "daily_stats": daily_stats,
        "top_products_by_revenue": top_products,
        "revenue_by_category": revenue_by_category
    }


@router.get("/user-activity", response_model=UserActivityResponse)
async def get_user_activity_analytics(
    days: int = 30,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получить аналитику активности пользователей"""
    
    print(f"👥 Запрос аналитики активности пользователей от {current_user.id}")
    
    # Общее количество пользователей
    total_users_result = await db.execute(select(func.count(User.id)))
    total_users = total_users_result.scalar() or 0
    
    # Активные сегодня (сделали заказ)
    today = datetime.now().date()
    active_today_result = await db.execute(
        select(func.count(func.distinct(Order.user_id))).where(
            Order.created_at >= today
        )
    )
    active_today = active_today_result.scalar() or 0
    
    # Новые за месяц
    month_ago = today - timedelta(days=30)
    new_this_month_result = await db.execute(
        select(func.count(User.id)).where(User.created_at >= month_ago)
    )
    new_this_month = new_this_month_result.scalar() or 0
    
    # Retention rate (упрощенный: пользователи с >1 заказом / всего пользователей)
    repeat_users_result = await db.execute(
        text("""
            SELECT COUNT(DISTINCT user_id)
            FROM market.orders
            GROUP BY user_id
            HAVING COUNT(*) > 1
        """)
    )
    repeat_users = len(repeat_users_result.fetchall())
    retention_rate = (repeat_users / total_users * 100) if total_users > 0 else 0
    
    # Статистика по дням
    daily_stats = []
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        next_date = current_date + timedelta(days=1)
        
        # Новые пользователи
        new_users_result = await db.execute(
            select(func.count(User.id)).where(
                and_(
                    User.created_at >= current_date,
                    User.created_at < next_date
                )
            )
        )
        new_users = new_users_result.scalar() or 0
        
        # Активные пользователи (сделали заказ)
        active_users_result = await db.execute(
            select(func.count(func.distinct(Order.user_id))).where(
                and_(
                    Order.created_at >= current_date,
                    Order.created_at < next_date
                )
            )
        )
        active_users = active_users_result.scalar() or 0
        
        # Количество заказов
        orders_result = await db.execute(
            select(func.count(Order.id)).where(
                and_(
                    Order.created_at >= current_date,
                    Order.created_at < next_date
                )
            )
        )
        orders_made = orders_result.scalar() or 0
        
        daily_stats.append(UserActivityStats(
            date=current_date.isoformat(),
            new_users=new_users,
            active_users=active_users,
            orders_made=orders_made
        ))
    
    # Источники регистрации (заглушка - у нас пока только телефон)
    users_by_source = [
        {"source": "Телефон", "count": total_users}
    ]
    
    # Топ активных пользователей
    top_users_result = await db.execute(
        text("""
            SELECT u.full_name, u.phone, COUNT(o.id) as orders_count
            FROM config.users u
            JOIN market.orders o ON o.user_id = u.id
            GROUP BY u.id, u.full_name, u.phone
            ORDER BY orders_count DESC
            LIMIT 10
        """)
    )
    top_active_users = [
        {"name": row[0] or row[1], "orders_count": row[2]}
        for row in top_users_result.fetchall()
    ]
    
    return {
        "total_users": total_users,
        "active_today": active_today,
        "new_this_month": new_this_month,
        "retention_rate": retention_rate,
        "daily_stats": daily_stats,
        "users_by_registration_source": users_by_source,
        "top_active_users": top_active_users
    }


@router.get("/conversion", response_model=ConversionResponse)
async def get_conversion_analytics(
    days: int = 30,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получить аналитику конверсии и воронки продаж"""
    
    print(f"🎯 Запрос аналитики конверсии от пользователя {current_user.id}")
    
    # Реальные просмотры из таблицы product_views
    from models.product_view import ProductView
    total_views_result = await db.execute(select(func.count(ProductView.id)))
    total_views = total_views_result.scalar() or 0
    
    # Добавления в корзину
    total_cart_adds_result = await db.execute(select(func.count(CartItem.id)))
    total_cart_adds = total_cart_adds_result.scalar() or 0
    
    # Заказы
    total_orders_result = await db.execute(
        select(func.count(Order.id)).where(Order.status != 'cancelled')
    )
    total_orders = total_orders_result.scalar() or 0
    
    # Конверсия
    overall_conversion_rate = (total_orders / total_views * 100) if total_views > 0 else 0
    cart_to_order_rate = (total_orders / total_cart_adds * 100) if total_cart_adds > 0 else 0
    
    # Брошенные корзины (товары в корзине, но заказ не оформлен)
    abandoned_carts_result = await db.execute(
        text("""
            SELECT COUNT(DISTINCT ci.user_id)
            FROM market.cart_items ci
            LEFT JOIN market.orders o ON o.user_id = ci.user_id 
                AND o.created_at > ci.created_at
            WHERE o.id IS NULL
        """)
    )
    abandoned_carts = abandoned_carts_result.scalar() or 0
    
    # Новые метрики из событий
    from models.user_event import UserEvent
    
    # Клики по товарам
    product_clicks_result = await db.execute(
        select(func.count(UserEvent.id)).where(UserEvent.event_type == 'product_click')
    )
    product_clicks = product_clicks_result.scalar() or 0
    
    # Клики "Добавить в корзину"
    add_to_cart_clicks_result = await db.execute(
        select(func.count(UserEvent.id)).where(UserEvent.event_type == 'add_to_cart_click')
    )
    add_to_cart_clicks = add_to_cart_clicks_result.scalar() or 0
    
    # Начало оформления заказа
    checkout_starts_result = await db.execute(
        select(func.count(UserEvent.id)).where(UserEvent.event_type == 'checkout_start')
    )
    checkout_starts = checkout_starts_result.scalar() or 0
    
    # Среднее время до покупки (от первого просмотра до заказа)
    avg_time_result = await db.execute(
        text("""
            SELECT AVG(EXTRACT(EPOCH FROM (o.created_at - pv.created_at)) / 60) as avg_minutes
            FROM market.orders o
            JOIN market.product_views pv ON pv.user_id = o.user_id
            WHERE o.status != 'cancelled'
            AND pv.created_at < o.created_at
            AND pv.created_at > o.created_at - INTERVAL '7 days'
        """)
    )
    avg_time_to_purchase = float(avg_time_result.scalar() or 0)
    
    # Средняя сумма брошенной корзины
    abandoned_value_result = await db.execute(
        text("""
            SELECT AVG(cart_total) FROM (
                SELECT ci.user_id, SUM(p.price * ci.quantity) as cart_total
                FROM market.cart_items ci
                JOIN market.products p ON p.id = ci.product_id
                LEFT JOIN market.orders o ON o.user_id = ci.user_id 
                    AND o.created_at > ci.created_at
                WHERE o.id IS NULL
                GROUP BY ci.user_id
            ) as abandoned_carts
        """)
    )
    abandoned_cart_value = float(abandoned_value_result.scalar() or 0)
    
    # Статистика по дням
    daily_stats = []
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        next_date = current_date + timedelta(days=1)
        
        # Реальные просмотры за день
        views_result = await db.execute(
            select(func.count(ProductView.id)).where(
                and_(
                    ProductView.created_at >= current_date,
                    ProductView.created_at < next_date
                )
            )
        )
        views = views_result.scalar() or 0
        
        # Добавления в корзину
        cart_adds_result = await db.execute(
            select(func.count(CartItem.id)).where(
                and_(
                    CartItem.created_at >= current_date,
                    CartItem.created_at < next_date
                )
            )
        )
        cart_adds = cart_adds_result.scalar() or 0
        
        # Заказы
        orders_result = await db.execute(
            select(func.count(Order.id)).where(
                and_(
                    Order.created_at >= current_date,
                    Order.created_at < next_date,
                    Order.status != 'cancelled'
                )
            )
        )
        orders = orders_result.scalar() or 0
        
        # Конверсия за день
        conversion_rate = (orders / views * 100) if views > 0 else 0
        
        daily_stats.append(ConversionStats(
            date=current_date.isoformat(),
            views=views,
            cart_adds=cart_adds,
            orders=orders,
            conversion_rate=conversion_rate
        ))
    
    # Конверсия по категориям
    conversion_by_category_result = await db.execute(
        text("""
            SELECT c.name, 
                   COUNT(DISTINCT p.id) as products,
                   COUNT(DISTINCT o.id) as orders
            FROM market.categories c
            LEFT JOIN market.products p ON p.category_id = c.id
            LEFT JOIN market.order_items oi ON oi.product_id = p.id
            LEFT JOIN market.orders o ON o.id = oi.order_id AND o.status != 'cancelled'
            GROUP BY c.id, c.name
            HAVING COUNT(DISTINCT p.id) > 0
            ORDER BY orders DESC
            LIMIT 10
        """)
    )
    conversion_by_category = [
        {
            "name": row[0], 
            "products": row[1],
            "orders": row[2],
            "conversion_rate": (row[2] / (row[1] * 10) * 100) if row[1] > 0 else 0
        }
        for row in conversion_by_category_result.fetchall()
    ]
    
    return {
        "total_views": total_views,
        "total_cart_adds": total_cart_adds,
        "total_orders": total_orders,
        "overall_conversion_rate": overall_conversion_rate,
        "cart_to_order_rate": cart_to_order_rate,
        "abandoned_carts": abandoned_carts,
        "daily_stats": daily_stats,
        "conversion_by_category": conversion_by_category,
        "product_clicks": product_clicks,
        "add_to_cart_clicks": add_to_cart_clicks,
        "checkout_starts": checkout_starts,
        "avg_time_to_purchase": avg_time_to_purchase,
        "abandoned_cart_value": abandoned_cart_value
    }


@router.get("/products", response_model=ProductAnalyticsResponse)
async def get_product_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получить товарную аналитику"""
    
    print(f"📦 Запрос товарной аналитики от пользователя {current_user.id}")
    
    from models.product_view import ProductView
    
    # Топ товаров по конверсии (просмотры → заказы)
    top_conversion_result = await db.execute(
        text("""
            SELECT p.id, p.name, 
                   COUNT(DISTINCT pv.id) as views,
                   COUNT(DISTINCT oi.order_id) as orders,
                   CASE WHEN COUNT(DISTINCT pv.id) > 0 
                        THEN (COUNT(DISTINCT oi.order_id)::float / COUNT(DISTINCT pv.id) * 100)
                        ELSE 0 
                   END as conversion_rate
            FROM market.products p
            LEFT JOIN market.product_views pv ON pv.product_id = p.id
            LEFT JOIN market.order_items oi ON oi.product_id = p.id
            LEFT JOIN market.orders o ON o.id = oi.order_id AND o.status != 'cancelled'
            GROUP BY p.id, p.name
            HAVING COUNT(DISTINCT pv.id) > 10
            ORDER BY conversion_rate DESC
            LIMIT 10
        """)
    )
    top_products = [
        {
            "id": row[0],
            "name": row[1],
            "views": row[2],
            "orders": row[3],
            "conversion_rate": float(row[4])
        }
        for row in top_conversion_result.fetchall()
    ]
    
    # Худшие товары по конверсии
    worst_conversion_result = await db.execute(
        text("""
            SELECT p.id, p.name, 
                   COUNT(DISTINCT pv.id) as views,
                   COUNT(DISTINCT oi.order_id) as orders,
                   CASE WHEN COUNT(DISTINCT pv.id) > 0 
                        THEN (COUNT(DISTINCT oi.order_id)::float / COUNT(DISTINCT pv.id) * 100)
                        ELSE 0 
                   END as conversion_rate
            FROM market.products p
            LEFT JOIN market.product_views pv ON pv.product_id = p.id
            LEFT JOIN market.order_items oi ON oi.product_id = p.id
            LEFT JOIN market.orders o ON o.id = oi.order_id AND o.status != 'cancelled'
            GROUP BY p.id, p.name
            HAVING COUNT(DISTINCT pv.id) > 10
            ORDER BY conversion_rate ASC
            LIMIT 10
        """)
    )
    worst_products = [
        {
            "id": row[0],
            "name": row[1],
            "views": row[2],
            "orders": row[3],
            "conversion_rate": float(row[4])
        }
        for row in worst_conversion_result.fetchall()
    ]
    
    # Товары-локомотивы (часто покупаются вместе с другими)
    locomotive_result = await db.execute(
        text("""
            SELECT p.id, p.name, 
                   COUNT(DISTINCT o.id) as orders_count,
                   AVG(order_items_count) as avg_items_in_order
            FROM market.products p
            JOIN market.order_items oi ON oi.product_id = p.id
            JOIN market.orders o ON o.id = oi.order_id AND o.status != 'cancelled'
            JOIN (
                SELECT order_id, COUNT(*) as order_items_count
                FROM market.order_items
                GROUP BY order_id
            ) oi_counts ON oi_counts.order_id = o.id
            GROUP BY p.id, p.name
            HAVING AVG(order_items_count) > 1.5
            ORDER BY orders_count DESC
            LIMIT 10
        """)
    )
    locomotive_products = [
        {
            "id": row[0],
            "name": row[1],
            "orders_count": row[2],
            "avg_items_in_order": float(row[3])
        }
        for row in locomotive_result.fetchall()
    ]
    
    # Cross-sell пары (товары, которые часто покупают вместе)
    cross_sell_result = await db.execute(
        text("""
            SELECT p1.name as product1, p2.name as product2, COUNT(*) as frequency
            FROM market.order_items oi1
            JOIN market.order_items oi2 ON oi1.order_id = oi2.order_id AND oi1.product_id < oi2.product_id
            JOIN market.products p1 ON p1.id = oi1.product_id
            JOIN market.products p2 ON p2.id = oi2.product_id
            JOIN market.orders o ON o.id = oi1.order_id AND o.status != 'cancelled'
            GROUP BY p1.id, p1.name, p2.id, p2.name
            ORDER BY frequency DESC
            LIMIT 10
        """)
    )
    cross_sell_pairs = [
        {
            "product1": row[0],
            "product2": row[1],
            "frequency": row[2]
        }
        for row in cross_sell_result.fetchall()
    ]
    
    return {
        "top_products_by_conversion": top_products,
        "worst_products_by_conversion": worst_products,
        "locomotive_products": locomotive_products,
        "cross_sell_pairs": cross_sell_pairs
    }


@router.get("/geography", response_model=GeoAnalyticsResponse)
async def get_geo_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получить географическую аналитику"""
    
    print(f"🗺️ Запрос географической аналитики от пользователя {current_user.id}")
    
    # Извлекаем город из адреса доставки (упрощенно - первое слово)
    # Конверсия по городам
    conversion_by_city_result = await db.execute(
        text("""
            WITH city_stats AS (
                SELECT 
                    SUBSTRING(delivery_address FROM 1 FOR POSITION(',' IN delivery_address || ',') - 1) as city,
                    COUNT(DISTINCT o.id) as orders,
                    COUNT(DISTINCT o.user_id) as users
                FROM market.orders o
                WHERE o.status != 'cancelled'
                AND delivery_address IS NOT NULL
                AND delivery_address != ''
                GROUP BY city
            )
            SELECT 
                city,
                orders,
                users,
                CASE WHEN users > 0 THEN (orders::float / users * 100) ELSE 0 END as conversion_rate
            FROM city_stats
            WHERE city != '' AND city IS NOT NULL
            ORDER BY orders DESC
            LIMIT 20
        """)
    )
    conversion_by_city = [
        {
            "city": row[0],
            "orders": row[1],
            "users": row[2],
            "conversion_rate": float(row[3])
        }
        for row in conversion_by_city_result.fetchall()
    ]
    
    # Заказы по городам
    orders_by_city_result = await db.execute(
        text("""
            SELECT 
                SUBSTRING(delivery_address FROM 1 FOR POSITION(',' IN delivery_address || ',') - 1) as city,
                COUNT(*) as orders_count
            FROM market.orders
            WHERE status != 'cancelled'
            AND delivery_address IS NOT NULL
            AND delivery_address != ''
            GROUP BY city
            HAVING SUBSTRING(delivery_address FROM 1 FOR POSITION(',' IN delivery_address || ',') - 1) != ''
            ORDER BY orders_count DESC
            LIMIT 20
        """)
    )
    orders_by_city = [
        {"city": row[0], "orders_count": row[1]}
        for row in orders_by_city_result.fetchall()
    ]
    
    # Выручка по городам
    revenue_by_city_result = await db.execute(
        text("""
            SELECT 
                SUBSTRING(o.delivery_address FROM 1 FOR POSITION(',' IN o.delivery_address || ',') - 1) as city,
                SUM(o.total_amount) as revenue
            FROM market.orders o
            WHERE o.status != 'cancelled'
            AND o.delivery_address IS NOT NULL
            AND o.delivery_address != ''
            GROUP BY city
            HAVING SUBSTRING(o.delivery_address FROM 1 FOR POSITION(',' IN o.delivery_address || ',') - 1) != ''
            ORDER BY revenue DESC
            LIMIT 20
        """)
    )
    revenue_by_city = [
        {"city": row[0], "revenue": float(row[1])}
        for row in revenue_by_city_result.fetchall()
    ]
    
    # Топ городов (комплексная метрика)
    top_cities_result = await db.execute(
        text("""
            SELECT 
                SUBSTRING(o.delivery_address FROM 1 FOR POSITION(',' IN o.delivery_address || ',') - 1) as city,
                COUNT(*) as orders,
                SUM(o.total_amount) as revenue,
                COUNT(DISTINCT o.user_id) as users
            FROM market.orders o
            WHERE o.status != 'cancelled'
            AND o.delivery_address IS NOT NULL
            AND o.delivery_address != ''
            GROUP BY city
            HAVING SUBSTRING(o.delivery_address FROM 1 FOR POSITION(',' IN o.delivery_address || ',') - 1) != ''
            ORDER BY orders DESC
            LIMIT 10
        """)
    )
    top_cities = [
        {
            "city": row[0],
            "orders": row[1],
            "revenue": float(row[2]),
            "users": row[3]
        }
        for row in top_cities_result.fetchall()
    ]
    
    return {
        "conversion_by_city": conversion_by_city,
        "orders_by_city": orders_by_city,
        "revenue_by_city": revenue_by_city,
        "top_cities": top_cities
    }


@router.get("/dashboard", response_model=AnalyticsResponse)
async def get_dashboard_analytics(
    days: int = 30,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получить данные для базового дашборда аналитики"""
    
    print(f"📊 Запрос базового дашборда от пользователя {current_user.id}")
    
    # Общая статистика
    total_products_result = await db.execute(select(func.count(Product.id)))
    total_products = total_products_result.scalar() or 0
    
    total_stores_result = await db.execute(select(func.count(StoreOwner.id)))
    total_stores = total_stores_result.scalar() or 0
    
    total_orders_result = await db.execute(select(func.count(Order.id)))
    total_orders = total_orders_result.scalar() or 0
    
    total_users_result = await db.execute(select(func.count(User.id)))
    total_users = total_users_result.scalar() or 0
    
    # Статистика по дням за последние N дней
    daily_stats = []
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        next_date = current_date + timedelta(days=1)
        
        # Товары созданные в этот день
        products_result = await db.execute(
            select(func.count(Product.id)).where(
                and_(
                    Product.created_at >= current_date,
                    Product.created_at < next_date
                )
            )
        )
        products_count = products_result.scalar() or 0
        
        # Магазины созданные в этот день
        stores_result = await db.execute(
            select(func.count(StoreOwner.id)).where(
                and_(
                    StoreOwner.created_at >= current_date,
                    StoreOwner.created_at < next_date
                )
            )
        )
        stores_count = stores_result.scalar() or 0
        
        # Заказы созданные в этот день
        orders_result = await db.execute(
            select(func.count(Order.id)).where(
                and_(
                    Order.created_at >= current_date,
                    Order.created_at < next_date
                )
            )
        )
        orders_count = orders_result.scalar() or 0
        
        # Пользователи зарегистрированные в этот день
        users_result = await db.execute(
            select(func.count(User.id)).where(
                and_(
                    User.created_at >= current_date,
                    User.created_at < next_date
                )
            )
        )
        users_count = users_result.scalar() or 0
        
        daily_stats.append(DailyStats(
            date=current_date.isoformat(),
            products=products_count,
            stores=stores_count,
            orders=orders_count,
            users=users_count
        ))
    
    # Топ категорий по количеству товаров
    top_categories_result = await db.execute(
        text("""
            SELECT c.name, c.image, COUNT(p.id) as count
            FROM market.categories c
            LEFT JOIN market.products p ON p.category_id = c.id
            GROUP BY c.id, c.name, c.image
            ORDER BY count DESC
            LIMIT 10
        """)
    )
    top_categories = [
        {"name": row[0], "icon": row[1] or "📦", "count": row[2]}
        for row in top_categories_result.fetchall()
    ]
    
    return {
        "total_products": total_products,
        "total_stores": total_stores,
        "total_orders": total_orders,
        "total_users": total_users,
        "daily_stats": daily_stats,
        "top_categories": top_categories
    }
