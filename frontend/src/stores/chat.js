import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'

export const useChatStore = defineStore('chat', () => {
  const chats = ref([])
  const currentChat = ref(null)
  const messages = ref([])

  async function fetchChats() {
    try {
      const response = await api.get('/chats')
      chats.value = response.data
    } catch (error) {
      console.error('Fetch chats error:', error)
    }
  }

  async function fetchChat(chatId) {
    try {
      const response = await api.get(`/chats/${chatId}`)
      currentChat.value = response.data
    } catch (error) {
      console.error('Fetch chat error:', error)
    }
  }

  async function fetchMessages(chatId) {
    try {
      const response = await api.get(`/messages/chat/${chatId}`)
      messages.value = response.data.reverse()
    } catch (error) {
      console.error('Fetch messages error:', error)
    }
  }

  async function sendMessage(chatId, content, messageType = 'text') {
    try {
      const response = await api.post('/messages', {
        chat_id: chatId,
        content,
        message_type: messageType
      })
      messages.value.push(response.data)
      return response.data
    } catch (error) {
      console.error('Send message error:', error)
    }
  }

  async function createChat(name, chatType, memberIds) {
    try {
      const response = await api.post('/chats', {
        name,
        chat_type: chatType,
        member_ids: memberIds
      })
      chats.value.push(response.data)
      return response.data
    } catch (error) {
      console.error('Create chat error:', error)
    }
  }

  function addMessage(message) {
    messages.value.push(message)
  }

  return {
    chats,
    currentChat,
    messages,
    fetchChats,
    fetchChat,
    fetchMessages,
    sendMessage,
    createChat,
    addMessage
  }
})
