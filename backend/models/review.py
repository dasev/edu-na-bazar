"""
Review model - отзывы на товары
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, Text, ForeignKey, BigInteger, Integer, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Review(Base):
    """Review model - отзывы на товары"""
    __tablename__ = "reviews"
    __table_args__ = {'schema': 'market'}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Связи
    product_id = Column(BigInteger, ForeignKey('market.products.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(BigInteger, ForeignKey('config.users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Отзыв
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text, nullable=True)
    
    # Модерация
    is_approved = Column(Boolean, default=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
    
    def __repr__(self):
        return f"<Review {self.id} - Product {self.product_id} - Rating {self.rating}>"
