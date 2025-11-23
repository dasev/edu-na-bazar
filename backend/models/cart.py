"""
Cart model
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class CartItem(Base):
    """CartItem model - товары в корзине"""
    __tablename__ = "cart_items"
    __table_args__ = {'schema': 'market'}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Пользователь
    user_id = Column(BigInteger, ForeignKey('config.users.id'), nullable=False, index=True)
    
    # Товар
    product_id = Column(BigInteger, ForeignKey('market.products.id'), nullable=False, index=True)
    
    # Количество
    quantity = Column(BigInteger, nullable=False, default=1)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="cart_items")
    product = relationship("Product", back_populates="cart_items")
    
    def __repr__(self):
        return f"<CartItem user={self.user_id} product={self.product_id} qty={self.quantity}>"
