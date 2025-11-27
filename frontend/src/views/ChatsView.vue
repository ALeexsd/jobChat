<template>
  <div class="h-full flex flex-col p-6 bg-white dark:bg-gray-900">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Чаты</h1>
      <button @click="showCreateModal = true" class="btn-primary flex items-center">
        <PlusIcon class="w-5 h-5 mr-2" />
        Новый чат
      </button>
    </div>
    
    <!-- Search -->
    <div class="mb-6">
      <div class="relative">
        <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          v-model="searchQuery"
          @input="handleSearch"
          type="text"
          placeholder="Поиск чатов или @username..."
          class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400"
        />
      </div>
      
      <!-- Search Results -->
      <div v-if="searchResults.length > 0" class="mt-2 card dark:bg-gray-800 dark:border-gray-700 p-2 max-h-60 overflow-y-auto">
        <p class="text-xs text-gray-500 dark:text-gray-400 px-2 py-1">Пользователи:</p>
        <button
          v-for="user in searchResults"
          :key="user.id"
          @click="createChatWithUser(user)"
          class="w-full flex items-center p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors text-left"
        >
          <div class="w-10 h-10 rounded-full bg-primary-600 flex items-center justify-center text-white font-semibold">
            {{ user.first_name?.[0] || '?' }}{{ user.last_name?.[0] || '' }}
          </div>
          <div class="ml-3">
            <p class="text-sm font-medium text-gray-900 dark:text-gray-100">{{ user.first_name }} {{ user.last_name }}</p>
            <p class="text-xs text-gray-500 dark:text-gray-400">@{{ user.username }}</p>
          </div>
        </button>
      </div>
    </div>
    
    <!-- Chats List -->
    <div class="flex-1 overflow-auto">
      <div v-if="filteredChats.length === 0" class="text-center py-12">
        <ChatBubbleLeftRightIcon class="w-16 h-16 mx-auto text-gray-400 mb-4" />
        <p class="text-gray-500 dark:text-gray-400 mb-4">Нет чатов</p>
        <button @click="showCreateModal = true" class="btn-primary">
          Создать первый чат
        </button>
      </div>
      
      <div v-else class="space-y-2">
        <div
          v-for="chat in filteredChats"
          :key="chat.id"
          class="relative overflow-hidden"
          @touchstart="handleTouchStart($event, chat.id)"
          @touchmove="handleTouchMove($event, chat.id)"
          @touchend="handleTouchEnd(chat.id)"
          @mousedown="handleMouseDown($event, chat.id)"
          @mousemove="handleMouseMove($event, chat.id)"
          @mouseup="handleMouseUp(chat.id)"
          @mouseleave="handleMouseLeave(chat.id)"
        >
          <!-- Delete Button (показывается при свайпе) -->
          <div
            class="absolute right-0 top-0 bottom-0 bg-red-600 flex items-center justify-center transition-all"
            :style="{ width: swipeStates[chat.id]?.deleteWidth || '0px' }"
          >
            <TrashIcon class="w-6 h-6 text-white" />
          </div>
          
          <!-- Chat Item -->
          <div
            class="relative bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg transition-transform cursor-pointer"
            :style="{ transform: `translateX(${swipeStates[chat.id]?.translateX || 0}px)` }"
          >
            <router-link
              :to="`/chats/${chat.id}`"
              class="block p-4 hover:shadow-md dark:hover:bg-gray-750 transition-shadow"
            >
              <div class="flex items-center">
                <div class="w-12 h-12 rounded-full bg-primary-600 flex items-center justify-center text-white font-semibold text-lg">
                  {{ (chat.displayName || chat.name)?.[0] || '?' }}
                </div>
                
                <div class="ml-4 flex-1 min-w-0">
                  <div class="flex items-center justify-between mb-1">
                    <h3 class="text-sm font-semibold text-gray-900 dark:text-gray-100 truncate">{{ chat.displayName || chat.name }}</h3>
                    <span v-if="chat.last_message" class="text-xs text-gray-500 dark:text-gray-400">
                      {{ formatTime(chat.last_message.created_at) }}
                    </span>
                  </div>
                  
                  <div class="flex items-center justify-between">
                    <p class="text-sm text-gray-600 dark:text-gray-400 truncate">
                      {{ chat.last_message?.content || 'Нет сообщений' }}
                    </p>
                    <span
                      v-if="getUnreadCount(chat.id) > 0"
                      class="ml-2 px-2 py-1 bg-red-600 text-white text-xs rounded-full font-semibold min-w-[20px] text-center"
                    >
                      {{ getUnreadCount(chat.id) }}
                    </span>
                  </div>
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Create Chat Modal -->
    <CreateChatModal
      :show="showCreateModal"
      @close="showCreateModal = false"
      @created="handleChatCreated"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useNotificationSounds } from '@/composables/useNotificationSounds'
