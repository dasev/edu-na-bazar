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
  const [userMenuVisible, setUserMenuVisible] = useState(false)
  const [searchValue, setSearchValue] = useState('')
  const { isAuthenticated, user, login, logout } = useAuthStore()
  const { getItemsCount, fetchCart, syncGuestCart } = useCartStore()
  const { setFilter } = useFiltersStore()
  
  // Загружаем корзину при монтировании если пользователь авторизован
  useEffect(() => {
    if (user && isAuthenticated) {
      // Синхронизируем гостевую корзину с серверной
      syncGuestCart().then(() => {
        fetchCart().catch(() => {})
      }).catch(() => {
        // Игнорируем ошибки синхронизации
      })
    }
  }, [user, isAuthenticated, fetchCart, syncGuestCart])

  // Закрытие меню при клике вне его
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as HTMLElement
      if (userMenuVisible && !target.closest('.ozon-header__user')) {
        setUserMenuVisible(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [userMenuVisible])
  
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
          <Link to="/map" className="header__nav-link">
            Карта
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
                <div 
                  className="user-avatar" 
                  title={user?.full_name || user?.phone}
                  onClick={() => setUserMenuVisible(!userMenuVisible)}
                >
                  👤
                </div>
                
                {/* Выпадающее меню */}
                {userMenuVisible && (
                  <div className="user-menu">
                    <div className="user-menu__header">
                      <div className="user-menu__name">{user?.full_name}</div>
                      <div className="user-menu__phone">{user?.phone}</div>
                    </div>
                    <div className="user-menu__divider"></div>
                    <div className="user-menu__items">
                      <div 
                        className="user-menu__item"
                        onClick={() => {
                          setUserMenuVisible(false)
                          navigate('/orders')
                        }}
                      >
                        <span className="user-menu__icon">📦</span>
                        <span>Мои заказы</span>
                      </div>
                      <div 
                        className="user-menu__item"
                        onClick={() => {
                          setUserMenuVisible(false)
                          navigate('/my-stores')
                        }}
                      >
                        <span className="user-menu__icon">🏪</span>
                        <span>Мои магазины</span>
                      </div>
                      <div 
                        className="user-menu__item user-menu__item--danger"
                        onClick={() => {
                          setUserMenuVisible(false)
                          logout()
                        }}
                      >
                        <span className="user-menu__icon">🚪</span>
                        <span>Выйти</span>
                      </div>
                    </div>
                  </div>
                )}
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
