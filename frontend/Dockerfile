# Frontend Dockerfile - Multi-stage build

# Stage 1: Builder
FROM node:18-alpine AS builder

WORKDIR /app

# Копирование package files
COPY package*.json ./

# Установка зависимостей
RUN npm ci --silent

# Копирование исходников
COPY . .

# Build аргументы
ARG VITE_API_URL=http://localhost:8000
ARG VITE_MAPBOX_TOKEN
ENV VITE_API_URL=$VITE_API_URL
ENV VITE_MAPBOX_TOKEN=$VITE_MAPBOX_TOKEN

# Build production
RUN npm run build

# Stage 2: Production
FROM nginx:alpine

# Установка curl для health check
RUN apk add --no-cache curl

# Копирование build (Vite использует dist, не build)
COPY --from=builder /app/dist /usr/share/nginx/html

# Nginx конфигурация
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Порт
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Запуск nginx
CMD ["nginx", "-g", "daemon off;"]
