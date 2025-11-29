"""
Product View model - отслеживание просмотров товаров
"""
from sqlalchemy import Column, Integer, BigInteger, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class ProductView(Base):
    """ProductView model - просмотры товаров"""
    __tablename__ = "product_views"
    __table_args__ = {'schema': 'market'}
    
    id = Column(BigInteger, primary_key=True, index=True)
    product_id = Column(BigInteger, ForeignKey('market.products.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(BigInteger, ForeignKey('config.users.id', ondelete='SET NULL'), nullable=True, index=True)
    session_id = Column(String(255), nullable=True, index=True)  # Для анонимных пользователей
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    product = relationship("Product", back_populates="views")
    user = relationship("User", back_populates="product_views")
