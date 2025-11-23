"""
ProductImage model
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, BigInteger, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship
from database import Base


class ProductImage(Base):
    """ProductImage model - изображения товаров"""
    __tablename__ = "product_images"
    __table_args__ = {'schema': 'market'}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger, ForeignKey('market.products.id', ondelete='CASCADE'), nullable=False, index=True)
    image_url = Column(Text, nullable=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="images")
    
    def __repr__(self):
        return f"<ProductImage {self.id} for Product {self.product_id}>"
