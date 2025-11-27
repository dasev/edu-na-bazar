/**
 * Компонент ввода адреса с автозаполнением через DaData
 */
import { useState, useEffect } from 'react'
import './AddressInput.css'

interface AddressSuggestion {
  value: string
  unrestricted_value: string
  data: {
    postal_code: string | null
    country: string
    region: string
    city: string | null
    street: string | null
    house: string | null
    flat: string | null
    geo_lat: string | null
    geo_lon: string | null
  }
}

interface AddressInputProps {
  value: string
  onValueChanged: (address: string, details?: AddressSuggestion['data']) => void
  placeholder?: string
  label?: string
}

const DADATA_TOKEN = 'e76739998f03541266e5b2f288d0d1c8b5d2f876' // Токен из CreateStorePage

export default function AddressInput({ value, onValueChanged, placeholder, label }: AddressInputProps) {
  const [suggestions, setSuggestions] = useState<AddressSuggestion[]>([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [loading, setLoading] = useState(false)
  const [isUserInput, setIsUserInput] = useState(false)
  const [selectedIndex, setSelectedIndex] = useState(-1)

  const fetchSuggestions = async (query: string) => {
    if (!query || query.length < 3) {
      setSuggestions([])
      return
    }

    setLoading(true)
    try {
      const response = await fetch('https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': `Token ${DADATA_TOKEN}`
        },
        body: JSON.stringify({ query, count: 5 })
      })

      const data = await response.json()
      setSuggestions(data.suggestions || [])
      setShowSuggestions(true)
    } catch (error) {
      console.error('DaData error:', error)
      setSuggestions([])
    } finally {
      setLoading(false)
    }
  }

  const handleSelect = (suggestion: AddressSuggestion) => {
    onValueChanged(suggestion.value, suggestion.data)
    setSuggestions([])
    setShowSuggestions(false)
    setSelectedIndex(-1)
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!showSuggestions || suggestions.length === 0) return

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault()
        setSelectedIndex(prev => 
          prev < suggestions.length - 1 ? prev + 1 : prev
        )
        break
      case 'ArrowUp':
        e.preventDefault()
        setSelectedIndex(prev => prev > 0 ? prev - 1 : -1)
        break
      case 'Enter':
        e.preventDefault()
        if (selectedIndex >= 0 && selectedIndex < suggestions.length) {
          handleSelect(suggestions[selectedIndex])
        }
        break
      case 'Escape':
        setShowSuggestions(false)
        setSelectedIndex(-1)
        break
    }
  }

  useEffect(() => {
    // Загружаем подсказки только если это пользовательский ввод
    if (!isUserInput) {
      return
    }
    
    const timer = setTimeout(() => {
      if (value && value.length >= 3) {
        fetchSuggestions(value)
      } else {
        setSuggestions([])
        setShowSuggestions(false)
      }
    }, 150)

    return () => clearTimeout(timer)
  }, [value, isUserInput])

  return (
    <div className="address-input">
      {label && <label className="address-input__label">{label}</label>}
      <div className="address-input__wrapper">
        <input
          type="text"
          className="address-input__field"
          value={value}
          onChange={(e) => {
            setIsUserInput(true) // Помечаем что это пользовательский ввод
            onValueChanged(e.target.value)
            if (!e.target.value) {
              setSuggestions([])
              setShowSuggestions(false)
            }
            setSelectedIndex(-1)
          }}
          onKeyDown={handleKeyDown}
          onFocus={() => {
            if (suggestions.length > 0) {
              setShowSuggestions(true)
            }
          }}
          placeholder={placeholder || 'Начните вводить адрес...'}
        />
        {loading && <div className="address-input__loader">⏳</div>}
        
        {showSuggestions && suggestions.length > 0 && (
          <div className="address-input__suggestions">
            {suggestions.map((suggestion, index) => (
              <div
                key={index}
                className={`address-input__suggestion ${index === selectedIndex ? 'selected' : ''}`}
                onClick={() => handleSelect(suggestion)}
                onMouseEnter={() => setSelectedIndex(index)}
              >
                {suggestion.value}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
