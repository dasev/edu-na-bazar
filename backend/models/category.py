"""
Category model
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, BigInteger, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base


class Category(Base):
    """Category model - категории товаров"""
    __tablename__ = "categories"
    __table_args__ = {'schema': 'market'}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Основная информация
    name = Column(Text, nullable=False, index=True)
    description = Column(Text, nullable=True)
    image = Column(Text, nullable=True)
    
    # Иерархия (для подкатегорий)
    parent_id = Column(BigInteger, ForeignKey('market.categories.id'), nullable=True)
    sort_order = Column(BigInteger, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    parent = relationship("Category", remote_side=[id], backref="subcategories")
    products = relationship("Product", back_populates="category")
    
    def __repr__(self):
        return f"<Category {self.name}>"
