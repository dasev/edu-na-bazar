/**
 * Централизованный API клиент
 */
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Создаем axios instance
export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Публичные endpoint'ы которые не требуют авторизации
const PUBLIC_ENDPOINTS = [
  '/api/categories',
  '/api/products',
  '/api/stores',
  '/api/store-owners',
  '/api/auth/login',
  '/api/auth/send-code',
  '/api/auth/verify-code',
]

// Interceptor для добавления токена авторизации
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    const isPublicEndpoint = PUBLIC_ENDPOINTS.some(endpoint => config.url?.startsWith(endpoint))
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    } else if (!isPublicEndpoint) {
      console.warn('⚠️ Токен отсутствует для защищённого запроса:', config.url)
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor для обработки ошибок
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Токен истек или невалиден
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user')
      // Можно добавить редирект на страницу входа
    }
    return Promise.reject(error)
  }
)

export default apiClient
