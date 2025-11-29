"""
User models
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, BigInteger, Text
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    """User model - без паролей, только SMS аутентификация"""
    __tablename__ = "users"
    __table_args__ = {'schema': 'config'}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Основная информация
    phone = Column(Text, unique=True, nullable=False, index=True)
    email = Column(Text, unique=True, nullable=True, index=True)
    full_name = Column(Text, nullable=False)
    address = Column(Text, nullable=True)  # Адрес доставки
    avatar = Column(Text, nullable=True)  # URL аватара
    
    # Статус
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)  # Подтвержден ли телефон (legacy)
    is_email_verified = Column(Boolean, default=False)  # Подтвержден ли email
    is_phone_verified = Column(Boolean, default=False)  # Подтвержден ли телефон
    is_moderator = Column(Boolean, default=False)  # Является ли модератором
    status = Column(Text, default='active')  # active, blocked - для миграции
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True, index=True)
    
    # Relationships
    orders = relationship("Order", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user")
    store_owners = relationship("StoreOwner", back_populates="owner")
    product_reviews = relationship("ProductReview", back_populates="user")
    product_questions = relationship("ProductQuestion", back_populates="user")
    sent_messages = relationship("Message", foreign_keys="Message.from_user_id", back_populates="from_user")
    received_messages = relationship("Message", foreign_keys="Message.to_user_id", back_populates="to_user")
    product_views = relationship("ProductView", back_populates="user")
    events = relationship("UserEvent", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.phone} - {self.full_name}>"


class SMSCode(Base):
    """SMS verification codes"""
    __tablename__ = "sms_codes"
    __table_args__ = {'schema': 'config'}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Телефон и код
    phone = Column(Text, nullable=False, index=True)
    code = Column(Text, nullable=False)  # 6-значный код
    
    # Статус
    is_used = Column(Boolean, default=False)
    attempts = Column(String, default="0")  # Количество попыток проверки
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)  # Код действителен 5 минут
    used_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<SMSCode {self.phone} - {self.code}>"
