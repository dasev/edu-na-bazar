# 📱 SMS-Аутентификация (как в Циане)

## 🎯 Концепция

Система аутентификации **БЕЗ ПАРОЛЕЙ** через SMS-коды:
- ✅ Вход/регистрация по номеру телефона
- ✅ SMS с 6-значным кодом
- ✅ Долгая сессия (90 дней)
- ✅ Никаких паролей
- ✅ Простой UX как в Циане

---

## 🔄 Процесс аутентификации

### 1️⃣ Отправка SMS кода

**Новый пользователь:**
```
1. Вводит телефон: +7 999 123-45-67
2. Вводит ФИО: Иванов Иван Иванович
3. Вводит email (опционально): ivan@example.com
4. Нажимает "Зарегистрироваться"
5. Получает SMS с кодом: 123456
```

**Существующий пользователь:**
```
1. Вводит телефон: +7 999 123-45-67
2. Нажимает "Получить код"
3. Получает SMS с кодом: 654321
```

### 2️⃣ Проверка кода

```
1. Вводит код из SMS: 123456
2. Нажимает "Подтвердить"
3. Получает JWT токен (действителен 90 дней)
4. Автоматически авторизован
```

---

## 🔧 Backend API

### POST `/api/auth/send-sms`

Отправить SMS код для входа/регистрации.

**Request:**
```json
{
  "phone": "+79991234567",
  "full_name": "Иванов Иван Иванович",  // Только для новых пользователей
  "email": "ivan@example.com"            // Опционально
}
```

**Response:**
```json
{
  "success": true,
  "message": "SMS код отправлен",
  "phone": "+79991234567",
  "expires_in": 300,  // 5 минут
  "code": "123456"    // ⚠️ Только в DEV режиме!
}
```

**Ошибки:**
- `400` - Неверный формат телефона
- `400` - Для регистрации необходимо указать ФИО
- `500` - Ошибка отправки SMS

---

### POST `/api/auth/verify-sms`

Проверить SMS код и получить токен.

**Request:**
```json
{
  "phone": "+79991234567",
  "code": "123456"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 7776000,  // 90 дней в секундах
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "phone": "+79991234567",
    "email": "ivan@example.com",
    "full_name": "Иванов Иван Иванович",
    "is_verified": true,
    "created_at": "2025-11-22T00:00:00",
    "last_login": "2025-11-22T02:30:00"
  }
}
```

**Ошибки:**
- `400` - Код не найден или истек
- `400` - Неверный код
- `400` - Превышено количество попыток (3 попытки)
- `404` - Пользователь не найден

---

### GET `/api/auth/me`

Получить информацию о текущем пользователе.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "phone": "+79991234567",
  "email": "ivan@example.com",
  "full_name": "Иванов Иван Иванович",
  "is_verified": true,
  "created_at": "2025-11-22T00:00:00",
  "last_login": "2025-11-22T02:30:00"
}
```

---

## 💾 База данных

### Таблица `users`

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone VARCHAR(20) UNIQUE NOT NULL,        -- +79991234567
    email VARCHAR(255) UNIQUE,                -- ivan@example.com
    full_name VARCHAR(255) NOT NULL,          -- Иванов Иван Иванович
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,        -- Подтвержден ли телефон
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

### Таблица `sms_codes`

```sql
CREATE TABLE sms_codes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone VARCHAR(20) NOT NULL,               -- +79991234567
    code VARCHAR(6) NOT NULL,                 -- 123456
    is_used BOOLEAN DEFAULT FALSE,
    attempts VARCHAR(10) DEFAULT '0',         -- Количество попыток
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,            -- Код действителен 5 минут
    used_at TIMESTAMP
);
```

---

## 🎨 Frontend компоненты

### AuthModal

Модальное окно для входа/регистрации.

**Использование:**
```tsx
import AuthModal from './components/Auth/AuthModal'
import { useAuthStore } from './store/authStore'

function App() {
  const [authModalVisible, setAuthModalVisible] = useState(false)
  const { login } = useAuthStore()

  const handleAuthSuccess = (token: string, user: any) => {
    login(token, user)
    // Пользователь авторизован!
  }

  return (
    <>
      <Button onClick={() => setAuthModalVisible(true)}>
        Войти
      </Button>

      <AuthModal
        visible={authModalVisible}
        onClose={() => setAuthModalVisible(false)}
        onSuccess={handleAuthSuccess}
      />
    </>
  )
}
```

### AuthStore (Zustand)

Глобальное состояние аутентификации.

**Использование:**
```tsx
import { useAuthStore } from './store/authStore'

