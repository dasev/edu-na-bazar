# 📸 Сервис хранения изображений

## ✅ Что создано:

### Backend:
1. **`services/image_service.py`** - Сервис обработки изображений
   - Загрузка и валидация
   - Создание миниатюр (300x300)
   - Оптимизация для веба (1200x1200, 90% качество)
   - Удаление изображений

2. **`api/routers/images.py`** - API endpoints
   - `POST /api/images/upload` - загрузка одного изображения
   - `POST /api/images/upload-multiple` - загрузка нескольких
   - `DELETE /api/images/{id}` - удаление
   - `GET /api/images/serve/{variant}/{filename}` - отдача файлов

### Frontend:
3. **`components/ImageUpload/ImageUpload.tsx`** - React компонент
   - Drag & drop (можно добавить)
   - Превью изображений
   - Валидация (тип, размер)
   - Прогресс загрузки

---

## 🚀 Как использовать:

### 1. Установка зависимостей

```bash
cd backend
pip install Pillow aiofiles
```

Или:
```bash
pip install -r requirements.txt
```

### 2. Создание папки для загрузок

Папка создается автоматически при первом запуске:
```
backend/
  uploads/
    products/
      - оригиналы
      thumbnails/
        - миниатюры 300x300
      optimized/
        - оптимизированные 1200x1200
```

### 3. Использование в React

```tsx
import ImageUpload, { UploadedImage } from './components/ImageUpload/ImageUpload'

function MyComponent() {
  const handleImagesUploaded = (images: UploadedImage[]) => {
    console.log('Загружено:', images)
    // images[0].id - уникальный ID
    // images[0].original_url - оригинал
    // images[0].thumbnail_url - миниатюра
    // images[0].optimized_url - оптимизированное
  }

  return (
    <ImageUpload
      onUpload={handleImagesUploaded}
      multiple={true}
      maxFiles={10}
    />
  )
}
```

---

## 📋 API Endpoints:

### Загрузка одного изображения
```http
POST /api/images/upload
Authorization: Bearer YOUR_TOKEN
Content-Type: multipart/form-data

file: <image file>
```

**Ответ:**
```json
{
  "success": true,
  "message": "Изображение успешно загружено",
  "data": {
    "id": "uuid-here",
    "filename": "uuid.jpg",
    "original_url": "/uploads/products/uuid.jpg",
    "thumbnail_url": "/uploads/products/thumbnails/uuid_thumb.jpg",
    "optimized_url": "/uploads/products/optimized/uuid_opt.jpg",
    "size": 1234567,
    "content_type": "image/jpeg"
  }
}
```

### Загрузка нескольких изображений
```http
POST /api/images/upload-multiple
Authorization: Bearer YOUR_TOKEN
Content-Type: multipart/form-data

files: <image file 1>
files: <image file 2>
...
```

**Ответ:**
```json
{
  "success": true,
  "uploaded": 3,
  "failed": 0,
  "data": [
    { "id": "...", "filename": "...", ... },
    { "id": "...", "filename": "...", ... },
    { "id": "...", "filename": "...", ... }
  ],
  "errors": []
}
```

### Удаление изображения
```http
DELETE /api/images/{image_id}
Authorization: Bearer YOUR_TOKEN
```

### Получение изображения
```http
GET /api/images/serve/original/filename.jpg
GET /api/images/serve/thumbnail/filename_thumb.jpg
GET /api/images/serve/optimized/filename_opt.jpg
```

Или через статику:
```http
GET /uploads/products/filename.jpg
GET /uploads/products/thumbnails/filename_thumb.jpg
GET /uploads/products/optimized/filename_opt.jpg
```

---

## 🔧 Настройки:

В `services/image_service.py`:

```python
class ImageService:
    def __init__(self):
        self.max_file_size = 5 * 1024 * 1024  # 5MB
        self.allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
        self.thumbnail_size = (300, 300)
        self.large_size = (1200, 1200)
```

Можно изменить:
- Максимальный размер файла
- Разрешенные форматы
- Размеры миниатюр и оптимизированных изображений

---

## 📦 Добавление изображений к товарам:

### 1. Обновите модель Product

