#!/bin/bash
# ============================================
# Скрипт запуска SolarappScreener / SonarQube Scanner (Linux/Mac)
# ============================================

set -e

echo ""
echo "============================================"
echo "  SolarappScreener - Анализ безопасности"
echo "============================================"
echo ""

# Проверка наличия sonar-scanner
if ! command -v sonar-scanner &> /dev/null; then
    echo "[ОШИБКА] sonar-scanner не найден!"
    echo ""
    echo "Установите SonarQube Scanner:"
    echo "  Ubuntu/Debian: sudo apt-get install sonar-scanner"
    echo "  macOS: brew install sonar-scanner"
    echo "  Или скачайте: https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/"
    echo ""
    exit 1
fi

# Проверка наличия sonar-project.properties
if [ ! -f "sonar-project.properties" ]; then
    echo "[ОШИБКА] Файл sonar-project.properties не найден!"
    echo "Создайте файл с конфигурацией проекта."
    exit 1
fi

echo "[1/4] Проверка конфигурации..."
echo "  ✓ sonar-project.properties: OK"
echo "  ✓ sonar-scanner: OK"
echo ""

echo "[2/4] Очистка предыдущих результатов..."
rm -rf .scannerwork
echo "  ✓ .scannerwork удалён"
echo ""

echo "[3/4] Запуск анализа..."
echo ""
echo "============================================"

# Запуск сканера
sonar-scanner \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login="${SONAR_TOKEN}"

echo ""
echo "============================================"
echo "[4/4] Анализ завершён успешно!"
echo "============================================"
echo ""
echo "Результаты доступны:"
echo "  - Локально: http://localhost:9000/dashboard?id=edu-na-bazar"
echo "  - Отчёт: .scannerwork/report-task.txt"
echo ""
echo "Следующие шаги:"
echo "1. Откройте дашборд SonarQube"
echo "2. Проверьте найденные проблемы"
echo "3. Исправьте критические уязвимости"
echo ""
