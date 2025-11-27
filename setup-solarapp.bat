@echo off
REM ============================================
REM Быстрая настройка SolarappScreener (РТК)
REM ============================================

echo.
echo ============================================
echo   Настройка SolarappScreener
echo ============================================
echo.

echo Выберите вариант:
echo.
echo 1. SolarappScreener (облачный сервер РТК)
echo 2. SonarQube (локальный для разработки)
echo.
set /p choice="Ваш выбор (1 или 2): "

if "%choice%"=="1" goto SOLARAPP
if "%choice%"=="2" goto SONARQUBE

echo Неверный выбор!
pause
exit /b 1

:SOLARAPP
echo.
echo ============================================
echo   Настройка SolarappScreener (РТК)
echo ============================================
echo.
set /p host="Введите URL сервера РТК (например, https://solar.rtk.ru): "
set /p token="Введите токен доступа: "

setx SONAR_HOST_URL "%host%"
setx SONAR_TOKEN "%token%"

echo.
echo ✅ Настройки сохранены!
echo.
echo Переменные окружения:
echo   SONAR_HOST_URL = %host%
echo   SONAR_TOKEN = %token%
echo.
echo ВАЖНО: Перезапустите командную строку для применения изменений!
echo.
goto END

:SONARQUBE
echo.
echo ============================================
echo   Настройка локального SonarQube
echo ============================================
echo.
echo Запускаем SonarQube в Docker...

docker ps | findstr sonarqube >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ SonarQube уже запущен
) else (
    echo Запуск контейнера SonarQube...
    docker run -d --name sonarqube -p 9000:9000 sonarqube:latest
    
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo ❌ Ошибка запуска Docker!
        echo.
        echo Убедитесь что Docker Desktop установлен и запущен.
        pause
        exit /b 1
    )
    
    echo.
    echo ⏳ Ожидание запуска SonarQube (это может занять 1-2 минуты)...
    timeout /t 60 /nobreak
)

setx SONAR_HOST_URL "http://localhost:9000"
setx SONAR_TOKEN "admin"

echo.
echo ✅ Настройки сохранены!
echo.
echo Переменные окружения:
echo   SONAR_HOST_URL = http://localhost:9000
echo   SONAR_TOKEN = admin
echo.
echo Следующие шаги:
echo 1. Откройте браузер: http://localhost:9000
echo 2. Войдите: admin / admin
echo 3. Смените пароль при первом входе
echo 4. Создайте токен: My Account → Security → Generate Token
echo 5. Обновите переменную: set SONAR_TOKEN=новый-токен
echo.
echo ВАЖНО: Перезапустите командную строку для применения изменений!
echo.

:END
echo Готово! Теперь можете запустить: sonar-scanner.bat
echo.
pause
