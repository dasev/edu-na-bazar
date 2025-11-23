"""
Product model
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID, NUMERIC
from sqlalchemy.orm import relationship
from decimal import Decimal
import uuid
from database import Base


class Product(Base):
    """Product model - товары"""
    __tablename__ = "products"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Основная информация
    name = Column(String(500), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Цены
    price = Column(NUMERIC(10, 2), nullable=False)
    old_price = Column(NUMERIC(10, 2), nullable=True)  # Для отображения скидки
    
    # Изображения
    image = Column(String(500), nullable=True)  # Основное изображение
    
    # Категория
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'), nullable=True, index=True)
    
    # Рейтинг и отзывы
    rating = Column(NUMERIC(3, 2), default=0.0)  # От 0.00 до 5.00
    reviews_count = Column(Integer, default=0)
    
    # Наличие
    in_stock = Column(Boolean, default=True)
    
    # Единица измерения
    unit = Column(String(50), default="шт")  # шт, кг, л, упак
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    
    def __repr__(self):
        return f"<Product {self.name} - {self.price}₽>"
    
    @property
    def discount_percent(self) -> int:
        """Процент скидки"""
        if self.old_price and self.old_price > self.price:
            return int((1 - float(self.price) / float(self.old_price)) * 100)
        return 0