```python
# backend/models/product.py
class Product(Base):
    # ... существующие поля
    images = Column(JSON, default=list)  # Массив URL изображений
```

### 2. Создайте миграцию

```sql
-- backend/migrations/009_add_images_to_products.sql
ALTER TABLE products ADD COLUMN images JSONB DEFAULT '[]';
COMMENT ON COLUMN products.images IS 'Массив URL изображений товара';
```

### 3. Обновите схему

```python
# backend/schemas/product.py
class ProductCreate(BaseModel):
    # ... существующие поля
    images: List[str] = []

class ProductResponse(BaseModel):
    # ... существующие поля
    images: List[str] = []
```

### 4. Обновите роутер

```python
# backend/api/routers/products.py
@router.post("/")
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    new_product = Product(
        # ... существующие поля
        images=product.images  # Сохраняем массив URL
    )
    # ...
```

### 5. Используйте в React

```tsx
function CreateProductForm() {
  const [images, setImages] = useState<string[]>([])

  const handleImagesUploaded = (uploadedImages: UploadedImage[]) => {
    // Сохраняем URL оптимизированных изображений
    const urls = uploadedImages.map(img => img.optimized_url || img.original_url)
    setImages(urls)
  }

  const handleSubmit = async () => {
    const productData = {
      name: '...',
      price: 100,
      images: images  // Отправляем массив URL
    }
    // POST /api/products
  }

  return (
    <div>
      <ImageUpload onUpload={handleImagesUploaded} />
      {/* ... остальная форма */}
    </div>
  )
}
```

---

## 🌐 Облачное хранилище (опционально):

### Вариант 1: AWS S3

```python
# backend/services/s3_service.py
import boto3

class S3ImageService:
    def __init__(self):
        self.s3 = boto3.client('s3',
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY
        )
        self.bucket = settings.S3_BUCKET
    
    async def upload_image(self, file: UploadFile):
        # Загрузка в S3
        self.s3.upload_fileobj(
            file.file,
            self.bucket,
            filename,
            ExtraArgs={'ContentType': file.content_type}
        )
        
        # URL
        url = f"https://{self.bucket}.s3.amazonaws.com/{filename}"
        return url
```

### Вариант 2: Cloudinary

```python
# backend/services/cloudinary_service.py
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

async def upload_to_cloudinary(file: UploadFile):
    result = cloudinary.uploader.upload(
        file.file,
        folder="edu-na-bazar/products",
        transformation=[
            {'width': 1200, 'height': 1200, 'crop': 'limit'},
            {'quality': 'auto'},
            {'fetch_format': 'auto'}
        ]
    )
    return result['secure_url']
```

---

## 🔒 Безопасность:

1. **Авторизация** - загрузка только для авторизованных пользователей
2. **Валидация типов** - только изображения (MIME type)
3. **Ограничение размера** - максимум 5MB
4. **Уникальные имена** - UUID для предотвращения конфликтов
5. **Санитизация** - конвертация в RGB, удаление EXIF

---

## 📊 Статистика:

Добавьте в админку:
```python
@router.get("/admin/images/stats")
async def get_images_stats():
    upload_dir = Path("uploads/products")
    
    total_files = len(list(upload_dir.rglob("*.*")))
    total_size = sum(f.stat().st_size for f in upload_dir.rglob("*.*"))
    
    return {
        "total_files": total_files,
        "total_size_mb": round(total_size / 1024 / 1024, 2),
        "thumbnails": len(list((upload_dir / "thumbnails").glob("*"))),
        "optimized": len(list((upload_dir / "optimized").glob("*")))
    }
```

---

## ✅ Готово!

Теперь у вас есть полноценный сервис для работы с изображениями:
- ✅ Загрузка с валидацией
- ✅ Автоматическое создание миниатюр
- ✅ Оптимизация для веба
- ✅ React компонент с превью
- ✅ API endpoints
- ✅ Готово к расширению (S3, Cloudinary)

**Следующие шаги:**
1. Запустите backend: `python main.py`
2. Установите зависимости: `pip install Pillow aiofiles`
3. Используйте компонент `ImageUpload` в формах товаров
4. Добавьте поле `images` в модель Product
