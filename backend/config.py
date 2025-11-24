"""
Configuration settings
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings"""
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")  # development, production
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/edu_na_bazar?client_encoding=utf8")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6380/0")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:52711",  # Cascade browser preview
        "*",  # Разрешить все для разработки
    ]
    
    # Mapbox
    MAPBOX_ACCESS_TOKEN: str = os.getenv("MAPBOX_ACCESS_TOKEN", "")
    
    # SMS (для разработки отключаем реальную отправку)
    SMS_ENABLED: bool = os.getenv("SMS_ENABLED", "false").lower() == "true"


settings = Settings()
