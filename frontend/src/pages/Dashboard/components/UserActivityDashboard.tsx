import { Chart, Series, ArgumentAxis, ValueAxis, Label, Tooltip, Legend, CommonSeriesSettings } from 'devextreme-react/chart'
import { LoadIndicator } from 'devextreme-react/load-indicator'
import { useUserActivityData } from '../hooks/useUserActivityData'

interface UserActivityDashboardProps {
  isActive: boolean
}

export const UserActivityDashboard = ({ isActive }: UserActivityDashboardProps) => {
  const { data, isLoading } = useUserActivityData(30, isActive)

  if (isLoading) {
    return (
      <div className="dashboard-loading">
        <LoadIndicator visible={true} />
        <p>Загрузка аналитики активности...</p>
      </div>
    )
  }

  if (!data) {
    return <div className="dashboard-error">Нет данных</div>
  }

  return (
    <div className="user-activity-dashboard">
      {/* Карточки с общей статистикой */}
      <div className="stats-cards">
        <div className="stat-card stat-card--total-users">
          <div className="stat-card__icon">👥</div>
          <div className="stat-card__content">
            <div className="stat-card__value">{data.total_users}</div>
            <div className="stat-card__label">Всего пользователей</div>
          </div>
        </div>

        <div className="stat-card stat-card--active-today">
          <div className="stat-card__icon">⚡</div>
          <div className="stat-card__content">
            <div className="stat-card__value">{data.active_today}</div>
            <div className="stat-card__label">Активных сегодня</div>
          </div>
        </div>

        <div className="stat-card stat-card--new-month">
          <div className="stat-card__icon">🆕</div>
          <div className="stat-card__content">
            <div className="stat-card__value">{data.new_this_month}</div>
            <div className="stat-card__label">Новых за месяц</div>
          </div>
        </div>

        <div className="stat-card stat-card--retention">
          <div className="stat-card__icon">🔄</div>
          <div className="stat-card__content">
            <div className="stat-card__value">{data.retention_rate.toFixed(1)}%</div>
            <div className="stat-card__label">Retention Rate</div>
          </div>
        </div>
      </div>

      {/* График новых пользователей */}
      <div className="chart-section">
        <Chart
          dataSource={data.daily_stats}
          title="Новые пользователи по дням"
        >
          <CommonSeriesSettings argumentField="date" />
          <Series
            valueField="new_users"
            name="Новые пользователи"
            type="bar"
            color="#667eea"
          />
          <ArgumentAxis>
            <Label format="dd.MM" />
          </ArgumentAxis>
          <ValueAxis>
            <Label />
          </ValueAxis>
          <Tooltip enabled={true} />
          <Legend visible={true} verticalAlignment="bottom" horizontalAlignment="center" />
        </Chart>
      </div>

      {/* График активных пользователей */}
      <div className="chart-section">
        <Chart
          dataSource={data.daily_stats}
          title="Активные пользователи по дням"
        >
          <CommonSeriesSettings argumentField="date" />
          <Series
            valueField="active_users"
            name="Активные пользователи"
            type="spline"
            color="#4caf50"
          />
          <ArgumentAxis>
            <Label format="dd.MM" />
          </ArgumentAxis>
          <ValueAxis>
            <Label />
          </ValueAxis>
          <Tooltip enabled={true} />
          <Legend visible={true} verticalAlignment="bottom" horizontalAlignment="center" />
        </Chart>
      </div>

      {/* График заказов */}
      <div className="chart-section">
        <Chart
          dataSource={data.daily_stats}
          title="Количество заказов по дням"
        >
          <CommonSeriesSettings argumentField="date" />
          <Series
            valueField="orders_made"
            name="Заказы"
            type="area"
            color="#ff9800"
          />
          <ArgumentAxis>
            <Label format="dd.MM" />
          </ArgumentAxis>
          <ValueAxis>
            <Label />
          </ValueAxis>
          <Tooltip enabled={true} />
          <Legend visible={true} verticalAlignment="bottom" horizontalAlignment="center" />
        </Chart>
      </div>

      {/* Топ активных пользователей */}
      <div className="chart-section">
        <Chart
          dataSource={data.top_active_users}
          title="Топ-10 активных пользователей"
          rotated={true}
        >
          <Series
            argumentField="name"
            valueField="orders_count"
            type="bar"
            color="#764ba2"
          />
          <ArgumentAxis />
          <ValueAxis>
            <Label />
          </ValueAxis>
          <Tooltip enabled={true} />
          <Legend visible={false} />
        </Chart>
      </div>
    </div>
  )
}
