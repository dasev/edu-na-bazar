/**
 * My Stores API service
 */
import apiClient from '../client'

export interface DaDataSuggestion {
  value: string
  unrestricted_value: string
  data: {
    inn: string
    kpp?: string
    ogrn?: string
    name: {
      full_with_opf: string
      short_with_opf: string
      full: string
      short: string
    }
    address: {
      value: string
      unrestricted_value: string
      data: {
        postal_code?: string
        country: string
        region: string
        city?: string
        street?: string
        house?: string
      }
    }
    management?: {
      name: string
      post: string
    }
    phones?: string[]
    emails?: string[]
  }
}

export interface Store {
  id: string
  owner_id: string
  name: string
  inn: string
  kpp?: string
  ogrn?: string
  legal_name: string
  address: string
  phone?: string
  email?: string
  description?: string
  logo?: string
  banner?: string
  status: 'pending' | 'active' | 'suspended' | 'rejected'
  created_at: string
  updated_at: string
  products_count?: number
}

export interface StoreProduct {
  id: string
  store_id: string
  name: string
  description?: string
  price: number
  old_price?: number
  images: string[]
  category_id?: string
  in_stock: boolean
  stock_quantity: number
  unit: string
  status: 'pending' | 'active' | 'rejected'
  created_at: string
  updated_at: string
}

export interface CreateStoreData {
  inn: string
  name: string
  legal_name: string
  address: string
  phone?: string
  email?: string
  description?: string
  kpp?: string
  ogrn?: string
}

export interface CreateProductData {
  store_id: string
  name: string
  description?: string
  price: number
  old_price?: number
  category_id?: string
  stock_quantity: number
  unit: string
}

export const myStoresApi = {
  /**
   * Получить магазины текущего пользователя
   */
  getMyStores: async (): Promise<Store[]> => {
    const response = await apiClient.get('/api/my-stores')
    return response.data
  },

  /**
   * Получить магазин по ID
   */
  getStore: async (id: string): Promise<Store> => {
    const response = await apiClient.get(`/api/my-stores/${id}`)
    return response.data
  },

  /**
   * Создать новый магазин
   */
  createStore: async (data: CreateStoreData): Promise<Store> => {
    const response = await apiClient.post('/api/my-stores', data)
    return response.data
  },

  /**
   * Обновить магазин
   */
  updateStore: async (id: string, data: Partial<CreateStoreData>): Promise<Store> => {
    const response = await apiClient.put(`/api/my-stores/${id}`, data)
    return response.data
  },

  /**
   * Удалить магазин
   */
  deleteStore: async (id: string): Promise<void> => {
    await apiClient.delete(`/api/my-stores/${id}`)
  },

  /**
   * Получить товары магазина
   */
  getStoreProducts: async (storeId: string): Promise<StoreProduct[]> => {
    const response = await apiClient.get(`/api/my-stores/${storeId}/products`)
    return response.data
  },

  /**
   * Создать товар в магазине
   */
  createProduct: async (data: CreateProductData): Promise<StoreProduct> => {
    const response = await apiClient.post('/api/my-stores/products', data)
    return response.data
  },

  /**
   * Обновить товар
   */
  updateProduct: async (id: string, data: Partial<CreateProductData>): Promise<StoreProduct> => {
    const response = await apiClient.put(`/api/my-stores/products/${id}`, data)
    return response.data
  },

  /**
   * Удалить товар
   */
  deleteProduct: async (id: string): Promise<void> => {
    await apiClient.delete(`/api/my-stores/products/${id}`)
  },

  /**
   * Загрузить изображение товара
   */
  uploadProductImage: async (productId: string, file: File): Promise<string> => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await apiClient.post(`/api/my-stores/products/${productId}/images`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data.url
  },

  /**
   * Поиск организации по ИНН через DaData
   */
  searchByInn: async (inn: string): Promise<DaDataSuggestion | null> => {
    const response = await apiClient.post('/api/dadata/find-party', { inn })
    return response.data
  },
}
