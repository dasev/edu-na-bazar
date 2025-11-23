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
    product_id: str
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
    id: str
    product_id: str
    product_name: str
    product_image: Optional[str]
    quantity: int
    price: Decimal
    subtotal: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    """Схема ответа с заказом"""
    id: str
    user_id: str
    status: str
    total: Decimal
    delivery_address: str
    delivery_time: Optional[datetime]
    delivery_comment: Optional[str]
    payment_method: str
    payment_status: str
    contact_phone: str
    contact_name: str
    comment: Optional[str]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    """Схема ответа со списком заказов"""
    data: List[OrderResponse]
    meta: dict
