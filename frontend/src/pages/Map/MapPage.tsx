/**
 * Страница с картой магазинов
 */
import { useEffect, useRef, useState } from 'react'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import './MapPage.css'
import axios from 'axios'
import { useCartStore } from '../../store/cartStore'
import { showToast } from '../../utils/toast'
import { useFiltersStore } from '../../store/filtersStore'
import FilterPanel from '../../components/FilterPanel/FilterPanel'

// Токен Mapbox
mapboxgl.accessToken = 'pk.eyJ1Ijoic2VyZ2VqZGFuNDUyIiwiYSI6ImNtaTd0dzQ4ajA0bHkyanIyNWJwa2JrNXYifQ.AWJBOIEEXVb-6AIKrbRXmw'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function MapPage() {
  const mapContainer = useRef<HTMLDivElement>(null)
  const map = useRef<mapboxgl.Map | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isFiltersOpen, setIsFiltersOpen] = useState(false)
  const { addToCart } = useCartStore()
  const filters = useFiltersStore()

  // Закрытие фильтров по клавише Escape
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isFiltersOpen) {
        setIsFiltersOpen(false)
      }
    }
    
    window.addEventListener('keydown', handleEscape)
    return () => window.removeEventListener('keydown', handleEscape)
  }, [isFiltersOpen])

  useEffect(() => {
    // Если карта уже создана, не создаем заново
    if (map.current) return

    // Проверяем наличие контейнера
    if (!mapContainer.current) {
      console.error('Контейнер карты не найден')
      return
    }

    console.log('🗺️ Инициализация карты Mapbox...')
    console.log('📦 Контейнер:', mapContainer.current)
    console.log('📏 Размеры:', mapContainer.current.offsetWidth, 'x', mapContainer.current.offsetHeight)

    try {
      // Создаем карту с Google Maps подложкой
      const mapInstance = new mapboxgl.Map({
        container: mapContainer.current,
        style: {
          version: 8,
          // Добавляем glyphs для поддержки текста
          glyphs: 'https://fonts.openmaptiles.org/{fontstack}/{range}.pbf',
          sources: {
            'google-tiles': {
              type: 'raster',
              tiles: [
                'https://mt0.google.com/maps/vt?lyrs=m@189&gl=cn&x={x}&y={y}&z={z}',
                'https://mt1.google.com/maps/vt?lyrs=m@189&gl=cn&x={x}&y={y}&z={z}',
                'https://mt2.google.com/maps/vt?lyrs=m@189&gl=cn&x={x}&y={y}&z={z}',
                'https://mt3.google.com/maps/vt?lyrs=m@189&gl=cn&x={x}&y={y}&z={z}'
              ],
              tileSize: 256,
              attribution: '© Google Maps'
            }
          },
          layers: [
            {
              id: 'google-tiles-layer',
              type: 'raster',
              source: 'google-tiles',
              minzoom: 0,
              maxzoom: 22
            }
          ]
        },
        center: [37.6173, 55.7558], // Москва
        zoom: 10,
        attributionControl: true
      })

      map.current = mapInstance
      console.log('✅ Карта создана')

      // Обработка ошибок
      mapInstance.on('error', (e) => {
        console.error('❌ Ошибка карты:', e)
        setError('Ошибка загрузки карты')
        setIsLoading(false)
      })

      // Когда карта загружена
      mapInstance.on('load', async () => {
        console.log('✅ Карта загружена')
        setIsLoading(false)

        // Добавляем контролы навигации
        mapInstance.addControl(new mapboxgl.NavigationControl(), 'top-right')
        mapInstance.addControl(new mapboxgl.FullscreenControl(), 'top-right')
        console.log('✅ Контролы добавлены')

        // Проверяем, нужно ли позиционироваться на конкретный товар
        const focusProductData = localStorage.getItem('mapFocusProduct')
        if (focusProductData) {
          try {
            const { lat, lng, id } = JSON.parse(focusProductData)
            console.log('📍 Позиционирование на товар:', id)
            
            // Позиционируем карту на товар (НЕ удаляем данные из localStorage пока)
            mapInstance.flyTo({
              center: [lng, lat],
              zoom: 14,
              duration: 2000
            })
          } catch (error) {
            console.error('Ошибка позиционирования:', error)
          }
        }

        try {
          // Загружаем товары с сервера с учетом фильтров
          console.log('📦 Загрузка товаров с геолокацией...')
          
          // Формируем параметры запроса из фильтров
          const params = new URLSearchParams()
          if (filters.category_id) params.append('category_id', filters.category_id.toString())
          if (filters.store_id) params.append('store_id', filters.store_id.toString())
          if (filters.min_price !== undefined) params.append('min_price', filters.min_price.toString())
          if (filters.max_price !== undefined) params.append('max_price', filters.max_price.toString())
          if (filters.min_rating !== undefined) params.append('min_rating', filters.min_rating.toString())
          if (filters.in_stock !== undefined) params.append('in_stock', filters.in_stock.toString())
          params.append('limit', '5000') // Загружаем больше товаров для карты
          
          const response = await axios.get(`${API_URL}/api/products/map/geojson?${params.toString()}`)
          const geojson = response.data
          
          console.log('✅ Загружено товаров:', geojson.features.length)

          // Добавляем источник данных GeoJSON с кластеризацией
          mapInstance.addSource('products', {
            type: 'geojson',
            data: geojson,
            cluster: true,
            clusterMaxZoom: 14, // Максимальный зум для кластеризации
            clusterRadius: 50 // Радиус кластеризации в пикселях
          })

          // Слой для кластеров (группы товаров)
          mapInstance.addLayer({
            id: 'clusters',
            type: 'circle',
            source: 'products',
            filter: ['has', 'point_count'],
            paint: {
              'circle-color': [
                'step',
                ['get', 'point_count'],
                '#667eea', // 1-10 товаров
                10,
                '#764ba2', // 10-30 товаров
                30,
                '#9b59b6'  // 30+ товаров
              ],
              'circle-radius': [
                'step',
                ['get', 'point_count'],
                20, // 1-10 товаров
                10,
                25, // 10-30 товаров
                30,
                30  // 30+ товаров
              ],
              'circle-stroke-width': 3,
              'circle-stroke-color': '#ffffff'
            }
          })

          // Слой с количеством товаров в кластере
          mapInstance.addLayer({
            id: 'cluster-count',
            type: 'symbol',
            source: 'products',
            filter: ['has', 'point_count'],
            layout: {
              'text-field': '{point_count_abbreviated}',
              'text-font': ['Open Sans Bold', 'Arial Unicode MS Bold'],
              'text-size': 14
            },
            paint: {
              'text-color': '#ffffff'
            }
          })

          // Слой для отдельных товаров (не в кластере)
          mapInstance.addLayer({
            id: 'products-layer',
            type: 'circle',
            source: 'products',
            filter: ['!', ['has', 'point_count']],
            paint: {
              'circle-radius': 20,
              'circle-color': '#667eea',
              'circle-stroke-width': 3,
              'circle-stroke-color': '#ffffff',
              'circle-opacity': 1
            }
          })

          // Слой для выделенного товара (темнее)
          mapInstance.addLayer({
            id: 'products-selected',
            type: 'circle',
            source: 'products',
            filter: ['==', ['get', 'id'], -1], // Изначально ничего не выделено
            paint: {
              'circle-radius': 22,
              'circle-color': '#4a5fc1', // Темнее основного цвета
              'circle-stroke-width': 4,
              'circle-stroke-color': '#ffffff',
              'circle-opacity': 1
            }
          })

          // Храним маркеры с иконками для обновления при зуме
          const iconMarkers: mapboxgl.Marker[] = []
          
          // Функция для обновления иконок
          const updateIcons = () => {
            // Удаляем старые маркеры
            iconMarkers.forEach(marker => marker.remove())
            iconMarkers.length = 0
            
            // Получаем видимые некластеризованные точки
            const features = mapInstance.querySourceFeatures('products', {
              sourceLayer: undefined
            })
            
            features.forEach((feature: any) => {
              // Пропускаем кластеры
              if (feature.properties.cluster) return
              
              const props = feature.properties
              const coords = feature.geometry.coordinates
              
              // Создаем элемент с эмодзи
              const el = document.createElement('div')
              el.className = 'product-icon-marker'
              el.style.cssText = `
                font-size: 22px;
                pointer-events: none;
                user-select: none;
              `
              el.textContent = props.category_icon
              
              // Добавляем маркер
              const marker = new mapboxgl.Marker({
                element: el,
                anchor: 'center'
              })
                .setLngLat(coords)
                .addTo(mapInstance)
              
              iconMarkers.push(marker)
            })
          }
          
          // Обновляем иконки при изменении зума или перемещении
          mapInstance.on('render', updateIcons)
          updateIcons() // Первоначальное добавление

          // Клик на кластер - увеличиваем зум
          mapInstance.on('click', 'clusters', (e) => {
            const features = mapInstance.queryRenderedFeatures(e.point, {
              layers: ['clusters']
            })
            
            if (features.length === 0) return
            
            const clusterId = features[0].properties?.cluster_id
            const source = mapInstance.getSource('products') as mapboxgl.GeoJSONSource
            
            source.getClusterExpansionZoom(clusterId, (err, zoom) => {
              if (err || !zoom) return
              
              mapInstance.easeTo({
                center: (features[0].geometry as any).coordinates,
                zoom: zoom
              })
            })
          })

          // Меняем курсор при наведении на кластеры
          mapInstance.on('mouseenter', 'clusters', () => {
            mapInstance.getCanvas().style.cursor = 'pointer'
          })
          mapInstance.on('mouseleave', 'clusters', () => {
            mapInstance.getCanvas().style.cursor = ''
          })

          // Меняем курсор при наведении на товары
          mapInstance.on('mouseenter', 'products-layer', () => {
            mapInstance.getCanvas().style.cursor = 'pointer'
          })
          mapInstance.on('mouseleave', 'products-layer', () => {
            mapInstance.getCanvas().style.cursor = ''
          })

          // Переменная для хранения текущего popup
          let currentPopup: mapboxgl.Popup | null = null

          // Обработчик клика на маркер
          mapInstance.on('click', 'products-layer', (e) => {
            if (!e.features || e.features.length === 0) return
            
            const feature = e.features[0]
            const props = feature.properties as any
            const coordinates = (feature.geometry as any).coordinates.slice()

            // Закрываем предыдущий popup если есть
            if (currentPopup) {
              currentPopup.remove()
            }

            // Выделяем выбранный товар
            mapInstance.setFilter('products-selected', ['==', ['get', 'id'], props.id])

            // Получаем все изображения товара
            const images = props.images ? JSON.parse(props.images) : (props.image ? [props.image] : [])
            const hasMultipleImages = images.length > 1
            
            // Создаем HTML для popup с галереей
            const popupHTML = `
              <div class="map-popup-product" style="min-width: 250px; max-width: 300px;">
                ${images.length > 0 ? `
                  <div 
                    class="popup-image-container" 
                    data-images='${JSON.stringify(images)}'
                    data-product-id="${props.id}"
                    style="position: relative; width: 100%; height: 150px; border-radius: 12px; overflow: hidden; margin-bottom: 12px; cursor: zoom-in;"
                  >
                    <img 
                      src="${API_URL}${images[0]}" 
                      class="popup-main-image"
                      style="width: 100%; height: 100%; object-fit: cover;" 
                    />
                    ${hasMultipleImages ? `
                      <div class="popup-image-counter" style="position: absolute; top: 8px; right: 8px; background: rgba(0,0,0,0.6); color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; pointer-events: none;">
                        <span class="current-image">1</span>/${images.length}
                      </div>
                      <div class="popup-image-dots" style="position: absolute; bottom: 8px; left: 50%; transform: translateX(-50%); display: flex; gap: 4px; z-index: 10; pointer-events: none;">
                        ${images.map((_: string, idx: number) => `
                          <div class="popup-dot ${idx === 0 ? 'active' : ''}" style="width: 6px; height: 6px; border-radius: 50%; background: ${idx === 0 ? 'white' : 'rgba(255,255,255,0.5)'}; box-shadow: 0 1px 3px rgba(0,0,0,0.3); transition: all 0.2s;"></div>
                        `).join('')}
                      </div>
                    ` : ''}
                  </div>
                ` : ''}
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                  <div style="font-size: 24px;">${props.category_icon}</div>
                  <div style="flex: 1;">
                    <a href="/product/${props.id}" style="text-decoration: none; color: inherit;">
                      <h3 style="margin: 0; font-size: 15px; font-weight: 600; color: #333; line-height: 1.3; cursor: pointer; transition: color 0.2s;" onmouseover="this.style.color='#667eea'" onmouseout="this.style.color='#333'">${props.name}</h3>
                    </a>
                  </div>
                </div>
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                  <div style="color: #667eea; font-weight: 700; font-size: 20px;">${props.price} ₽</div>
                  ${props.rating > 0 ? `<div style="font-size: 13px; color: #ffa500;">⭐ ${props.rating.toFixed(1)}</div>` : ''}
                </div>
                <div style="font-size: 12px; color: #888; margin-bottom: 12px; padding: 4px 8px; background: #f5f5f5; border-radius: 6px; display: inline-block;">${props.category_name || 'Без категории'}</div>
                <button 
                  class="add-to-cart-btn" 
                  data-product-id="${props.id}"
                  style="width: 100%; padding: 12px 16px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; transition: transform 0.2s; display: flex; align-items: center; justify-content: center; gap: 8px;" 
                  onmouseover="this.style.transform='translateY(-2px)'" 
                  onmouseout="this.style.transform='translateY(0)'"
                >
                  <span style="font-size: 18px;">🛒</span> В корзину
                </button>
              </div>
            `

            // Создаем и показываем popup
            currentPopup = new mapboxgl.Popup({ 
              offset: 25,
              maxWidth: '320px',
              closeButton: true,
              closeOnClick: false,
              className: 'custom-popup'
            })
              .setLngLat(coordinates)
              .setHTML(popupHTML)
              .addTo(mapInstance)
            
            // При закрытии popup сбрасываем выделение
            currentPopup.on('close', () => {
              mapInstance.setFilter('products-selected', ['==', ['get', 'id'], -1])
              currentPopup = null
            })
            
            // Добавляем обработчики для popup после небольшой задержки
            setTimeout(() => {
              const container = document.querySelector('.popup-image-container') as HTMLElement
              const addToCartBtn = document.querySelector('.add-to-cart-btn') as HTMLButtonElement
              
              // Обработчик клика по изображению - открыть модальное окно
              if (container) {
                const img = container.querySelector('.popup-main-image') as HTMLImageElement
                
                container.addEventListener('click', (e) => {
                  e.stopPropagation()
                  
                  // Создаем модальное окно
                  const modal = document.createElement('div')
                  modal.className = 'image-modal'
                  modal.style.cssText = `
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: rgba(0, 0, 0, 0.9);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 10000;
                    cursor: zoom-out;
                  `
                  
                  const modalContent = document.createElement('div')
                  modalContent.style.cssText = `
                    position: relative;
                    max-width: 90vw;
                    max-height: 90vh;
                  `
                  
                  const modalImg = document.createElement('img')
                  modalImg.src = img.src
                  modalImg.style.cssText = `
                    max-width: 100%;
                    max-height: 90vh;
                    object-fit: contain;
                    border-radius: 8px;
                  `
                  
                  const closeBtn = document.createElement('button')
                  closeBtn.textContent = '✕'
                  closeBtn.style.cssText = `
                    position: absolute;
                    top: -40px;
                    right: 0;
                    background: rgba(255, 255, 255, 0.9);
                    border: none;
                    width: 36px;
                    height: 36px;
                    border-radius: 50%;
                    font-size: 20px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: all 0.2s;
                  `
                  
                  closeBtn.addEventListener('mouseenter', () => {
                    closeBtn.style.background = 'white'
                    closeBtn.style.transform = 'scale(1.1)'
                  })
                  closeBtn.addEventListener('mouseleave', () => {
                    closeBtn.style.background = 'rgba(255, 255, 255, 0.9)'
                    closeBtn.style.transform = 'scale(1)'
                  })
                  
                  const closeModal = () => {
                    modal.remove()
                  }
                  
                  closeBtn.addEventListener('click', closeModal)
                  modal.addEventListener('click', closeModal)
                  modalContent.addEventListener('click', (e) => e.stopPropagation())
                  
                  modalContent.appendChild(closeBtn)
                  modalContent.appendChild(modalImg)
                  modal.appendChild(modalContent)
                  document.body.appendChild(modal)
                })
                
                // Галерея при движении мыши (только если несколько изображений)
                if (images.length > 1) {
                  const dots = container.querySelectorAll('.popup-dot')
                  const counter = container.querySelector('.current-image')
                  const imagesData = JSON.parse(container.dataset.images || '[]')
                  
                  let currentIndex = 0
                  
                  container.addEventListener('mousemove', (e) => {
                    const rect = container.getBoundingClientRect()
                    const x = e.clientX - rect.left
                    const segmentWidth = rect.width / imagesData.length
                    const newIndex = Math.min(Math.floor(x / segmentWidth), imagesData.length - 1)
                    
                    if (newIndex !== currentIndex) {
                      currentIndex = newIndex
                      
                      // Меняем изображение
                      img.src = `${API_URL}${imagesData[currentIndex]}`
                      
                      // Обновляем точки
                      dots.forEach((dot, idx) => {
                        const dotEl = dot as HTMLElement
                        if (idx === currentIndex) {
                          dotEl.style.background = 'white'
                          dotEl.classList.add('active')
                        } else {
                          dotEl.style.background = 'rgba(255,255,255,0.5)'
                          dotEl.classList.remove('active')
                        }
                      })
                      
                      // Обновляем счетчик
                      if (counter) {
                        counter.textContent = String(currentIndex + 1)
                      }
                    }
                  })
                  
                  // Сброс при выходе мыши
                  container.addEventListener('mouseleave', () => {
                    currentIndex = 0
                    img.src = `${API_URL}${imagesData[0]}`
                    dots.forEach((dot, idx) => {
                      const dotEl = dot as HTMLElement
                      if (idx === 0) {
                        dotEl.style.background = 'white'
                        dotEl.classList.add('active')
                      } else {
                        dotEl.style.background = 'rgba(255,255,255,0.5)'
                        dotEl.classList.remove('active')
                      }
                    })
                    if (counter) counter.textContent = '1'
                  })
                }
              }
              
              // Обработчик кнопки "В корзину"
              if (addToCartBtn) {
                addToCartBtn.addEventListener('click', async () => {
                  const productId = addToCartBtn.dataset.productId
                  
                  if (!productId) return
                  
                  try {
                    addToCartBtn.disabled = true
                    const originalHTML = addToCartBtn.innerHTML
                    addToCartBtn.innerHTML = '<span style="font-size: 18px;">⏳</span> Добавление...'
                    
                    // Формируем объект товара для гостевой корзины
                    const productData = {
                      id: parseInt(productId),
                      name: props.name,
                      price: props.price,
                      image: props.image,
                      category_id: props.category_id,
                      in_stock: props.in_stock
                    }
                    
                    // Используем addToCart из store (работает и для гостей, и для авторизованных)
                    await addToCart(productId, 1, productData)
                    
                    // Показываем успех
                    showToast.success(`${props.name} добавлен в корзину!`)
                    addToCartBtn.innerHTML = '<span style="font-size: 18px;">✅</span> Добавлено'
                    addToCartBtn.style.background = 'linear-gradient(135deg, #4caf50 0%, #45a049 100%)'
                    
                    // Возвращаем обратно через 1.5 секунды
                    setTimeout(() => {
                      addToCartBtn.innerHTML = originalHTML
                      addToCartBtn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                      addToCartBtn.disabled = false
                    }, 1500)
                  } catch (error) {
                    console.error('Ошибка добавления в корзину:', error)
                    showToast.error('Ошибка добавления в корзину')
                    // Просто возвращаем кнопку в исходное состояние
                    addToCartBtn.innerHTML = '<span style="font-size: 18px;">🛒</span> В корзину'
                    addToCartBtn.disabled = false
                  }
                })
              }
            }, 100) // Небольшая задержка для рендеринга DOM
          })

          console.log('✅ Маркеры товаров добавлены')
          
          // Если есть фокус на товар, открываем его popup
          const focusProductData2 = localStorage.getItem('mapFocusProduct')
          if (focusProductData2) {
            try {
              const { id } = JSON.parse(focusProductData2)
              
              // Ищем товар в загруженных данных
              const productFeature = geojson.features.find((f: any) => f.properties.id === id)
              if (productFeature) {
                const props = productFeature.properties
                const coordinates = productFeature.geometry.coordinates
                
                // Выделяем товар
                mapInstance.setFilter('products-selected', ['==', ['get', 'id'], id])
                
                // Создаем popup программно через небольшую задержку
                setTimeout(() => {
                  // Используем тот же код создания popup что и при клике
                  const images = props.images ? JSON.parse(props.images) : (props.image ? [props.image] : [])
                  const hasMultipleImages = images.length > 1
                  
                  const popupHTML = `
                    <div class="map-popup-product" style="min-width: 250px; max-width: 300px;">
                      ${images.length > 0 ? `
                        <div 
                          class="popup-image-container" 
                          data-images='${JSON.stringify(images)}'
                          data-product-id="${props.id}"
                          style="position: relative; width: 100%; height: 150px; border-radius: 12px; overflow: hidden; margin-bottom: 12px; cursor: zoom-in;"
                        >
                          <img 
                            src="${API_URL}${images[0]}" 
                            class="popup-main-image"
                            style="width: 100%; height: 100%; object-fit: cover;" 
                          />
                          ${hasMultipleImages ? `
                            <div class="popup-image-counter" style="position: absolute; top: 8px; right: 8px; background: rgba(0,0,0,0.6); color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; pointer-events: none;">
                              <span class="current-image">1</span>/${images.length}
                            </div>
                            <div class="popup-image-dots" style="position: absolute; bottom: 8px; left: 50%; transform: translateX(-50%); display: flex; gap: 4px; z-index: 10; pointer-events: none;">
                              ${images.map((_: string, idx: number) => `
                                <div class="popup-dot ${idx === 0 ? 'active' : ''}" style="width: 6px; height: 6px; border-radius: 50%; background: ${idx === 0 ? 'white' : 'rgba(255,255,255,0.5)'}; box-shadow: 0 1px 3px rgba(0,0,0,0.3); transition: all 0.2s;"></div>
                              `).join('')}
                            </div>
                          ` : ''}
                        </div>
                      ` : ''}
                      <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                        <div style="font-size: 24px;">${props.category_icon}</div>
                        <div style="flex: 1;">
                          <a href="/product/${props.id}" style="text-decoration: none; color: inherit;">
                            <h3 style="margin: 0; font-size: 15px; font-weight: 600; color: #333; line-height: 1.3; cursor: pointer; transition: color 0.2s;" onmouseover="this.style.color='#667eea'" onmouseout="this.style.color='#333'">${props.name}</h3>
                          </a>
                        </div>
                      </div>
                      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                        <div style="color: #667eea; font-weight: 700; font-size: 20px;">${props.price} ₽</div>
                        ${props.rating > 0 ? `<div style="font-size: 13px; color: #ffa500;">⭐ ${props.rating.toFixed(1)}</div>` : ''}
                      </div>
                      <div style="font-size: 12px; color: #888; margin-bottom: 12px; padding: 4px 8px; background: #f5f5f5; border-radius: 6px; display: inline-block;">${props.category_name || 'Без категории'}</div>
                      <button 
                        class="add-to-cart-btn" 
                        data-product-id="${props.id}"
                        style="width: 100%; padding: 12px 16px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; transition: transform 0.2s; display: flex; align-items: center; justify-content: center; gap: 8px;" 
                        onmouseover="this.style.transform='translateY(-2px)'" 
                        onmouseout="this.style.transform='translateY(0)'"
                      >
                        <span style="font-size: 18px;">🛒</span> В корзину
                      </button>
                    </div>
                  `
                  
                  new mapboxgl.Popup({ 
                    offset: 25,
                    maxWidth: '320px',
                    closeButton: true,
                    closeOnClick: false,
                    className: 'custom-popup'
                  })
                    .setLngLat(coordinates)
                    .setHTML(popupHTML)
                    .addTo(mapInstance)
                  
                  // Добавляем обработчики для popup
                  setTimeout(() => {
                    const container = document.querySelector('.popup-image-container') as HTMLElement
                    const addToCartBtn = document.querySelector('.add-to-cart-btn') as HTMLButtonElement
                    
                    // Обработчик клика по изображению
                    if (container) {
                      const img = container.querySelector('.popup-main-image') as HTMLImageElement
                      
                      container.addEventListener('click', (e) => {
                        e.stopPropagation()
                        
                        // Создаем модальное окно
                        const modal = document.createElement('div')
                        modal.className = 'image-modal'
                        modal.style.cssText = `
                          position: fixed;
                          top: 0;
                          left: 0;
                          right: 0;
                          bottom: 0;
                          background: rgba(0, 0, 0, 0.9);
                          display: flex;
                          align-items: center;
                          justify-content: center;
                          z-index: 10000;
                          cursor: zoom-out;
                        `
                        
                        const modalContent = document.createElement('div')
                        modalContent.style.cssText = `
                          position: relative;
                          max-width: 90vw;
                          max-height: 90vh;
                        `
                        
                        const modalImg = document.createElement('img')
                        modalImg.src = img.src
                        modalImg.style.cssText = `
                          max-width: 100%;
                          max-height: 90vh;
                          object-fit: contain;
                          border-radius: 8px;
                        `
                        
                        const closeBtn = document.createElement('button')
                        closeBtn.textContent = '✕'
                        closeBtn.style.cssText = `
                          position: absolute;
                          top: -40px;
                          right: 0;
                          background: rgba(255, 255, 255, 0.9);
                          border: none;
                          width: 36px;
                          height: 36px;
                          border-radius: 50%;
                          font-size: 20px;
                          cursor: pointer;
                          display: flex;
                          align-items: center;
                          justify-content: center;
                          transition: all 0.2s;
                        `
                        
                        closeBtn.addEventListener('mouseenter', () => {
                          closeBtn.style.background = 'white'
                          closeBtn.style.transform = 'scale(1.1)'
                        })
                        closeBtn.addEventListener('mouseleave', () => {
                          closeBtn.style.background = 'rgba(255, 255, 255, 0.9)'
                          closeBtn.style.transform = 'scale(1)'
                        })
                        
                        const closeModal = () => {
                          modal.remove()
                        }
                        
                        closeBtn.addEventListener('click', closeModal)
                        modal.addEventListener('click', closeModal)
                        modalContent.addEventListener('click', (e) => e.stopPropagation())
                        
                        modalContent.appendChild(closeBtn)
                        modalContent.appendChild(modalImg)
                        modal.appendChild(modalContent)
                        document.body.appendChild(modal)
                      })
                      
                      // Галерея при движении мыши
                      if (images.length > 1) {
                        const dots = container.querySelectorAll('.popup-dot')
                        const counter = container.querySelector('.current-image')
                        const imagesData = JSON.parse(container.dataset.images || '[]')
                        
                        let currentIndex = 0
                        
                        container.addEventListener('mousemove', (e) => {
                          const rect = container.getBoundingClientRect()
                          const x = e.clientX - rect.left
                          const segmentWidth = rect.width / imagesData.length
                          const newIndex = Math.floor(x / segmentWidth)
                          
                          if (newIndex !== currentIndex && newIndex >= 0 && newIndex < imagesData.length) {
                            currentIndex = newIndex
                            img.src = `${API_URL}${imagesData[currentIndex]}`
                            if (counter) counter.textContent = (currentIndex + 1).toString()
                            
                            dots.forEach((dot, idx) => {
                              if (idx === currentIndex) {
                                (dot as HTMLElement).style.background = 'white'
                              } else {
                                (dot as HTMLElement).style.background = 'rgba(255,255,255,0.5)'
                              }
                            })
                          }
                        })
                        
                        container.addEventListener('mouseleave', () => {
                          currentIndex = 0
                          img.src = `${API_URL}${imagesData[0]}`
                          if (counter) counter.textContent = '1'
                          
                          dots.forEach((dot, idx) => {
                            if (idx === 0) {
                              (dot as HTMLElement).style.background = 'white'
                            } else {
                              (dot as HTMLElement).style.background = 'rgba(255,255,255,0.5)'
                            }
                          })
                        })
                      }
                    }
                    
                    // Обработчик кнопки "В корзину"
                    if (addToCartBtn) {
                      addToCartBtn.addEventListener('click', async () => {
                        const productId = addToCartBtn.dataset.productId
                        
                        if (!productId) return
                        
                        try {
                          addToCartBtn.disabled = true
                          const originalHTML = addToCartBtn.innerHTML
                          addToCartBtn.innerHTML = '<span style="font-size: 18px;">⏳</span> Добавление...'
                          
                          const productData = {
                            id: parseInt(productId),
                            name: props.name,
                            price: props.price,
                            image: props.image,
                            category_id: props.category_id,
                            in_stock: props.in_stock
                          }
                          
                          await addToCart(productId, 1, productData)
                          
                          showToast.success(`${props.name} добавлен в корзину!`)
                          addToCartBtn.innerHTML = '<span style="font-size: 18px;">✅</span> Добавлено'
                          addToCartBtn.style.background = 'linear-gradient(135deg, #4caf50 0%, #45a049 100%)'
                          
                          setTimeout(() => {
                            addToCartBtn.innerHTML = originalHTML
                            addToCartBtn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                            addToCartBtn.disabled = false
                          }, 1500)
                        } catch (error) {
                          console.error('Ошибка добавления в корзину:', error)
                          showToast.error('Ошибка добавления в корзину')
                          addToCartBtn.innerHTML = '<span style="font-size: 18px;">🛒</span> В корзину'
                          addToCartBtn.disabled = false
                        }
                      })
                    }
                  }, 100)
                  
                  // Удаляем данные из localStorage после успешного открытия popup
                  localStorage.removeItem('mapFocusProduct')
                  console.log('✅ Popup открыт, данные очищены')
                }, 2500) // Задержка после анимации flyTo
              }
            } catch (error) {
              console.error('Ошибка открытия popup:', error)
              localStorage.removeItem('mapFocusProduct')
            }
          }
        } catch (error) {
          console.error('❌ Ошибка загрузки товаров:', error)
        }
      })

    } catch (err) {
      console.error('❌ Ошибка инициализации карты:', err)
      setError(err instanceof Error ? err.message : 'Неизвестная ошибка')
      setIsLoading(false)
    }

    // Cleanup при размонтировании
    return () => {
      console.log('🧹 Удаление карты')
      map.current?.remove()
      map.current = null
    }
  }, []) // Пустой массив зависимостей - инициализация только один раз

  // Обновление данных при изменении фильтров
  useEffect(() => {
    if (!map.current) return

    const updateMapData = async () => {
      try {
        console.log('🔄 Обновление данных карты по фильтрам...')
        
        // Формируем параметры запроса из фильтров
        const params = new URLSearchParams()
        if (filters.category_id) params.append('category_id', filters.category_id.toString())
        if (filters.store_id) params.append('store_id', filters.store_id.toString())
        if (filters.min_price !== undefined) params.append('min_price', filters.min_price.toString())
        if (filters.max_price !== undefined) params.append('max_price', filters.max_price.toString())
        if (filters.min_rating !== undefined) params.append('min_rating', filters.min_rating.toString())
        if (filters.in_stock !== undefined) params.append('in_stock', filters.in_stock.toString())
        params.append('limit', '5000')
        
        const response = await axios.get(`${API_URL}/api/products/map/geojson?${params.toString()}`)
        const geojson = response.data
        
        console.log('✅ Обновлено товаров:', geojson.features.length)
        
        // Обновляем источник данных
        if (map.current) {
          const source = map.current.getSource('products') as mapboxgl.GeoJSONSource
          if (source) {
            source.setData(geojson)
          }
        }
      } catch (error) {
        console.error('❌ Ошибка обновления данных:', error)
      }
    }

    updateMapData()
    
    // Закрываем фильтры на мобильных после применения
    if (window.innerWidth <= 768) {
      setIsFiltersOpen(false)
    }
  }, [filters.category_id, filters.store_id, filters.min_price, filters.max_price, filters.min_rating, filters.in_stock]) // Обновляем при изменении фильтров

  return (
    <div className="map-page-container">
      {/* Кнопка переключения фильтров (только на мобильных) */}
      <button 
        className="map-filters-toggle"
        onClick={() => setIsFiltersOpen(!isFiltersOpen)}
        aria-label="Фильтры"
      >
        {isFiltersOpen ? '✕' : '☰'}
      </button>

      {/* Оверлей для закрытия фильтров (только на мобильных) */}
      <div 
        className={`map-filters-overlay ${isFiltersOpen ? 'visible' : ''}`}
        onClick={() => setIsFiltersOpen(false)}
      />

      {/* Фильтры */}
      <aside className={`map-page-filters ${isFiltersOpen ? 'open' : ''}`}>
        <FilterPanel />
      </aside>
      
      {/* Карта */}
      <div className="map-page">
        {error && (
          <div style={{ 
            padding: '20px', 
            background: '#ffebee', 
            color: '#c62828', 
            textAlign: 'center',
            fontWeight: 600
          }}>
            ❌ Ошибка загрузки карты: {error}
          </div>
        )}
        
        <div 
          ref={mapContainer} 
          className="map-container"
          style={{ position: 'relative' }}
        >
          {isLoading && (
            <div style={{ 
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              background: 'rgba(255, 255, 255, 0.95)',
              zIndex: 1000,
              fontSize: '18px',
              fontWeight: 600,
              color: '#1976d2'
            }}>
              ⏳ Загрузка карты...
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
