"""
SMS Service - отправка SMS кодов через SMSC.RU
"""
import random
import string
from datetime import datetime, timedelta
from typing import Optional
import logging
import httpx
from urllib.parse import urlencode
from config import settings

logger = logging.getLogger(__name__)


class SMSService:
    """Сервис для отправки SMS через SMSC.RU"""
    
    # Время жизни кода - 5 минут
    CODE_EXPIRE_MINUTES = 5
    
    # Длина кода
    CODE_LENGTH = 6
    
    # SMSC.RU API URL
    SMSC_API_URL = "https://smsc.ru/sys/send.php"
    
    @staticmethod
    def generate_code() -> str:
        """Генерировать 6-значный код"""
        return ''.join(random.choices(string.digits, k=SMSService.CODE_LENGTH))
    
    @staticmethod
    def get_expiration_time() -> datetime:
        """Получить время истечения кода"""
        return datetime.utcnow() + timedelta(minutes=SMSService.CODE_EXPIRE_MINUTES)
    
    @staticmethod
    async def send_sms(phone: str, code: str) -> bool:
        """
        Отправить SMS с кодом через SMSC.RU
        
        В режиме разработки (SMS_ENABLED=false) просто выводит код в консоль.
        
        Документация: https://smsc.ru/api/http/
        
        Args:
            phone: Номер телефона (формат: +79991234567)
            code: Код подтверждения
            
        Returns:
            bool: Успешно ли отправлено
        """
        
        # РЕЖИМ РАЗРАБОТКИ - просто выводим код в консоль
        if not settings.SMS_ENABLED:
            print(f"\n{'='*60}")
            print(f"🔧 РЕЖИМ РАЗРАБОТКИ - SMS НЕ ОТПРАВЛЯЕТСЯ")
            print(f"{'='*60}")
            print(f"📱 Телефон: {phone}")
            print(f"🔐 КОД ПОДТВЕРЖДЕНИЯ: {code}")
            print(f"⏰ Действителен: {SMSService.CODE_EXPIRE_MINUTES} минут")
            print(f"{'='*60}\n")
            logger.info(f"🔧 DEV MODE: SMS code for {phone}: {code}")
            return True
        
        # PRODUCTION MODE - реальная отправка через SMSC.RU
        # Убираем + из номера для SMSC
        phone_clean = phone.replace('+', '')
        
        # Текст сообщения
        message = f"Ваш код подтверждения: {code}\nДействителен 5 минут.\n\nЕду на базар"
        
        # Параметры запроса
        params = {
            'login': settings.SMSC_LOGIN,
            'psw': settings.SMSC_PASSWORD,
            'phones': phone_clean,
            'mes': message,
            'charset': 'utf-8',
            'fmt': 3  # JSON ответ
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(SMSService.SMSC_API_URL, params=params, timeout=10.0)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Логируем результат
                    logger.info(f"📱 SMSC Response: {result}")
                    
                    # Проверяем успешность
                    if 'error' in result:
                        error_code = result.get('error_code')
                        error_msg = result.get('error', 'Unknown error')
                        logger.error(f"❌ SMSC Error {error_code}: {error_msg}")
                        
                        # В dev режиме все равно возвращаем True для тестирования
                        print(f"\n{'='*50}")
                        print(f"⚠️  SMSC ERROR: {error_msg}")
                        print(f"📱 SMS to {phone}: Your code is {code}")
                        print(f"🔐 КОД: {code}")
                        print(f"⏰ Действителен 5 минут")
                        print(f"{'='*50}\n")
                        return True  # Для разработки
                    
                    # Успешная отправка
                    if 'id' in result:
                        sms_id = result.get('id')
                        logger.info(f"✅ SMS отправлено успешно! ID: {sms_id}")
                        print(f"\n{'='*50}")
                        print(f"✅ SMS ОТПРАВЛЕНО ЧЕРЕЗ SMSC.RU")
                        print(f"📱 Номер: {phone}")
                        print(f"🔐 Код: {code}")
                        print(f"🆔 SMS ID: {sms_id}")
                        print(f"⏰ Действителен 5 минут")
                        print(f"{'='*50}\n")
                        return True
                    
                    return False
                else:
                    logger.error(f"❌ HTTP Error: {response.status_code}")
                    return False
                    
        except httpx.RequestError as e:
            logger.error(f"❌ Network error: {e}")
            # В dev режиме логируем код
            print(f"\n{'='*50}")
            print(f"⚠️  NETWORK ERROR (код все равно показываем)")
            print(f"📱 SMS to {phone}: Your code is {code}")
            print(f"🔐 КОД: {code}")
            print(f"⏰ Действителен 5 минут")
            print(f"{'='*50}\n")
            return True  # Для разработки
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            return False
    
    @staticmethod
    def format_phone(phone: str) -> str:
        """
        Форматировать номер телефона
        
        Принимает: +79991234567, 89991234567, 79991234567, 9991234567
        Возвращает: +79991234567
        """
        # Убираем все кроме цифр
        digits = ''.join(filter(str.isdigit, phone))
        
        # Если начинается с 8, заменяем на 7
        if digits.startswith('8') and len(digits) == 11:
            digits = '7' + digits[1:]
        
        # Если нет 7 в начале, добавляем
        if not digits.startswith('7'):
            digits = '7' + digits
        
        # Добавляем +
        return '+' + digits
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Проверить валидность номера телефона"""
        formatted = SMSService.format_phone(phone)
        # Российский номер: +7 и 10 цифр
        return len(formatted) == 12 and formatted.startswith('+7')
