"""
JWT Service - создание и проверка токенов
"""
from datetime import datetime, timedelta
from typing import Optional
import jwt
from config import settings


class JWTService:
    """Сервис для работы с JWT токенами"""
    
    # Долгая сессия - 90 дней (как в Циане)
    ACCESS_TOKEN_EXPIRE_DAYS = 90
    
    @staticmethod
    def create_access_token(user_id: str, phone: str) -> tuple[str, int]:
        """
        Создать JWT токен
        
        Returns:
            tuple: (token, expires_in_seconds)
        """
        expires_delta = timedelta(days=JWTService.ACCESS_TOKEN_EXPIRE_DAYS)
        expire = datetime.utcnow() + expires_delta
        
        payload = {
            "sub": user_id,  # Subject - ID пользователя
            "phone": phone,
            "exp": expire,  # Expiration time
            "iat": datetime.utcnow(),  # Issued at
            "type": "access"
        }
        
        token = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        
        expires_in = int(expires_delta.total_seconds())
        
        return token, expires_in
    
    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """
        Проверить и декодировать токен
        
        Returns:
            dict: Payload токена или None если невалидный
        """
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.JWTError:
            return None
    
    @staticmethod
    def get_user_id_from_token(token: str) -> Optional[str]:
        """Получить ID пользователя из токена"""
        payload = JWTService.verify_token(token)
        if payload:
            return payload.get("sub")
        return None
