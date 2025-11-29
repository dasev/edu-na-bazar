"""
Email service для отправки уведомлений
"""
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from typing import List, Dict, Any
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import logging

from config import settings

logger = logging.getLogger(__name__)

# Конфигурация FastAPI-Mail
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.MAIL_USE_CREDENTIALS,
    VALIDATE_CERTS=settings.MAIL_VALIDATE_CERTS,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / 'templates' / 'email'
)

fm = FastMail(conf)

# Jinja2 для шаблонов
template_env = Environment(
    loader=FileSystemLoader(str(Path(__file__).parent.parent / 'templates' / 'email'))
)


class EmailService:
    """Сервис для отправки email уведомлений"""
    
    @staticmethod
    async def send_email(
        email_to: EmailStr,
        subject: str,
        template_name: str,
        template_data: Dict[str, Any]
    ) -> bool:
        """
        Отправка email с использованием шаблона
        
        Args:
            email_to: Email получателя
            subject: Тема письма
            template_name: Имя шаблона (без расширения)
            template_data: Данные для шаблона
            
        Returns:
            True если отправлено успешно
        """
        if not settings.MAIL_ENABLED:
            logger.info(f"📧 [DEV MODE] Email не отправлен (MAIL_ENABLED=false): {email_to} - {subject}")
            logger.info(f"   Шаблон: {template_name}, Данные: {template_data}")
            return True
        
        try:
            # Рендерим HTML шаблон
            template = template_env.get_template(f"{template_name}.html")
            html_content = template.render(**template_data)
            
            message = MessageSchema(
                subject=subject,
                recipients=[email_to],
                body=html_content,
                subtype=MessageType.html
            )
            
            await fm.send_message(message)
            logger.info(f"✅ Email отправлен: {email_to} - {subject}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка отправки email: {e}")
            return False
    
    @staticmethod
    async def send_order_created(email_to: EmailStr, order_data: Dict[str, Any]) -> bool:
        """Уведомление покупателю о создании заказа"""
        return await EmailService.send_email(
            email_to=email_to,
            subject=f"Заказ #{order_data['order_id']} оформлен",
            template_name="order_created",
            template_data=order_data
        )
    
    @staticmethod
    async def send_order_confirmed(email_to: EmailStr, order_data: Dict[str, Any]) -> bool:
        """Уведомление покупателю о подтверждении заказа магазином"""
        return await EmailService.send_email(
            email_to=email_to,
            subject=f"Заказ #{order_data['order_id']} подтвержден",
            template_name="order_confirmed",
            template_data=order_data
        )
    
    @staticmethod
    async def send_order_ready(email_to: EmailStr, order_data: Dict[str, Any]) -> bool:
        """Уведомление покупателю о готовности заказа к выдаче"""
        return await EmailService.send_email(
            email_to=email_to,
            subject=f"Заказ #{order_data['order_id']} готов к выдаче",
            template_name="order_ready",
            template_data=order_data
        )
    
    @staticmethod
    async def send_order_completed(email_to: EmailStr, order_data: Dict[str, Any]) -> bool:
        """Уведомление покупателю о завершении заказа"""
        return await EmailService.send_email(
            email_to=email_to,
            subject=f"Заказ #{order_data['order_id']} завершен",
            template_name="order_completed",
            template_data=order_data
        )
    
    @staticmethod
    async def send_order_cancelled(email_to: EmailStr, order_data: Dict[str, Any]) -> bool:
        """Уведомление покупателю об отмене заказа"""
        return await EmailService.send_email(
            email_to=email_to,
            subject=f"Заказ #{order_data['order_id']} отменен",
            template_name="order_cancelled",
            template_data=order_data
        )
    
    @staticmethod
    async def send_new_order_to_store(email_to: EmailStr, order_data: Dict[str, Any]) -> bool:
        """Уведомление магазину о новом заказе"""
        return await EmailService.send_email(
            email_to=email_to,
            subject=f"Новый заказ #{order_data['order_id']}",
            template_name="new_order_store",
            template_data=order_data
        )


email_service = EmailService()
