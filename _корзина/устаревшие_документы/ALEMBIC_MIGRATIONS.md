# 🔄 Alembic Migrations - Руководство

## ✅ Что готово

- ✅ Alembic настроен и инициализирован
- ✅ Создана initial migration: `8828a8665651_initial_schema.py`
- ✅ Текущая БД помечена как базовая (stamp head)
- ✅ Добавлен `psycopg2-binary` в requirements.txt

---

## 📋 Структура

```
backend/
├── alembic/
│   ├── versions/
│   │   └── 8828a8665651_initial_schema.py  # Initial migration
│   ├── env.py                               # Alembic environment
│   ├── script.py.mako                       # Template для миграций
│   └── README
├── alembic.ini                              # Alembic конфигурация
└── requirements.txt                         # psycopg2-binary добавлен
```

---

## 🚀 Команды

### Проверить текущую версию
```bash
docker-compose -f docker-compose.dev.yml exec -T backend alembic current
```

### Создать новую миграцию
```bash
# Автоматическая генерация (на основе изменений в моделях)
docker-compose -f docker-compose.dev.yml exec -T backend alembic revision --autogenerate -m "Add new field"

# Пустая миграция (для ручного написания)
docker-compose -f docker-compose.dev.yml exec -T backend alembic revision -m "Custom migration"
```

### Применить миграции
```bash
# Применить все миграции
docker-compose -f docker-compose.dev.yml exec -T backend alembic upgrade head

# Применить одну миграцию вперед
docker-compose -f docker-compose.dev.yml exec -T backend alembic upgrade +1

# Применить до конкретной версии
docker-compose -f docker-compose.dev.yml exec -T backend alembic upgrade 8828a8665651
```

### Откатить миграции
```bash
# Откатить одну миграцию назад
docker-compose -f docker-compose.dev.yml exec -T backend alembic downgrade -1

# Откатить до конкретной версии
docker-compose -f docker-compose.dev.yml exec -T backend alembic downgrade 8828a8665651

# Откатить все миграции
docker-compose -f docker-compose.dev.yml exec -T backend alembic downgrade base
```

### История миграций
```bash
# Показать историю
docker-compose -f docker-compose.dev.yml exec -T backend alembic history

# Показать текущую версию
docker-compose -f docker-compose.dev.yml exec -T backend alembic current
```

### Пометить БД версией (без применения)
```bash
# Пометить текущее состояние как head
docker-compose -f docker-compose.dev.yml exec -T backend alembic stamp head

# Пометить конкретной версией
docker-compose -f docker-compose.dev.yml exec -T backend alembic stamp 8828a8665651
```

---

## 📝 Workflow разработки

### 1. Изменить модель
```python
# backend/models/product.py
class Product(Base):
    __tablename__ = "products"
    __table_args__ = {"schema": "market"}
    
    # Добавили новое поле
    discount_percent = Column(Integer, default=0)
```

### 2. Создать миграцию
```bash
docker-compose -f docker-compose.dev.yml exec -T backend alembic revision --autogenerate -m "Add discount_percent to products"
```

### 3. Проверить миграцию
```bash
# Открыть файл в backend/alembic/versions/
# Проверить что upgrade() и downgrade() корректны
```

### 4. Применить миграцию
```bash
docker-compose -f docker-compose.dev.yml exec -T backend alembic upgrade head
```

### 5. Проверить результат
```bash
docker-compose -f docker-compose.dev.yml exec -T backend alembic current
```

---

## 🚀 Деплой на production

### Вариант 1: Автоматический (в CI/CD)

Добавить в `.github/workflows/deploy.yml`:

```yaml
- name: 🔄 Run migrations
  uses: appleboy/ssh-action@v1.0.0
  with:
    host: ${{ secrets.SERVER_HOST }}
    username: ${{ secrets.SERVER_USER }}
    key: ${{ secrets.SSH_PRIVATE_KEY }}
    script: |
      cd /opt/edu-na-bazar
      docker-compose exec -T backend alembic upgrade head
```

### Вариант 2: Ручной

```bash
# На сервере
cd /opt/edu-na-bazar
docker-compose exec -T backend alembic upgrade head
```

---

## 🔧 Настройка для новой БД

### 1. Создать пустую БД
```bash
docker-compose exec postgres createdb -U postgres edu_na_bazar_new
```

### 2. Применить все миграции
```bash
# Изменить DATABASE_URL в .env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/edu_na_bazar_new

# Применить миграции
docker-compose exec -T backend alembic upgrade head
```

### 3. Загрузить данные (если нужно)
```bash
docker-compose exec -T postgres psql -U postgres edu_na_bazar_new < backup.sql
```

---

## ⚠️ Важные замечания

### 1. Всегда проверяйте автогенерированные миграции
Alembic может не всегда корректно определить изменения. Проверяйте:
- Правильность типов данных
- Наличие NOT NULL constraints
- Foreign keys
- Индексы

### 2. Тестируйте миграции локально
```bash
# Применить
alembic upgrade head

# Откатить
alembic downgrade -1

# Снова применить
alembic upgrade head
```

### 3. Backup перед миграцией в production
```bash
# Создать backup
docker-compose exec postgres pg_dump -U postgres edu_na_bazar > backup_before_migration.sql
```

### 4. Используйте транзакции
Alembic автоматически использует транзакции, но для сложных миграций можно отключить:
```python
def upgrade():
    # Отключить транзакцию для этой миграции
    op.execute("SET statement_timeout = 0")
```

---

## 🐛 Troubleshooting

### Ошибка: "relation already exists"
```bash
# Пометить текущее состояние БД
docker-compose exec -T backend alembic stamp head
```

### Ошибка: "Can't locate revision"
```bash
# Проверить историю
docker-compose exec -T backend alembic history

# Пересоздать alembic_version таблицу
docker-compose exec postgres psql -U postgres edu_na_bazar -c "DROP TABLE IF EXISTS alembic_version;"
docker-compose exec -T backend alembic stamp head
```

### Миграция зависла
```bash
# Проверить логи
docker-compose logs backend

# Откатить транзакцию в PostgreSQL
docker-compose exec postgres psql -U postgres edu_na_bazar -c "SELECT pg_cancel_backend(pid) FROM pg_stat_activity WHERE state = 'active';"
```

---

## 📚 Полезные ссылки

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## ✅ Checklist для production

- [x] Initial migration создана
- [x] Текущая БД помечена (stamp head)
- [x] psycopg2-binary установлен
- [ ] Миграции добавлены в CI/CD pipeline
- [ ] Backup стратегия настроена
- [ ] Rollback процедура документирована
- [ ] Тестирование миграций на staging

---

**Создано**: 25.11.2025  
**Текущая версия**: `8828a8665651` (Initial schema)  
**Статус**: ✅ Готово к использованию
