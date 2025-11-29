import { useProductAnalytics } from '../hooks/useProductAnalytics'
import { Chart, Series, ArgumentAxis, ValueAxis, Legend, Tooltip, Label } from 'devextreme-react/chart'
import { DataGrid, Column } from 'devextreme-react/data-grid'

interface ProductAnalyticsDashboardProps {
  isActive: boolean
}

export default function ProductAnalyticsDashboard({ isActive }: ProductAnalyticsDashboardProps) {
  const { data, isLoading } = useProductAnalytics(isActive)

  if (isLoading) {
    return <div className="dashboard-loading">Загрузка товарной аналитики...</div>
  }

  if (!data) {
    return <div className="dashboard-error">Нет данных</div>
  }

  return (
    <div className="product-analytics-dashboard">
      {/* Топ товаров по конверсии */}
      <div className="chart-section">
        <h2>Топ товаров по конверсии</h2>
        <Chart
          dataSource={data.top_products_by_conversion}
          rotated={true}
        >
          <Series
            valueField="conversion_rate"
            argumentField="name"
            type="bar"
            color="#667eea"
          />
          <ArgumentAxis>
            <Label overlappingBehavior="rotate" rotationAngle={-45} />
          </ArgumentAxis>
          <ValueAxis title="Конверсия (%)" />
          <Tooltip enabled={true} />
          <Legend visible={false} />
        </Chart>
      </div>

      {/* Худшие товары */}
      <div className="chart-section">
        <h2>Товары с низкой конверсией</h2>
        <DataGrid
          dataSource={data.worst_products_by_conversion}
          showBorders={true}
          columnAutoWidth={true}
        >
          <Column dataField="name" caption="Товар" />
          <Column dataField="views" caption="Просмотры" />
          <Column dataField="orders" caption="Заказы" />
          <Column 
            dataField="conversion_rate" 
            caption="Конверсия (%)" 
            format={{ type: 'fixedPoint', precision: 2 }}
          />
        </DataGrid>
      </div>

      {/* Товары-локомотивы */}
      <div className="chart-section">
        <h2>Товары-локомотивы</h2>
        <p style={{ color: '#666', marginBottom: '16px' }}>
          Товары, которые часто покупаются вместе с другими
        </p>
        <Chart
          dataSource={data.locomotive_products}
          rotated={true}
        >
          <Series
            valueField="avg_items_in_order"
            argumentField="name"
            type="bar"
            color="#4caf50"
          />
          <ArgumentAxis>
            <Label overlappingBehavior="rotate" rotationAngle={-45} />
          </ArgumentAxis>
          <ValueAxis title="Среднее кол-во товаров в заказе" />
          <Tooltip enabled={true} />
          <Legend visible={false} />
        </Chart>
      </div>

      {/* Cross-sell пары */}
      <div className="chart-section">
        <h2>Cross-sell: товары, покупаемые вместе</h2>
        <DataGrid
          dataSource={data.cross_sell_pairs}
          showBorders={true}
          columnAutoWidth={true}
        >
          <Column dataField="product1" caption="Товар 1" />
          <Column dataField="product2" caption="Товар 2" />
          <Column dataField="frequency" caption="Частота" />
        </DataGrid>
      </div>
    </div>
  )
}
