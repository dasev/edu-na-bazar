/**
 * Cart Store (Zustand) с поддержкой гостевой корзины
 */
import { create } from 'zustand'
import { cartApi } from '../api'
import type { Cart } from '../api/types'

const GUEST_CART_KEY = 'guest_cart'

// Гостевая корзина в localStorage
interface GuestCartItem {
  product_id: string
  quantity: number
  product?: any
}

interface GuestCart {
  items: GuestCartItem[]
}

// Утилиты для работы с гостевой корзиной
const getGuestCart = (): GuestCart => {
  try {
    const data = localStorage.getItem(GUEST_CART_KEY)
    return data ? JSON.parse(data) : { items: [] }
  } catch {
    return { items: [] }
  }
}

const saveGuestCart = (cart: GuestCart) => {
  try {
    localStorage.setItem(GUEST_CART_KEY, JSON.stringify(cart))
  } catch (error) {
    console.error('Error saving guest cart:', error)
  }
}

const clearGuestCart = () => {
  try {
    localStorage.removeItem(GUEST_CART_KEY)
  } catch (error) {
    console.error('Error clearing guest cart:', error)
  }
}

interface CartState {
  cart: Cart | null
  guestCart: GuestCart
  isLoading: boolean
  error: string | null
  
  // Actions
  fetchCart: () => Promise<void>
  addToCart: (productId: string, quantity?: number, product?: any) => Promise<void>
  updateQuantity: (itemId: string, quantity: number) => Promise<void>
  removeItem: (itemId: string) => Promise<void>
  clearCart: () => Promise<void>
  syncGuestCart: () => Promise<void>
  
  // Computed
  getItemsCount: () => number
  getTotal: () => number
}

export const useCartStore = create<CartState>((set, get) => ({
  cart: null,
  guestCart: getGuestCart(),
  isLoading: false,
  error: null,

  fetchCart: async () => {
    // Проверяем наличие токена авторизации
    const token = localStorage.getItem('auth_token')
    if (!token) {
      // Если не авторизован, используем гостевую корзину
      set({ cart: null, isLoading: false })
      return
    }
    
    set({ isLoading: true, error: null })
    try {
      const cart = await cartApi.getCart()
      set({ cart, isLoading: false })
    } catch (error: any) {
      // Если 401 - пользователь не авторизован, используем гостевую корзину
      if (error.response?.status === 401) {
        set({ cart: null, isLoading: false })
        return
      }
      set({ 
        error: error.response?.data?.detail || 'Ошибка загрузки корзины',
        isLoading: false 
      })
    }
  },

  addToCart: async (productId: string, quantity: number = 1, product?: any) => {
    const { cart } = get()
    
    // Если пользователь авторизован - добавляем через API
    if (cart !== null) {
      set({ isLoading: true, error: null })
      try {
        await cartApi.addToCart(productId, quantity)
        await get().fetchCart()
      } catch (error: any) {
        set({ 
          error: error.response?.data?.detail || 'Ошибка добавления в корзину',
          isLoading: false 
        })
        throw error
      }
    } else {
      // Гостевая корзина - сохраняем в localStorage
      const guestCart = getGuestCart()
      const existingItem = guestCart.items.find(item => item.product_id === productId)
      
      if (existingItem) {
        existingItem.quantity += quantity
      } else {
        guestCart.items.push({ product_id: productId, quantity, product })
      }
      
      saveGuestCart(guestCart)
      set({ guestCart })
    }
  },

  updateQuantity: async (itemId: string, quantity: number) => {
    const { cart } = get()
    
    if (cart !== null) {
      // Авторизованный пользователь
      set({ isLoading: true, error: null })
      try {
        await cartApi.updateCartItem(itemId, quantity)
        await get().fetchCart()
      } catch (error: any) {
        set({ 
          error: error.response?.data?.detail || 'Ошибка обновления количества',
          isLoading: false 
        })
        throw error
      }
    } else {
      // Гостевая корзина (itemId = product_id)
      const guestCart = getGuestCart()
      const item = guestCart.items.find(i => i.product_id === itemId)
      if (item) {
        item.quantity = quantity
        saveGuestCart(guestCart)
        set({ guestCart })
      }
    }
  },

  removeItem: async (itemId: string) => {
    const { cart } = get()
    
    if (cart !== null) {
      // Авторизованный пользователь
      set({ isLoading: true, error: null })
      try {
        await cartApi.removeFromCart(itemId)
        await get().fetchCart()
      } catch (error: any) {
        set({ 
          error: error.response?.data?.detail || 'Ошибка удаления товара',
          isLoading: false 
        })
        throw error
      }
    } else {
      // Гостевая корзина
      const guestCart = getGuestCart()
      guestCart.items = guestCart.items.filter(i => i.product_id !== itemId)
      saveGuestCart(guestCart)
      set({ guestCart })
    }
  },

  clearCart: async () => {
    const { cart } = get()
    
    if (cart !== null) {
      // Авторизованный пользователь
      set({ isLoading: true, error: null })
      try {
        await cartApi.clearCart()
        set({ cart: null, isLoading: false })
      } catch (error: any) {
        set({ 
          error: error.response?.data?.detail || 'Ошибка очистки корзины',
          isLoading: false 
        })
        throw error
      }
    } else {
      // Гостевая корзина
      clearGuestCart()
      set({ guestCart: { items: [] } })
    }
  },

  // Синхронизация гостевой корзины с серверной при входе
  syncGuestCart: async () => {
    // Проверяем наличие токена авторизации
    const token = localStorage.getItem('auth_token')
    if (!token) {
      // Если не авторизован, не синхронизируем
      return
    }
    
    const guestCart = getGuestCart()
    if (guestCart.items.length === 0) return
    
    set({ isLoading: true })
    try {
      // Добавляем все товары из гостевой корзины в серверную
      for (const item of guestCart.items) {
        await cartApi.addToCart(item.product_id, item.quantity)
      }
      
      // Очищаем гостевую корзину
      clearGuestCart()
      
      // Загружаем обновленную корзину
      await get().fetchCart()
      
      set({ guestCart: { items: [] }, isLoading: false })
    } catch (error: any) {
      // Если 401 - игнорируем, пользователь не авторизован
      if (error.response?.status === 401) {
        set({ isLoading: false })
        return
      }
      console.error('Error syncing guest cart:', error)
      set({ isLoading: false })
    }
  },

  getItemsCount: () => {
    const { cart, guestCart } = get()
    if (cart !== null) {
      return cart?.items_count || 0
    }
    return guestCart.items.reduce((sum, item) => sum + item.quantity, 0)
  },

  getTotal: () => {
    const { cart, guestCart } = get()
    if (cart !== null) {
      return cart?.total || 0
    }
    return guestCart.items.reduce((sum, item) => {
      const price = item.product?.price || 0
      return sum + (price * item.quantity)
    }, 0)
  },
}))
