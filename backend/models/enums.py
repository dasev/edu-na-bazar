"""
Enums for models
"""
import enum


class UserRole(str, enum.Enum):
    """Роли пользователей"""
    CUSTOMER = "customer"      # Покупатель (по умолчанию)
    SELLER = "seller"          # Продавец (владелец магазина)
    ADMIN = "admin"            # Администратор платформы


class StoreStatus(str, enum.Enum):
    """Статусы магазина"""
    PENDING = "pending"        # На модерации
    ACTIVE = "active"          # Активен
    SUSPENDED = "suspended"    # Приостановлен
    REJECTED = "rejected"      # Отклонен


class ProductStatus(str, enum.Enum):
    """Статусы товара"""
    PENDING = "pending"        # На модерации
    ACTIVE = "active"          # Активен
    REJECTED = "rejected"      # Отклонен
    OUT_OF_STOCK = "out_of_stock"  # Нет в наличии
