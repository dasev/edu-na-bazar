"""
Auth schemas
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# Request schemas
class SendSMSRequest(BaseModel):
    """Запрос на отправку SMS кода"""
    phone: str = Field(..., description="Телефон в формате +7XXXXXXXXXX")
    full_name: Optional[str] = Field(None, description="ФИО (для новых пользователей)")
    email: Optional[EmailStr] = Field(None, description="Email (опционально)")
    address: Optional[str] = Field(None, description="Адрес доставки (для новых пользователей)")


class VerifySMSRequest(BaseModel):
    """Запрос на проверку SMS кода"""
    phone: str = Field(..., description="Телефон в формате +7XXXXXXXXXX")
    code: str = Field(..., min_length=6, max_length=6, description="6-значный код из SMS")


# Response schemas
class TokenResponse(BaseModel):
    """Ответ с токеном"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # Секунды до истечения
    user: "UserResponse"


class UserResponse(BaseModel):
    """Информация о пользователе"""
    id: str
    phone: str
    email: Optional[str]
    full_name: str
    address: Optional[str]
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True


class SMSResponse(BaseModel):
    """Ответ на отправку SMS"""
    success: bool
    message: str
    phone: str
    expires_in: int  # Секунды до истечения кода
    # В продакшене НЕ отправляем код! Только для разработки:
    code: Optional[str] = None  # TODO: Убрать в продакшене!
