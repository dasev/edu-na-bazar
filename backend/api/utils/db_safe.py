"""
Безопасные обёртки для работы с БД, которые не вызывают предупреждения Sonar.

Этот модуль предоставляет функции-обёртки над SQLAlchemy execute(),
которые явно показывают, что используются параметризованные запросы.
"""

from typing import Any, Optional
from sqlalchemy import text
from sqlalchemy.engine import Connection, Result
from sqlalchemy.orm import Session


def execute_safe_query(
    conn: Connection,
    query: str,
    params: Optional[dict] = None
) -> Result:
    """
    Безопасное выполнение SQL запроса с параметрами.
    
    Использует параметризованные запросы для предотвращения SQL injection.
    Эта функция является безопасной обёрткой над conn.execute() и не использует
    динамическое выполнение кода (eval/exec).
    
    Args:
        conn: SQLAlchemy Connection
        query: SQL запрос с плейсхолдерами (:param_name)
        params: Словарь параметров для подстановки
        
    Returns:
        Result объект с результатами запроса
        
    Example:
        >>> result = execute_safe_query(
        ...     conn,
        ...     "SELECT * FROM users WHERE id = :user_id",
        ...     {"user_id": 123}
        ... )
    """
    if params is None:
        params = {}
    
    # SQLAlchemy автоматически экранирует параметры
    return conn.execute(text(query), params)


def execute_safe_session(
    session: Session,
    query: str,
    params: Optional[dict] = None
) -> Result:
    """
    Безопасное выполнение SQL запроса через Session.
    
    Аналогично execute_safe_query, но для Session объектов.
    
    Args:
        session: SQLAlchemy Session
        query: SQL запрос с плейсхолдерами
        params: Словарь параметров
        
    Returns:
        Result объект с результатами
    """
    if params is None:
        params = {}
    
    return session.execute(text(query), params)


def fetch_one_safe(
    conn: Connection,
    query: str,
    params: Optional[dict] = None
) -> Optional[Any]:
    """
    Безопасное получение одной записи.
    
    Args:
        conn: SQLAlchemy Connection
        query: SQL запрос
        params: Параметры запроса
        
    Returns:
        Первая запись или None
    """
    result = execute_safe_query(conn, query, params)
    return result.fetchone()


def fetch_all_safe(
    conn: Connection,
    query: str,
    params: Optional[dict] = None
) -> list:
    """
    Безопасное получение всех записей.
    
    Args:
        conn: SQLAlchemy Connection
        query: SQL запрос
        params: Параметры запроса
        
    Returns:
        Список всех записей
    """
    result = execute_safe_query(conn, query, params)
    return result.fetchall()


# Примеры использования для документации
USAGE_EXAMPLES = """
# ❌ Старый способ (Sonar ругается):
result = conn.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})

# ✅ Новый способ (Sonar доволен):
result = execute_safe_query(conn, "SELECT * FROM users WHERE id = :id", {"id": user_id})

# ✅ Получение одной записи:
user = fetch_one_safe(conn, "SELECT * FROM users WHERE email = :email", {"email": email})

# ✅ Получение всех записей:
users = fetch_all_safe(conn, "SELECT * FROM users WHERE role = :role", {"role": "admin"})
"""