function Profile() {
  const { isAuthenticated, user, logout } = useAuthStore()

  if (!isAuthenticated) {
    return <div>Войдите в систему</div>
  }

  return (
    <div>
      <h1>Привет, {user.full_name}!</h1>
      <p>Телефон: {user.phone}</p>
      <Button onClick={logout}>Выйти</Button>
    </div>
  )
}
```

---

## 🔐 Безопасность

### JWT токены

- **Алгоритм:** HS256
- **Срок действия:** 90 дней
- **Payload:**
  ```json
  {
    "sub": "user_id",
    "phone": "+79991234567",
    "exp": 1234567890,
    "iat": 1234567890,
    "type": "access"
  }
  ```

### SMS коды

- **Длина:** 6 цифр
- **Срок действия:** 5 минут
- **Попытки:** Максимум 3
- **Повторная отправка:** Без ограничений

### Форматирование телефона

Принимаются форматы:
- `+79991234567` ✅
- `89991234567` ✅ → `+79991234567`
- `79991234567` ✅ → `+79991234567`
- `9991234567` ✅ → `+79991234567`

---

## 📲 Интеграция SMS провайдеров

### Текущий статус: MOCK (разработка)

В разработке SMS коды выводятся в консоль:
```
==================================================
📱 SMS ОТПРАВЛЕНО НА +79991234567
🔐 КОД: 123456
⏰ Действителен 5 минут
==================================================
```

### Интеграция с реальными провайдерами

#### 1. SMS.RU (Россия)

```python
# backend/services/sms_service.py

import aiohttp

async def send_sms(phone: str, code: str) -> bool:
    async with aiohttp.ClientSession() as session:
        url = "https://sms.ru/sms/send"
        params = {
            "api_id": settings.SMS_RU_API_KEY,
            "to": phone,
            "msg": f"Ваш код: {code}",
            "json": 1
        }
        async with session.get(url, params=params) as resp:
            result = await resp.json()
            return result.get("status") == "OK"
```

**Регистрация:** https://sms.ru/  
**Цена:** ~2-3₽ за SMS

#### 2. SMSC.RU (Россия)

```python
async def send_sms(phone: str, code: str) -> bool:
    async with aiohttp.ClientSession() as session:
        url = "https://smsc.ru/sys/send.php"
        params = {
            "login": settings.SMSC_LOGIN,
            "psw": settings.SMSC_PASSWORD,
            "phones": phone,
            "mes": f"Ваш код: {code}",
            "fmt": 3  # JSON
        }
        async with session.get(url, params=params) as resp:
            result = await resp.json()
            return "id" in result
```

**Регистрация:** https://smsc.ru/  
**Цена:** ~1.5-2₽ за SMS

#### 3. Twilio (международный)

```python
from twilio.rest import Client

async def send_sms(phone: str, code: str) -> bool:
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    message = client.messages.create(
        body=f"Ваш код: {code}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone
    )
    
    return message.status in ["queued", "sent"]
```

**Регистрация:** https://www.twilio.com/  
**Цена:** ~$0.05-0.10 за SMS

---

## 🧪 Тестирование

### Тест регистрации нового пользователя

```bash
# 1. Отправить SMS
curl -X POST http://localhost:8000/api/auth/send-sms \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+79991234567",
    "full_name": "Тест Тестович",
    "email": "test@example.com"
  }'

# Response: {"success": true, "code": "123456", ...}

# 2. Проверить код
curl -X POST http://localhost:8000/api/auth/verify-sms \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+79991234567",
    "code": "123456"
  }'

# Response: {"access_token": "...", "user": {...}}
```

### Тест входа существующего пользователя

```bash
# 1. Отправить SMS (без ФИО)
curl -X POST http://localhost:8000/api/auth/send-sms \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+79991234567"
  }'

# 2. Проверить код
curl -X POST http://localhost:8000/api/auth/verify-sms \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+79991234567",
    "code": "654321"
  }'
```

---

## 📋 TODO

- [ ] Интеграция с реальным SMS провайдером (SMS.RU)
- [ ] Rate limiting (защита от спама)
- [ ] Логирование попыток входа
- [ ] Блокировка после N неудачных попыток
- [ ] Refresh tokens (опционально)
- [ ] 2FA для админов (опционально)

---

## 🚀 Готово к использованию!

Система SMS-аутентификации полностью работает:
- ✅ Backend API готов
- ✅ База данных создана
- ✅ Frontend форма готова
- ✅ JWT токены работают
- ✅ Долгая сессия (90 дней)

**Для продакшена:** Замените MOCK отправку SMS на реального провайдера!
