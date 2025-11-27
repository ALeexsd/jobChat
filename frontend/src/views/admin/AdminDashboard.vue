<template>
  <div class="h-full overflow-auto p-6 bg-gray-50 dark:bg-gray-900">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-8">Панель администратора</h1>
      
      <!-- Статистика -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="card dark:bg-gray-800 dark:border-gray-700 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">Всего пользователей</p>
              <p class="text-3xl font-bold text-gray-900 dark:text-gray-100">{{ stats.totalUsers }}</p>
            </div>
            <div class="w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
              <UsersIcon class="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
          </div>
        </div>

        <div class="card dark:bg-gray-800 dark:border-gray-700 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">Активных задач</p>
              <p class="text-3xl font-bold text-gray-900 dark:text-gray-100">{{ stats.totalTasks }}</p>
            </div>
            <div class="w-12 h-12 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center">
              <ClipboardDocumentListIcon class="w-6 h-6 text-green-600 dark:text-green-400" />
            </div>
          </div>
        </div>

        <div class="card dark:bg-gray-800 dark:border-gray-700 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">Отпусков</p>
              <p class="text-3xl font-bold text-gray-900 dark:text-gray-100">{{ stats.totalVacations }}</p>
            </div>
            <div class="w-12 h-12 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center">
              <CalendarIcon class="w-6 h-6 text-purple-600 dark:text-purple-400" />
            </div>
          </div>
        </div>

        <div class="card dark:bg-gray-800 dark:border-gray-700 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">Активных чатов</p>
              <p class="text-3xl font-bold text-gray-900 dark:text-gray-100">{{ stats.totalChats }}</p>
            </div>
            <div class="w-12 h-12 bg-orange-100 dark:bg-orange-900 rounded-lg flex items-center justify-center">
              <ChatBubbleLeftRightIcon class="w-6 h-6 text-orange-600 dark:text-orange-400" />
            </div>
          </div>
        </div>
      </div>

      <!-- Разделы управления -->
      <div class="mb-8">
        <h2 class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Управление системой</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          
          <!-- Управление пользователями -->
          <router-link to="/admin/users" class="card dark:bg-gray-800 dark:border-gray-700 p-6 hover:shadow-lg transition-shadow cursor-pointer">
            <div class="flex items-start space-x-4">
              <div class="w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center flex-shrink-0">
                <UsersIcon class="w-6 h-6 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">Пользователи</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">Управление учетными записями, ролями и правами доступа</p>
              </div>
            </div>
          </router-link>

          <!-- Управление отпусками -->
          <router-link to="/admin/vacations" class="card dark:bg-gray-800 dark:border-gray-700 p-6 hover:shadow-lg transition-shadow cursor-pointer">
            <div class="flex items-start space-x-4">
              <div class="w-12 h-12 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center flex-shrink-0">
                <CalendarIcon class="w-6 h-6 text-purple-600 dark:text-purple-400" />
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">Отпуска</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">Одобрение и управление заявками на отпуск</p>
              </div>
            </div>
          </router-link>

          <!-- Управление задачами -->
          <router-link to="/admin/tasks" class="card dark:bg-gray-800 dark:border-gray-700 p-6 hover:shadow-lg transition-shadow cursor-pointer">
            <div class="flex items-start space-x-4">
              <div class="w-12 h-12 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center flex-shrink-0">
                <ClipboardDocumentListIcon class="w-6 h-6 text-green-600 dark:text-green-400" />
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">Задачи</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">Мониторинг и управление всеми задачами</p>
              </div>
            </div>
          </router-link>

          <!-- Управление маршрутами -->
          <router-link to="/admin/routes" class="card dark:bg-gray-800 dark:border-gray-700 p-6 hover:shadow-lg transition-shadow cursor-pointer">
            <div class="flex items-start space-x-4">
              <div class="w-12 h-12 bg-yellow-100 dark:bg-yellow-900 rounded-lg flex items-center justify-center flex-shrink-0">
                <MapIcon class="w-6 h-6 text-yellow-600 dark:text-yellow-400" />
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">Маршруты</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">Управление маршрутами и логистикой</p>
              </div>
            </div>
          </router-link>

          <!-- Управление заметками -->
          <router-link to="/admin/notes" class="card dark:bg-gray-800 dark:border-gray-700 p-6 hover:shadow-lg transition-shadow cursor-pointer">
            <div class="flex items-start space-x-4">
              <div class="w-12 h-12 bg-indigo-100 dark:bg-indigo-900 rounded-lg flex items-center justify-center flex-shrink-0">
                <DocumentTextIcon class="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">Заметки</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">Просмотр и управление заметками пользователей</p>
              </div>
            </div>
          </router-link>

          <!-- Управление чатами -->
          <router-link to="/admin/chats" class="card dark:bg-gray-800 dark:border-gray-700 p-6 hover:shadow-lg transition-shadow cursor-pointer">
            <div class="flex items-start space-x-4">
              <div class="w-12 h-12 bg-orange-100 dark:bg-orange-900 rounded-lg flex items-center justify-center flex-shrink-0">
                <ChatBubbleLeftRightIcon class="w-6 h-6 text-orange-600 dark:text-orange-400" />
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">Чаты</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">Мониторинг и модерация чатов</p>
              </div>
            </div>
          </router-link>

        </div>
      </div>

      <!-- Последняя активность -->
      <div>
        <h2 class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Последняя активность</h2>
        <div class="card dark:bg-gray-800 dark:border-gray-700 p-6">
          <div class="space-y-4">
            <div v-for="activity in recentActivity" :key="activity.id" class="flex items-start space-x-3 pb-4 border-b border-gray-200 dark:border-gray-700 last:border-0 last:pb-0">
              <div class="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
              <div class="flex-1">
                <p class="text-sm text-gray-900 dark:text-gray-100">{{ activity.text }}</p>
                <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">{{ activity.time }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import { 
  UsersIcon, 
  ClipboardDocumentListIcon, 
  CalendarIcon, 
  ChatBubbleLeftRightIcon,
  MapIcon,
  DocumentTextIcon
} from '@heroicons/vue/24/outline'

const stats = ref({
  totalUsers: 0,
  totalTasks: 0,
  totalVacations: 0,
  totalChats: 0
})

const recentActivity = ref([])

onMounted(() => {
  loadStats()
  loadRecentActivity()
})

async function loadStats() {
  try {
    const [usersRes, tasksRes, vacationsRes, chatsRes] = await Promise.all([
      api.get('/users/'),
      api.get('/tasks/'),
      api.get('/vacations/'),
      api.get('/chats/')
    ])
    
    stats.value.totalUsers = usersRes.data.length
    stats.value.totalTasks = tasksRes.data.length
    stats.value.totalVacations = vacationsRes.data.length
    stats.value.totalChats = chatsRes.data.length
  } catch (error) {
    console.error('Load stats error:', error)
  }
}

async function loadRecentActivity() {
  // Заглушка для последней активности
  recentActivity.value = [
    { id: 1, text: 'Новый пользователь зарегистрирован', time: '5 минут назад' },
    { id: 2, text: 'Задача "Разработка API" завершена', time: '15 минут назад' },
    { id: 3, text: 'Заявка на отпуск одобрена', time: '1 час назад' },
    { id: 4, text: 'Создан новый групповой чат', time: '2 часа назад' }
  ]
}
</script>
