import { useState } from 'react'
import { Popup } from 'devextreme-react/popup'
import { TextBox } from 'devextreme-react/text-box'
import { Button } from 'devextreme-react/button'
import axios from 'axios'
import './AuthModal.css'

const API_URL = 'http://localhost:8000'

interface AuthModalProps {
  visible: boolean
  onClose: () => void
  onSuccess: (token: string, user: any) => void
}

export default function AuthModal({ visible, onClose, onSuccess }: AuthModalProps) {
  const [step, setStep] = useState<'phone' | 'register' | 'code'>('phone')
  const [phone, setPhone] = useState('')
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [address, setAddress] = useState('')
  const [code, setCode] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [smsCode, setSmsCode] = useState('') // Для отображения в dev режиме

  const handleCheckPhone = async () => {
    setError('')
    
    if (!phone) {
      setError('Введите номер телефона')
      return
    }

    setLoading(true)

    try {
      // Проверяем существует ли пользователь
      const checkResponse = await axios.post(`${API_URL}/api/auth/check-phone`, {
        phone
      })

      if (checkResponse.data.exists) {
        // Пользователь существует - отправляем SMS
        await handleSendSMS()
      } else {
        // Новый пользователь - показываем форму регистрации
        setStep('register')
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка проверки телефона')
    } finally {
      setLoading(false)
    }
  }

  const handleSendSMS = async () => {
    setError('')

    if (step === 'register') {
      // Валидация для регистрации
      if (!fullName) {
        setError('Введите ФИО')
        return
      }
      if (!address) {
        setError('Введите адрес доставки')
        return
      }
    }

    setLoading(true)

    try {
      const response = await axios.post(`${API_URL}/api/auth/send-sms`, {
        phone,
        full_name: step === 'register' ? fullName : undefined,
        email: step === 'register' ? email : undefined,
        address: step === 'register' ? address : undefined
      })

      if (response.data.success) {
        setStep('code')
        setSmsCode(response.data.code) // Только для разработки!
        console.log('📱 SMS код:', response.data.code)
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка отправки SMS')
    } finally {
      setLoading(false)
    }
  }

  const handleVerifyCode = async () => {
    setError('')
    
    if (!code || code.length !== 6) {
      setError('Введите 6-значный код')
      return
    }

    setLoading(true)

    try {
      const response = await axios.post(`${API_URL}/api/auth/verify-sms`, {
        phone,
        code
      })

      const { access_token, user } = response.data
      
      // Сохраняем токен
      localStorage.setItem('auth_token', access_token)
      localStorage.setItem('user', JSON.stringify(user))
      
      onSuccess(access_token, user)
      handleClose()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Неверный код')
    } finally {
      setLoading(false)
    }
  }

  const handleClose = () => {
    setStep('phone')
    setPhone('')
    setFullName('')
    setEmail('')
    setAddress('')
    setCode('')
    setError('')
    setSmsCode('')
    onClose()
  }

  const handleResendCode = () => {
    setCode('')
    setError('')
    handleSendSMS()
  }

  const getTitle = () => {
    if (step === 'phone') return 'Вход или регистрация'
    if (step === 'register') return 'Регистрация'
    return 'Подтверждение телефона'
  }

  return (
    <Popup
      visible={visible}
      onHiding={handleClose}
      dragEnabled={false}
      closeOnOutsideClick={true}
      showTitle={true}
      title={getTitle()}
      width={440}
      height="auto"
    >
      <div className="auth-modal">
        {step === 'phone' && (
          <>
            <div className="auth-modal__description">
              Введите номер телефона, мы отправим SMS с кодом подтверждения
            </div>

            <div className="auth-modal__form">
              <TextBox
                label="Телефон"
                placeholder="+7 (999) 123-45-67"
                value={phone}
                onValueChanged={(e) => setPhone(e.value)}
                mode="tel"
                disabled={loading}
              />

              {error && <div className="auth-modal__error">{error}</div>}

              <Button
                text="Продолжить"
                type="default"
                stylingMode="contained"
                width="100%"
                onClick={handleCheckPhone}
                disabled={loading || !phone}
              />
            </div>
          </>
        )}

        {step === 'register' && (
          <>
            <div className="auth-modal__description">
              Вы новый пользователь. Заполните данные для регистрации
            </div>

            <div className="auth-modal__form">
              <TextBox
                label="Телефон"
                value={phone}
                disabled={true}
                mode="tel"
              />

              <TextBox
                label="ФИО *"
                placeholder="Иванов Иван Иванович"
                value={fullName}
                onValueChanged={(e) => setFullName(e.value)}
                disabled={loading}
              />

              <TextBox
                label="Email"
                placeholder="ivan@example.com"
                value={email}
                onValueChanged={(e) => setEmail(e.value)}
                mode="email"
                disabled={loading}
              />

              <TextBox
                label="Адрес доставки *"
                placeholder="г. Москва, ул. Ленина, д. 1, кв. 1"
                value={address}
                onValueChanged={(e) => setAddress(e.value)}
                disabled={loading}
              />

              {error && <div className="auth-modal__error">{error}</div>}

              <div className="auth-modal__buttons">
                <Button
                  text="Назад"
                  type="normal"
                  stylingMode="outlined"
                  onClick={() => setStep('phone')}
                  disabled={loading}
                />
                <Button
                  text="Зарегистрироваться"
                  type="default"
                  stylingMode="contained"
                  onClick={handleSendSMS}
                  disabled={loading || !fullName || !address}
                />
              </div>
            </div>
          </>
        )}

        {step === 'code' && (
          <>
            <div className="auth-modal__description">
              Мы отправили код на номер<br />
              <strong>{phone}</strong>
            </div>

            {/* DEV MODE: Показываем код */}
            {smsCode && (
              <div className="auth-modal__dev-code">
                🔐 Код для разработки: <strong>{smsCode}</strong>
              </div>
            )}

            <div className="auth-modal__form">
              <TextBox
                label="Код из SMS"
                placeholder="000000"
                value={code}
                onValueChanged={(e) => setCode(e.value)}
                mode="tel"
                maxLength={6}
                disabled={loading}
                inputAttr={{ style: { fontSize: '24px', textAlign: 'center', letterSpacing: '8px' } }}
              />

              {error && <div className="auth-modal__error">{error}</div>}

              <Button
                text="Подтвердить"
                type="default"
                width="100%"
                height={48}
                onClick={handleVerifyCode}
                disabled={loading || code.length !== 6}
              />

              <Button
                text="Отправить код повторно"
                stylingMode="text"
                width="100%"
                onClick={handleResendCode}
                disabled={loading}
              />
            </div>

            <div className="auth-modal__footer">
              <a onClick={() => setStep('phone')}>Изменить номер телефона</a>
            </div>
          </>
        )}
      </div>
    </Popup>
  )
}
