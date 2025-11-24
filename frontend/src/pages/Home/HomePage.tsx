import { useQuery } from '@tanstack/react-query'
import { Link, useNavigate } from 'react-router-dom'
import { categoriesApi } from '../../api'
import { useFiltersStore } from '../../store/filtersStore'
import './HomePage.css'

export default function HomePage() {
  const navigate = useNavigate()
  const { setFilter } = useFiltersStore()
  
  const { data: categories = [] } = useQuery({
    queryKey: ['categories'],
    queryFn: categoriesApi.getCategories
  })

  const handleCategoryClick = (categoryId: string) => {
    setFilter('category_id', categoryId)
    navigate('/catalog')
  }

  return (
    <div className="home-page">
      <div className="home-page__container">
        {/* Hero Section */}
        <section className="hero">
          <h1>🛒 Еду на базар</h1>
          <p className="hero__subtitle">Маркетплейс фермерских хозяйств</p>
          <p className="hero__description">Покупайте свежие продукты напрямую у производителей без посредников</p>
          <div className="hero__buttons">
            <Link to="/catalog" className="hero__button">
              Перейти в каталог
            </Link>
            <Link to="/map" className="hero__button hero__button--secondary">
              На карту
            </Link>
          </div>
        </section>

        {/* Categories */}
        <section className="categories">
          <div className="categories__grid">
            {categories?.map((category: any) => (
              <div
                key={category.id}
                onClick={() => handleCategoryClick(category.id)}
                className="category-card"
                style={{ cursor: 'pointer' }}
              >
                <div className="category-card__icon">{category.image || category.icon}</div>
                <div className="category-card__name">{category.name}</div>
              </div>
            ))}
          </div>
        </section>

        {/* Features */}
        <section className="features">
          <div className="feature">
            <div className="feature__icon">🌾</div>
            <h3>Напрямую от фермеров</h3>
            <p>Без посредников и наценок</p>
          </div>
          <div className="feature">
            <div className="feature__icon">✨</div>
            <h3>100% свежесть</h3>
            <p>Продукты прямо с полей и ферм</p>
          </div>
          <div className="feature">
            <div className="feature__icon">🤝</div>
            <h3>Поддержка фермеров</h3>
            <p>Помогаем местным производителям</p>
          </div>
          <div className="feature">
            <div className="feature__icon">🚚</div>
            <h3>Быстрая доставка</h3>
            <p>Свежие продукты к вашему столу</p>
          </div>
        </section>
      </div>
    </div>
  )
}
