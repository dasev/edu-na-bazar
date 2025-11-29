# 📤 Загрузка исправленной миграции на сервер

## ✅ Что исправлено
Добавлен импорт `geoalchemy2` в файл миграции.

## 🚀 Загрузить на сервер

### Способ 1: Через SCP (Windows PowerShell)

```powershell
# На локальной машине
scp backend\alembic\versions\8828a8665651_initial_schema.py root@176.99.5.211:/opt/edu-na-bazar/backend/alembic/versions/
# Пароль: sIAS6APDsKh0bL
```

### Способ 2: Через WinSCP / FileZilla

1. Подключиться к серверу:
   - Host: 176.99.5.211
   - User: root
   - Password: sIAS6APDsKh0bL

2. Загрузить файл:
   - Локальный: `C:\python\edu-na-bazar\backend\alembic\versions\8828a8665651_initial_schema.py`
   - Удаленный: `/opt/edu-na-bazar/backend/alembic/versions/8828a8665651_initial_schema.py`

### Способ 3: Скопировать содержимое вручную

```bash
# На сервере
ssh root@176.99.5.211
cd /opt/edu-na-bazar/backend/alembic/versions
nano 8828a8665651_initial_schema.py

# Найти строку (около строки 10):
# from sqlalchemy.dialects import postgresql

# Добавить после неё:
# import geoalchemy2

# Сохранить: Ctrl+X, Y, Enter
```

## ✅ После загрузки - применить миграцию

```bash
# На сервере
ssh root@176.99.5.211
cd /opt/edu-na-bazar

# Применить миграцию
docker-compose exec backend alembic upgrade head

# Проверить
curl http://localhost:8000/api/categories/
```

## 🎯 Полная последовательность команд

```powershell
# 1. На локальной машине - загрузить файл
scp backend\alembic\versions\8828a8665651_initial_schema.py root@176.99.5.211:/opt/edu-na-bazar/backend/alembic/versions/
```

```bash
# 2. На сервере - применить миграцию
ssh root@176.99.5.211
cd /opt/edu-na-bazar
docker-compose exec backend alembic upgrade head
curl http://localhost:8000/api/categories/
```

---

**После успешной миграции таблицы будут созданы, но пустые!**

Нужно будет загрузить данные (см. следующий шаг).
