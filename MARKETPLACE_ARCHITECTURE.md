# 🏪 Архитектура Маркетплейса "Еду на базар"

## 📋 Концепция

Маркетплейс, где:
- **Покупатели** (обычные пользователи) - покупают товары
- **Продавцы** (организации) - управляют своими магазинами и товарами
- **Администраторы** - модерируют платформу

---

## 🗂️ Структура БД

### 1. **Роли пользователей (User Roles)**

```python
class UserRole(enum.Enum):
    CUSTOMER = "customer"      # Покупатель (по умолчанию)
    SELLER = "seller"          # Продавец (владелец магазина)
    ADMIN = "admin"            # Администратор платформы
```

### 2. **Обновленная модель User**

```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    
    # Основная информация
    phone = Column(String(20), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    full_name = Column(String(255), nullable=False)
    address = Column(String(500), nullable=True)
    
    # ✅ НОВОЕ: Роль пользователя
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False, index=True)
    
    # Статус
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    stores = relationship("Store", back_populates="owner")  # Магазины продавца
```

### 3. **Обновленная модель Store (Магазин)**

```python
class Store(Base):
    __tablename__ = "stores"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    
    # ✅ НОВОЕ: Владелец магазина
    owner_id = Column(UUID, ForeignKey('users.id'), nullable=False, index=True)
    
    # Основная информация
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)  # URL-friendly имя
    description = Column(Text, nullable=True)
    
    # Контакты
    address = Column(String(500), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    
    # Время работы
    working_hours = Column(String(255), nullable=True)
    
    # Геолокация (PostGIS)
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    delivery_zone = Column(Geometry('POLYGON', srid=4326), nullable=True)
    
    # Изображения
    logo = Column(String(500), nullable=True)
    banner = Column(String(500), nullable=True)
    
    # ✅ НОВОЕ: Рейтинг и статистика
    rating = Column(NUMERIC(3, 2), default=0.0)
    reviews_count = Column(Integer, default=0)
    products_count = Column(Integer, default=0)
    orders_count = Column(Integer, default=0)
    
    # ✅ НОВОЕ: Статус модерации
    status = Column(Enum(StoreStatus), default=StoreStatus.PENDING, nullable=False)
    # PENDING - на модерации
    # ACTIVE - активен
    # SUSPENDED - приостановлен
    # REJECTED - отклонен
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="stores")
    products = relationship("Product", back_populates="store")
```

### 4. **Обновленная модель Product (Товар)**

```python
class Product(Base):
    __tablename__ = "products"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    
    # ✅ НОВОЕ: Принадлежность к магазину
    store_id = Column(UUID, ForeignKey('stores.id'), nullable=False, index=True)
    
    # Основная информация
    name = Column(String(500), nullable=False, index=True)
    slug = Column(String(500), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Цены
    price = Column(NUMERIC(10, 2), nullable=False)
    old_price = Column(NUMERIC(10, 2), nullable=True)
    
    # Изображения
    images = Column(ARRAY(String), default=[])  # Массив URL изображений
    
    # Категория
    category_id = Column(UUID, ForeignKey('categories.id'), nullable=True, index=True)
    
    # Рейтинг и отзывы
    rating = Column(NUMERIC(3, 2), default=0.0)
    reviews_count = Column(Integer, default=0)
    
    # Наличие и остатки
    in_stock = Column(Boolean, default=True)
    stock_quantity = Column(Integer, default=0)  # Количество на складе
    
    # Единица измерения
    unit = Column(String(50), default="шт")
    
    # ✅ НОВОЕ: Статус модерации
    status = Column(Enum(ProductStatus), default=ProductStatus.PENDING, nullable=False)
    # PENDING - на модерации
    # ACTIVE - активен
    # REJECTED - отклонен
    # OUT_OF_STOCK - нет в наличии
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    store = relationship("Store", back_populates="products")
    category = relationship("Category", back_populates="products")
```

### 5. **Новая модель: StoreReview (Отзывы о магазине)**

```python
class StoreReview(Base):
    __tablename__ = "store_reviews"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    
    store_id = Column(UUID, ForeignKey('stores.id'), nullable=False, index=True)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False, index=True)
    order_id = Column(UUID, ForeignKey('orders.id'), nullable=True)  # Связь с заказом
    
    # Оценка
    rating = Column(Integer, nullable=False)  # 1-5
    
    # Отзыв
    comment = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    store = relationship("Store")
    user = relationship("User")
    order = relationship("Order")
```

### 6. **Новая модель: ProductReview (Отзывы о товаре)**

```python
class ProductReview(Base):
    __tablename__ = "product_reviews"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    
    product_id = Column(UUID, ForeignKey('products.id'), nullable=False, index=True)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False, index=True)
    order_id = Column(UUID, ForeignKey('orders.id'), nullable=True)
    
    # Оценка
    rating = Column(Integer, nullable=False)  # 1-5
    
    # Отзыв
    comment = Column(Text, nullable=True)
    images = Column(ARRAY(String), default=[])  # Фото к отзыву
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = relationship("Product")
    user = relationship("User")
    order = relationship("Order")
```

---

## 🔐 Права доступа (Permissions)

### **Покупатель (Customer)**
- ✅ Просмотр товаров и магазинов
- ✅ Добавление в корзину
- ✅ Оформление заказов
- ✅ Оставление отзывов (после покупки)
- ❌ Создание/редактирование товаров
- ❌ Управление магазинами

### **Продавец (Seller)**
- ✅ Все права покупателя
- ✅ Создание и управление своими магазинами
- ✅ Добавление/редактирование товаров в своих магазинах
- ✅ Просмотр заказов своих товаров
- ✅ Управление остатками и ценами
- ✅ Просмотр статистики продаж
- ❌ Редактирование чужих магазинов/товаров
- ❌ Модерация платформы

