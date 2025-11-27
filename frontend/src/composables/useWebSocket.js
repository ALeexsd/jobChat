/**
 * Composable для использования WebSocket в компонентах
 */
import { onMounted, onBeforeUnmount, ref } from 'vue'
import websocket from '@/services/websocket'

export function useWebSocket() {
  const isConnected = ref(false)
  const isReconnecting = ref(false)

  onMounted(() => {
    // Подключаемся при монтировании
    if (!websocket.isConnected()) {
      websocket.connect()
    }

    // Слушаем события подключения
    const unsubscribeConnected = websocket.on('connected', () => {
      isConnected.value = true
      isReconnecting.value = false
    })

    const unsubscribeDisconnected = websocket.on('disconnected', () => {
      isConnected.value = false
      isReconnecting.value = true
    })

    // Отписываемся при размонтировании
    onBeforeUnmount(() => {
      unsubscribeConnected()
      unsubscribeDisconnected()
    })
  })

  return {
    isConnected,
    isReconnecting,
    websocket
  }
}

/**
 * Composable для чата с WebSocket
 */
export function useChatWebSocket(chatId) {
  const { isConnected, websocket } = useWebSocket()
  const typingUsers = ref(new Set())
  const onlineUsers = ref(new Set())
  
  // Получаем числовое значение chatId
  const getChatId = () => {
    return typeof chatId === 'object' && chatId.value !== undefined ? chatId.value : chatId
  }

  onMounted(() => {
    // Присоединяемся к чату
    if (websocket.isConnected()) {
      websocket.joinChat(getChatId())
    }

    // Слушаем события чата
    const currentChatId = getChatId()
    
    const unsubscribeTyping = websocket.on('typing', (data) => {
      if (data.chat_id === currentChatId) {
        if (data.is_typing) {
          typingUsers.value.add(data.user_id)
        } else {
          typingUsers.value.delete(data.user_id)
        }
      }
    })

    const unsubscribeNewMessage = websocket.on('new_message', (data) => {
      if (data.chat_id === currentChatId) {
        // Обработка нового сообщения
        console.log('New message received:', data)
      }
    })

    const unsubscribeMessageUpdated = websocket.on('message_updated', (data) => {
      if (data.chat_id === currentChatId) {
        console.log('Message updated:', data)
      }
    })

    const unsubscribeMessageDeleted = websocket.on('message_deleted', (data) => {
      if (data.chat_id === currentChatId) {
        console.log('Message deleted:', data)
      }
    })

    const unsubscribeUserStatus = websocket.on('user_status', (data) => {
      if (data.status === 'online') {
        onlineUsers.value.add(data.user_id)
      } else {
        onlineUsers.value.delete(data.user_id)
      }
    })

    // Отписываемся и покидаем чат при размонтировании
    onBeforeUnmount(() => {
      websocket.leaveChat(getChatId())
      unsubscribeTyping()
      unsubscribeNewMessage()
      unsubscribeMessageUpdated()
      unsubscribeMessageDeleted()
      unsubscribeUserStatus()
    })
  })

  /**
   * Отправить индикатор печати
   */
  const sendTyping = (isTyping = true) => {
    websocket.sendTyping(getChatId(), isTyping)
  }

  /**
   * Отметить сообщения как прочитанные
   */
  const markAsRead = () => {
    websocket.markMessagesRead(getChatId())
  }

  return {
    isConnected,
    typingUsers,
    onlineUsers,
    sendTyping,
    markAsRead,
    websocket
  }
}
