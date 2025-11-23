# 🔄 Руководство по миграции на маркетплейс

## ✅ Что уже сделано

### 1. **Модели БД обновлены**
- ✅ `models/enums.py` - добавлены enum для ролей и статусов
- ✅ `models/user.py` - добавлено поле `role` и relationship `stores`
- ✅ `models/store.py` - добавлены `owner_id`, `slug`, `status`, рейтинги
- ✅ `models/product.py` - добавлены `store_id`, `slug`, `status`, `images` (массив)

### 2. **Новые поля**

**User:**
- `role` - роль пользователя (customer/seller/admin)
- `stores` - relationship к магазинам

**Store:**
- `owner_id` - владелец магазина (FK на users)
- `slug` - URL-friendly имя
- `description` - описание магазина
- `logo` - логотип
- `banner` - баннер
- `rating` - рейтинг магазина
- `reviews_count` - количество отзывов
- `products_count` - количество товаров
- `orders_count` - количество заказов
- `status` - статус модерации (pending/active/suspended/rejected)

**Product:**
- `store_id` - принадлежность к магазину (FK на stores)
- `slug` - URL-friendly имя
- `images` - массив URL изображений (вместо одного `image`)
- `stock_quantity` - количество на складе
- `status` - статус модерации (pending/active/rejected/out_of_stock)

---

## 🚀 Следующие шаги

### Шаг 1: Создать миграцию Alembic

```bash
# В директории backend
cd c:\python\edu-na-bazar\backend

# Создать миграцию
alembic revision --autogenerate -m "Add marketplace features: roles, store owners, product stores"

# Проверить сгенерированную миграцию
# Файл будет в: backend/alembic/versions/

# Применить миграцию
alembic upgrade head
```

### Шаг 2: Миграция существующих данных

После применения миграции нужно:

1. **Создать дефолтного владельца для существующих магазинов:**
```sql
-- Создать админа-владельца
INSERT INTO users (id, phone, email, full_name, role, is_verified, is_active)
VALUES (
    gen_random_uuid(),
    '+79999999999',
    'admin@edunabazar.ru',
    'Администратор платформы',
    'admin',
    true,
    true
);

-- Привязать существующие магазины к админу
UPDATE stores 
SET owner_id = (SELECT id FROM users WHERE role = 'admin' LIMIT 1)
WHERE owner_id IS NULL;
```

2. **Создать дефолтный магазин для существующих товаров:**
```sql
-- Если нет магазинов, создать дефолтный
INSERT INTO stores (id, owner_id, name, slug, address, location, status)
VALUES (
    gen_random_uuid(),
    (SELECT id FROM users WHERE role = 'admin' LIMIT 1),
    'Общий каталог',
    'general-catalog',
    'г. Москва',
    ST_GeomFromText('POINT(37.6173 55.7558)', 4326),
    'active'
);

-- Привязать существующие товары к дефолтному магазину
UPDATE products 
SET store_id = (SELECT id FROM stores WHERE slug = 'general-catalog' LIMIT 1)
WHERE store_id IS NULL;
```

3. **Сгенерировать slug для существующих записей:**
```sql
-- Для магазинов (если slug пустой)
UPDATE stores 
SET slug = LOWER(REGEXP_REPLACE(name, '[^a-zA-Z0-9а-яА-Я]+', '-', 'g'))
WHERE slug IS NULL OR slug = '';

-- Для товаров (если slug пустой)
UPDATE products 
SET slug = LOWER(REGEXP_REPLACE(name, '[^a-zA-Z0-9а-яА-Я]+', '-', 'g'))
WHERE slug IS NULL OR slug = '';
```

4. **Конвертировать старое поле image в массив images:**
```sql
-- Для товаров с одним изображением
UPDATE products 
SET images = ARRAY[image]
WHERE image IS NOT NULL AND (images IS NULL OR array_length(images, 1) IS NULL);
```

### Шаг 3: Обновить schemas

Создать/обновить Pydantic schemas:
- `schemas/user.py` - добавить `role` в UserResponse
- `schemas/store.py` - добавить новые поля
- `schemas/product.py` - добавить `store_id`, `images`

### Шаг 4: Создать middleware для проверки ролей

```python
# backend/middleware/auth.py

from fastapi import HTTPException, Depends
from models.enums import UserRole
from models.user import User

def require_role(*allowed_roles: UserRole):
    """Decorator для проверки роли пользователя"""
    def decorator(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. Required roles: {[r.value for r in allowed_roles]}"
            )
        return current_user
    return decorator

# Использование:
# @router.post("/seller/stores")
# async def create_store(
#     current_user: User = Depends(require_role(UserRole.SELLER, UserRole.ADMIN))
# ):
#     ...
```

### Шаг 5: Создать API endpoints для продавцов

Создать файл `backend/api/routers/seller.py`:
```python
from fastapi import APIRouter, Depends
from models.user import User
from models.enums import UserRole
from middleware.auth import require_role

router = APIRouter()

@router.get("/stores")
async def get_my_stores(
    current_user: User = Depends(require_role(UserRole.SELLER, UserRole.ADMIN))
):
    """Получить магазины текущего пользователя"""
    # ...

@router.post("/stores")
async def create_store(
    current_user: User = Depends(require_role(UserRole.SELLER, UserRole.ADMIN))
):
    """Создать новый магазин"""
    # ...
```

### Шаг 6: Обновить frontend

1. Добавить роли в authStore
2. Создать страницы для продавцов
3. Обновить карточки товаров (показывать магазин)
4. Добавить страницу магазина

---

## 📋 Чеклист миграции

- [ ] Создать миграцию Alembic
- [ ] Применить миграцию к БД
- [ ] Создать дефолтного админа
- [ ] Привязать существующие магазины к админу
- [ ] Создать дефолтный магазин (если нужно)
- [ ] Привязать существующие товары к магазинам
- [ ] Сгенерировать slug для всех записей
- [ ] Конвертировать image → images
- [ ] Обновить schemas
- [ ] Создать middleware для ролей
- [ ] Создать API для продавцов
- [ ] Обновить frontend
- [ ] Протестировать все роли
- [ ] Создать документацию для продавцов

---

## ⚠️ Важные замечания

1. **Обратная совместимость:**
   - Старые товары будут работать (привязаны к дефолтному магазину)
   - Старые пользователи получат роль `customer`
   - API останется работать для существующих клиентов

2. **Безопасность:**
   - Обязательно сделать backup БД перед миграцией
   - Тестировать на dev окружении
   - Проверить все права доступа

3. **Производительность:**
   - Добавлены индексы на `role`, `store_id`, `status`
   - Slug индексирован для быстрого поиска

---

## 🎯 Приоритет реализации

### MVP (сейчас)
1. ✅ Обновить модели
2. ⏳ Создать миграцию
3. ⏳ Мигрировать данные
4. ⏳ Обновить schemas
5. ⏳ Создать middleware ролей

### Этап 2
6. API для продавцов (CRUD магазинов и товаров)
7. Frontend для продавцов
8. Страница магазина для покупателей

### Этап 3
9. Модерация (админ-панель)
10. Система отзывов
11. Статистика для продавцов
