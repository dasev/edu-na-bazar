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
ARG REACT_APP_API_URL=http://localhost:8000
ARG REACT_APP_MAPBOX_TOKEN
ENV REACT_APP_API_URL=$REACT_APP_API_URL
ENV REACT_APP_MAPBOX_TOKEN=$REACT_APP_MAPBOX_TOKEN

# Build production
RUN npm run build

# Stage 2: Production
FROM nginx:alpine

# Установка curl для health check
RUN apk add --no-cache curl

# Копирование build
COPY --from=builder /app/build /usr/share/nginx/html

# Nginx конфигурация
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Порт
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Запуск nginx
CMD ["nginx", "-g", "daemon off;"]
