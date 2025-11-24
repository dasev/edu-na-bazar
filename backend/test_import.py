"""
Тест импорта моделей
"""
print("🔍 Проверка импортов...\n")

try:
    print("1. Импорт review моделей...")
    from models.review import ProductReview, ReviewResponse, ProductQuestion, QuestionAnswer, ReviewVote
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

try:
    print("2. Импорт product...")
    from models.product import Product
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

try:
    print("3. Импорт user...")
    from models.user import User
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

try:
    print("4. Импорт роутера reviews...")
    from api.routers import reviews
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

try:
    print("5. Импорт main...")
    import main
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ Проверка завершена")
