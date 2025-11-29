"""
Product model
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, Boolean, BigInteger, ForeignKey, Text, ARRAY, Double
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from database import Base

# Forward reference для избежания циклического импорта
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.product_image import ProductImage


class Product(Base):
    """Product model - товары"""
    __tablename__ = "products"
    __table_args__ = {'schema': 'market'}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Основная информация
    name = Column(Text, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Цены
    price = Column(Double, nullable=False)
    
    # Изображения
    image = Column(Text, nullable=True)  # Основное изображение
    
    # Категория
    category_id = Column(BigInteger, ForeignKey('market.categories.id'), nullable=True, index=True)
    
    # Магазин (владелец)
    store_owner_id = Column(BigInteger, ForeignKey('market.store_owners.id'), nullable=True, index=True)
    
    # Рейтинг и отзывы
    rating = Column(Double, default=0.0)
    reviews_count = Column(BigInteger, default=0)
    
    # Наличие
    in_stock = Column(Boolean, default=True)
    
    # Единица измерения
    unit = Column(Text, default="шт")  # шт, кг, л, упак
    
    # Дополнительные поля для миграции
    views = Column(BigInteger, default=0)  # Количество просмотров
    location = Column(Text, nullable=True)  # Адрес/местоположение товара
    status = Column(Text, default="active")  # active, archived, moderation
    
    # Геолокация (PostGIS)
    latitude = Column(Double, nullable=True)  # Широта
    longitude = Column(Double, nullable=True)  # Долгота
    geo_location = Column(Geometry('POINT', srid=4326), nullable=True)  # Точка на карте
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = relationship("Category", back_populates="products")
    store_owner = relationship("StoreOwner", back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan", lazy="selectin", order_by="ProductImage.sort_order")
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    product_reviews = relationship("ProductReview", back_populates="product", cascade="all, delete-orphan", lazy="noload")
    product_questions = relationship("ProductQuestion", back_populates="product", cascade="all, delete-orphan", lazy="noload")
    messages = relationship("Message", back_populates="product")
    views = relationship("ProductView", back_populates="product", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Product {self.name} - {self.price}₽>"
    
    @property
    def discount_percent(self) -> int:
        """Процент скидки"""
        if self.old_price and self.old_price > self.price:
            return int((1 - float(self.price) / float(self.old_price)) * 100)
        return 0
