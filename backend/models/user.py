"""
User models
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database import Base


class User(Base):
    """User model - без паролей, только SMS аутентификация"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Основная информация
    phone = Column(String(20), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    full_name = Column(String(255), nullable=False)
    address = Column(String(500), nullable=True)  # Адрес доставки
    
    # Статус
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)  # Подтвержден ли телефон
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<User {self.phone} - {self.full_name}>"


class SMSCode(Base):
    """SMS verification codes"""
    __tablename__ = "sms_codes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Телефон и код
    phone = Column(String(20), nullable=False, index=True)
    code = Column(String(6), nullable=False)  # 6-значный код
    
    # Статус
    is_used = Column(Boolean, default=False)
    attempts = Column(String, default="0")  # Количество попыток проверки
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)  # Код действителен 5 минут
    used_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<SMSCode {self.phone} - {self.code}>"
