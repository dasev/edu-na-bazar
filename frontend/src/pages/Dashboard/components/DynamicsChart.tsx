import { Chart, Series, ArgumentAxis, ValueAxis, Label, Tooltip, Legend, CommonSeriesSettings } from 'devextreme-react/chart'
import { DailyStats } from '../hooks/useDashboardData'

interface DynamicsChartProps {
  data: DailyStats[]
  valueField: 'products' | 'stores' | 'orders' | 'users'
  title: string
  seriesName: string
  color: string
  type?: 'spline' | 'bar' | 'line'
}

export const DynamicsChart = ({ 
  data, 
  valueField, 
  title, 
  seriesName, 
  color,
  type = 'spline'
}: DynamicsChartProps) => {
  return (
    <div className="chart-section">
      <Chart
        dataSource={data}
        title={title}
      >
        <CommonSeriesSettings argumentField="date" />
        <Series
          valueField={valueField}
          name={seriesName}
          type={type}
          color={color}
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
  )
}
