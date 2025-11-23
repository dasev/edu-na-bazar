"""
Product model
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, Boolean, BigInteger, ForeignKey, Text, ARRAY, Double
from sqlalchemy.orm import relationship
from database import Base


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
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = relationship("Category", back_populates="products")
    store_owner = relationship("StoreOwner", back_populates="products")
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
