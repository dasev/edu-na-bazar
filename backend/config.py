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
    
    # SMS Service
    SMSC_LOGIN: str = os.getenv("SMSC_LOGIN", "")
    SMSC_PASSWORD: str = os.getenv("SMSC_PASSWORD", "")
    
    # CORS
    @property
    def ALLOWED_ORIGINS(self) -> list:
        """Parse CORS origins from environment variable"""
        origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001")
        origins = [origin.strip() for origin in origins_str.split(",")]
        
        # В development добавляем дополнительные origins
        if self.ENVIRONMENT == "development":
            origins.extend([
                "http://127.0.0.1:3000",
                "http://127.0.0.1:3001",
                "http://localhost",
                "http://127.0.0.1",
            ])
            # Добавляем все порты 127.0.0.1 для Cascade browser preview
            # Cascade использует динамические порты вида http://127.0.0.1:63646
            origins.append("*")  # В dev режиме разрешаем все
        
        return origins
    
    # Mapbox
    MAPBOX_ACCESS_TOKEN: str = os.getenv("MAPBOX_ACCESS_TOKEN", "")
    
    # SMS (для разработки отключаем реальную отправку)
    SMS_ENABLED: bool = os.getenv("SMS_ENABLED", "false").lower() == "true"


settings = Settings()
