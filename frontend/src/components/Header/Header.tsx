import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { TextBox } from 'devextreme-react/text-box'
import { Button } from 'devextreme-react/button'
import AuthModal from '../Auth/AuthModal'
import { useAuthStore } from '../../store/authStore'
import { useCartStore } from '../../store/cartStore'
import { useFiltersStore } from '../../store/filtersStore'
import './Header.css'

export default function Header() {
  const navigate = useNavigate()
  const [authModalVisible, setAuthModalVisible] = useState(false)
  const [searchValue, setSearchValue] = useState('')
  const { isAuthenticated, user, login, logout } = useAuthStore()
  const { getItemsCount, fetchCart, syncGuestCart } = useCartStore()
  const { setFilter } = useFiltersStore()
  
  // Загружаем корзину при монтировании если пользователь авторизован
  useEffect(() => {
    if (user) {
      // Синхронизируем гостевую корзину с серверной
      syncGuestCart().then(() => {
        fetchCart().catch(() => {})
      })
    }
  }, [user, fetchCart, syncGuestCart])
  
  const cartItemsCount = getItemsCount()

  const handleSearch = () => {
    if (searchValue.trim()) {
      setFilter('search', searchValue.trim())
      navigate('/catalog')
    }
  }

  const handleSearchKeyPress = (e: any) => {
    if (e.event?.key === 'Enter') {
      handleSearch()
    }
  }

  const handleAuthSuccess = (token: string, userData: any) => {
    login(token, userData)
  }

  return (
    <>
      <header className="ozon-header">
        <div className="ozon-header__container">
          {/* Логотип */}
          <Link to="/" className="ozon-header__logo">
            <h1>🛒 Еду на базар</h1>
          </Link>
          <Link to="/catalog" className="header__nav-link">
            Каталог
          </Link>
          <Link to="/stores" className="header__nav-link">
            Магазины
          </Link>
          <Link to="/about" className="header__nav-link">
            О нас
          </Link>
          {/* Поиск */}
          <div className="ozon-header__search">
            <TextBox
              placeholder="Искать товары"
              mode="search"
              value={searchValue}
              onValueChanged={(e) => setSearchValue(e.value)}
              onEnterKey={handleSearchKeyPress}
              showClearButton={true}
              width="100%"
            />
            <Button
              icon="search"
              onClick={handleSearch}
              stylingMode="contained"
              type="default"
            />
          </div>
          {/* Правая часть */}
          <div className="ozon-header__right">
            {/* Заказы (только для авторизованных) */}
            {isAuthenticated && (
              <Link to="/orders" className="ozon-header__orders">
                <span className="orders-icon">📦</span>
                <span className="orders-text">Заказы</span>
              </Link>
            )}

            {/* Корзина */}
            <Link to="/cart" className="ozon-header__cart">
              <span className="cart-icon">🛒</span>
              {cartItemsCount > 0 && (
                <span className="cart-badge">{cartItemsCount}</span>
              )}
            </Link>

            {/* Авторизация */}
            {isAuthenticated ? (
              <div className="ozon-header__user">
                <span className="user-name">{user?.full_name || user?.phone}</span>
                <Button
                  text="Выйти"
                  type="normal"
                  stylingMode="text"
                  onClick={logout}
                />
              </div>
            ) : (
              <Button
                text="Войти"
                type="default"
                stylingMode="contained"
                onClick={() => setAuthModalVisible(true)}
              />
            )}
          </div>
        </div>
        
        {/* Категории */}
        <div className="ozon-header__categories">
          <nav>
            <Link to="/">Главная</Link>
            <Link to="/catalog">Каталог</Link>
            <Link to="/stores">Магазины</Link>
          </nav>
        </div>
      </header>

      {/* Auth Modal */}
      <AuthModal
        visible={authModalVisible}
        onClose={() => setAuthModalVisible(false)}
        onSuccess={handleAuthSuccess}
      />
    </>
  )
}
