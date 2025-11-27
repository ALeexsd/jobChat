<template>
  <div class="h-full overflow-auto p-6 bg-gray-50 dark:bg-gray-900">
    <div v-if="loading" class="flex items-center justify-center h-full">
      <div class="text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
        <p class="text-gray-600 dark:text-gray-400">Загрузка...</p>
      </div>
    </div>
    
    <div v-else-if="error" class="flex items-center justify-center h-full">
      <div class="text-center">
        <p class="text-red-600 dark:text-red-400 mb-4">{{ error }}</p>
        <button @click="$router.go(-1)" class="btn-secondary">
          Назад
        </button>
      </div>
    </div>
    
    <div v-else class="max-w-4xl mx-auto">
      <div class="flex items-center mb-6">
        <button @click="$router.go(-1)" class="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg mr-4">
          <ArrowLeftIcon class="w-6 h-6 text-gray-600 dark:text-gray-400" />
        </button>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Профиль пользователя</h1>
      </div>
      
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Avatar Card -->
        <div class="card dark:bg-gray-800 dark:border-gray-700 p-6">
          <div class="text-center">
            <div v-if="user.avatar_url" class="w-24 h-24 rounded-full mx-auto mb-4 overflow-hidden">
              <img :src="`http://localhost:8000${user.avatar_url}`" alt="Avatar" class="w-full h-full object-cover" />
            </div>
            <div v-else class="w-24 h-24 rounded-full bg-primary-600 flex items-center justify-center text-white text-3xl font-semibold mx-auto mb-4">
              {{ userInitials }}
            </div>
            <h2 class="text-xl font-semibold text-gray-900 dark:text-gray-100">
              {{ user.first_name }} {{ user.last_name }}
            </h2>
            <p class="text-gray-600 dark:text-gray-400 mt-1">@{{ user.username }}</p>
            <p class="text-gray-500 dark:text-gray-500 text-sm mt-2">{{ user.position || 'Сотрудник' }}</p>
            
            <!-- Status -->
            <div class="mt-4 flex items-center justify-center">
              <div :class="[
                'w-3 h-3 rounded-full mr-2',
                user.status === 'online' ? 'bg-green-500' : 'bg-gray-400'
              ]"></div>
              <span class="text-sm text-gray-600 dark:text-gray-400">
                {{ getStatusLabel(user.status) }}
              </span>
            </div>
            
            <!-- Actions -->
            <div class="mt-6 space-y-2">
              <button @click="startChat" class="w-full btn-primary">
                <ChatBubbleLeftRightIcon class="w-5 h-5 inline mr-2" />
                Написать сообщение
              </button>
              <button @click="createTask" class="w-full btn-secondary">
                <ClipboardDocumentListIcon class="w-5 h-5 inline mr-2" />
                Назначить задачу
              </button>
            </div>
          </div>
        </div>
        
        <!-- Info Card -->
        <div class="lg:col-span-2 space-y-6">
          <div class="card dark:bg-gray-800 dark:border-gray-700 p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Информация</h3>
            
            <div class="space-y-4">
              <div v-if="user.email">
                <label class="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                  Email
                </label>
                <p class="text-gray-900 dark:text-gray-100">{{ user.email }}</p>
              </div>
              
              <div v-if="user.phone">
                <label class="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                  Телефон
                </label>
                <p class="text-gray-900 dark:text-gray-100">{{ user.phone }}</p>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                  Роль
                </label>
                <span :class="[
                  'px-2 py-1 text-xs font-medium rounded',
                  getRoleClass(user.role)
                ]">
                  {{ getRoleLabel(user.role) }}
                </span>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                  Последняя активность
                </label>
                <p class="text-gray-900 dark:text-gray-100">{{ formatDate(user.last_seen) }}</p>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                  Дата регистрации
                </label>
                <p class="text-gray-900 dark:text-gray-100">{{ formatDate(user.created_at) }}</p>
              </div>
            </div>
          </div>
          
          <!-- Stats Card -->
          <div class="card dark:bg-gray-800 dark:border-gray-700 p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Статистика</h3>
            
            <div class="grid grid-cols-3 gap-4">
              <div class="text-center">
                <p class="text-2xl font-bold text-primary-600 dark:text-primary-400">0</p>
                <p class="text-sm text-gray-600 dark:text-gray-400">Задач</p>
              </div>
              <div class="text-center">
                <p class="text-2xl font-bold text-primary-600 dark:text-primary-400">0</p>
                <p class="text-sm text-gray-600 dark:text-gray-400">Сообщений</p>
              </div>
              <div class="text-center">
                <p class="text-2xl font-bold text-primary-600 dark:text-primary-400">0</p>
                <p class="text-sm text-gray-600 dark:text-gray-400">Заметок</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'
import {
  ArrowLeftIcon,
  ChatBubbleLeftRightIcon,
  ClipboardDocumentListIcon
} from '@heroicons/vue/24/outline'

const route = useRoute()
const router = useRouter()

const user = ref(null)
const loading = ref(true)
const error = ref('')

const userInitials = computed(() => {
  if (!user.value) return '?'
  return `${user.value.first_name?.[0] || ''}${user.value.last_name?.[0] || ''}`
})

onMounted(async () => {
  await loadUser()
})

async function loadUser() {
  loading.value = true
  error.value = ''
  
  try {
    // Проверяем, это ID или username
    const identifier = route.params.id
    let response
    
    if (identifier.startsWith('@')) {
      // Поиск по username
      const username = identifier.substring(1)
      response = await api.get(`/users?search=${username}`)
      if (response.data.length > 0) {
        // Ищем точное совпадение username
        const exactMatch = response.data.find(u => u.username === username)
        user.value = exactMatch || response.data[0]
      } else {
        error.value = 'Пользователь не найден'
      }
    } else {
      // Поиск по ID
      response = await api.get(`/users/${identifier}`)
      user.value = response.data
    }
  } catch (err) {
    console.error('Load user error:', err)
    error.value = 'Ошибка загрузки профиля пользователя'
  } finally {
    loading.value = false
  }
}

async function startChat() {
  try {
    // Создаем личный чат с пользователем
    const response = await api.post('/chats/', {
      name: `${user.value.first_name} ${user.value.last_name}`,
      chat_type: 'private',
      member_ids: [user.value.id]
    })
    
    router.push(`/chats/${response.data.id}`)
  } catch (error) {
    console.error('Create chat error:', error)
    alert('Ошибка создания чата: ' + (error.response?.data?.detail || error.message))
  }
}

function createTask() {
  // Перенаправляем на страницу задач с параметром assignee
  router.push({
    path: '/tasks',
    query: { assignee: user.value.id }
  })
}

function getStatusLabel(status) {
  const labels = {
    online: 'Онлайн',
    offline: 'Оффлайн',
    away: 'Отошел',
    busy: 'Занят'
  }
  return labels[status] || status
}

function getRoleClass(role) {
  const classes = {
    admin: 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300',
    manager: 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300',
    employee: 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
  }
  return classes[role] || classes.employee
}

function getRoleLabel(role) {
  const labels = {
    admin: 'Администратор',
    manager: 'Менеджер',
    employee: 'Сотрудник'
  }
  return labels[role] || role
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleString('ru-RU')
}
</script>