### **Администратор (Admin)**
- ✅ Все права продавца
- ✅ Модерация магазинов (одобрение/отклонение)
- ✅ Модерация товаров
- ✅ Управление пользователями
- ✅ Просмотр всей статистики
- ✅ Управление категориями

---

## 🛠️ API Endpoints

### **Для продавцов**

```
POST   /api/seller/stores                    # Создать магазин
GET    /api/seller/stores                    # Мои магазины
GET    /api/seller/stores/{id}               # Детали магазина
PUT    /api/seller/stores/{id}               # Обновить магазин
DELETE /api/seller/stores/{id}               # Удалить магазин

POST   /api/seller/stores/{id}/products      # Добавить товар
GET    /api/seller/stores/{id}/products      # Товары магазина
PUT    /api/seller/products/{id}             # Обновить товар
DELETE /api/seller/products/{id}             # Удалить товар

GET    /api/seller/orders                    # Заказы моих товаров
GET    /api/seller/statistics                # Статистика продаж
```

### **Для администраторов**

```
GET    /api/admin/stores/pending             # Магазины на модерации
PUT    /api/admin/stores/{id}/approve        # Одобрить магазин
PUT    /api/admin/stores/{id}/reject         # Отклонить магазин

GET    /api/admin/products/pending           # Товары на модерации
PUT    /api/admin/products/{id}/approve      # Одобрить товар
PUT    /api/admin/products/{id}/reject       # Отклонить товар

GET    /api/admin/users                      # Управление пользователями
PUT    /api/admin/users/{id}/role            # Изменить роль
```

### **Публичные (для всех)**

```
GET    /api/stores                           # Список магазинов
GET    /api/stores/{slug}                    # Детали магазина
GET    /api/stores/{slug}/products           # Товары магазина

GET    /api/products                         # Все товары (с фильтрами)
GET    /api/products/{slug}                  # Детали товара
```

---

## 📱 Frontend - Новые страницы

### **Для покупателей**
- `/stores` - Список всех магазинов
- `/stores/{slug}` - Страница магазина с товарами
- `/products/{slug}` - Страница товара (с указанием магазина)

### **Для продавцов**
- `/seller/dashboard` - Дашборд продавца
- `/seller/stores` - Мои магазины
- `/seller/stores/new` - Создать магазин
- `/seller/stores/{id}/edit` - Редактировать магазин
- `/seller/products` - Мои товары
- `/seller/products/new` - Добавить товар
- `/seller/orders` - Заказы моих товаров
- `/seller/statistics` - Статистика продаж

### **Для администраторов**
- `/admin/dashboard` - Админ панель
- `/admin/stores/moderation` - Модерация магазинов
- `/admin/products/moderation` - Модерация товаров
- `/admin/users` - Управление пользователями

---

## 🚀 План миграции

### **Этап 1: База данных**
1. Добавить `role` в таблицу `users`
2. Добавить `owner_id` в таблицу `stores`
3. Добавить `store_id` в таблицу `products`
4. Добавить `status` в `stores` и `products`
5. Создать таблицы `store_reviews` и `product_reviews`
6. Создать миграцию Alembic

### **Этап 2: Backend API**
1. Создать middleware для проверки ролей
2. Реализовать endpoints для продавцов (`/api/seller/*`)
3. Реализовать endpoints для админов (`/api/admin/*`)
4. Обновить существующие endpoints (добавить фильтрацию по магазинам)
5. Добавить систему отзывов

### **Этап 3: Frontend**
1. Создать страницы для продавцов
2. Создать админ-панель
3. Обновить карточки товаров (показывать магазин)
4. Добавить страницу магазина
5. Реализовать систему отзывов

### **Этап 4: Тестирование**
1. Создать тестовых пользователей с разными ролями
2. Протестировать права доступа
3. Протестировать модерацию
4. Протестировать создание магазинов и товаров

---

## 💡 Дополнительные фичи

### **Для продавцов**
- 📊 Аналитика продаж (графики, топ товаров)
- 💬 Чат с покупателями
- 📦 Управление остатками (автоматическое списание)
- 🎯 Промо-акции и скидки
- 📸 Массовая загрузка товаров (CSV/Excel)

### **Для покупателей**
- ⭐ Избранные магазины
- 🔔 Уведомления о новых товарах
- 🏆 Рейтинг магазинов
- 🔍 Поиск по магазинам
- 📍 Магазины рядом со мной (геолокация)

### **Для платформы**
- 💳 Комиссия с продаж
- 📈 Статистика платформы
- 🎨 Кастомизация витрины магазина
- 🔐 Двухфакторная аутентификация для продавцов
- 📧 Email-рассылки

---

## 🎯 Приоритеты реализации

### **MVP (Минимум)**
1. ✅ Роли пользователей (Customer, Seller, Admin)
2. ✅ Привязка магазинов к владельцам
3. ✅ Привязка товаров к магазинам
4. ✅ Базовые права доступа
5. ✅ Страница магазина для покупателей
6. ✅ Дашборд продавца (создание магазина и товаров)

### **Этап 2**
1. Модерация магазинов и товаров
2. Система отзывов
3. Статистика для продавцов
4. Админ-панель

### **Этап 3**
1. Аналитика и графики
2. Промо-акции
3. Массовая загрузка товаров
4. Расширенные фильтры

---

## 📝 Примечания

- Все изменения обратно совместимы
- Существующие товары можно привязать к дефолтному магазину
- Существующие пользователи получат роль `CUSTOMER`
- Миграция данных будет безопасной (с бэкапом)
