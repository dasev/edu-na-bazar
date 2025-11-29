import { Button } from 'devextreme-react/button'
import { Popup } from 'devextreme-react/popup'
import { Form, SimpleItem, GroupItem, Label } from 'devextreme-react/form'
import { User } from '../hooks/useUsersData'

interface UserEditFormProps {
  visible: boolean
  user: User | null
  onHide: () => void
  onSave: (user: User) => void
  onDelete: (id: number) => void
  onChange: (user: User) => void
}

export const UserEditForm = ({ visible, user, onHide, onSave, onDelete, onChange }: UserEditFormProps) => {
  if (!user) return null

  return (
    <Popup 
      visible={visible} 
      onHiding={onHide} 
      title="Карточка пользователя" 
      width={900}
      height={700}
      showCloseButton={true}
    >
      <div style={{ padding: '10px', height: '100%', display: 'flex', flexDirection: 'column' }}>
        <Form 
          formData={user}
          labelLocation="top"
          colCount={2}
          onFieldDataChanged={(e) => {
            if (e.dataField) {
              onChange({ ...user, [e.dataField]: e.value })
            }
          }}
        >
          <GroupItem caption="Основная информация" colSpan={2} colCount={2}>
            <SimpleItem dataField="id" editorOptions={{ readOnly: true }}>
              <Label text="ID пользователя" />
            </SimpleItem>
            <SimpleItem dataField="phone" editorOptions={{ readOnly: true }}>
              <Label text="Телефон" />
            </SimpleItem>
            <SimpleItem dataField="full_name">
              <Label text="Полное имя" />
            </SimpleItem>
            <SimpleItem dataField="email">
              <Label text="Email" />
            </SimpleItem>
            <SimpleItem dataField="address" colSpan={2}>
              <Label text="Адрес" />
            </SimpleItem>
          </GroupItem>
          
          <GroupItem caption="Статусы и роли" colCount={1}>
            <SimpleItem dataField="is_active" editorType="dxCheckBox" editorOptions={{ text: 'Пользователь активен' }}>
              <Label visible={false} />
            </SimpleItem>
            <SimpleItem dataField="is_verified" editorType="dxCheckBox" editorOptions={{ text: 'Телефон верифицирован (legacy)' }}>
              <Label visible={false} />
            </SimpleItem>
            <SimpleItem dataField="is_email_verified" editorType="dxCheckBox" editorOptions={{ text: 'Email верифицирован', readOnly: true }}>
              <Label visible={false} />
            </SimpleItem>
            <SimpleItem dataField="is_phone_verified" editorType="dxCheckBox" editorOptions={{ text: 'Телефон верифицирован', readOnly: true }}>
              <Label visible={false} />
            </SimpleItem>
            <SimpleItem dataField="is_moderator" editorType="dxCheckBox" editorOptions={{ text: 'Модератор системы' }}>
              <Label visible={false} />
            </SimpleItem>
          </GroupItem>
          
          <GroupItem caption="Статистика" colCount={2}>
            <SimpleItem dataField="stores_count" editorOptions={{ readOnly: true }}>
              <Label text="Магазины" />
            </SimpleItem>
            <SimpleItem dataField="products_count" editorOptions={{ readOnly: true }}>
              <Label text="Товары" />
            </SimpleItem>
            <SimpleItem dataField="orders_count" editorOptions={{ readOnly: true }}>
              <Label text="Заказы" />
            </SimpleItem>
            <SimpleItem dataField="created_at" editorType="dxDateBox" editorOptions={{ readOnly: true, displayFormat: 'dd.MM.yyyy HH:mm', type: 'datetime' }}>
              <Label text="Дата регистрации" />
            </SimpleItem>
          </GroupItem>
        </Form>
        
        <div className="popup-button-bar">
          <Button text="Сохранить" type="success" icon="save" onClick={() => onSave(user)} stylingMode="contained" width={140} />
          <Button text="Отмена" icon="close" onClick={onHide} stylingMode="outlined" width={140} />
          <Button text="Удалить" type="danger" icon="trash" onClick={() => onDelete(user.id)} stylingMode="contained" width={140} />
        </div>
      </div>
    </Popup>
  )
}
