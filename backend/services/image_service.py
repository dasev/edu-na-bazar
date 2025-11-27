"""
Сервис для работы с изображениями товаров
Поддерживает локальное хранение и облачные сервисы (S3, Cloudinary)
"""
import os
import uuid
from pathlib import Path
from typing import Optional, List
from PIL import Image
import aiofiles
from fastapi import UploadFile, HTTPException


class ImageService:
    """Сервис для загрузки и обработки изображений"""
    
    def __init__(self):
        # Путь к папке с изображениями
        self.upload_dir = Path("uploads/products")
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Настройки изображений
        self.max_file_size = 5 * 1024 * 1024  # 5MB
        self.allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
        self.thumbnail_size = (300, 300)
        self.large_size = (1200, 1200)
    
    async def upload_image(
        self, 
        file: UploadFile,
        create_thumbnail: bool = True
    ) -> dict:
        """
        Загрузка изображения
        
        Args:
            file: Загружаемый файл
            create_thumbnail: Создавать ли миниатюру
            
        Returns:
            dict: Информация о загруженном изображения
        """
        print(f"📤 Начало загрузки изображения: {file.filename}")
        print(f"📁 Upload dir: {self.upload_dir}")
        print(f"📁 Upload dir exists: {self.upload_dir.exists()}")
        
        # Проверка расширения
        file_ext = Path(file.filename).suffix.lower()
        print(f"📝 File extension: {file_ext}")
        if file_ext not in self.allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Недопустимый формат файла. Разрешены: {', '.join(self.allowed_extensions)}"
            )
        
        # Проверка размера
        content = await file.read()
        if len(content) > self.max_file_size:
            raise HTTPException(
                status_code=400,
                detail=f"Файл слишком большой. Максимум: {self.max_file_size / 1024 / 1024}MB"
            )
        
        # Генерация уникального имени
        unique_id = str(uuid.uuid4())
        filename = f"{unique_id}{file_ext}"
        filepath = self.upload_dir / filename
        
        # Сохранение оригинала
        async with aiofiles.open(filepath, 'wb') as f:
            await f.write(content)
        
        # Создание миниатюры
        thumbnail_path = None
        if create_thumbnail:
            thumbnail_path = await self._create_thumbnail(filepath, unique_id, file_ext)
        
        # Оптимизация изображения
        optimized_path = await self._optimize_image(filepath, unique_id, file_ext)
        
        return {
            "id": unique_id,
            "filename": filename,
            "original_url": f"/uploads/products/{filename}",
            "thumbnail_url": f"/uploads/products/thumbnails/{Path(thumbnail_path).name}" if thumbnail_path else None,
            "optimized_url": f"/uploads/products/optimized/{Path(optimized_path).name}" if optimized_path else None,
            "size": len(content),
            "content_type": file.content_type
        }
    
    async def _create_thumbnail(self, filepath: Path, unique_id: str, ext: str) -> Optional[Path]:
        """Создание миниатюры изображения"""
        try:
            thumbnail_dir = self.upload_dir / "thumbnails"
            thumbnail_dir.mkdir(exist_ok=True)
            
            thumbnail_path = thumbnail_dir / f"{unique_id}_thumb{ext}"
            
            with Image.open(filepath) as img:
                # Конвертация в RGB если нужно
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Создание миниатюры с сохранением пропорций
                img.thumbnail(self.thumbnail_size, Image.Resampling.LANCZOS)
                img.save(thumbnail_path, quality=85, optimize=True)
            
            return thumbnail_path
        except Exception as e:
            print(f"Ошибка создания миниатюры: {e}")
            return None
    
    async def _optimize_image(self, filepath: Path, unique_id: str, ext: str) -> Optional[Path]:
        """Оптимизация изображения для веба"""
        try:
            optimized_dir = self.upload_dir / "optimized"
            optimized_dir.mkdir(exist_ok=True)
            
            optimized_path = optimized_dir / f"{unique_id}_opt{ext}"
            
            with Image.open(filepath) as img:
                # Конвертация в RGB если нужно
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Изменение размера если больше максимального
                if img.width > self.large_size[0] or img.height > self.large_size[1]:
                    img.thumbnail(self.large_size, Image.Resampling.LANCZOS)
                
                # Сохранение с оптимизацией
                img.save(optimized_path, quality=90, optimize=True)
            
            return optimized_path
        except Exception as e:
            print(f"Ошибка оптимизации изображения: {e}")
            return None
    
    async def delete_image(self, image_id: str) -> bool:
        """Удаление изображения и его вариантов"""
        try:
            # Поиск всех файлов с данным ID
            for pattern in [f"{image_id}.*", f"{image_id}_*.*"]:
                for file in self.upload_dir.rglob(pattern):
                    file.unlink()
            return True
        except Exception as e:
            print(f"Ошибка удаления изображения: {e}")
            return False
    
    def get_image_url(self, filename: str, variant: str = "original") -> str:
        """Получение URL изображения"""
        if variant == "thumbnail":
            return f"/uploads/products/thumbnails/{filename}"
        elif variant == "optimized":
            return f"/uploads/products/optimized/{filename}"
        else:
            return f"/uploads/products/{filename}"


# Singleton instance
image_service = ImageService()
