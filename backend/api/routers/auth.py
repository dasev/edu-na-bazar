"""
Authentication API router
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import logging

from database import get_db
from models.user import User, SMSCode
from schemas.auth import SendSMSRequest, VerifySMSRequest, TokenResponse, SMSResponse, UserResponse
from services.sms_service import SMSService
from services.jwt_service import JWTService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/send-sms", response_model=SMSResponse)
async def send_sms_code(
    request: SendSMSRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Отправить SMS код для входа/регистрации
    
    - Если пользователь существует - отправляем код для входа
    - Если новый - требуем ФИО и создаем пользователя
    """
    
    # Валидация и форматирование телефона
    if not SMSService.validate_phone(request.phone):
        raise HTTPException(status_code=400, detail="Неверный формат номера телефона")
    
    phone = SMSService.format_phone(request.phone)
    
    # Проверяем существует ли пользователь
    result = await db.execute(select(User).where(User.phone == phone))
    user = result.scalar_one_or_none()
    
    # Если новый пользователь - требуем ФИО
    if not user and not request.full_name:
        raise HTTPException(
            status_code=400,
            detail="Для регистрации необходимо указать ФИО"
        )
    
    # Создаем нового пользователя если нужно
    if not user:
        user = User(
            phone=phone,
            full_name=request.full_name,
            email=request.email,
            address=request.address,
            is_verified=False
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"✅ Создан новый пользователь: {phone}")
    
    # Генерируем код
    code = SMSService.generate_code()
    expires_at = SMSService.get_expiration_time()
    
    # Сохраняем код в БД
    sms_code = SMSCode(
        phone=phone,
        code=code,
        expires_at=expires_at,
        is_used=False
    )
    db.add(sms_code)
    await db.commit()
    
    # Отправляем SMS
    success = await SMSService.send_sms(phone, code)
    
    if not success:
        raise HTTPException(status_code=500, detail="Ошибка отправки SMS")
    
    return SMSResponse(
        success=True,
        message="SMS код отправлен",
        phone=phone,
        expires_in=SMSService.CODE_EXPIRE_MINUTES * 60,
        code=code  # TODO: Убрать в продакшене!
    )


@router.post("/verify-sms", response_model=TokenResponse)
async def verify_sms_code(
    request: VerifySMSRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Проверить SMS код и выдать токен
    
    - Проверяем код
    - Обновляем статус пользователя
    - Выдаем JWT токен на 90 дней
    """
    
    phone = SMSService.format_phone(request.phone)
    
    # Ищем последний неиспользованный код
    result = await db.execute(
        select(SMSCode)
        .where(SMSCode.phone == phone)
        .where(SMSCode.is_used == False)
        .where(SMSCode.expires_at > datetime.utcnow())
        .order_by(SMSCode.created_at.desc())
    )
    sms_code = result.scalar_one_or_none()
    
    if not sms_code:
        raise HTTPException(
            status_code=400,
            detail="Код не найден или истек. Запросите новый код"
        )
    
    # Проверяем код
    if sms_code.code != request.code:
        # Увеличиваем счетчик попыток
        attempts = int(sms_code.attempts) + 1
        sms_code.attempts = str(attempts)
        await db.commit()
        
        if attempts >= 3:
            sms_code.is_used = True
            await db.commit()
            raise HTTPException(
                status_code=400,
                detail="Превышено количество попыток. Запросите новый код"
            )
        
        raise HTTPException(status_code=400, detail="Неверный код")
    
    # Код верный - помечаем как использованный
    sms_code.is_used = True
    sms_code.used_at = datetime.utcnow()
    await db.commit()
    
    # Получаем пользователя
    result = await db.execute(select(User).where(User.phone == phone))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Обновляем статус пользователя
    user.is_verified = True
    user.last_login = datetime.utcnow()
    await db.commit()
    await db.refresh(user)
    
    # Создаем JWT токен (90 дней)
    token, expires_in = JWTService.create_access_token(
        user_id=str(user.id),
        phone=user.phone
    )
    
    logger.info(f"✅ Успешный вход: {phone}")
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=expires_in,
        user=UserResponse.from_orm(user)
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    token: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Получить информацию о текущем пользователе
    
    Передавать токен в заголовке: Authorization: Bearer <token>
    """
    
    user_id = JWTService.get_user_id_from_token(token)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Невалидный токен")
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    return UserResponse.from_orm(user)
