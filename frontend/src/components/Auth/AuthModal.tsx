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
  const [step, setStep] = useState<'phone' | 'code'>('phone')
  const [phone, setPhone] = useState('')
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [address, setAddress] = useState('')
  const [code, setCode] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [isNewUser, setIsNewUser] = useState(false)
  const [smsCode, setSmsCode] = useState('') // Для отображения в dev режиме

  const handleSendSMS = async () => {
    setError('')
    
    if (!phone) {
      setError('Введите номер телефона')
      return
    }

    if (isNewUser && !fullName) {
      setError('Введите ФИО')
      return
    }

    if (isNewUser && !address) {
      setError('Введите адрес доставки')
      return
    }

    setLoading(true)

    try {
      const response = await axios.post(`${API_URL}/api/auth/send-sms`, {
        phone,
        full_name: isNewUser ? fullName : undefined,
        email: isNewUser ? email : undefined,
        address: isNewUser ? address : undefined
      })

      if (response.data.success) {
        setStep('code')
        setSmsCode(response.data.code) // Только для разработки!
        console.log('📱 SMS код:', response.data.code)
      }
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Ошибка отправки SMS'
      
      // Если новый пользователь - показываем поля регистрации
      if (errorMsg.includes('ФИО')) {
        setIsNewUser(true)
        setError('Вы новый пользователь. Заполните данные для регистрации')
      } else {
        setError(errorMsg)
      }
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
    setIsNewUser(false)
    setSmsCode('')
    onClose()
  }

  const handleResendCode = () => {
    setCode('')
    setError('')
    handleSendSMS()
  }

  return (
    <Popup
      visible={visible}
      onHiding={handleClose}
      dragEnabled={false}
      closeOnOutsideClick={true}
      showTitle={true}
      title={step === 'phone' ? 'Вход или регистрация' : 'Подтверждение телефона'}
      width={440}
      height="auto"
    >
      <div className="auth-modal">
        {step === 'phone' ? (
          <>
            <div className="auth-modal__description">
              {isNewUser 
                ? 'Заполните данные для регистрации'
                : 'Введите номер телефона, мы отправим SMS с кодом подтверждения'
              }
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

              {isNewUser && (
                <>
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
                </>
              )}

              {error && <div className="auth-modal__error">{error}</div>}

              <Button
                text={isNewUser ? 'Зарегистрироваться' : 'Получить код'}
                type="default"
                width="100%"
                height={48}
                onClick={handleSendSMS}
                disabled={loading}
              />
            </div>

            <div className="auth-modal__footer">
              Нажимая кнопку, вы соглашаетесь с условиями использования
            </div>
          </>
        ) : (
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
