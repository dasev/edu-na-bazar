import { useState, useRef } from 'react'
import { Button } from 'devextreme-react/button'
import './ImageUpload.css'

interface ImageUploadProps {
  onUpload: (images: UploadedImage[]) => void
  multiple?: boolean
  maxFiles?: number
  existingImages?: string[]
}

export interface UploadedImage {
  id: string
  filename: string
  original_url: string
  thumbnail_url: string | null
  optimized_url: string | null
  size: number
}

export default function ImageUpload({ 
  onUpload, 
  multiple = true, 
  maxFiles = 10,
  existingImages = []
}: ImageUploadProps) {
  const [uploading, setUploading] = useState(false)
  const [preview, setPreview] = useState<string[]>(existingImages)
  const [error, setError] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (!files || files.length === 0) return

    // Проверка количества
    if (files.length > maxFiles) {
      setError(`Максимум ${maxFiles} изображений за раз`)
      return
    }

    // Проверка размера и типа
    const validFiles: File[] = []
    for (let i = 0; i < files.length; i++) {
      const file = files[i]
      
      // Проверка типа
      if (!file.type.startsWith('image/')) {
        setError(`Файл ${file.name} не является изображением`)
        continue
      }
      
      // Проверка размера (5MB)
      if (file.size > 5 * 1024 * 1024) {
        setError(`Файл ${file.name} слишком большой (макс. 5MB)`)
        continue
      }
      
      validFiles.push(file)
    }

    if (validFiles.length === 0) return

    // Превью
    const previewUrls = validFiles.map(file => URL.createObjectURL(file))
    setPreview(prev => [...prev, ...previewUrls])

    // Загрузка
    setUploading(true)
    setError(null)

    try {
      const token = localStorage.getItem('token')
      if (!token) {
        throw new Error('Требуется авторизация')
      }

      const formData = new FormData()
      validFiles.forEach(file => {
        formData.append('files', file)
      })

      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${API_URL}/api/images/upload-multiple`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Ошибка загрузки')
      }

      const result = await response.json()
      
      if (result.success) {
        onUpload(result.data)
        
        // Обновляем превью на реальные URL
        const realUrls = result.data.map((img: UploadedImage) => 
          `${API_URL}${img.thumbnail_url || img.optimized_url || img.original_url}`
        )
        setPreview(() => {
          // Удаляем временные blob URL
          previewUrls.forEach(url => URL.revokeObjectURL(url))
          return realUrls
        })
      } else {
        throw new Error('Не удалось загрузить изображения')
      }
    } catch (err: any) {
      setError(err.message || 'Ошибка загрузки')
      // Удаляем превью при ошибке
      previewUrls.forEach(url => URL.revokeObjectURL(url))
      setPreview(prev => prev.filter(url => !previewUrls.includes(url)))
    } finally {
      setUploading(false)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  const handleRemoveImage = (index: number) => {
    setPreview(prev => {
      const newPreview = [...prev]
      const url = newPreview[index]
      if (url.startsWith('blob:')) {
        URL.revokeObjectURL(url)
      }
      newPreview.splice(index, 1)
      return newPreview
    })
  }

  return (
    <div className="image-upload">
      <div className="image-upload__controls">
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          multiple={multiple}
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />
        
        <Button
          text={uploading ? 'Загрузка...' : 'Выбрать изображения'}
          icon="upload"
          type="default"
          stylingMode="contained"
          onClick={() => fileInputRef.current?.click()}
          disabled={uploading}
        />
        
        {preview.length > 0 && (
          <span className="image-upload__count">
            {preview.length} {preview.length === 1 ? 'изображение' : 'изображений'}
          </span>
        )}
      </div>

      {error && (
        <div className="image-upload__error">
          ⚠️ {error}
        </div>
      )}

      {preview.length > 0 && (
        <div className="image-upload__preview">
          {preview.map((url, index) => (
            <div key={index} className="image-upload__preview-item">
              <img src={url} alt={`Preview ${index + 1}`} />
              <button
                className="image-upload__remove"
                onClick={() => handleRemoveImage(index)}
                title="Удалить"
              >
                ×
              </button>
            </div>
          ))}
        </div>
      )}

      <div className="image-upload__hint">
        Максимум {maxFiles} изображений, до 5MB каждое
        <br />
        Форматы: JPG, PNG, WebP
      </div>
    </div>
  )
}
