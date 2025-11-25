"""
Создание placeholder изображений для товаров
"""
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Добавляем корневую директорию в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from sqlalchemy import select
from database import AsyncSessionLocal
from models.product import Product


async def create_placeholder_image(filename: str, text: str = "No Image"):
    """Создать placeholder изображение"""
    # Размер изображения
    width, height = 800, 600
    
    # Создаем изображение с градиентом
    img = Image.new('RGB', (width, height), color='#f0f0f0')
    draw = ImageDraw.Draw(img)
    
    # Рисуем градиент
    for i in range(height):
        color = int(240 - (i / height) * 40)
        draw.rectangle([(0, i), (width, i+1)], fill=(color, color, color))
    
    # Рисуем рамку
    draw.rectangle([(10, 10), (width-10, height-10)], outline='#cccccc', width=3)
    
    # Добавляем текст
    try:
        # Пытаемся использовать системный шрифт
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    except:
        # Если не найден, используем стандартный
        font = ImageFont.load_default()
    
    # Центрируем текст
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Рисуем тень
    draw.text((x+2, y+2), text, fill='#999999', font=font)
    # Рисуем текст
    draw.text((x, y), text, fill='#666666', font=font)
    
    # Сохраняем
    img.save(filename, 'JPEG', quality=85)
    print(f"✅ Создан: {filename}")


async def main():
    """Создать placeholder изображения для всех товаров"""
    print("🖼️  Создание placeholder изображений...")
    
    # Создаем директорию если не существует
    uploads_dir = Path(__file__).parent.parent / "uploads" / "products" / "original"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    
    async with AsyncSessionLocal() as db:
        # Получаем все уникальные пути к изображениям
        result = await db.execute(
            select(Product.image).distinct()
        )
        images = [row[0] for row in result.fetchall() if row[0]]
        
        print(f"📊 Найдено {len(images)} уникальных изображений")
        
        created = 0
        skipped = 0
        
        for image_path in images:
            if not image_path:
                continue
            
            # Извлекаем имя файла
            filename = Path(image_path).name
            full_path = uploads_dir / filename
            
            # Проверяем, существует ли файл
            if full_path.exists():
                skipped += 1
                continue
            
            # Создаем placeholder
            await create_placeholder_image(
                str(full_path),
                text="Placeholder"
            )
            created += 1
    
    print(f"\n✅ Готово!")
    print(f"   Создано: {created}")
    print(f"   Пропущено: {skipped}")
    print(f"   Всего: {len(images)}")


if __name__ == "__main__":
    asyncio.run(main())
