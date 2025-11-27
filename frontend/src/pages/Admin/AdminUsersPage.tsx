import { useState, useRef } from 'react'
import { Button } from 'devextreme-react/button'
import { locale, loadMessages } from 'devextreme/localization'
import { useUsersData, User } from './hooks/useUsersData'
import { UserStatsCards } from './components/UserStatsCards'
import { UserDataGrid } from './components/UserDataGrid'
import { UserEditForm } from './components/UserEditForm'
import './AdminUsersPage.css'

loadMessages({
  'ru': {
    'dxDataGrid-filterRowShowAllText': 'Все',
    'dxDataGrid-filterRowResetOperationText': 'Сброс',
    'dxDataGrid-filterRowOperationEquals': 'Равно',
    'dxDataGrid-filterRowOperationNotEquals': 'Не равно',
    'dxDataGrid-filterRowOperationLess': 'Меньше',
    'dxDataGrid-filterRowOperationLessOrEquals': 'Меньше или равно',
    'dxDataGrid-filterRowOperationGreater': 'Больше',
    'dxDataGrid-filterRowOperationGreaterOrEquals': 'Больше или равно',
    'dxDataGrid-filterRowOperationStartsWith': 'Начинается с',
    'dxDataGrid-filterRowOperationContains': 'Содержит',
    'dxDataGrid-filterRowOperationNotContains': 'Не содержит',
    'dxDataGrid-filterRowOperationEndsWith': 'Заканчивается на',
    'dxDataGrid-filterRowOperationBetween': 'Между',
    'dxDataGrid-trueText': 'Да',
    'dxDataGrid-falseText': 'Нет',
    'dxDataGrid-searchPanelPlaceholder': 'Поиск...',
    'dxDataGrid-noDataText': 'Нет данных',
  }
})
locale('ru')

export default function AdminUsersPage() {
  const [filterValue, setFilterValue] = useState<'all' | 'active' | 'moderators'>('all')
  const [editingUser, setEditingUser] = useState<User | null>(null)
  const [showEditPopup, setShowEditPopup] = useState(false)
  const [refreshKey, setRefreshKey] = useState(0)
  const gridRef = useRef<any>(null)

  const { stats, dataSource, updateMutation, deleteMutation } = useUsersData(filterValue)

  const handleRowDblClick = (e: any) => {
    setEditingUser({ ...e.data })
    setShowEditPopup(true)
  }

  const handleSave = (user: User) => {
    updateMutation.mutate({
      id: user.id,
      updates: {
        full_name: user.full_name,
        email: user.email,
        address: user.address,
        is_active: user.is_active,
        is_verified: user.is_verified,
        is_moderator: user.is_moderator
      }
    }, {
      onSuccess: () => {
        setShowEditPopup(false)
        setRefreshKey(prev => prev + 1)
      }
    })
  }

  const handleDelete = (id: number) => {
    if (window.confirm('Вы уверены, что хотите удалить этого пользователя?')) {
      deleteMutation.mutate(id, {
        onSuccess: () => {
          setShowEditPopup(false)
          setRefreshKey(prev => prev + 1)
        }
      })
    }
  }

  const handleRefresh = () => {
    setRefreshKey(prev => prev + 1)
  }

  return (
    <div className="admin-page">
      <div className="page-header">
        <h1> Управление пользователями</h1>
        <Button 
          text="Обновить" 
          icon="refresh" 
          onClick={handleRefresh} 
          stylingMode="outlined"
        />
      </div>
      
      <UserStatsCards 
        stats={stats} 
        filterValue={filterValue} 
        onFilterChange={setFilterValue} 
      />
      
      <UserDataGrid 
        key={refreshKey}
        ref={gridRef}
        dataSource={dataSource} 
        onRowDblClick={handleRowDblClick} 
      />
      
      <UserEditForm 
        visible={showEditPopup}
        user={editingUser}
        onHide={() => setShowEditPopup(false)}
        onSave={handleSave}
        onDelete={handleDelete}
        onChange={setEditingUser}
      />
    </div>
  )
}
