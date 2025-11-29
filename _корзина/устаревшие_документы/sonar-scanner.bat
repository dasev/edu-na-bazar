@echo off
REM ============================================
REM Скрипт запуска SolarappScreener / SonarQube Scanner
REM ============================================

echo.
echo ============================================
echo   SolarappScreener (RTK) - Анализ безопасности
echo   Совместим также с SonarQube
echo ============================================
echo.

REM Проверка наличия sonar-scanner
where sonar-scanner >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ОШИБКА] sonar-scanner не найден!
    echo.
    echo Установите SonarQube Scanner:
    echo 1. Скачайте: https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/
    echo 2. Распакуйте в C:\sonar-scanner
    echo 3. Добавьте в PATH: C:\sonar-scanner\bin
    echo.
    pause
    exit /b 1
)

REM Проверка наличия sonar-project.properties
if not exist "sonar-project.properties" (
    echo [ОШИБКА] Файл sonar-project.properties не найден!
    echo Создайте файл с конфигурацией проекта.
    pause
    exit /b 1
)

echo [1/4] Проверка конфигурации...
echo   - sonar-project.properties: OK
echo   - sonar-scanner: OK
echo.

echo [2/4] Очистка предыдущих результатов...
if exist ".scannerwork" rmdir /s /q .scannerwork
echo   - .scannerwork удалён
echo.

echo [3/4] Запуск анализа...
echo.
echo ============================================

REM Запуск сканера
REM Для SolarappScreener используйте URL вашего сервера РТК
REM Для локального SonarQube: http://localhost:9000
sonar-scanner.bat ^
  -Dsonar.host.url=%SONAR_HOST_URL% ^
  -Dsonar.login=%SONAR_TOKEN%

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ============================================
    echo [ОШИБКА] Анализ завершился с ошибкой!
    echo ============================================
    echo.
    echo Возможные причины:
    echo 1. SonarQube сервер не запущен (http://localhost:9000)
    echo 2. Неверный SONAR_TOKEN
    echo 3. Ошибки в sonar-project.properties
    echo.
    echo Проверьте логи выше для деталей.
    pause
    exit /b 1
)

echo.
echo ============================================
echo [4/4] Анализ завершён успешно!
echo ============================================
echo.
echo Результаты доступны:
echo   - Локально: http://localhost:9000/dashboard?id=edu-na-bazar
echo   - Отчёт: .scannerwork/report-task.txt
echo.
echo Следующие шаги:
echo 1. Откройте дашборд SonarQube
echo 2. Проверьте найденные проблемы
echo 3. Исправьте критические уязвимости
echo.

pause
