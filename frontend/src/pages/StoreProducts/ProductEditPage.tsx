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
    image: '',
    latitude: null as number | null,
    longitude: null as number | null,
    location: '',
  })

  const [images, setImages] = useState<string[]>([])
  const [selectedImageIndex, setSelectedImageIndex] = useState(0)
  const [addressSuggestions, setAddressSuggestions] = useState<string[]>([])
  const [isUploadingImage, setIsUploadingImage] = useState(false)
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

  useEffect(() => {
    if (product && !isNew) {
      setFormData({
        name: product.name || '',
        description: product.description || '',
        price: product.price || 0,
        category_id: product.category_id || null,
        in_stock: product.in_stock ?? true,
        unit: product.unit || 'шт',
        image: product.image || '',
        latitude: product.latitude || null,
        longitude: product.longitude || null,
        location: product.location || '',
      })
      if (product.image) {
        setImages([product.image])
      }
    }
  }, [product, isNew])

  // Инициализация карты
  useEffect(() => {
    if (!mapContainer.current || map.current) return

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
      center: [formData.longitude || 37.6173, formData.latitude || 55.7558],
      zoom: formData.latitude ? 13 : 10,
      attributionControl: false
    })

    // Клик по карте для установки маркера
    map.current.on('click', (e) => {
      const { lng, lat } = e.lngLat
      setFormData(prev => ({
        ...prev,
        latitude: lat,
        longitude: lng
      }))
      
      // Обновляем маркер
      if (marker.current) {
        marker.current.setLngLat([lng, lat])
      } else {
        marker.current = new mapboxgl.Marker({ color: '#667eea', draggable: true })
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
        })
      }
    })

    return () => {
      map.current?.remove()
      map.current = null
    }
  }, [])

  // Обновление маркера при изменении координат
  useEffect(() => {
    if (!map.current) return

    if (formData.latitude && formData.longitude) {
      if (marker.current) {
        marker.current.setLngLat([formData.longitude, formData.latitude])
      } else {
        marker.current = new mapboxgl.Marker({ color: '#667eea', draggable: true })
          .setLngLat([formData.longitude, formData.latitude])
          .addTo(map.current)
        
        marker.current.on('dragend', () => {
          const lngLat = marker.current!.getLngLat()
          setFormData(prev => ({
            ...prev,
            latitude: lngLat.lat,
            longitude: lngLat.lng
          }))
        })
      }
      map.current.flyTo({
        center: [formData.longitude, formData.latitude],
        zoom: 13
      })
    }
  }, [formData.latitude, formData.longitude])

  // Поиск адресов через DaData
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
          'Authorization': 'Token 5f3ff95c0c6a9f6e4a8e0b5c8f3ff95c0c6a9f6e' // Бесплатный тестовый токен
        },
        body: JSON.stringify({ query, count: 10 })
      })

      const data = await response.json()
      if (data.suggestions) {
        const addresses = data.suggestions.map((s: any) => s.value)
        setAddressSuggestions(addresses)
        
        // Если есть координаты, обновляем их
        if (data.suggestions[0]?.data?.geo_lat && data.suggestions[0]?.data?.geo_lon) {
          const lat = parseFloat(data.suggestions[0].data.geo_lat)
          const lon = parseFloat(data.suggestions[0].data.geo_lon)
          if (!isNaN(lat) && !isNaN(lon)) {
            setFormData(prev => ({ ...prev, latitude: lat, longitude: lon }))
          }
        }
      }
    } catch (error) {
      console.error('DaData error:', error)
    }
  }

  const addImage = (url: string) => {
    if (url && !images.includes(url)) {
      const newImages = [...images, url]
      setImages(newImages)
      setFormData({ ...formData, image: url })
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
    if (newImages.length > 0) {
      setSelectedImageIndex(0)
      setFormData({ ...formData, image: newImages[0] })
    } else {
      setSelectedImageIndex(0)
      setFormData({ ...formData, image: '' })
    }
  }

  // Создание товара
  const createMutation = useMutation({
    mutationFn: async (data: any) => {
      const response = await apiClient.post(`/api/my-stores/${storeId}/products`, data)
      return response.data
    },
    onSuccess: async () => {
      toast.success('Товар создан')
      // Инвалидируем кэш товаров магазина
      queryClient.invalidateQueries({ queryKey: ['store-products', storeId] })
      // Небольшая задержка чтобы инвалидация успела сработать
      setTimeout(() => {
        navigate(`/my-stores/${storeId}/products`)
      }, 100)
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
      // Инвалидируем кэш товаров магазина и конкретного товара
      queryClient.invalidateQueries({ queryKey: ['store-products', storeId] })
      queryClient.invalidateQueries({ queryKey: ['product', productId] })
      // Небольшая задержка чтобы инвалидация успела сработать
      setTimeout(() => {
        navigate(`/my-stores/${storeId}/products`)
      }, 100)
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

    if (isNew) {
      createMutation.mutate(formData)
    } else {
      updateMutation.mutate(formData)
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
            <div className="thumbnails">
              {images.map((img, index) => (
                <div
                  key={index}
                  className={`thumbnail ${index === selectedImageIndex ? 'active' : ''}`}
                  onClick={() => setSelectedImageIndex(index)}
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

                    if (response.data?.data?.url) {
                      addImage(response.data.data.url)
                      toast.success('Изображение загружено')
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
              onValueChanged={(e) => setFormData({ ...formData, name: e.value })}
              placeholder="Введите название товара"
            />
          </div>

          <div className="form-field">
            <label>Описание</label>
            <TextArea
              value={formData.description}
              onValueChanged={(e) => setFormData({ ...formData, description: e.value })}
              placeholder="Введите описание товара"
              height={100}
            />
          </div>

          <div className="form-row">
            <div className="form-field">
              <label>Цена *</label>
              <NumberBox
                value={formData.price}
                onValueChanged={(e) => setFormData({ ...formData, price: e.value })}
                format="#,##0.00 ₽"
                min={0}
              />
            </div>

            <div className="form-field">
              <label>Единица измерения</label>
              <TextBox
                value={formData.unit}
                onValueChanged={(e) => setFormData({ ...formData, unit: e.value })}
                placeholder="шт, кг, л"
              />
            </div>
          </div>

          <div className="form-field">
            <label>Категория</label>
            <SelectBox
              value={formData.category_id}
              onValueChanged={(e) => setFormData({ ...formData, category_id: e.value })}
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
              onValueChanged={(e) => setFormData({ ...formData, in_stock: e.value })}
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
              onValueChanged={(e) => {
                setFormData({ ...formData, location: e.value })
                searchAddress(e.value)
              }}
              dataSource={addressSuggestions}
              placeholder="Начните вводить адрес..."
              minSearchLength={3}
              searchTimeout={500}
              onItemClick={(e) => {
                setFormData({ ...formData, location: e.itemData })
              }}
            />
            <div className="field-hint">Используется DaData для подсказок адресов</div>
          </div>

          <div className="form-row">
            <div className="form-field">
              <label>Широта</label>
              <NumberBox
                value={formData.latitude ?? undefined}
                onValueChanged={(e) => setFormData({ ...formData, latitude: e.value ?? null })}
                format="#0.######"
                placeholder="55.7558"
              />
            </div>

            <div className="form-field">
              <label>Долгота</label>
              <NumberBox
                value={formData.longitude ?? undefined}
                onValueChanged={(e) => setFormData({ ...formData, longitude: e.value ?? null })}
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
