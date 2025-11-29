@echo off
chcp 65001 > nul
echo ========================================
echo 📦 Создание архива с изображениями
echo ========================================
echo.

REM Проверка наличия папки uploads
if not exist "backend\uploads" (
    echo ❌ Папка backend\uploads не найдена!
    echo.
    pause
    exit /b 1
)

REM Подсчет файлов
echo 📊 Подсчет файлов...
for /f %%A in ('dir /s /b backend\uploads\*.jpg backend\uploads\*.png 2^>nul ^| find /c /v ""') do set FILE_COUNT=%%A
echo    Найдено изображений: %FILE_COUNT%
echo.

REM Создание архива
echo 📦 Создание архива uploads.zip...
echo.

powershell -Command "Compress-Archive -Path 'backend\uploads\*' -DestinationPath 'uploads.zip' -Force"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo ✅ Архив успешно создан!
    echo ========================================
    echo.
    
    REM Показать размер архива
    for %%A in (uploads.zip) do (
        set SIZE=%%~zA
        set /a SIZE_MB=%%~zA/1024/1024
    )
    
    echo 📦 Файл: uploads.zip
    echo 📊 Размер: !SIZE_MB! MB
    echo 📁 Файлов: %FILE_COUNT%
    echo.
    echo 🚀 Следующие шаги:
    echo    1. Загрузите uploads.zip на сервер
    echo    2. Следуйте инструкциям в UPLOAD_IMAGES_GUIDE.md
    echo.
    
) else (
    echo.
    echo ❌ Ошибка при создании архива!
    echo.
)

pause
