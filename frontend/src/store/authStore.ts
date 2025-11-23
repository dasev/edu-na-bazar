/**
 * Auth Store - управление состоянием аутентификации
 */
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: string
  phone: string
  email?: string
  full_name: string
  is_verified: boolean
  created_at: string
  last_login?: string
}

interface AuthState {
  token: string | null
  user: User | null
  isAuthenticated: boolean
  
  // Actions
  login: (token: string, user: User) => void
  logout: () => void
  updateUser: (user: User) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      isAuthenticated: false,

      login: (token: string, user: User) => {
        // Сохраняем токен в localStorage для API client
        localStorage.setItem('auth_token', token)
        localStorage.setItem('user', JSON.stringify(user))
        
        set({
          token,
          user,
          isAuthenticated: true
        })
      },

      logout: () => {
        localStorage.removeItem('auth_token')
        localStorage.removeItem('user')
        set({
          token: null,
          user: null,
          isAuthenticated: false
        })
      },

      updateUser: (user: User) => {
        set({ user })
      }
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        token: state.token,
        user: state.user,
        isAuthenticated: state.isAuthenticated
      }),
      onRehydrateStorage: () => (state) => {
        // После загрузки из persist синхронизируем с localStorage
        if (state?.token) {
          localStorage.setItem('auth_token', state.token)
        }
        if (state?.user) {
          localStorage.setItem('user', JSON.stringify(state.user))
        }
      }
    }
  )
)

// Принудительная синхронизация при загрузке модуля
// Это гарантирует что токен будет в localStorage даже если onRehydrateStorage не сработал
setTimeout(() => {
  const state = useAuthStore.getState()
  if (state.token && !localStorage.getItem('auth_token')) {
    localStorage.setItem('auth_token', state.token)
    console.log('🔄 Токен синхронизирован с localStorage')
  }
  if (state.user && !localStorage.getItem('user')) {
    localStorage.setItem('user', JSON.stringify(state.user))
  }
}, 100)