import websocket from '@/services/websocket'
import api from '@/services/api'
import CreateChatModal from '@/components/CreateChatModal.vue'
import {
  PlusIcon,
  MagnifyingGlassIcon,
  ChatBubbleLeftRightIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()
const { playSound } = useNotificationSounds()
const chats = ref([])
const searchQuery = ref('')
const searchResults = ref([])
const showCreateModal = ref(false)
const unreadMessages = ref({}) // { chatId: count }
const swipeStates = ref({}) // { chatId: { startX, translateX, deleteWidth } }
let searchTimeout = null
let updateInterval = null
let unsubscribeNewMessage = null
let unsubscribeMessagesRead = null

const filteredChats = computed(() => {
  // Создаем копию массива для сортировки
  let result = [...chats.value]
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(chat => {
      // Поиск по отображаемому имени или названию чата
      const displayName = chat.displayName || chat.name || ''
      if (displayName.toLowerCase().includes(query)) {
        return true
      }
      
      return false
    })
  }
  
  // Сортируем только по времени последнего сообщения (новые сверху)
  // Статус прочитанности не влияет на позицию чата
  return result.sort((a, b) => {
    const timeA = a.last_message?.created_at ? new Date(a.last_message.created_at).getTime() : 0
    const timeB = b.last_message?.created_at ? new Date(b.last_message.created_at).getTime() : 0
    return timeB - timeA // От новых к старым
  })
})

onMounted(async () => {
  await loadChats()
  await loadUnreadCounts()
  
  // Подключаемся к WebSocket если не подключен
  if (!websocket.isConnected()) {
    console.log('🔌 Connecting to WebSocket from ChatsView...')
    websocket.connect()
    
    // Ждем подключения
    await new Promise((resolve) => {
      if (websocket.isConnected()) {
        resolve()
      } else {
        const unsubscribe = websocket.on('connected', () => {
          console.log('✅ WebSocket connected in ChatsView')
          unsubscribe()
          resolve()
        })
        // Таймаут на случай если не подключится
        setTimeout(resolve, 3000)
      }
    })
  }
  
  console.log('📡 Subscribing to WebSocket events in ChatsView')
  
  // Подписываемся на новые сообщения
  unsubscribeNewMessage = websocket.on('new_message', async (data) => {
    console.log('📨 New message in chat list:', data)
    
    // Обновляем последнее сообщение в чате
    const chat = chats.value.find(c => c.id === data.chat_id)
    if (chat) {
      chat.last_message = {
        content: data.message.content,
        created_at: data.message.created_at
      }
      
      // Увеличиваем счетчик непрочитанных только если сообщение от другого пользователя
      if (data.message.sender_id !== authStore.user?.id) {
        const currentCount = unreadMessages.value[data.chat_id] || 0
        // Создаем новый объект для триггера реактивности
        unreadMessages.value = {
          ...unreadMessages.value,
          [data.chat_id]: currentCount + 1
        }
        console.log(`📊 Unread count for chat ${data.chat_id}: ${unreadMessages.value[data.chat_id]}`)
        
        // Воспроизводим звук уведомления
        playSound(data.chat_id)
      }
      
      // Сортировка теперь происходит автоматически через computed свойство filteredChats
      console.log(`✅ Chat ${data.chat_id} updated, sorting handled by computed property`)
    } else {
      // Новый чат - перезагружаем список
      console.log('🔄 New chat detected, reloading list')
      await loadChats()
    }
  })
  
  // Подписываемся на прочтение сообщений
  unsubscribeMessagesRead = websocket.on('messages_read', (data) => {
    console.log('✅ Messages read:', data)
    if (data.user_id === authStore.user?.id) {
      // Создаем новый объект для триггера реактивности
      unreadMessages.value = {
        ...unreadMessages.value,
        [data.chat_id]: 0
      }
      console.log(`📊 Reset unread count for chat ${data.chat_id}`)
    }
  })
  
  // Обновляем счетчики каждые 10 секунд (резервный механизм)
  updateInterval = setInterval(() => {
    if (!websocket.isConnected()) {
      console.log('⚠️ WebSocket disconnected, using polling for unread counts')
      loadUnreadCounts()
    }
  }, 10000)
})

