/**
 * Страница профиля пользователя
 */
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { Button } from 'devextreme-react/button'
import { TextBox } from 'devextreme-react/text-box'
import { useAuthStore } from '../../store/authStore'
import { showToast } from '../../utils/toast'
import './ProfilePage.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const ProfilePage = () => {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { isAuthenticated, user } = useAuthStore()

  // Состояние формы
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [phone, setPhone] = useState('')
  const [address, setAddress] = useState('')
  const [avatar, setAvatar] = useState<string | null>(null)
  const [avatarFile, setAvatarFile] = useState<File | null>(null)

  // Состояние валидации
  const [isEmailVerified, setIsEmailVerified] = useState(false)
  const [isPhoneVerified, setIsPhoneVerified] = useState(false)
  const [emailCode, setEmailCode] = useState('')
  const [phoneCode, setPhoneCode] = useState('')
  const [showEmailVerification, setShowEmailVerification] = useState(false)
  const [showPhoneVerification, setShowPhoneVerification] = useState(false)

  // Состояние загрузки
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // Автоматический редирект если не авторизован
  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/')
    }
  }, [isAuthenticated, navigate])

  // Загрузка данных пользователя
  const { data: userData, isLoading } = useQuery({
    queryKey: ['user-profile'],
    queryFn: async () => {
      const token = localStorage.getItem('auth_token')
      const response = await fetch(`${API_URL}/api/users/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
      if (!response.ok) throw new Error('Failed to fetch user')
      return response.json()
    },
    enabled: isAuthenticated,
  })

  // Заполнение формы при загрузке данных
  useEffect(() => {
    if (userData) {
      setFullName(userData.full_name || '')
      setEmail(userData.email || '')
      setPhone(userData.phone || '')
      setAddress(userData.address || '')
      setAvatar(userData.avatar || null)
      setIsEmailVerified(userData.is_email_verified || false)
      setIsPhoneVerified(userData.is_phone_verified || false)
    }
  }, [userData])

  // Загрузка аватара
  const handleAvatarChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      if (!file.type.startsWith('image/')) {
        setError('Выберите изображение')
        return
      }
      if (file.size > 5 * 1024 * 1024) {
        setError('Размер файла не должен превышать 5MB')
        return
      }
      setAvatarFile(file)
      const reader = new FileReader()
      reader.onloadend = () => {
        setAvatar(reader.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleRemoveAvatar = () => {
    setAvatar(null)
    setAvatarFile(null)
  }

  // Отправка кода на email
  const handleSendEmailCode = async () => {
    if (!email) {
      setError('Введите email')
      return
    }
    setLoading(true)
    try {
      const token = localStorage.getItem('auth_token')
      const response = await fetch(`${API_URL}/api/users/send-email-code`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ email }),
      })
      if (response.ok) {
        showToast.success('Код отправлен на email')
        setShowEmailVerification(true)
      } else {
        const data = await response.json()
        setError(data.detail || 'Ошибка отправки кода')
      }
    } catch (err) {
      setError('Ошибка отправки кода')
    } finally {
      setLoading(false)
    }
  }

  // Проверка кода email
  const handleVerifyEmail = async () => {
    if (!emailCode) {
      setError('Введите код из письма')
      return
    }
    setLoading(true)
    try {
      const token = localStorage.getItem('auth_token')
      const response = await fetch(`${API_URL}/api/users/verify-email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ email, code: emailCode }),
      })
      if (response.ok) {
        showToast.success('Email подтвержден')
        setIsEmailVerified(true)
        setShowEmailVerification(false)
        
        // Обновляем данные пользователя в authStore сразу
        const currentUser = useAuthStore.getState().user
        if (currentUser) {
          useAuthStore.getState().updateUser({
            ...currentUser,
            email: email,
          })
        }
        
        // Обновляем данные профиля и перезагружаем
        await queryClient.invalidateQueries({ queryKey: ['user-profile'] })
        await queryClient.refetchQueries({ queryKey: ['user-profile'] })
      } else {
        const data = await response.json()
        setError(data.detail || 'Неверный код')
      }
    } catch (err) {
      setError('Ошибка проверки кода')
    } finally {
      setLoading(false)
    }
  }

  // Отправка SMS кода
  const handleSendPhoneCode = async () => {
    if (!phone) {
      setError('Введите телефон')
      return
    }
    setLoading(true)
    try {
      const token = localStorage.getItem('auth_token')
      const response = await fetch(`${API_URL}/api/users/send-phone-code`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ phone }),
      })
      if (response.ok) {
        showToast.success('SMS код отправлен')
        setShowPhoneVerification(true)
      } else {
        const data = await response.json()
        setError(data.detail || 'Ошибка отправки SMS')
      }
    } catch (err) {
      setError('Ошибка отправки SMS')
    } finally {
      setLoading(false)
    }
  }

  // Проверка SMS кода
  const handleVerifyPhone = async () => {
    if (!phoneCode) {
      setError('Введите код из SMS')
      return
    }
    setLoading(true)
    try {
      const token = localStorage.getItem('auth_token')
      const response = await fetch(`${API_URL}/api/users/verify-phone`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ phone, code: phoneCode }),
      })
      if (response.ok) {
        showToast.success('Телефон подтвержден')
        setIsPhoneVerified(true)
        setShowPhoneVerification(false)
        
        // Обновляем данные пользователя в authStore сразу
        const currentUser = useAuthStore.getState().user
        if (currentUser) {
          useAuthStore.getState().updateUser({
            ...currentUser,
            phone: phone,
          })
        }
        
        // Обновляем данные профиля и перезагружаем
        await queryClient.invalidateQueries({ queryKey: ['user-profile'] })
        await queryClient.refetchQueries({ queryKey: ['user-profile'] })
      } else {
        const data = await response.json()
        setError(data.detail || 'Неверный код')
      }
    } catch (err) {
      setError('Ошибка проверки кода')
    } finally {
      setLoading(false)
    }
  }

  // Сохранение профиля
  const handleSaveProfile = async () => {
    setError('')
    
    const token = localStorage.getItem('auth_token')
    if (!token) {
      setError('Ошибка авторизации')
      return
    }

    setLoading(true)

    try {
      // Загрузка аватара если есть
      let avatarUrl = avatar
      if (avatarFile) {
        const formData = new FormData()
        formData.append('file', avatarFile)
        const response = await fetch(`${API_URL}/api/users/avatar`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
          body: formData,
        })
        if (response.ok) {
          const data = await response.json()
          avatarUrl = data.avatar_url
        }
      }

      // Обновление профиля (email и phone уже сохранены при верификации)
      const response = await fetch(`${API_URL}/api/users/me`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          full_name: fullName,
          address,
        }),
      })

      if (response.ok) {
        showToast.success('Профиль обновлен')
        await queryClient.invalidateQueries({ queryKey: ['user-profile'] })
        await queryClient.refetchQueries({ queryKey: ['user-profile'] })
        
        // Обновляем данные пользователя в authStore
        const updatedUserData: any = await queryClient.fetchQuery({ queryKey: ['user-profile'] })
        if (updatedUserData) {
          const currentUser = useAuthStore.getState().user
          if (currentUser) {
            useAuthStore.getState().updateUser({
              ...currentUser,
              full_name: updatedUserData.full_name || currentUser.full_name,
              email: updatedUserData.email || currentUser.email,
              avatar: updatedUserData.avatar,
            })
          }
        }
      } else {
        const data = await response.json()
        setError(data.detail || 'Ошибка обновления профиля')
      }
    } catch (err) {
      setError('Ошибка обновления профиля')
    } finally {
      setLoading(false)
    }
  }

  if (!isAuthenticated || isLoading) {
    return null
  }

  return (
    <div className="profile-page">
      <div className="profile-container">
        <div className="profile-header">
          <Button
            icon="back"
            text="Назад"
            stylingMode="text"
            onClick={() => navigate('/')}
          />
          <h1>Мой профиль</h1>
        </div>

        <div className="profile-content">
          {/* Аватар */}
          <div className="profile-avatar-section">
            <h2>Фото профиля</h2>
            <div className="avatar-upload">
              {avatar ? (
                <div className="avatar-preview">
                  <img 
                    src={avatar.startsWith('http') || avatar.startsWith('data:') ? avatar : `${API_URL}${avatar}`} 
                    alt="Аватар" 
                  />
                  <Button
                    icon="trash"
                    stylingMode="text"
                    onClick={handleRemoveAvatar}
                    disabled={loading}
                  />
                </div>
              ) : (
                <div className="avatar-placeholder">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleAvatarChange}
                    style={{ display: 'none' }}
                    id="avatar-upload"
                    disabled={loading}
                  />
                  <label htmlFor="avatar-upload" className="avatar-upload-label">
                    <div className="upload-icon">👤</div>
                    <div className="upload-text">Загрузить фото</div>
                  </label>
                </div>
              )}
            </div>
          </div>

          {/* Основные данные */}
          <div className="profile-section">
            <h2>Основные данные</h2>
            
            <div className="form-group">
              <label>ФИО</label>
              <TextBox
                value={fullName}
                onValueChanged={(e) => setFullName(e.value)}
                placeholder="Иванов Иван Иванович"
                disabled={loading}
              />
            </div>

            <div className="form-group">
              <label>Адрес</label>
              <TextBox
                value={address}
                onValueChanged={(e) => setAddress(e.value)}
                placeholder="г. Москва, ул. Ленина, д. 1"
                disabled={loading}
              />
            </div>
          </div>

          {/* Email */}
          <div className="profile-section">
            <h2>
              Email 
              {isEmailVerified ? (
                <span className="verified-badge">✓ Подтвержден</span>
              ) : (
                <span className="unverified-badge">⚠️ Не подтвержден</span>
              )}
            </h2>
            
            <div className="form-group">
              <TextBox
                value={email}
                onValueChanged={(e) => {
                  setEmail(e.value)
                  setIsEmailVerified(false)
                }}
                placeholder="email@example.com"
                disabled={loading || isEmailVerified}
                mode="email"
              />
              {!isEmailVerified && (
                <Button
                  text="Отправить код"
                  onClick={handleSendEmailCode}
                  disabled={loading || !email}
                  stylingMode="outlined"
                />
              )}
            </div>

            {showEmailVerification && !isEmailVerified && (
              <div className="verification-block">
                <TextBox
                  value={emailCode}
                  onValueChanged={(e) => setEmailCode(e.value)}
                  placeholder="Код из письма"
                  disabled={loading}
                />
                <Button
                  text="Подтвердить"
                  onClick={handleVerifyEmail}
                  disabled={loading || !emailCode}
                />
              </div>
            )}
          </div>

          {/* Телефон */}
          <div className="profile-section">
            <h2>
              Телефон 
              {isPhoneVerified ? (
                <span className="verified-badge">✓ Подтвержден</span>
              ) : (
                <span className="unverified-badge">⚠️ Не подтвержден</span>
              )}
            </h2>
            
            <div className="form-group">
              <TextBox
                value={phone}
                onValueChanged={(e) => {
                  setPhone(e.value)
                  setIsPhoneVerified(false)
                }}
                placeholder="+7 (999) 123-45-67"
                disabled={loading || isPhoneVerified}
                mode="tel"
              />
              {!isPhoneVerified && (
                <Button
                  text="Отправить SMS"
                  onClick={handleSendPhoneCode}
                  disabled={loading || !phone}
                  stylingMode="outlined"
                />
              )}
            </div>

            {showPhoneVerification && !isPhoneVerified && (
              <div className="verification-block">
                <TextBox
                  value={phoneCode}
                  onValueChanged={(e) => setPhoneCode(e.value)}
                  placeholder="Код из SMS"
                  disabled={loading}
                />
                <Button
                  text="Подтвердить"
                  onClick={handleVerifyPhone}
                  disabled={loading || !phoneCode}
                />
              </div>
            )}
          </div>

          {/* Ошибка */}
          {error && (
            <div className="error-message">
              ❌ {error}
            </div>
          )}

          {/* Кнопки */}
          <div className="profile-actions">
            <Button
              text="Отмена"
              stylingMode="outlined"
              onClick={() => navigate('/')}
              disabled={loading}
            />
            <Button
              text={loading ? 'Сохранение...' : 'Сохранить'}
              type="default"
              onClick={handleSaveProfile}
              disabled={loading}
            />
          </div>
        </div>
      </div>
    </div>
  )
}
