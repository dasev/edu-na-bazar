"""
Еду на базар - FastAPI Backend
"""
from fastapi import FastAPI, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
import traceback
import json

from api.routers import products, categories, stores, orders, auth, cart, images, my_stores, store_products
from database import engine, Base, get_db
from config import settings
from fastapi.staticfiles import StaticFiles


# Настройка кодировки для JSON
import sys
import locale
if sys.platform == 'win32':
    # Для Windows устанавливаем UTF-8
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


# Custom JSON Response для правильной кодировки
class UnicodeJSONResponse(JSONResponse):
    """JSONResponse с правильной обработкой Unicode"""
    def render(self, content) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events"""
    # Startup
    print("🚀 Starting Еду на базар API...")
    print(f"📊 Database: {settings.DATABASE_URL}")
    print(f"🔴 Redis: {settings.REDIS_URL}")
    
    # Импортируем все модели чтобы SQLAlchemy знал о них
    from models import product_image  # noqa
    
    yield
    
    # Shutdown
    print("👋 Shutting down...")


# Create FastAPI app  
app = FastAPI(
    title="Еду на базар API",
    description="Маркетплейс фермерских хозяйств - прямые продажи от производителей без посредников",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    debug=True,  # Включаем debug для детальных ошибок
    exception_handlers={},  # Отключаем встроенные обработчики
    default_response_class=UnicodeJSONResponse,  # Используем кастомный JSON
)


# Custom error handling middleware
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    """Middleware для обработки всех ошибок"""
    try:
        response = await call_next(request)
        # Добавляем заголовок Content-Type с charset=utf-8
        if "application/json" in response.headers.get("content-type", ""):
            response.headers["content-type"] = "application/json; charset=utf-8"
        return response
    except Exception as exc:
        error_detail = {
            "error": exc.__class__.__name__,
            "message": str(exc),
            "path": str(request.url.path),
            "method": request.method,
        }
        
        # В debug режиме добавляем traceback
        if app.debug:
            error_detail["traceback"] = traceback.format_exc().split('\n')
        
        return UnicodeJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_detail,
        )

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Обработчик HTTP ошибок"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTPException",
            "message": exc.detail,
            "status_code": exc.status_code,
            "path": request.url.path,
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Глобальный обработчик всех ошибок"""
    error_detail = {
        "error": exc.__class__.__name__,
        "message": str(exc),
        "path": request.url.path,
        "method": request.method,
    }
    
    # В debug режиме добавляем traceback
    if app.debug:
        error_detail["traceback"] = traceback.format_exc().split('\n')
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_detail
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Обработчик ошибок валидации"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "ValidationError",
            "message": "Ошибка валидации данных",
            "details": exc.errors(),
            "body": exc.body,
        }
    )

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(categories.router, prefix="/api/categories", tags=["categories"])
app.include_router(stores.router, prefix="/api/stores", tags=["stores"])
app.include_router(orders.router, prefix="/api/orders", tags=["orders"])
app.include_router(cart.router, prefix="/api/cart", tags=["cart"])
app.include_router(images.router, prefix="/api/images", tags=["images"])
app.include_router(my_stores.router)
app.include_router(store_products.router)

# Статические файлы для изображений
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Еду на базар API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "ok"}


@app.get("/test-db")
async def test_db_endpoint(db: AsyncSession = Depends(get_db)):
    """Test DB connection"""
    from sqlalchemy import text, select
    from models.category import Category
    
    # Test count
    result = await db.execute(text("SELECT COUNT(*) FROM products"))
    count = result.scalar()
    
    # Test category
    result = await db.execute(select(Category).limit(1))
    category = result.scalar_one_or_none()
    
    return {
        "products_count": count,
        "category_test": {
            "id": str(category.id) if category else None,
            "name": category.name if category else None,
            "slug": category.slug if category else None,
        } if category else None,
        "status": "ok"
    }


@app.get("/test-error")
async def test_error_endpoint():
    """Test error handling"""
    raise ValueError("Это тестовая ошибка для проверки обработчика")


@app.get("/test-encoding")
async def test_encoding_endpoint():
    """Test UTF-8 encoding"""
    return {
        "message": "Привет мир!",
        "categories": ["Фрукты", "Овощи", "Молочные продукты"],
        "product": "Яблоки Гренни Смит",
        "description": "Свежие зеленые яблоки"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
