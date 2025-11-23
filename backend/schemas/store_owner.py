"""
Store Owner schemas
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re


class StoreOwnerCreate(BaseModel):
    """Схема для создания магазина"""
    inn: str = Field(..., min_length=10, max_length=12, description="ИНН организации")
    kpp: Optional[str] = Field(None, min_length=9, max_length=9, description="КПП")
    ogrn: Optional[str] = Field(None, min_length=13, max_length=15, description="ОГРН")
    name: str = Field(..., min_length=1, max_length=500, description="Название магазина")
    legal_name: str = Field(..., min_length=1, max_length=1000, description="Юридическое название")
    address: str = Field(..., min_length=1, description="Адрес")
    phone: Optional[str] = Field(None, max_length=20, description="Телефон")
    email: Optional[str] = Field(None, max_length=255, description="Email")
    description: Optional[str] = Field(None, description="Описание")
    
    @field_validator('inn')
    @classmethod
    def validate_inn(cls, v: str) -> str:
        """Валидация ИНН"""
        # Убираем пробелы
        v = v.strip()
        
        # Проверяем что только цифры
        if not re.match(r'^\d+$', v):
            raise ValueError('ИНН должен содержать только цифры')
        
        # Проверяем длину (10 для организаций, 12 для ИП)
        if len(v) not in [10, 12]:
            raise ValueError('ИНН должен быть 10 или 12 цифр')
        
        return v
    
    @field_validator('kpp')
    @classmethod
    def validate_kpp(cls, v: Optional[str]) -> Optional[str]:
        """Валидация КПП"""
        if v is None:
            return v
        
        v = v.strip()
        
        if not re.match(r'^\d{9}$', v):
            raise ValueError('КПП должен содержать 9 цифр')
        
        return v
    
    @field_validator('ogrn')
    @classmethod
    def validate_ogrn(cls, v: Optional[str]) -> Optional[str]:
        """Валидация ОГРН"""
        if v is None:
            return v
        
        v = v.strip()
        
        if not re.match(r'^\d{13,15}$', v):
            raise ValueError('ОГРН должен содержать 13 или 15 цифр')
        
        return v


class StoreOwnerUpdate(BaseModel):
    """Схема для обновления магазина"""
    name: Optional[str] = Field(None, min_length=1, max_length=500)
    legal_name: Optional[str] = Field(None, min_length=1, max_length=1000)
    address: Optional[str] = Field(None, min_length=1)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    logo: Optional[str] = None
    banner: Optional[str] = None


class StoreOwnerResponse(BaseModel):
    """Схема ответа с данными магазина"""
    id: str
    owner_id: str
    inn: str
    kpp: Optional[str]
    ogrn: Optional[str]
    name: str
    legal_name: str
    address: str
    phone: Optional[str]
    email: Optional[str]
    description: Optional[str]
    logo: Optional[str]
    banner: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
    @classmethod
    def model_validate(cls, obj):
        """Преобразуем UUID в строки"""
        if hasattr(obj, '__dict__'):
            data = {}
            for key, value in obj.__dict__.items():
                if key.startswith('_'):
                    continue
                # Преобразуем UUID в строку
                if hasattr(value, 'hex'):  # UUID объект
                    data[key] = str(value)
                else:
                    data[key] = value
            return super().model_validate(data)
        return super().model_validate(obj)
