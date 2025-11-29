import { useGeoAnalytics } from '../hooks/useGeoAnalytics'
import { Chart, Series, ArgumentAxis, ValueAxis, Legend, Tooltip, Label } from 'devextreme-react/chart'
import { DataGrid, Column } from 'devextreme-react/data-grid'
import { PieChart, Label as PieLabel, Connector } from 'devextreme-react/pie-chart'

interface GeoDashboardProps {
  isActive: boolean
}

export default function GeoDashboard({ isActive }: GeoDashboardProps) {
  const { data, isLoading } = useGeoAnalytics(isActive)

  if (isLoading) {
    return <div className="dashboard-loading">Загрузка географической аналитики...</div>
  }

  if (!data) {
    return <div className="dashboard-error">Нет данных</div>
  }

  return (
    <div className="geo-dashboard">
      {/* Топ городов */}
      <div className="chart-section">
        <h2>Топ-10 городов</h2>
        <DataGrid
          dataSource={data.top_cities}
          showBorders={true}
          columnAutoWidth={true}
        >
          <Column dataField="city" caption="Город" />
          <Column dataField="orders" caption="Заказы" />
          <Column 
            dataField="revenue" 
            caption="Выручка (₽)" 
            format={{ type: 'fixedPoint', precision: 2 }}
          />
          <Column dataField="users" caption="Пользователи" />
        </DataGrid>
      </div>

      {/* Заказы по городам */}
      <div className="chart-section">
        <h2>Заказы по городам</h2>
        <Chart
          dataSource={data.orders_by_city.slice(0, 10)}
          rotated={true}
        >
          <Series
            valueField="orders_count"
            argumentField="city"
            type="bar"
            color="#667eea"
          />
          <ArgumentAxis>
            <Label overlappingBehavior="rotate" rotationAngle={-45} />
          </ArgumentAxis>
          <ValueAxis title="Количество заказов" />
          <Tooltip enabled={true} />
          <Legend visible={false} />
        </Chart>
      </div>

      {/* Выручка по городам (Pie) */}
      <div className="chart-section">
        <h2>Распределение выручки по городам</h2>
        <PieChart
          dataSource={data.revenue_by_city.slice(0, 10)}
          palette="Soft Pastel"
          title="Выручка по городам"
        >
          <Series
            argumentField="city"
            valueField="revenue"
          >
            <Label visible={true} format={{ type: 'fixedPoint', precision: 0 }}>
              <Connector visible={true} />
            </Label>
          </Series>
          <Legend
            orientation="horizontal"
            itemTextPosition="right"
            horizontalAlignment="center"
            verticalAlignment="bottom"
          />
          <Tooltip enabled={true} format={{ type: 'fixedPoint', precision: 2 }} />
        </PieChart>
      </div>

      {/* Конверсия по городам */}
      <div className="chart-section">
        <h2>Конверсия по городам</h2>
        <DataGrid
          dataSource={data.conversion_by_city}
          showBorders={true}
          columnAutoWidth={true}
        >
          <Column dataField="city" caption="Город" />
          <Column dataField="orders" caption="Заказы" />
          <Column dataField="users" caption="Пользователи" />
          <Column 
            dataField="conversion_rate" 
            caption="Конверсия (%)" 
            format={{ type: 'fixedPoint', precision: 2 }}
          />
        </DataGrid>
      </div>
    </div>
  )
}
