# Установка MySQL 5.7 для миграции данных

## Шаг 1: Скачать MySQL 5.7

1. Перейдите на: https://downloads.mysql.com/archives/community/
2. Выберите:
   - Product Version: **5.7.44** (последняя 5.7)
   - Operating System: **Microsoft Windows**
   - OS Version: **Windows (x86, 64-bit), ZIP Archive**
3. Скачайте файл: `mysql-5.7.44-winx64.zip`

## Шаг 2: Установка

```powershell
# Создайте папку
mkdir C:\mysql57

# Распакуйте архив в C:\mysql57
# Должна получиться структура: C:\mysql57\bin, C:\mysql57\lib и т.д.
```

## Шаг 3: Инициализация

```powershell
# Откройте PowerShell от имени администратора
cd C:\mysql57\bin

# Инициализация (создаст временный пароль)
.\mysqld.exe --initialize-insecure --datadir=C:\python\sites_mysql --console
```

## Шаг 4: Запуск MySQL 5.7

```powershell
# В отдельном окне PowerShell
cd C:\mysql57\bin
.\mysqld.exe --datadir=C:\python\sites_mysql --console
```

## Шаг 5: Проверка подключения

```powershell
# В новом окне PowerShell
cd C:\mysql57\bin
.\mysql.exe -u root

# В MySQL консоли:
USE enb;
SHOW TABLES;
SELECT COUNT(*) FROM user;
SELECT COUNT(*) FROM companies;
SELECT COUNT(*) FROM advert;
```

## Шаг 6: Создание дампа

```powershell
cd C:\mysql57\bin
.\mysqldump.exe -u root --skip-lock-tables --complete-insert enb user companies advert categories file review messages city region > C:\python\edu-na-bazar\enb_full_dump.sql
```

## Шаг 7: Запуск миграции

```powershell
cd C:\python\edu-na-bazar\backend\scripts

# Обновите порт в migrate_data.py если нужно (MySQL 5.7 по умолчанию 3306)
python migrate_data.py
```

## Альтернатива: Portable MySQL 5.7

Если не хотите устанавливать, можно использовать portable версию:

1. Скачайте XAMPP 7.4.x (содержит MySQL 5.7)
2. Или используйте USBWebserver с MySQL 5.7

## Проблемы и решения

### Проблема: "Can't connect to MySQL server"
**Решение:** Убедитесь что MySQL 5.7 запущен и слушает порт 3306

### Проблема: "Access denied for user 'root'"
**Решение:** 
```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';
FLUSH PRIVILEGES;
```

### Проблема: MariaDB 12.1 занимает порт 3306
**Решение:** Остановите MariaDB:
```powershell
net stop MariaDB
```

Или запустите MySQL 5.7 на другом порту:
```powershell
.\mysqld.exe --datadir=C:\python\sites_mysql --port=3307 --console
```

И обновите порт в `migrate_data.py`:
```python
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3307,  # Добавьте эту строку
    'user': 'root',
    'password': 'root',
    'database': 'enb',
}
```
