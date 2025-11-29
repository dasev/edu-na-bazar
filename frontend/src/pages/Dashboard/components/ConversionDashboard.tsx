import { Chart, Series, ArgumentAxis, ValueAxis, Label, Tooltip, Legend, CommonSeriesSettings } from 'devextreme-react/chart'
import { Funnel, Item as FunnelItem, Label as FunnelLabel } from 'devextreme-react/funnel'
import { LoadIndicator } from 'devextreme-react/load-indicator'
import { useConversionData } from '../hooks/useConversionData'

interface ConversionDashboardProps {
  isActive: boolean
}

export const ConversionDashboard = ({ isActive }: ConversionDashboardProps) => {
  const { data, isLoading } = useConversionData(30, isActive)

  if (isLoading) {
    return (
      <div className="dashboard-loading">
        <LoadIndicator visible={true} />
        <p>Загрузка аналитики конверсии...</p>
      </div>
    )
  }

  if (!data) {
    return <div className="dashboard-error">Нет данных</div>
  }

  // Данные для воронки
  const funnelData = [
    { stage: 'Просмотры', value: data.total_views },
    { stage: 'В корзину', value: data.total_cart_adds },
    { stage: 'Заказы', value: data.total_orders }
  ]

  return (
    <div className="conversion-dashboard">
      {/* Карточки с общей статистикой */}
      <div className="stats-cards">
        <div className="stat-card stat-card--conversion">
          <div className="stat-card__content">
            <div className="stat-card__value">{data.overall_conversion_rate.toFixed(2)}%</div>
            <div className="stat-card__label">Общая конверсия</div>
          </div>
        </div>

        <div className="stat-card stat-card--cart-conversion">
          <div className="stat-card__content">
            <div className="stat-card__value">{data.cart_to_order_rate.toFixed(2)}%</div>
            <div className="stat-card__label">Корзина → Заказ</div>
          </div>
        </div>

        <div className="stat-card stat-card--abandoned">
          <div className="stat-card__content">
            <div className="stat-card__value">{data.abandoned_carts}</div>
            <div className="stat-card__label">Брошенные корзины</div>
          </div>
        </div>
      </div>

      {/* Микро-конверсии */}
      <div className="stats-cards">
        <div className="stat-card stat-card--clicks">
          <div className="stat-card__content">
            <div className="stat-card__value">{data.product_clicks}</div>
            <div className="stat-card__label">Клики по товарам</div>
          </div>
        </div>

        <div className="stat-card stat-card--add-clicks">
          <div className="stat-card__content">
            <div className="stat-card__value">{data.add_to_cart_clicks}</div>
            <div className="stat-card__label">Клики "В корзину"</div>
          </div>
        </div>

        <div className="stat-card stat-card--checkout">
          <div className="stat-card__content">
            <div className="stat-card__value">{data.checkout_starts}</div>
            <div className="stat-card__label">Начало оформления</div>
          </div>
        </div>
      </div>

      {/* Временные метрики */}
      <div className="stats-cards">
        <div className="stat-card stat-card--time">
          <div className="stat-card__content">
            <div className="stat-card__value">{data.avg_time_to_purchase.toFixed(0)} мин</div>
            <div className="stat-card__label">Среднее время до покупки</div>
          </div>
        </div>

        <div className="stat-card stat-card--cart-value">
          <div className="stat-card__content">
            <div className="stat-card__value">{data.abandoned_cart_value.toLocaleString('ru-RU')} ₽</div>
            <div className="stat-card__label">Средняя брошенная корзина</div>
          </div>
        </div>
      </div>

      {/* Воронка продаж */}
      <div className="chart-section">
        <Funnel
          dataSource={funnelData}
          argumentField="stage"
          valueField="value"
          title="Воронка продаж"
          palette="Soft Pastel"
        >
          <FunnelItem>
            <FunnelLabel visible={true} />
          </FunnelItem>
          <Tooltip enabled={true} />
        </Funnel>
      </div>

      {/* График конверсии по дням */}
      <div className="chart-section">
        <Chart
          dataSource={data.daily_stats}
          title="Динамика конверсии за 30 дней"
        >
          <CommonSeriesSettings argumentField="date" />
          <Series
            valueField="conversion_rate"
            name="Конверсия (%)"
            type="spline"
            color="#667eea"
          />
          <ArgumentAxis>
            <Label format="dd.MM" />
          </ArgumentAxis>
          <ValueAxis>
            <Label format="#0.##%" />
          </ValueAxis>
          <Tooltip enabled={true} format="#0.##%" />
          <Legend visible={true} verticalAlignment="bottom" horizontalAlignment="center" />
        </Chart>
      </div>

      {/* График воронки по дням */}
      <div className="chart-section">
        <Chart
          dataSource={data.daily_stats}
          title="Воронка по дням"
        >
          <CommonSeriesSettings argumentField="date" />
          <Series
            valueField="views"
            name="Просмотры"
            type="line"
            color="#667eea"
          />
          <Series
            valueField="cart_adds"
            name="В корзину"
            type="line"
            color="#ff9800"
          />
          <Series
            valueField="orders"
            name="Заказы"
            type="line"
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

      {/* Конверсия по категориям */}
      <div className="chart-section">
        <Chart
          dataSource={data.conversion_by_category}
          title="Конверсия по категориям"
          rotated={true}
        >
          <Series
            argumentField="name"
            valueField="conversion_rate"
            type="bar"
            color="#764ba2"
          />
          <ArgumentAxis />
          <ValueAxis>
            <Label format="#0.##%" />
          </ValueAxis>
          <Tooltip enabled={true} format="#0.##%" />
          <Legend visible={false} />
        </Chart>
      </div>
    </div>
  )
}
