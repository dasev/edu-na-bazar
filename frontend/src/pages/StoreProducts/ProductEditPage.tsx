import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useState, useEffect, useRef } from 'react'
import { Button } from 'devextreme-react/button'
import { TextBox } from 'devextreme-react/text-box'
import { TextArea } from 'devextreme-react/text-area'
import { NumberBox } from 'devextreme-react/number-box'
import { SelectBox } from 'devextreme-react/select-box'
import { CheckBox } from 'devextreme-react/check-box'
import { Autocomplete } from 'devextreme-react/autocomplete'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import { apiClient } from '../../api/client'
import toast from 'react-hot-toast'
import './ProductEditPage.css'

mapboxgl.accessToken = 'pk.eyJ1Ijoic2VyZ2VqZGFuNDUyIiwiYSI6ImNtaTd0dzQ4ajA0bHkyanIyNWJwa2JrNXYifQ.AWJBOIEEXVb-6AIKrbRXmw'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function ProductEditPage() {
  const { storeId, productId } = useParams<{ storeId: string; productId: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const isNew = productId === 'new'

  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: 0,
    category_id: null as number | null,
    in_stock: true,
    unit: 'шт',
    latitude: null as number | null,
    longitude: null as number | null,
    location: '',
  })

  const [images, setImages] = useState<string[]>([])
  const [selectedImageIndex, setSelectedImageIndex] = useState(0)
  const [addressSuggestions, setAddressSuggestions] = useState<any[]>([])
  const [isUploadingImage, setIsUploadingImage] = useState(false)
  const [draggedIndex, setDraggedIndex] = useState<number | null>(null)
  const [isAddressInputActive, setIsAddressInputActive] = useState(false) // Флаг активного ввода адреса
  const [isMapReady, setIsMapReady] = useState(false) // Флаг готовности карты
  const mapContainer = useRef<HTMLDivElement>(null)
  const map = useRef<mapboxgl.Map | null>(null)
  const marker = useRef<mapboxgl.Marker | null>(null)


  // Получаем товар если редактируем
  const { data: product, isLoading } = useQuery({
    queryKey: ['product', productId],
    queryFn: async () => {
      const response = await apiClient.get(`/api/products/${productId}`)
      return response.data
    },
    enabled: !isNew,
  })

  // Получаем категории
  const { data: categories = [] } = useQuery({
    queryKey: ['categories'],
    queryFn: async () => {
      const response = await apiClient.get('/api/categories/')
      return response.data
    },
  })

  // Получаем иконку текущей категории
  const getCategoryIcon = () => {
    if (!formData.category_id || !categories.length) return '🥬'
    const category = categories.find((c: any) => c.id === formData.category_id)
    return category?.icon || '🥬'
  }

  useEffect(() => {
    if (product && !isNew) {
      const newFormData = {
        name: product.name || '',
        description: product.description || '',
        price: product.price ?? 0,
        category_id: product.category_id || null,
        in_stock: product.in_stock ?? true,
        unit: product.unit || 'шт',
        latitude: product.latitude ?? null,
        longitude: product.longitude ?? null,
        location: product.location || '',
      }
      console.log('📦 Загружен товар:', product.name, 'Координаты:', newFormData.latitude, newFormData.longitude)
      setFormData(newFormData)
      // Загружаем все изображения товара
      const productImages: string[] = []
      if (product.image) {
        productImages.push(product.image)
      }
      // Добавляем дополнительные изображения, если есть
      if (product.images && Array.isArray(product.images)) {
        product.images.forEach((img: any) => {
          const imgUrl = img.image_url || img.url
          if (imgUrl && !productImages.includes(imgUrl)) {
            productImages.push(imgUrl)
          }
        })
      }
      if (productImages.length > 0) {
        setImages(productImages)
      }
    }
  }, [product, isNew])

  // Инициализация карты
  useEffect(() => {
    console.log('🗺️ useEffect карты запущен')
    console.log('  mapContainer.current =', !!mapContainer.current)
    console.log('  map.current =', !!map.current)
    
    if (!mapContainer.current) {
      console.log('❌ mapContainer.current отсутствует, ждем рендера')
      // Пробуем через небольшую задержку
      const timer = setTimeout(() => {
        if (mapContainer.current && !map.current) {
          console.log('🔄 Повторная попытка инициализации карты')
          initMap()
        }
      }, 100)
      return () => clearTimeout(timer)
    }
    
    if (map.current) {
      console.log('⚠️ Карта уже инициализирована')
      return
    }

    initMap()
  }, [])

  const initMap = () => {
    if (!mapContainer.current || map.current) return
    
    console.log('🚀 Начинаем инициализацию карты...')
    try {
      map.current = new mapboxgl.Map({
        container: mapContainer.current,
        style: {
          version: 8,
          glyphs: 'mapbox://fonts/mapbox/{fontstack}/{range}.pbf',
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
              attribution: ''
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
        center: [37.6173, 55.7558], // Центр Москвы по умолчанию
        zoom: 10,
        attributionControl: false
      })

      console.log('✅ Карта создана успешно')

      // Ждем загрузки карты
      map.current.on('load', () => {
        console.log('✅ Карта полностью загружена')
        setIsMapReady(true) // Устанавливаем флаг готовности
      })

      map.current.on('error', (e) => {
        console.error('❌ Ошибка карты:', e)
      })
    } catch (error) {
      console.error('❌ Ошибка при создании карты:', error)
      map.current = null
      return
    }

    // Клик по карте для установки маркера
    map.current.on('click', (e) => {
      const { lng, lat } = e.lngLat
      setFormData(prev => ({
        ...prev,
        latitude: lat,
        longitude: lng
      }))
      
      // Получаем адрес по координатам клика
      reverseGeocode(lat, lng)
      
      // Обновляем маркер
      if (marker.current) {
        marker.current.setLngLat([lng, lat])
      } else {
        const markerElement = createMarkerElement(getCategoryIcon())
        marker.current = new mapboxgl.Marker({ element: markerElement, draggable: true })
          .setLngLat([lng, lat])
          .addTo(map.current!)
        
        // Обработка перетаскивания маркера
        marker.current.on('dragend', () => {
          const lngLat = marker.current!.getLngLat()
          setFormData(prev => ({
            ...prev,
            latitude: lngLat.lat,
            longitude: lngLat.lng
          }))
          // Получаем адрес по новым координатам
          reverseGeocode(lngLat.lat, lngLat.lng)
        })
      }
    })
  }

  // Cleanup при размонтировании
  useEffect(() => {
    return () => {
      if (map.current) {
        map.current.remove()
        map.current = null
      }
    }
  }, [])

  // Обновление маркера при изменении координат или после инициализации карты
  useEffect(() => {
    console.log('📍 useEffect маркера: map.current =', !!map.current, 'coordinates =', formData.latitude, formData.longitude)
    
    if (!map.current) {
      console.log('⚠️ Карта еще не инициализирована, пропускаем создание маркера')
      return
    }

    if (formData.latitude && formData.longitude) {
      console.log('🎯 Создаем/обновляем маркер на координатах:', formData.latitude, formData.longitude)
      
      if (marker.current) {
        console.log('♻️ Обновляем существующий маркер')
        marker.current.setLngLat([formData.longitude, formData.latitude])
      } else {
        console.log('🆕 Создаем новый маркер')
        const markerElement = createMarkerElement(getCategoryIcon())
        marker.current = new mapboxgl.Marker({ element: markerElement, draggable: true })
          .setLngLat([formData.longitude, formData.latitude])
          .addTo(map.current)
        
        marker.current.on('dragend', () => {
          const lngLat = marker.current!.getLngLat()
          setFormData(prev => ({
            ...prev,
            latitude: lngLat.lat,
            longitude: lngLat.lng
          }))
          // Получаем адрес по новым координатам
          reverseGeocode(lngLat.lat, lngLat.lng)
        })
      }
      map.current.flyTo({
        center: [formData.longitude, formData.latitude],
        zoom: 13
      })
    }
  }, [formData.latitude, formData.longitude, isMapReady])

  // Обновление иконки маркера при изменении категории
  useEffect(() => {
    if (marker.current) {
      const markerElement = marker.current.getElement()
      if (markerElement) {
        markerElement.style.backgroundImage = `url("${createEmojiIcon(getCategoryIcon())}")`
      }
    }
  }, [formData.category_id, categories])

  // Поиск адресов через DaData
  // Создание SVG иконки с эмодзи (как на основной карте)
  const createEmojiIcon = (emoji: string, size = 48) => {
    const svg = `
      <svg width="${size}" height="${size}" xmlns="http://www.w3.org/2000/svg">
        <circle cx="${size/2}" cy="${size/2}" r="${size/2 - 4}" fill="#667eea" stroke="white" stroke-width="4"/>
        <text x="50%" y="50%" text-anchor="middle" dy=".35em" font-size="${size * 0.5}" fill="white">${emoji}</text>
      </svg>
    `
    return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg)
  }

  // Создание HTML элемента маркера с SVG иконкой
  const createMarkerElement = (categoryIcon: string) => {
    const el = document.createElement('div')
    el.style.cssText = `
      width: 48px;
      height: 48px;
      background-image: url("${createEmojiIcon(categoryIcon)}");
      background-size: contain;
      cursor: pointer;
    `
    return el
  }

  const searchAddress = async (query: string) => {
    if (!query || query.length < 3) {
      setAddressSuggestions([])
      return
    }

    try {
      const response = await fetch('https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': 'Token e76739998f03541266e5b2f288d0d1c8b5d2f876' // API ключ как в CreateStorePage
        },
        body: JSON.stringify({ query, count: 10 })
      })

      const data = await response.json()
      if (data.suggestions && data.suggestions.length > 0) {
        setAddressSuggestions(data.suggestions)
      } else {
        setAddressSuggestions([])
      }
    } catch (error) {
      console.error('DaData error:', error)
      setAddressSuggestions([])
    }
  }

  // Обратное геокодирование - получение адреса по координатам
  const reverseGeocode = async (lat: number, lon: number) => {
    try {
      const response = await fetch('https://suggestions.dadata.ru/suggestions/api/4_1/rs/geolocate/address', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': 'Token e76739998f03541266e5b2f288d0d1c8b5d2f876'
        },
        body: JSON.stringify({ lat, lon, count: 1 })
      })

      const data = await response.json()
      if (data.suggestions && data.suggestions.length > 0) {
        const address = data.suggestions[0].value
        setFormData(prev => ({ ...prev, location: address }))
      }
    } catch (error) {
      console.error('Reverse geocode error:', error)
    }
  }

  const addImage = (url: string) => {
    if (url && !images.includes(url)) {
      const newImages = [...images, url]
      setImages(newImages)
      setSelectedImageIndex(newImages.length - 1)
    }
  }

  const getImageUrl = (url: string) => {
    if (!url) return ''
    if (url.startsWith('http://') || url.startsWith('https://')) {
      return url
    }
    return `${API_URL}${url.startsWith('/') ? url : '/' + url}`
  }

  const removeImage = (index: number) => {
    const newImages = images.filter((_, i) => i !== index)
    setImages(newImages)
    setSelectedImageIndex(newImages.length > 0 ? 0 : 0)
  }

  // Drag and drop handlers
  const handleDragStart = (index: number) => {
    setDraggedIndex(index)
  }

  const handleDragOver = (e: React.DragEvent, index: number) => {
    e.preventDefault()
    if (draggedIndex === null || draggedIndex === index) return

    const newImages = [...images]
    const draggedImage = newImages[draggedIndex]
    newImages.splice(draggedIndex, 1)
    newImages.splice(index, 0, draggedImage)
    
    setImages(newImages)
    setDraggedIndex(index)
  }

  const handleDragEnd = () => {
    setDraggedIndex(null)
  }

  // Создание товара
  const createMutation = useMutation({
    mutationFn: async (data: any) => {
      const response = await apiClient.post(`/api/my-stores/${storeId}/products`, data)
      return response.data
    },
    onSuccess: async (data) => {
      toast.success('Товар создан')
      // Перезагружаем данные
      await queryClient.refetchQueries({ queryKey: ['store-products', storeId] })
      await queryClient.refetchQueries({ queryKey: ['store-products-count', storeId] })
      // Переходим к редактированию созданного товара
      navigate(`/my-stores/${storeId}/products/${data.id}`)
    },
    onError: () => {
      toast.error('Ошибка при создании товара')
    },
  })

  // Обновление товара
  const updateMutation = useMutation({
    mutationFn: async (data: any) => {
      const response = await apiClient.put(`/api/my-stores/${storeId}/products/${productId}`, data)
      return response.data
    },
    onSuccess: async () => {
      toast.success('Товар обновлен')
      // Перезагружаем данные
      await queryClient.refetchQueries({ queryKey: ['store-products', storeId] })
      await queryClient.refetchQueries({ queryKey: ['store-products-count', storeId] })
      await queryClient.refetchQueries({ queryKey: ['product', productId] })
      // Остаемся на странице редактирования
    },
    onError: () => {
      toast.error('Ошибка при обновлении товара')
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!formData.name || !formData.price) {
      toast.error('Заполните обязательные поля')
      return
    }

    // Подготавливаем данные для отправки
    const dataToSend = {
      ...formData,
      // Первое изображение как основное
      image: images.length > 0 ? images[0] : '',
      // Все изображения
      images: images
    }


    if (isNew) {
      createMutation.mutate(dataToSend)
    } else {
      updateMutation.mutate(dataToSend)
    }
  }

  if (isLoading && !isNew) {
    return <div className="product-edit-page">Загрузка...</div>
  }

  return (
    <div className="product-edit-page">
      <div className="page-header">
        <Button
          icon="back"
          text="Назад к товарам"
          onClick={() => navigate(`/my-stores/${storeId}/products`)}
          stylingMode="text"
        />
        <h1>{isNew ? 'Создание товара' : 'Редактирование товара'}</h1>
      </div>

      <form onSubmit={handleSubmit} className="product-form">
        <div className="product-preview">
          <div className="preview-gallery">
            <div className="thumbnails" title="Перетащите миниатюры для изменения порядка">
              {images.map((img, index) => (
                <div
                  key={index}
                  className={`thumbnail ${index === selectedImageIndex ? 'active' : ''} ${draggedIndex === index ? 'dragging' : ''}`}
                  onClick={() => setSelectedImageIndex(index)}
                  draggable
                  onDragStart={() => handleDragStart(index)}
                  onDragOver={(e) => handleDragOver(e, index)}
                  onDragEnd={handleDragEnd}
                >
                  <img src={getImageUrl(img)} alt={`Thumbnail ${index + 1}`} onError={(e) => {
                    (e.target as HTMLImageElement).src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="80" height="80"%3E%3Crect fill="%23f0f0f0" width="80" height="80"/%3E%3Ctext fill="%23999" x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-size="12"%3EНет фото%3C/text%3E%3C/svg%3E'
                  }} />
                  <Button
                    icon="trash"
                    onClick={() => removeImage(index)}
                    className="remove-thumb-btn"
                    type="danger"
                  />
                </div>
              ))}
              {images.length > 1 && (
                <div className="drag-hint">↕️ Перетащите</div>
              )}
            </div>
            <div className="main-image">
              {images.length > 0 ? (
                <img src={getImageUrl(images[selectedImageIndex])} alt="Main preview" onError={(e) => {
                  (e.target as HTMLImageElement).src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="500" height="500"%3E%3Crect fill="%23f0f0f0" width="500" height="500"/%3E%3Ctext fill="%23999" x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-size="24"%3EНет фото%3C/text%3E%3C/svg%3E'
                }} />
              ) : (
                <div className="no-preview">📦<br/>Добавьте изображение</div>
              )}
            </div>
          </div>
          <div className="preview-info">
            <h3>{formData.name || 'Новый товар'}</h3>
            <p className="preview-price">{formData.price || 0} ₽/{formData.unit || 'шт'}</p>
            {formData.description && (
              <p className="preview-description">{formData.description}</p>
            )}
            <div className="preview-meta">
              <span>{formData.in_stock ? '✅ В наличии' : '❌ Нет в наличии'}</span>
            </div>
            <div className="add-image-field">
              <input
                type="file"
                accept="image/*"
                onChange={async (e) => {
                  const file = e.target.files?.[0]
                  if (!file) return

                  setIsUploadingImage(true)
                  const formData = new FormData()
                  formData.append('file', file)

                  try {
                    const response = await apiClient.post('/api/images/upload', formData, {
                      headers: {
                        'Content-Type': 'multipart/form-data',
                      },
                    })

                    console.log('Upload response:', response.data)

                    // API возвращает original_url, optimized_url, thumbnail_url
                    const imageData = response.data?.data
                    if (imageData) {
                      // Используем оптимизированное изображение, если есть, иначе оригинал
                      const imageUrl = imageData.optimized_url || imageData.original_url || imageData.url
                      if (imageUrl) {
                        addImage(imageUrl)
                        toast.success('Изображение загружено')
                      } else {
                        toast.error('URL изображения не найден в ответе')
                      }
                    } else {
                      toast.error('Некорректный ответ от сервера')
                    }
                  } catch (error: any) {
                    console.error('Upload error:', error)
                    toast.error(error.response?.data?.detail || 'Ошибка загрузки')
                  } finally {
                    setIsUploadingImage(false)
                    e.target.value = '' // Очищаем input
                  }
                }}
                disabled={isUploadingImage}
                className="file-input"
              />
              {isUploadingImage && <div className="upload-progress">Загрузка...</div>}
            </div>
          </div>
        </div>

        <div className="form-section">
          <h2>Основная информация</h2>
          
          <div className="form-field">
            <label>Название товара *</label>
            <TextBox
              value={formData.name}
              onValueChanged={(e) => setFormData(prev => ({ ...prev, name: e.value }))}
              placeholder="Введите название товара"
            />
          </div>

          <div className="form-field">
            <label>Описание</label>
            <TextArea
              value={formData.description}
              onValueChanged={(e) => setFormData(prev => ({ ...prev, description: e.value }))}
              placeholder="Введите описание товара"
              height={100}
            />
          </div>

          <div className="form-row">
            <div className="form-field">
              <label>Цена *</label>
              <NumberBox
                value={formData.price}
                onValueChanged={(e) => setFormData(prev => ({ ...prev, price: e.value }))}
                format="#,##0.00 ₽"
                min={0}
              />
            </div>

            <div className="form-field">
              <label>Единица измерения</label>
              <TextBox
                value={formData.unit}
                onValueChanged={(e) => setFormData(prev => ({ ...prev, unit: e.value }))}
                placeholder="шт, кг, л"
              />
            </div>
          </div>

          <div className="form-field">
            <label>Категория</label>
            <SelectBox
              value={formData.category_id}
              onValueChanged={(e) => setFormData(prev => ({ ...prev, category_id: e.value }))}
              dataSource={categories}
              displayExpr="name"
              valueExpr="id"
              placeholder="Выберите категорию"
              searchEnabled={true}
            />
          </div>

          <div className="form-field">
            <CheckBox
              value={formData.in_stock}
              onValueChanged={(e) => setFormData(prev => ({ ...prev, in_stock: e.value }))}
              text="Товар в наличии"
            />
          </div>
        </div>

        <div className="form-section">
          <h2>Местоположение товара</h2>
          <p className="section-hint">Кликните на карту, чтобы указать местоположение товара. Маркер можно перетаскивать.</p>
          
          <div className="form-field">
            <label>Адрес (необязательно)</label>
            <Autocomplete
              value={formData.location}
              onFocusIn={() => setIsAddressInputActive(true)}
              onValueChanged={(e) => {
                setFormData(prev => ({ ...prev, location: e.value }))
                // Вызываем поиск при изменении значения
                if (e.value && e.value.length >= 3 && isAddressInputActive) {
                  searchAddress(e.value)
                } else {
                  setAddressSuggestions([])
                }
              }}
              dataSource={addressSuggestions}
              valueExpr="value"
              displayExpr="value"
              placeholder="Начните вводить адрес..."
              minSearchLength={3}
              searchTimeout={500}
              showClearButton={true}
              opened={addressSuggestions.length > 0 && isAddressInputActive}
              onItemClick={(e) => {
                const suggestion = e.itemData
                setFormData(prev => ({ ...prev, location: suggestion.value }))
                
                // Обновляем координаты из выбранного адреса
                if (suggestion?.data?.geo_lat && suggestion?.data?.geo_lon) {
                  const lat = parseFloat(suggestion.data.geo_lat)
                  const lon = parseFloat(suggestion.data.geo_lon)
                  if (!isNaN(lat) && !isNaN(lon)) {
                    setFormData(prev => ({ ...prev, latitude: lat, longitude: lon }))
                  }
                }
                
                // Очищаем suggestions и сбрасываем флаг после выбора
                setAddressSuggestions([])
                setIsAddressInputActive(false)
              }}
            />
          </div>

          <div className="form-row">
            <div className="form-field">
              <label>Широта</label>
              <NumberBox
                value={formData.latitude ?? undefined}
                onValueChanged={(e) => setFormData(prev => ({ ...prev, latitude: e.value ?? null }))}
                format="#0.######"
                placeholder="55.7558"
              />
            </div>

            <div className="form-field">
              <label>Долгота</label>
              <NumberBox
                value={formData.longitude ?? undefined}
                onValueChanged={(e) => setFormData(prev => ({ ...prev, longitude: e.value ?? null }))}
                format="#0.######"
                placeholder="37.6173"
              />
            </div>
          </div>

          <div className="map-container" ref={mapContainer} style={{ height: '400px', borderRadius: '12px', marginTop: '16px' }} />
        </div>

        <div className="form-actions">
          <Button
            text="Отмена"
            onClick={() => navigate(`/my-stores/${storeId}/products`)}
            stylingMode="outlined"
          />
          <Button
            text={isNew ? 'Создать товар' : 'Сохранить изменения'}
            type="default"
            useSubmitBehavior={true}
          />
        </div>
      </form>
    </div>
  )
}