onBeforeUnmount(() => {
  console.log('🔌 Unsubscribing from WebSocket events in ChatsView')
  if (updateInterval) {
    clearInterval(updateInterval)
  }
  if (unsubscribeNewMessage) {
    unsubscribeNewMessage()
  }
  if (unsubscribeMessagesRead) {
    unsubscribeMessagesRead()
  }
})

async function loadChats() {
  try {
    const response = await api.get('/chats')
    const currentUserId = authStore.user?.id
    
    // Обрабатываем каждый чат для правильного отображения имени
    for (const chat of response.data) {
      if (chat.chat_type === 'private' && chat.members?.length > 0) {
        // Находим собеседника
        const otherMember = chat.members.find(m => m.user_id !== currentUserId)
        
        if (otherMember) {
          // Загружаем данные пользователя
          try {
            const userResponse = await api.get(`/users/${otherMember.user_id}`)
            const user = userResponse.data
            
            // Проверяем, это чат с самим собой?
            if (otherMember.user_id === currentUserId) {
              chat.displayName = '📝 Сообщения для себя'
            } else {
              chat.displayName = `${user.first_name} ${user.last_name}`
            }
          } catch (error) {
            console.error('Load user error:', error)
            chat.displayName = chat.name || 'Чат'
          }
        } else {
          // Это чат с самим собой
          chat.displayName = '📝 Сообщения для себя'
        }
      } else {
        // Групповой чат - используем название
        chat.displayName = chat.name || 'Групповой чат'
      }
    }
    
    // Сортировка происходит автоматически через computed свойство filteredChats
    chats.value = response.data
  } catch (error) {
    console.error('Load chats error:', error)
  }
}

async function loadUnreadCounts() {
  try {
    for (const chat of chats.value) {
      const response = await api.get(`/chats/${chat.id}/unread-count`)
      unreadMessages.value[chat.id] = response.data.count || 0
    }
  } catch (error) {
    console.error('Load unread counts error:', error)
  }
}

function getUnreadCount(chatId) {
  return unreadMessages.value[chatId] || 0
}

function handleChatCreated() {
  loadChats()
}

async function handleSearch() {
  // Очищаем предыдущий таймаут
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
  
  // Если поиск начинается с @, ищем пользователей
  if (searchQuery.value.startsWith('@') && searchQuery.value.length > 1) {
    searchTimeout = setTimeout(async () => {
      try {
        const username = searchQuery.value.substring(1)
        const response = await api.get(`/users?search=${username}`)
        searchResults.value = response.data
      } catch (error) {
        console.error('Search users error:', error)
        searchResults.value = []
      }
    }, 300)
  } else {
    searchResults.value = []
  }
}

function createChatWithUser(user) {
  // Очищаем поиск
  searchQuery.value = ''
  searchResults.value = []
  
  // Переходим в профиль пользователя
  router.push(`/users/${user.id}`)
}

