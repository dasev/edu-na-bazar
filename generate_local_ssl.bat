@echo off
REM Генерация self-signed SSL сертификата для локальной разработки

echo ========================================
echo Генерация SSL сертификата для localhost
echo ========================================
echo.

REM Создать папку для сертификатов
if not exist "ssl" mkdir ssl

REM Генерация приватного ключа и сертификата
openssl req -x509 -nodes -days 365 -newkey rsa:2048 ^
  -keyout ssl/localhost.key ^
  -out ssl/localhost.crt ^
  -subj "/C=RU/ST=Moscow/L=Moscow/O=Dev/CN=localhost"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo ✅ SSL сертификат создан успешно!
    echo ========================================
    echo.
    echo Файлы:
    echo   - ssl/localhost.key  (приватный ключ)
    echo   - ssl/localhost.crt  (сертификат)
    echo.
    echo Следующий шаг:
    echo   1. Перезапустить контейнеры с SSL конфигурацией
    echo   2. docker-compose -f docker-compose.ssl.yml up -d
    echo.
) else (
    echo.
    echo ❌ Ошибка! OpenSSL не найден.
    echo.
    echo Установите OpenSSL:
    echo   - Скачать: https://slproweb.com/products/Win32OpenSSL.html
    echo   - Или через Chocolatey: choco install openssl
    echo.
)

pause
