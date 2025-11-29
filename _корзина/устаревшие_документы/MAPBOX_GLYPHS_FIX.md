# 🗺️ Исправление ошибки Mapbox Glyphs

## ❌ Проблема

```
Error: layers.cluster-count.layout.text-field: 
use of "text-field" requires a style "glyphs" property
```

## 🔍 Причина

При использовании кастомного стиля Mapbox (не стандартного `mapbox://styles/...`), необходимо **явно указать URL для загрузки шрифтов (glyphs)**.

Mapbox использует шрифты для отображения текста на карте (например, количество товаров в кластере).

## ✅ Решение

### 1. Добавить `glyphs` в стиль карты

```typescript
const mapInstance = new mapboxgl.Map({
  container: mapContainer.current,
  style: {
    version: 8,
    // ✅ Добавляем glyphs для поддержки текста
    glyphs: 'https://fonts.openmaptiles.org/{fontstack}/{range}.pbf',
    sources: { ... },
    layers: [ ... ]
  }
})
```

### 2. Использовать доступные шрифты

Изменить шрифт в `text-font` на тот, который доступен в OpenMapTiles:

```typescript
layout: {
  'text-field': '{point_count_abbreviated}',
  // ✅ Open Sans Bold доступен в OpenMapTiles
  'text-font': ['Open Sans Bold', 'Arial Unicode MS Bold'],
  'text-size': 14
}
```

## 📚 Доступные источники шрифтов

### OpenMapTiles (бесплатно)
```
https://fonts.openmaptiles.org/{fontstack}/{range}.pbf
```

**Доступные шрифты:**
- Open Sans Regular
- Open Sans Bold
- Open Sans Italic
- Noto Sans Regular
- Noto Sans Bold
- Klokantech Noto Sans Regular
- Klokantech Noto Sans Bold

### Mapbox (требует токен)
```
https://api.mapbox.com/fonts/v1/mapbox/{fontstack}/{range}.pbf?access_token={token}
```

**Доступные шрифты:**
- DIN Offc Pro Regular
- DIN Offc Pro Medium
- DIN Offc Pro Bold
- Arial Unicode MS Regular
- Arial Unicode MS Bold

## 🎯 Рекомендации

1. **Для production:** используйте OpenMapTiles (бесплатно, без токена)
2. **Для Mapbox стилей:** используйте стандартные стили `mapbox://styles/mapbox/streets-v12`
3. **Для кастомных стилей:** всегда добавляйте `glyphs` URL

## 🐛 Troubleshooting

### Ошибка: "Font stack not found"

Проверьте, что шрифт доступен в выбранном источнике:
```typescript
// ❌ Не работает с OpenMapTiles
'text-font': ['DIN Offc Pro Medium']

// ✅ Работает с OpenMapTiles
'text-font': ['Open Sans Bold']
```

### Ошибка: "Failed to load glyphs"

Проверьте доступность URL:
```bash
# Проверить в браузере
https://fonts.openmaptiles.org/Open%20Sans%20Bold/0-255.pbf
```

## 📝 Изменения в коде

**Файл:** `frontend/src/pages/Map/MapPage.tsx`

**Строки 47-48:** Добавлен `glyphs` URL
```typescript
glyphs: 'https://fonts.openmaptiles.org/{fontstack}/{range}.pbf',
```

**Строка 181:** Изменен шрифт
```typescript
'text-font': ['Open Sans Bold', 'Arial Unicode MS Bold'],
```

---

**Исправлено:** 27.11.2025  
**Проект:** Еду на базар
