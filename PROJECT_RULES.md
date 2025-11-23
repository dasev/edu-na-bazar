# 📋 Правила разработки проекта "Еду на базар"

## 🎯 Основные принципы

### 1. **Архитектура**
- Монорепозиторий: frontend + backend в одном репо
- Frontend: DevExtreme React Template как основа
- Backend: FastAPI с async/await
- БД: PostgreSQL + PostGIS для геоданных

### 2. **Дизайн в стиле Ozon**
- Цвета: Синий #005BFF, Оранжевый #FF6934, Серый фон #F2F3F5
- Закругленные углы: 8-12px везде
- Крупные элементы: кнопки минимум 44px
- Белые карточки на сером фоне
- Жирные цены: 20-24px, font-weight 700

### 3. **Компоненты**

#### ✅ Используем DevExtreme для:
- **DataGrid** - таблицы товаров, заказов
- **Form** - формы редактирования
- **Popup** - модальные окна
- **Button** - все кнопки
- **TextBox, SelectBox, NumberBox** - поля ввода
- **Chart, PieChart** - графики в админке

#### ✅ Добавляем сверху:
- **Mapbox GL JS** - карты (DevExtreme не имеет карт)
- **TanStack Query** - управление серверным состоянием
- **Zustand** - клиентское состояние (корзина, фильтры)

#### ❌ НЕ используем:
- Material-UI, Ant Design - конфликтуют с DevExtreme
- Свои кастомные таблицы - есть DataGrid
- Свои кастомные формы - есть Form

### 4. **Структура кода**

#### Frontend:
```
src/
├── components/
│   ├── header/           # Header в стиле Ozon
│   ├── product/          # ProductCard, ProductGrid
│   ├── filters/          # FilterPanel
│   ├── cart/             # CartButton, CartDrawer
│   └── map/              # StoreMap, DeliveryZones
├── pages/
│   ├── home/             # Главная
│   ├── catalog/          # Каталог с фильтрами
│   ├── product-detail/   # Детальная страница
│   ├── cart/             # Корзина
│   ├── checkout/         # Оформление заказа
│   └── map/              # Карта магазинов
├── api/
│   └── api-client.js     # Axios клиент
├── store/
│   ├── cart.js           # Zustand store корзины
│   └── filters.js        # Zustand store фильтров
└── styles/
    ├── ozon-theme.scss   # Кастомная тема
    └── variables.scss    # CSS переменные
```

#### Backend:
```
api/
├── routers/
│   ├── products.py       # CRUD товаров
│   ├── orders.py         # Заказы
│   ├── stores.py         # Магазины (ГИС)
│   └── auth.py           # Аутентификация
├── models/               # SQLAlchemy модели
├── schemas/              # Pydantic схемы
├── services/             # Бизнес-логика
└── main.py
```

### 5. **Правила кода**

#### TypeScript/JavaScript:
```typescript
// ✅ Всегда типы
interface Product {
  id: string;
  name: string;
  price: number;
}

// ✅ Async/await
const data = await api.getProducts();

// ❌ НЕ используй any
const data: any = {}; // ПЛОХО
```

#### Python:
```python
# ✅ Type hints
async def get_product(product_id: int) -> Product:
    ...

# ✅ Pydantic валидация
class ProductCreate(BaseModel):
    name: str = Field(min_length=3)
    price: float = Field(gt=0)

# ✅ Async для I/O
async def get_products(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()
```

### 6. **API Design**

#### RESTful endpoints:
```
GET    /api/products          # Список
GET    /api/products/{id}     # Один элемент
POST   /api/products          # Создать
PUT    /api/products/{id}     # Обновить
DELETE /api/products/{id}     # Удалить
```

#### Структура ответа:
```json
{
  "data": [...],
  "meta": {
    "total": 100,
    "page": 1,
    "per_page": 20
  }
}
```

### 7. **Работа с БД**

#### Миграции (обязательно!):
```bash
alembic revision --autogenerate -m "Add products table"
alembic upgrade head
```

#### Модели:
```python
class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
```

#### ГИС (PostGIS):
```python
from geoalchemy2 import Geometry

class Store(Base):
    __tablename__ = "stores"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str]
    location: Mapped[str] = mapped_column(
        Geometry('POINT', srid=4326)
    )
    delivery_zone: Mapped[str] = mapped_column(
        Geometry('POLYGON', srid=4326)
    )
```

### 8. **Безопасность**

```python
# ✅ JWT токены
from fastapi_users.authentication import JWTStrategy

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Rate limiting
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.get("/api/products")
@limiter.limit("100/minute")
async def get_products():
    ...
```

### 9. **Производительность**

#### Frontend:
```typescript
// ✅ Кэширование запросов
const { data } = useQuery({
  queryKey: ['products'],
  queryFn: getProducts,
  staleTime: 5 * 60 * 1000, // 5 минут
});

// ✅ Lazy loading
const Map = dynamic(() => import('@/components/Map'), {
  ssr: false,
  loading: () => <Spinner />
});
```

#### Backend:
```python
# ✅ Индексы в БД
name: Mapped[str] = mapped_column(String(255), index=True)

# ✅ Кэширование в Redis
@cache(expire=300)
async def get_products():
    ...

# ✅ Пагинация
@app.get("/api/products")
async def get_products(skip: int = 0, limit: int = 20):
    ...
```

### 10. **Git workflow**

```bash
# ✅ Conventional Commits
git commit -m "feat: add product catalog"
git commit -m "fix: resolve cart calculation"
git commit -m "docs: update API documentation"

# ✅ Feature branches
git checkout -b feature/product-filters
git checkout -b fix/cart-bug
```

## 🎯 Чек-лист перед коммитом

- [ ] ✅ Код работает локально
- [ ] ✅ Нет console.log / print для отладки
- [ ] ✅ Добавлены типы (TypeScript/Python)
- [ ] ✅ Код отформатирован (Prettier/Black)
- [ ] ✅ Нет ошибок ESLint/Pylint
- [ ] ✅ Миграции созданы (если изменена БД)
- [ ] ✅ Обновлена документация (если нужно)

## 🚀 Порядок разработки

1. **Инфраструктура** (1-2 дня)
   - Docker Compose
   - БД + миграции
   - Базовая структура

2. **Аутентификация** (2-3 дня)
   - Регистрация/логин
   - JWT токены

3. **Core функционал** (2-4 недели)
   - Каталог товаров
   - Карточка товара
   - Корзина
   - Оформление заказа
   - Карта магазинов

4. **Админка** (1-2 недели)
   - Управление товарами
   - Управление заказами
   - Аналитика

5. **Деплой** (2-3 дня)
   - CI/CD
   - Production окружение

---

**Следуй этим правилам и проект будет чистым и поддерживаемым!** 🚀
