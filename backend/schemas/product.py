"""
Product schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# Request schemas
class ProductCreate(BaseModel):
    """Схема для создания товара"""
    name: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    image: Optional[str] = None
    images: Optional[List[str]] = None  # Массив URL изображений
    category_id: Optional[int] = None
    rating: float = Field(default=0.0, ge=0, le=5)
    reviews_count: int = Field(default=0, ge=0)
    in_stock: bool = True
    unit: str = Field(default="шт", max_length=50)
    latitude: Optional[float] = None  # Широта
    longitude: Optional[float] = None  # Долгота
    location: Optional[str] = None  # Текстовый адрес


class ProductUpdate(BaseModel):
    """Схема для обновления товара"""
    name: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    image: Optional[str] = None
    images: Optional[List[str]] = None  # Массив URL изображений
    category_id: Optional[int] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    reviews_count: Optional[int] = Field(None, ge=0)
    in_stock: Optional[bool] = None
    unit: Optional[str] = Field(None, max_length=50)
    stock_quantity: Optional[int] = Field(None, ge=0)
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=500)
    latitude: Optional[float] = None  # Широта
    longitude: Optional[float] = None  # Долгота
    location: Optional[str] = None  # Текстовый адрес


# Response schemas
class ProductImageSchema(BaseModel):
    """Схема изображения товара"""
    id: int
    image_url: str
    sort_order: int = 0
    
    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    """Схема ответа с товаром"""
    id: int
    name: str
    description: Optional[str]
    price: float
    image: Optional[str]
    category_id: Optional[int]
    store_owner_id: Optional[int] = None  # ID магазина
    rating: float
    reviews_count: int
    in_stock: bool
    unit: str
    created_at: datetime
    updated_at: datetime
    images: List[ProductImageSchema] = []  # Все изображения товара
    latitude: Optional[float] = None  # Широта для карты
    longitude: Optional[float] = None  # Долгота для карты
    location: Optional[str] = None  # Текстовый адрес
    
    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """Схема ответа со списком товаров"""
    data: List[ProductResponse]
    meta: dict


# Filters
class ProductFilters(BaseModel):
    """Фильтры для товаров"""
    category_id: Optional[int] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    in_stock: Optional[bool] = None
    search: Optional[str] = None
    sort_by: Optional[str] = Field(default="created_at", pattern="^(price|created_at|name)$")
    sort_order: Optional[str] = Field(default="desc", pattern="^(asc|desc)$")
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)
