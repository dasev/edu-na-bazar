"""
API роутер для работы с изображениями
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Header
from fastapi.responses import FileResponse
from typing import List, Optional
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from services.image_service import image_service
from services.jwt_service import JWTService
from models.user import User


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Получить текущего пользователя из токена"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Требуется авторизация")
    
    token = authorization.replace("Bearer ", "")
    user_id = JWTService.get_user_id_from_token(token)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Невалидный токен")
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    
    return user


router = APIRouter()


@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Загрузка изображения товара
    
    Требуется авторизация
    """
    try:
        result = await image_service.upload_image(file)
        return {
            "success": True,
            "message": "Изображение успешно загружено",
            "data": result
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка загрузки: {str(e)}")


@router.post("/upload-multiple")
async def upload_multiple_images(
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Загрузка нескольких изображений
    
    Требуется авторизация
    """
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Максимум 10 изображений за раз")
    
    results = []
    errors = []
    
    for file in files:
        try:
            result = await image_service.upload_image(file)
            results.append(result)
        except Exception as e:
            errors.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return {
        "success": len(results) > 0,
        "uploaded": len(results),
        "failed": len(errors),
        "data": results,
        "errors": errors
    }


@router.delete("/{image_id}")
async def delete_image(
    image_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Удаление изображения
    
    Требуется авторизация
    """
    success = await image_service.delete_image(image_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    
    return {
        "success": True,
        "message": "Изображение успешно удалено"
    }


@router.get("/serve/{variant}/{filename}")
async def serve_image(variant: str, filename: str):
    """
    Отдача изображения
    
    variant: original, thumbnail, optimized
    """
    if variant not in ["original", "thumbnail", "optimized"]:
        raise HTTPException(status_code=400, detail="Недопустимый вариант изображения")
    
    # Определяем путь к файлу
    base_path = Path("uploads/products")
    
    if variant == "original":
        filepath = base_path / filename
    else:
        filepath = base_path / variant / filename
    
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    
    return FileResponse(filepath)
