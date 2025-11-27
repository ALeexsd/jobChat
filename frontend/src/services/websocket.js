/**
 * WebSocket Service для реального времени
 */
import { useAuthStore } from '@/stores/auth'

class WebSocketService {
  constructor() {
    this.ws = null
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectDelay = 1000
    this.isConnecting = false
    this.isManualClose = false
    this.messageHandlers = new Map()
    this.pingInterval = null
  }

  /**
   * Подключение к WebSocket
   */
  connect() {
    console.log('🔌 WebSocket connect() called')
    console.log('Current state:', this.ws?.readyState)
    console.log('Is connecting:', this.isConnecting)
    
    if (this.ws?.readyState === WebSocket.OPEN || this.isConnecting) {
      console.log('WebSocket already connected or connecting')
      return
    }

    this.isConnecting = true
    this.isManualClose = false

    const authStore = useAuthStore()
    const token = authStore.accessToken

    if (!token) {
      console.error('❌ No access token available')
      this.isConnecting = false
      return
    }

    const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'
    const url = `${wsUrl}/ws?token=${token}`

    console.log('🔗 Connecting to WebSocket:', url)
    console.log('Token (first 20 chars):', token.substring(0, 20) + '...')
    this.ws = new WebSocket(url)

    this.ws.onopen = () => {
      console.log('✅ WebSocket onopen fired - connection established!')
      this.isConnecting = false
      this.reconnectAttempts = 0
      this.startPing()
      this.emit('connected')
    }

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        console.log('📨 WebSocket message received:', data.type, data)
        this.handleMessage(data)
      } catch (error) {
        console.error('❌ Error parsing WebSocket message:', error)
      }
    }

    this.ws.onclose = (event) => {
      console.log('🔌 WebSocket closed - Code:', event.code, 'Reason:', event.reason)
      this.isConnecting = false
      this.stopPing()
      this.emit('disconnected')

      if (!this.isManualClose) {
        this.reconnect()
      }
    }

    this.ws.onerror = (error) => {
      console.error('❌ WebSocket error fired:', error)
      this.isConnecting = false
      this.emit('error', error)
    }
  }

  /**
   * Переподключение
   */
  reconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnect attempts reached')
      this.emit('max_reconnect_attempts')
      return
    }

    this.reconnectAttempts++
    const delay = this.reconnectDelay * this.reconnectAttempts

    console.log(`Reconnecting in ${delay}ms... (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`)

    setTimeout(() => {
      this.connect()
    }, delay)
  }

  /**
   * Отключение
   */
  disconnect() {
    this.isManualClose = true
    this.stopPing()
    
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
  }

  /**
   * Отправка сообщения
   */
  send(data) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data))
      return true
    } else {
      console.warn('WebSocket is not connected')
      return false
    }
  }

  /**
   * Ping для поддержания соединения
   */
  startPing() {
    this.stopPing()
    this.pingInterval = setInterval(() => {
      this.send({ type: 'ping' })
    }, 30000) // Каждые 30 секунд
  }

  stopPing() {
    if (this.pingInterval) {
      clearInterval(this.pingInterval)
      this.pingInterval = null
    }
  }

  /**
   * Обработка входящих сообщений
   */
  handleMessage(data) {
    const type = data.type

    // Вызываем все обработчики для этого типа
    if (this.messageHandlers.has(type)) {
      this.messageHandlers.get(type).forEach(handler => {
        try {
          handler(data)
        } catch (error) {
          console.error(`Error in message handler for type ${type}:`, error)
        }
      })
    }

    // Вызываем общие обработчики
    if (this.messageHandlers.has('*')) {
      this.messageHandlers.get('*').forEach(handler => {
        try {
          handler(data)
        } catch (error) {
          console.error('Error in wildcard message handler:', error)
        }
      })
    }
  }

  /**
   * Подписка на события
   */
  on(type, handler) {
    if (!this.messageHandlers.has(type)) {
      this.messageHandlers.set(type, new Set())
    }
    this.messageHandlers.get(type).add(handler)

    // Возвращаем функцию для отписки
    return () => {
      this.off(type, handler)
    }
  }

  /**
   * Отписка от событий
   */
  off(type, handler) {
    if (this.messageHandlers.has(type)) {
      this.messageHandlers.get(type).delete(handler)
    }
  }

  /**
   * Emit события (для внутреннего использования)
   */
  emit(type, data = null) {
    this.handleMessage({ type, ...data })
  }

  /**
   * Проверка подключения
   */
  isConnected() {
    return this.ws?.readyState === WebSocket.OPEN
  }

  // === Специфичные методы для чата ===

  /**
   * Присоединиться к чату
   */
  joinChat(chatId) {
    return this.send({
      type: 'join_chat',
      chat_id: chatId
    })
  }

  /**
   * Покинуть чат
   */
  leaveChat(chatId) {
    return this.send({
      type: 'leave_chat',
      chat_id: chatId
    })
  }

  /**
   * Отправить индикатор печати
   */
  sendTyping(chatId, isTyping = true) {
    return this.send({
      type: 'typing',
      chat_id: chatId,
      is_typing: isTyping
    })
  }

  /**
   * Обновить статус
   */
  updateStatus(status) {
    return this.send({
      type: 'status',
      status: status
    })
  }

  /**
   * Отметить сообщения как прочитанные
   */
  markMessagesRead(chatId) {
    return this.send({
      type: 'read_messages',
      chat_id: chatId
    })
  }
}

// Экспортируем singleton
export default new WebSocketService()