function formatTime(dateStr) {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) return 'только что'
  if (diff < 3600000) return `${Math.floor(diff / 60000)} мин`
  if (diff < 86400000) return date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
  return date.toLocaleDateString('ru-RU')
}

// Swipe to delete functionality
function handleTouchStart(event, chatId) {
  swipeStates.value[chatId] = {
    startX: event.touches[0].clientX,
    translateX: 0,
    deleteWidth: 0
  }
}

function handleTouchMove(event, chatId) {
  if (!swipeStates.value[chatId]) return
  
  const currentX = event.touches[0].clientX
  const diff = swipeStates.value[chatId].startX - currentX
  
  // Свайп влево (показываем кнопку удаления)
  if (diff > 0) {
    const translateX = Math.min(diff, 80) // Максимум 80px
    swipeStates.value[chatId].translateX = -translateX
    swipeStates.value[chatId].deleteWidth = translateX
  }
}

async function handleTouchEnd(chatId) {
  if (!swipeStates.value[chatId]) return
  
  const translateX = Math.abs(swipeStates.value[chatId].translateX)
  
  // Если свайп больше 60px - удаляем
  if (translateX > 60) {
    const chat = chats.value.find(c => c.id === chatId)
    if (chat) {
      await confirmDeleteChat(chat)
    }
  }
  
  // Сбрасываем состояние
  swipeStates.value[chatId] = {
    startX: 0,
    translateX: 0,
    deleteWidth: 0
  }
}

// Mouse swipe handlers for desktop
function handleMouseDown(event, chatId) {
  swipeStates.value[chatId] = {
    startX: event.clientX,
    translateX: 0,
    deleteWidth: 0,
    isDragging: true
  }
  event.preventDefault()
}

function handleMouseMove(event, chatId) {
  if (!swipeStates.value[chatId]?.isDragging) return
  
  const currentX = event.clientX
  const diff = swipeStates.value[chatId].startX - currentX
  
  // Свайп влево (показываем кнопку удаления)
  if (diff > 0) {
    const translateX = Math.min(diff, 80) // Максимум 80px
    swipeStates.value[chatId].translateX = -translateX
    swipeStates.value[chatId].deleteWidth = translateX
  }
}

async function handleMouseUp(chatId) {
  if (!swipeStates.value[chatId]) return
  
  const translateX = Math.abs(swipeStates.value[chatId].translateX)
  swipeStates.value[chatId].isDragging = false
  
  // Если свайп больше 60px - удаляем
  if (translateX > 60) {
    const chat = chats.value.find(c => c.id === chatId)
    if (chat) {
      await confirmDeleteChat(chat)
    }
  }
  
  // Сбрасываем состояние
  swipeStates.value[chatId] = {
    startX: 0,
    translateX: 0,
    deleteWidth: 0,
    isDragging: false
  }
}

function handleMouseLeave(chatId) {
  if (swipeStates.value[chatId]?.isDragging) {
    swipeStates.value[chatId] = {
      startX: 0,
      translateX: 0,
      deleteWidth: 0,
      isDragging: false
    }
  }
}

async function confirmDeleteChat(chat) {
  if (!confirm(`Удалить чат "${chat.displayName || chat.name}"? Все сообщения будут удалены безвозвратно.`)) {
    return
  }
  
  try {
    const chatId = chat.id
    await api.delete(`/chats/${chatId}/`)
    chats.value = chats.value.filter(c => c.id !== chatId)
    delete unreadMessages.value[chatId]
    delete swipeStates.value[chatId]
    
    // Если мы находимся в удаленном чате - редиректим на список
    if (router.currentRoute.value.params.id == chatId) {
      router.push('/chats')
    }
  } catch (error) {
    console.error('Delete chat error:', error)
    alert('Ошибка удаления чата: ' + (error.response?.data?.detail || error.message))
  }
}
</script>
