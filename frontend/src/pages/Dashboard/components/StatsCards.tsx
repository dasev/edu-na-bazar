interface StatsCardsProps {
  totalProducts: number
  totalStores: number
  totalOrders: number
  totalUsers: number
}

export const StatsCards = ({ totalProducts, totalStores, totalOrders, totalUsers }: StatsCardsProps) => {
  return (
    <div className="stats-cards">
      <div className="stat-card stat-card--products">
        <div className="stat-card__icon">📦</div>
        <div className="stat-card__content">
          <div className="stat-card__value">{totalProducts}</div>
          <div className="stat-card__label">Товаров</div>
        </div>
      </div>

      <div className="stat-card stat-card--stores">
        <div className="stat-card__icon">🏪</div>
        <div className="stat-card__content">
          <div className="stat-card__value">{totalStores}</div>
          <div className="stat-card__label">Магазинов</div>
        </div>
      </div>

      <div className="stat-card stat-card--orders">
        <div className="stat-card__icon">🛒</div>
        <div className="stat-card__content">
          <div className="stat-card__value">{totalOrders}</div>
          <div className="stat-card__label">Заказов</div>
        </div>
      </div>

      <div className="stat-card stat-card--users">
        <div className="stat-card__icon">👥</div>
        <div className="stat-card__content">
          <div className="stat-card__value">{totalUsers}</div>
          <div className="stat-card__label">Пользователей</div>
        </div>
      </div>
    </div>
  )
}
