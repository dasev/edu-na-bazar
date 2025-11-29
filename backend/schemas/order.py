"""
Order schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


# Request schemas
class OrderItemCreate(BaseModel):
    """Схема для создания товара в заказе"""
    product_id: int
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    """Схема для создания заказа"""
    items: List[OrderItemCreate] = Field(..., min_length=1)
    delivery_address: str = Field(..., min_length=1, max_length=500)
    delivery_time: Optional[datetime] = None
    delivery_comment: Optional[str] = None
    payment_method: str = Field(..., pattern="^(card|cash|online)$")
    contact_phone: str = Field(..., min_length=10, max_length=20)
    contact_name: str = Field(..., min_length=1, max_length=255)
    comment: Optional[str] = None


class OrderUpdateStatus(BaseModel):
    """Схема для обновления статуса заказа"""
    status: str = Field(..., pattern="^(created|paid|processing|delivering|completed|cancelled)$")


# Response schemas
class OrderItemResponse(BaseModel):
    """Схема ответа с товаром в заказе"""
    id: int
    order_id: int
    product_id: int
    product_name: Optional[str] = None  # Название товара
    product_image: Optional[str] = None  # Изображение товара
    quantity: int
    price: float
    subtotal: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    """Схема ответа с заказом"""
    id: int
    user_id: int
    store_id: Optional[int]
    status: str
    total_amount: float
    delivery_address: str
    delivery_phone: str
    payment_method: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    """Схема ответа со списком заказов"""
    data: List[OrderResponse]
    meta: dict
