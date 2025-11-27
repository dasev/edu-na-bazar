import { forwardRef } from 'react'
import DataGrid, { Column, Scrolling, SearchPanel, FilterRow, ColumnChooser, ColumnFixing, RemoteOperations } from 'devextreme-react/data-grid'
import CustomStore from 'devextreme/data/custom_store'
import { User } from '../hooks/useUsersData'

interface UserDataGridProps {
  dataSource: CustomStore
  onRowDblClick: (e: any) => void
}

export const UserDataGrid = forwardRef<any, UserDataGridProps>(({ dataSource, onRowDblClick }, ref) => {
  return (
    <div className="users-grid-container">
      <DataGrid 
        ref={ref}
        dataSource={dataSource} 
        keyExpr="id" 
        showBorders={false}
        showRowLines={true}
        showColumnLines={false}
        rowAlternationEnabled={true}
        hoverStateEnabled={true}
        allowColumnResizing={true} 
        allowColumnReordering={true}
        columnAutoWidth={true}
        onRowDblClick={onRowDblClick}
      >
        <RemoteOperations sorting={true} paging={true} filtering={true} />
        <Scrolling mode="virtual" rowRenderingMode="virtual" />
        <SearchPanel visible={true} width={300} placeholder="Поиск..." />
        <FilterRow visible={true} />
        <ColumnChooser enabled={true} mode="select" />
        <ColumnFixing enabled={true} />
        
        <Column dataField="id" caption="ID" width={70} alignment="center" fixed={true} allowSearch={false} sortOrder="asc" />
        <Column dataField="phone" caption="Телефон" minWidth={140} />
        <Column dataField="full_name" caption="Имя" minWidth={200} />
        <Column dataField="email" caption="Email" minWidth={220} />
        <Column 
          dataField="is_active" 
          caption="Активен" 
          width={90}
          alignment="center"
          dataType="boolean"
          trueText="Да"
          falseText="Нет"
        />
        <Column 
          dataField="is_moderator" 
          caption="Модератор" 
          width={130}
          alignment="center"
          dataType="boolean"
          trueText="Да"
          falseText="Нет"
          cellRender={(data: any) => data.value ? <span className="badge moderator">⚖️ Модератор</span> : null}
        />
        <Column dataField="stores_count" caption="Магазины" width={100} alignment="center" allowSearch={false} />
        <Column dataField="products_count" caption="Товары" width={90} alignment="center" allowSearch={false} />
        <Column 
          dataField="created_at" 
          caption="Дата регистрации" 
          width={160}
          dataType="datetime"
          format="dd.MM.yyyy HH:mm"
        />
      </DataGrid>
    </div>
  )
})

UserDataGrid.displayName = 'UserDataGrid'
