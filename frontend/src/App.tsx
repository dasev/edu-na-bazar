import { useEffect } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'react-hot-toast'
import Header from './components/Header/Header'
import HomePage from './pages/Home/HomePage'
import CatalogPage from './pages/Catalog/CatalogPage'
import ProductPage from './pages/Product/ProductPage'
import CartPage from './pages/Cart/CartPage'
import CheckoutPage from './pages/Checkout/CheckoutPage'
import { OrdersPage } from './pages/Orders/OrdersPage'
import { MyStoresPage } from './pages/MyStores/MyStoresPage'
import { CreateStorePage } from './pages/MyStores/CreateStorePage'
import StoreProductsPage from './pages/StoreProducts/StoreProductsPage'
import ProductEditPage from './pages/StoreProducts/ProductEditPage'
import StoresPage from './pages/Stores/StoresPage'
import MapPage from './pages/Map/MapPage'
import { NotFoundPage } from './pages/NotFound/NotFoundPage'
import { AboutPage } from './pages/About/AboutPage'
import './App.css'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 минут - данные считаются свежими
      gcTime: 10 * 60 * 1000, // 10 минут - время хранения в кэше
      refetchOnWindowFocus: false, // Не перезапрашивать при фокусе окна
      refetchOnMount: false, // Не перезапрашивать при монтировании если есть кэш
      retry: 1, // Только 1 повтор при ошибке
    },
  },
})

function App() {
  // Автоматически закрываем панель DevExpress trial (эмулируем клик по крестику)
  useEffect(() => {
    const closeDevExpressBanner = (): boolean => {
      // Ищем элемент dx-license
      const dxLicense = document.querySelector('dx-license')
      
      if (!dxLicense) {
        return false
      }
      
      // Ищем div с cursor: pointer внутри dx-license (это кнопка закрытия)
      const allDivs = dxLicense.querySelectorAll('div')
      
      for (const div of allDivs) {
        const element = div as HTMLElement
        const style = window.getComputedStyle(element)
        
        // Кнопка закрытия имеет cursor: pointer и содержит SVG
        if (style.cursor === 'pointer' && element.querySelector('svg')) {
          // Кликаем по кнопке
          element.click()
          
          // Также пробуем dispatchEvent для надежности
          const clickEvent = new MouseEvent('click', {
            bubbles: true,
            cancelable: true,
            view: window
          })
          element.dispatchEvent(clickEvent)
          
          return true
        }
      }
      
      return false
    }
    
    // Запускаем сразу и с очень коротким интервалом
    closeDevExpressBanner() // Первая попытка сразу
    
    let attempts = 0
    const timer = setInterval(() => {
      attempts++
      if (closeDevExpressBanner()) {
        clearInterval(timer)
      }
      if (attempts >= 100) { // Максимум 100 попыток (1 секунда)
        clearInterval(timer)
      }
    }, 10) // Проверяем каждые 10мс
    
    return () => clearInterval(timer)
  }, [])

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="app">
          <Header />
          <Toaster 
            position="bottom-right"
            toastOptions={{
              duration: 3000,
              style: {
                background: '#363636',
                color: '#fff',
              },
              success: {
                duration: 3000,
                iconTheme: {
                  primary: '#4CAF50',
                  secondary: '#fff',
                },
              },
              error: {
                duration: 4000,
                iconTheme: {
                  primary: '#f44336',
                  secondary: '#fff',
                },
              },
            }}
          />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/catalog" element={<CatalogPage />} />
              <Route path="/map" element={<MapPage />} />
              <Route path="/product/:id" element={<ProductPage />} />
              <Route path="/cart" element={<CartPage />} />
              <Route path="/checkout" element={<CheckoutPage />} />
              <Route path="/orders" element={<OrdersPage />} />
              <Route path="/stores" element={<StoresPage />} />
              <Route path="/my-stores" element={<MyStoresPage />} />
              <Route path="/my-stores/create" element={<CreateStorePage />} />
              <Route path="/my-stores/:storeId/products" element={<StoreProductsPage />} />
              <Route path="/my-stores/:storeId/products/:productId" element={<ProductEditPage />} />
              <Route path="/about" element={<AboutPage />} />
              <Route path="*" element={<NotFoundPage />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App
