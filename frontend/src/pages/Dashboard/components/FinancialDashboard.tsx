import { Chart, Series, ArgumentAxis, ValueAxis, Label, Tooltip, Legend, CommonSeriesSettings } from 'devextreme-react/chart'
import { PieChart, Series as PieSeries, Label as PieLabel, Connector } from 'devextreme-react/pie-chart'
import { LoadIndicator } from 'devextreme-react/load-indicator'
import { useFinancialData } from '../hooks/useFinancialData'

interface FinancialDashboardProps {
  isActive: boolean
}

export const FinancialDashboard = ({ isActive }: FinancialDashboardProps) => {
  const { data, isLoading } = useFinancialData(30, isActive)

  if (isLoading) {
    return (
      <div className="dashboard-loading">
        <LoadIndicator visible={true} />
        <p>Загрузка финансовой аналитики...</p>
      </div>
    )
  }

  if (!data) {
    return <div className="dashboard-error">Нет данных</div>
  }

  return (
    <div className="financial-dashboard">
      {/* Карточки с общей статистикой */}
      <div className="stats-cards">
        <div className="stat-card stat-card--revenue">
          <div className="stat-card__icon">💰</div>
          <div className="stat-card__content">
            <div className="stat-card__value">{data.total_revenue.toLocaleString('ru-RU')} ₽</div>
            <div className="stat-card__label">Общая выручка</div>
          </div>
        </div>

        <div className="stat-card stat-card--avg-order">
          <div className="stat-card__icon">🧾</div>
          <div className="stat-card__content">
            <div className="stat-card__value">{data.avg_order_value.toLocaleString('ru-RU')} ₽</div>
            <div className="stat-card__label">Средний чек</div>
          </div>
        </div>
      </div>

      {/* График выручки */}
      <div className="chart-section">
        <Chart
          dataSource={data.daily_stats}
          title="Динамика выручки за 30 дней"
        >
          <CommonSeriesSettings argumentField="date" />
          <Series
            valueField="revenue"
            name="Выручка (₽)"
            type="spline"
            color="#4caf50"
          />
          <ArgumentAxis>
            <Label format="dd.MM" />
          </ArgumentAxis>
          <ValueAxis>
            <Label format="#,##0 ₽" />
          </ValueAxis>
          <Tooltip enabled={true} format="#,##0 ₽" />
          <Legend visible={true} verticalAlignment="bottom" horizontalAlignment="center" />
        </Chart>
      </div>

      {/* График среднего чека */}
      <div className="chart-section">
        <Chart
          dataSource={data.daily_stats}
          title="Средний чек по дням"
        >
          <CommonSeriesSettings argumentField="date" />
          <Series
            valueField="avg_order_value"
            name="Средний чек (₽)"
            type="bar"
            color="#ff9800"
          />
          <ArgumentAxis>
            <Label format="dd.MM" />
          </ArgumentAxis>
          <ValueAxis>
            <Label format="#,##0 ₽" />
          </ValueAxis>
          <Tooltip enabled={true} format="#,##0 ₽" />
          <Legend visible={true} verticalAlignment="bottom" horizontalAlignment="center" />
        </Chart>
      </div>

      {/* Топ товаров по выручке */}
      <div className="chart-section">
        <Chart
          dataSource={data.top_products_by_revenue}
          title="Топ-10 товаров по выручке"
          rotated={true}
        >
          <Series
            argumentField="name"
            valueField="revenue"
            type="bar"
            color="#667eea"
          />
          <ArgumentAxis />
          <ValueAxis>
            <Label format="#,##0 ₽" />
          </ValueAxis>
          <Tooltip enabled={true} format="#,##0 ₽" />
          <Legend visible={false} />
        </Chart>
      </div>

      {/* Выручка по категориям */}
      <div className="chart-section">
        <PieChart
          dataSource={data.revenue_by_category}
          title="Выручка по категориям"
          palette="Soft Pastel"
        >
          <PieSeries
            argumentField="name"
            valueField="revenue"
          >
            <PieLabel visible={true} format="#,##0 ₽">
              <Connector visible={true} />
            </PieLabel>
          </PieSeries>
          <Tooltip enabled={true} format="#,##0 ₽" />
          <Legend visible={true} verticalAlignment="bottom" horizontalAlignment="center" />
        </PieChart>
      </div>
    </div>
  )
}
