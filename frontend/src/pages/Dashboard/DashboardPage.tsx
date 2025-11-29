import { useState } from 'react'
import { TabPanel, Item } from 'devextreme-react/tab-panel'
import { LoadIndicator } from 'devextreme-react/load-indicator'
import { useDashboardData } from './hooks/useDashboardData'
import { StatsCards } from './components/StatsCards'
import { DynamicsChart } from './components/DynamicsChart'
import { CategoriesPieChart } from './components/CategoriesPieChart'
import { FinancialDashboard } from './components/FinancialDashboard'
import { UserActivityDashboard } from './components/UserActivityDashboard'
import { ConversionDashboard } from './components/ConversionDashboard'
import ProductAnalyticsDashboard from './components/ProductAnalyticsDashboard'
import GeoDashboard from './components/GeoDashboard'
import './DashboardPage.css'

export default function DashboardPage() {
  const [selectedTab, setSelectedTab] = useState(0)
  
  // Базовый дашборд загружается всегда
  const { data, isLoading } = useDashboardData(30)

  if (isLoading) {
    return (
      <div className="dashboard-page">
        <div className="dashboard-loading">
          <LoadIndicator visible={true} />
          <p>Загрузка аналитики...</p>
        </div>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="dashboard-page">
        <div className="dashboard-error">Ошибка загрузки данных</div>
      </div>
    )
  }

  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <h1>📊 Дашборды</h1>
        <p className="dashboard-subtitle">Аналитика и статистика маркетплейса</p>
      </div>

      {/* Карточки с общей статистикой */}
      <StatsCards
        totalProducts={data.total_products}
        totalStores={data.total_stores}
        totalOrders={data.total_orders}
        totalUsers={data.total_users}
      />

      {/* Вкладки с разными дашбордами */}
      <TabPanel
        selectedIndex={selectedTab}
        onSelectedIndexChange={setSelectedTab}
        animationEnabled={true}
        swipeEnabled={true}
      >
        <Item title="📊 Общая динамика">
          <div>
            <DynamicsChart
              data={data.daily_stats}
              valueField="products"
              title="Новые товары за последние 30 дней"
              seriesName="Товары"
              color="#667eea"
              type="spline"
            />
            
            <DynamicsChart
              data={data.daily_stats}
              valueField="stores"
              title="Новые магазины за последние 30 дней"
              seriesName="Магазины"
              color="#764ba2"
              type="spline"
            />
            
            <DynamicsChart
              data={data.daily_stats}
              valueField="orders"
              title="Новые заказы за последние 30 дней"
              seriesName="Заказы"
              color="#4caf50"
              type="bar"
            />
            
            <CategoriesPieChart data={data.top_categories} />
          </div>
        </Item>

        <Item title="💰 Финансовая аналитика">
          <FinancialDashboard isActive={selectedTab === 1} />
        </Item>

        <Item title="👥 Активность пользователей">
          <UserActivityDashboard isActive={selectedTab === 2} />
        </Item>

        <Item title="🎯 Конверсия и воронка">
          <ConversionDashboard isActive={selectedTab === 3} />
        </Item>

        <Item title="📦 Товарная аналитика">
          <ProductAnalyticsDashboard isActive={selectedTab === 4} />
        </Item>

        <Item title="🗺️ География">
          <GeoDashboard isActive={selectedTab === 5} />
        </Item>
      </TabPanel>
    </div>
  )
}
