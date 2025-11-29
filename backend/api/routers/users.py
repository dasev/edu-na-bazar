"""
Users Router - управление профилем пользователя
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from database import get_db
from models.user import User
from services.jwt_service import JWTService
from services.image_service import ImageService
import os
import uuid
import random

router = APIRouter(prefix="/api/users", tags=["users"])


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Получить текущего пользователя из токена"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Требуется авторизация"
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверная схема авторизации"
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный формат токена"
        )
    
    payload = JWTService.verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен"
        )
    
    # user_id хранится в поле "sub" (subject) токена
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный формат токена"
        )
    
    # Преобразуем строку в int
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный формат user_id"
        )
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден"
        )
    
    return user


# Схемы
class UserProfileResponse(BaseModel):
    id: int
    phone: str
    email: Optional[str]
    full_name: Optional[str]
    address: Optional[str]
    avatar: Optional[str]
    is_email_verified: bool = False
    is_phone_verified: bool = False
    
    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class SendEmailCodeRequest(BaseModel):
    email: EmailStr


class VerifyEmailRequest(BaseModel):
    email: EmailStr
    code: str


class SendPhoneCodeRequest(BaseModel):
    phone: str


class VerifyPhoneRequest(BaseModel):
    phone: str
    code: str


# Временное хранилище кодов (в продакшене использовать Redis)
email_codes = {}
phone_codes = {}


@router.get("/me", response_model=UserProfileResponse)
async def get_profile(
    user: User = Depends(get_current_user)
):
    """Получить профиль текущего пользователя"""
    return user


@router.put("/me", response_model=UserProfileResponse)
async def update_profile(
    data: UserProfileUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Обновить профиль пользователя"""
    if data.full_name is not None:
        user.full_name = data.full_name
    if data.address is not None:
        user.address = data.address
    # Email и phone обновляются только после верификации
    
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Загрузить аватар пользователя"""
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Файл должен быть изображением"
        )
    
    upload_dir = "uploads/avatars"
    os.makedirs(upload_dir, exist_ok=True)
    
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    
    try:
        # Обрезаем и оптимизируем аватар до квадрата 300x300
        from PIL import Image
        img = Image.open(file_path)
        
        # Обрезаем до квадрата (crop to square)
        width, height = img.size
        min_dimension = min(width, height)
        left = (width - min_dimension) // 2
        top = (height - min_dimension) // 2
        right = left + min_dimension
        bottom = top + min_dimension
        img = img.crop((left, top, right, bottom))
        
        # Изменяем размер до 300x300
        img = img.resize((300, 300), Image.Resampling.LANCZOS)
        
        # Конвертируем в RGB если нужно
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        
        # Сохраняем оптимизированное изображение
        img.save(file_path, 'JPEG', quality=85, optimize=True)
    except Exception as e:
        print(f"Ошибка оптимизации аватара: {e}")
    
    avatar_url = f"/{file_path}"
    user.avatar = avatar_url
    await db.commit()
    
    return {"avatar_url": avatar_url}


@router.post("/send-email-code")
async def send_email_code(
    data: SendEmailCodeRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Отправить код подтверждения на email"""
    from services.email_service import send_email_verification_code
    
    # Генерируем код
    code = str(random.randint(100000, 999999))
    email_codes[data.email] = code
    
    # Отправляем email
    try:
        await send_email_verification_code(data.email, code, user.full_name or "Пользователь")
        print(f"📧 Email код отправлен на {data.email}: {code}")
    except Exception as e:
        print(f"❌ Ошибка отправки email: {e}")
        # Код все равно сохраняем для тестирования
        print(f"📧 Код для тестирования {data.email}: {code}")
    
    return {"message": "Код отправлен на email"}


@router.post("/verify-email")
async def verify_email(
    data: VerifyEmailRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Подтвердить email"""
    if data.email not in email_codes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Код не найден"
        )
    
    if email_codes[data.email] != data.code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный код"
        )
    
    # Обновляем email и статус верификации email
    user.email = data.email
    user.is_email_verified = True
    await db.commit()
    
    # Удаляем код
    del email_codes[data.email]
    
    return {"message": "Email подтвержден"}


@router.post("/send-phone-code")
async def send_phone_code(
    data: SendPhoneCodeRequest,
    user: User = Depends(get_current_user)
):
    """Отправить SMS код"""
    # Генерируем код
    code = str(random.randint(100000, 999999))
    phone_codes[data.phone] = code
    
    # TODO: Отправить SMS через sms_service
    print(f"📱 SMS код для {data.phone}: {code}")
    
    return {"message": "SMS код отправлен"}


@router.post("/verify-phone")
async def verify_phone(
    data: VerifyPhoneRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Подтвердить телефон"""
    if data.phone not in phone_codes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Код не найден"
        )
    
    if phone_codes[data.phone] != data.code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный код"
        )
    
    # Обновляем телефон и статус верификации телефона
    user.phone = data.phone
    user.is_phone_verified = True
    await db.commit()
    
    # Удаляем код
    del phone_codes[data.phone]
    
    return {"message": "Телефон подтвержден"}
