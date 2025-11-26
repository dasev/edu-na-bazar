#!/bin/bash

###############################################################################
# Скрипт для исправления конфликта Git и обновления кода
###############################################################################

set -e

# Цвета
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Исправление конфликта Git${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

cd /opt/edu-na-bazar

print_info "Проверяем текущий статус..."
git status

echo ""
print_warning "Сохраняем локальные изменения..."
git stash save "Локальные изменения перед обновлением SSL"

print_success "Изменения сохранены в stash"

echo ""
print_info "Обновляем код из Git..."
git pull origin main

print_success "Код обновлен!"

echo ""
print_info "Проверяем что скрипт загружен..."
if [ -f "setup_ssl_prod.sh" ]; then
    print_success "setup_ssl_prod.sh найден"
    chmod +x setup_ssl_prod.sh
    print_success "Права установлены"
else
    print_warning "setup_ssl_prod.sh не найден"
    exit 1
fi

echo ""
print_info "Список файлов в stash (можно восстановить позже):"
git stash list

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ Готово! Теперь можно запустить:${NC}"
echo -e "${GREEN}  bash setup_ssl_prod.sh${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo ""
echo "💡 Чтобы восстановить локальные изменения позже:"
echo "   git stash pop"
echo ""
