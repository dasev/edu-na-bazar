@echo off
chcp 65001 >nul
echo ============================================
echo 🚀 МИГРАЦИЯ ДАННЫХ С СОХРАНЕНИЕМ СВЯЗЕЙ
echo ============================================
echo.
echo 📋 Что будет мигрировано:
echo    1. Категории (331 + 500)
echo    2. Пользователи (2,571)
echo    3. Магазины (678)
echo    4. Товары (14,139)
echo    5. Изображения (9,765)
echo    6. Отзывы (15)
echo.
echo 🔗 Все связи будут сохранены:
echo    - Пользователи → Магазины
echo    - Магазины → Товары
echo    - Категории → Товары
echo    - Товары → Изображения
echo    - Товары → Отзывы
echo.
pause
echo.

cd backend

echo 📦 Активируем виртуальное окружение...
call venv\Scripts\activate.bat

echo.
echo 🔄 Запускаем миграцию...
echo.
python scripts\migrate_from_temp.py

echo.
echo ============================================
echo ✅ Готово!
echo ============================================
echo.
echo 📊 Проверьте данные в PostgreSQL:
echo    SELECT COUNT(*) FROM market.categories;
echo    SELECT COUNT(*) FROM config.users;
echo    SELECT COUNT(*) FROM market.store_owners;
echo    SELECT COUNT(*) FROM market.products;
echo    SELECT COUNT(*) FROM market.product_images;
echo    SELECT COUNT(*) FROM market.reviews;
echo.
pause
