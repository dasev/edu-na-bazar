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
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="app">
          <Header />
          <Toaster position="top-right" />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/catalog" element={<CatalogPage />} />
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
