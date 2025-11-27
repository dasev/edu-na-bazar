"""
Moderation models
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, BigInteger, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class ModerationLog(Base):
    """Лог модерации товаров"""
    __tablename__ = "moderation_logs"
    __table_args__ = {'schema': 'market'}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Товар
    product_id = Column(BigInteger, ForeignKey('market.products.id'), nullable=False, index=True)
    
    # Модератор
    moderator_id = Column(BigInteger, ForeignKey('config.users.id'), nullable=False, index=True)
    
    # Действие: approved, rejected
    action = Column(Text, nullable=False)
    
    # Причина отклонения (если отклонен)
    reason = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    product = relationship("Product", foreign_keys=[product_id])
    moderator = relationship("User", foreign_keys=[moderator_id])
    
    def __repr__(self):
        return f"<ModerationLog {self.action} product={self.product_id} by={self.moderator_id}>"
