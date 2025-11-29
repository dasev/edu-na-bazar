import { PieChart, Series, Label, Connector, Tooltip, Legend } from 'devextreme-react/pie-chart'

interface Category {
  name: string
  icon: string
  count: number
}

interface CategoriesPieChartProps {
  data: Category[]
}

export const CategoriesPieChart = ({ data }: CategoriesPieChartProps) => {
  return (
    <div className="chart-section">
      <PieChart
        dataSource={data}
        title="Распределение товаров по категориям"
        palette="Soft Pastel"
      >
        <Series
          argumentField="name"
          valueField="count"
        >
          <Label visible={true} format="fixedPoint">
            <Connector visible={true} />
          </Label>
        </Series>
        <Tooltip enabled={true} />
        <Legend visible={true} verticalAlignment="bottom" horizontalAlignment="center" />
      </PieChart>
    </div>
  )
}
