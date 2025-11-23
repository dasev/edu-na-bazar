import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Button } from 'devextreme-react/button'
import { DataGrid } from 'devextreme-react/data-grid'
import { Column, Editing, Paging, SearchPanel, Toolbar, Item } from 'devextreme-react/data-grid'
import { apiClient } from '../../api/client'
import './StoreProductsPage.css'

export default function StoreProductsPage() {
  const { storeId } = useParams<{ storeId: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  // Получаем товары магазина
  const { data: productsData, isLoading } = useQuery({
    queryKey: ['store-products', storeId],
    queryFn: async () => {
      const response = await apiClient.get(`/api/my-stores/${storeId}/products`)
      return response.data
    },
  })

  // Получаем категории для выбора
  const { data: categories = [] } = useQuery({
    queryKey: ['categories'],
    queryFn: async () => {
      const response = await apiClient.get('/api/categories/')
      return response.data
    },
  })

  // Создание товара
  const createMutation = useMutation({
    mutationFn: async (data: any) => {
      const response = await apiClient.post(`/api/my-stores/${storeId}/products`, data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['store-products', storeId] })
    },
  })

  // Обновление товара
  const updateMutation = useMutation({
    mutationFn: async ({ id, data }: { id: number; data: any }) => {
      const response = await apiClient.put(`/api/my-stores/${storeId}/products/${id}`, data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['store-products', storeId] })
    },
  })

  // Удаление товара
  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      await apiClient.delete(`/api/my-stores/${storeId}/products/${id}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['store-products', storeId] })
    },
  })

  const products = productsData?.data || []

  const onRowInserting = (e: any) => {
    e.cancel = createMutation.mutateAsync(e.data)
  }

  const onRowUpdating = (e: any) => {
    e.cancel = updateMutation.mutateAsync({
      id: e.key,
      data: e.newData,
    })
  }

  const onRowRemoving = (e: any) => {
    e.cancel = deleteMutation.mutateAsync(e.key)
  }

  if (isLoading) {
    return <div className="store-products-page">Загрузка...</div>
  }

  return (
    <div className="store-products-page">
      <div className="page-header">
        <Button
          icon="back"
          text="Назад к магазинам"
          onClick={() => navigate('/my-stores')}
        />
        <h1>Товары магазина</h1>
      </div>

      <DataGrid
        dataSource={products}
        keyExpr="id"
        showBorders={true}
        columnAutoWidth={true}
        onRowInserting={onRowInserting}
        onRowUpdating={onRowUpdating}
        onRowRemoving={onRowRemoving}
      >
        <SearchPanel visible={true} width={240} placeholder="Поиск..." />
        <Editing
          mode="popup"
          allowAdding={true}
          allowUpdating={true}
          allowDeleting={true}
          popup={{
            title: 'Товар',
            showTitle: true,
            width: 700,
            height: 525,
          }}
        />
        <Paging defaultPageSize={20} />

        <Column dataField="id" caption="ID" width={70} allowEditing={false} />
        <Column dataField="name" caption="Название" />
        <Column dataField="description" caption="Описание" />
        <Column
          dataField="price"
          caption="Цена"
          dataType="number"
          format="currency"
        />
        <Column
          dataField="category_id"
          caption="Категория"
          lookup={{
            dataSource: categories,
            valueExpr: 'id',
            displayExpr: 'name',
          }}
        />
        <Column
          dataField="in_stock"
          caption="В наличии"
          dataType="boolean"
        />
        <Column dataField="unit" caption="Единица" width={100} />
        <Column
          dataField="rating"
          caption="Рейтинг"
          dataType="number"
          format="#0.0"
          width={100}
        />
        <Column
          dataField="reviews_count"
          caption="Отзывов"
          dataType="number"
          width={100}
        />
        <Column dataField="image" caption="Изображение (URL)" />

        <Toolbar>
          <Item name="addRowButton" />
          <Item name="searchPanel" />
        </Toolbar>
      </DataGrid>
    </div>
  )
}
