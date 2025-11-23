"""
Message model - личные сообщения
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, Text, ForeignKey, BigInteger, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Message(Base):
    """Message model - личные сообщения между пользователями"""
    __tablename__ = "messages"
    __table_args__ = {'schema': 'market'}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Связи
    from_user_id = Column(BigInteger, ForeignKey('config.users.id', ondelete='CASCADE'), nullable=False, index=True)
    to_user_id = Column(BigInteger, ForeignKey('config.users.id', ondelete='CASCADE'), nullable=False, index=True)
    product_id = Column(BigInteger, ForeignKey('market.products.id', ondelete='SET NULL'), nullable=True, index=True)
    
    # Сообщение
    message = Column(Text, nullable=False)
    
    # Статус
    is_read = Column(Boolean, default=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    from_user = relationship("User", foreign_keys=[from_user_id], back_populates="sent_messages")
    to_user = relationship("User", foreign_keys=[to_user_id], back_populates="received_messages")
    product = relationship("Product", back_populates="messages")
    
    def __repr__(self):
        return f"<Message {self.id} - From {self.from_user_id} To {self.to_user_id}>"
