import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useState, useEffect } from 'react'
import { Button } from 'devextreme-react/button'
import { TextBox } from 'devextreme-react/text-box'
import { TextArea } from 'devextreme-react/text-area'
import { NumberBox } from 'devextreme-react/number-box'
import { SelectBox } from 'devextreme-react/select-box'
import { CheckBox } from 'devextreme-react/check-box'
import { apiClient } from '../../api/client'
import toast from 'react-hot-toast'
import './ProductEditPage.css'

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
    rating: 0,
    reviews_count: 0,
    image: '',
  })

  const [images, setImages] = useState<string[]>([])
  const [selectedImageIndex, setSelectedImageIndex] = useState(0)

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
        rating: product.rating || 0,
        reviews_count: product.reviews_count || 0,
        image: product.image || '',
      })
      if (product.image) {
        setImages([product.image])
      }
    }
  }, [product, isNew])

  const addImage = (url: string) => {
    if (url && !images.includes(url)) {
      const newImages = [...images, url]
      setImages(newImages)
      setFormData({ ...formData, image: url })
      setSelectedImageIndex(newImages.length - 1)
    }
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
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['store-products', storeId] })
      toast.success('Товар создан')
      navigate(`/my-stores/${storeId}/products`)
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
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['store-products', storeId] })
      queryClient.invalidateQueries({ queryKey: ['product', productId] })
      toast.success('Товар обновлен')
      navigate(`/my-stores/${storeId}/products`)
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
                  <img src={img} alt={`Thumbnail ${index + 1}`} />
                  <Button
                    icon="trash"
                    onClick={() => removeImage(index)}
                    className="remove-thumb-btn"
                    type="danger"
                  />
                </div>
              ))}
              <div className="add-image-thumb">
                <TextBox
                  placeholder="URL изображения"
                  onValueChanged={(e) => {
                    if (e.value && e.event?.type === 'change') {
                      addImage(e.value)
                      e.component.option('value', '')
                    }
                  }}
                  mode="text"
                />
              </div>
            </div>
            <div className="main-image">
              {images.length > 0 ? (
                <img src={images[selectedImageIndex]} alt="Main preview" />
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
              <span>⭐ {formData.rating || 0}</span>
              <span>{formData.in_stock ? '✅ В наличии' : '❌ Нет в наличии'}</span>
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
            <label>Изображение (URL)</label>
            <TextBox
              value={formData.image}
              onValueChanged={(e) => setFormData({ ...formData, image: e.value })}
              placeholder="https://example.com/image.jpg"
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
          <h2>Дополнительно</h2>
          
          <div className="form-row">
            <div className="form-field">
              <label>Рейтинг</label>
              <NumberBox
                value={formData.rating}
                onValueChanged={(e) => setFormData({ ...formData, rating: e.value })}
                min={0}
                max={5}
                step={0.1}
                format="#0.0"
              />
            </div>

            <div className="form-field">
              <label>Количество отзывов</label>
              <NumberBox
                value={formData.reviews_count}
                onValueChanged={(e) => setFormData({ ...formData, reviews_count: e.value })}
                min={0}
              />
            </div>
          </div>
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
