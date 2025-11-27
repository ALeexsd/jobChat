<template>
  <div class="h-full flex flex-col bg-gray-50 dark:bg-gray-900">
    <!-- Заголовок -->
    <div class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Пользователи</h1>
          <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">Просмотр и поиск пользователей системы</p>
        </div>
        <div class="relative">
          <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Поиск пользователей..."
            class="input pl-10 w-64"
          />
        </div>
      </div>
    </div>

    <!-- Список пользователей -->
    <div class="flex-1 overflow-auto p-6">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="user in filteredUsers"
            :key="user.id"
            @click="viewUserProfile(user.id)"
            class="card dark:bg-gray-800 dark:border-gray-700 p-4 hover:shadow-lg transition-shadow cursor-pointer"
          >
            <div class="flex items-start space-x-4">
              <div v-if="user.avatar" class="relative">
                <img
                  :src="user.avatar"
                  :alt="user.first_name"
                  class="w-16 h-16 rounded-full"
                />
                <!-- Online status indicator -->
                <div
                  :class="[
                    'absolute bottom-0 right-0 w-4 h-4 rounded-full border-2 border-white dark:border-gray-800',
                    user.status === 'online' ? 'bg-green-500' : 
                    user.status === 'away' ? 'bg-yellow-500' : 
                    'bg-gray-400'
                  ]"
                ></div>
              </div>
              <div v-else class="w-16 h-16 rounded-full bg-blue-600 flex items-center justify-center text-white text-xl font-semibold relative">
                {{ user.first_name?.[0] }}{{ user.last_name?.[0] }}
                <!-- Online status indicator -->
                <div
                  :class="[
                    'absolute bottom-0 right-0 w-4 h-4 rounded-full border-2 border-white dark:border-gray-800',
                    user.status === 'online' ? 'bg-green-500' : 
                    user.status === 'away' ? 'bg-yellow-500' : 
                    'bg-gray-400'
                  ]"
                ></div>
              </div>
              
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2">
                  <h3 class="font-semibold text-gray-900 dark:text-gray-100 truncate">
                    {{ user.first_name }} {{ user.last_name }}
                  </h3>
                  <span
                    :class="[
                      'text-xs px-2 py-0.5 rounded-full',
                      user.status === 'online' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' : 
                      user.status === 'away' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200' : 
                      'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
                    ]"
                  >
                    {{ getStatusLabel(user.status) }}
                  </span>
                </div>
                <p class="text-sm text-gray-600 dark:text-gray-400 truncate">{{ user.email }}</p>
                <p v-if="user.position" class="text-sm text-gray-500 dark:text-gray-500 mt-1">
                  {{ user.position }}
                </p>
                <div class="flex items-center gap-2 mt-2">
                  <span
                    :class="[
                      'px-2 py-1 text-xs font-medium rounded-full',
                      user.role === 'admin'
                        ? 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
                        : 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
                    ]"
                  >
                    {{ user.role === 'admin' ? 'Администратор' : 'Пользователь' }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="filteredUsers.length === 0" class="text-center py-12">
          <UsersIcon class="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <p class="text-gray-600 dark:text-gray-400">Пользователи не найдены</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import { MagnifyingGlassIcon, UsersIcon } from '@heroicons/vue/24/outline'

const router = useRouter()
const users = ref([])
const searchQuery = ref('')

const filteredUsers = computed(() => {
  if (!searchQuery.value) return users.value

  const query = searchQuery.value.toLowerCase()
  return users.value.filter(u =>
    u.first_name?.toLowerCase().includes(query) ||
    u.last_name?.toLowerCase().includes(query) ||
    u.email?.toLowerCase().includes(query) ||
    u.position?.toLowerCase().includes(query)
  )
})

onMounted(() => {
  loadUsers()
})

async function loadUsers() {
  try {
    const response = await api.get('/users/')
    users.value = response.data
  } catch (error) {
    console.error('Load users error:', error)
  }
}

function viewUserProfile(userId) {
  router.push(`/users/${userId}`)
}

function getStatusLabel(status) {
  const labels = {
    online: 'Онлайн',
    offline: 'Оффлайн',
    away: 'Отошел'
  }
  return labels[status] || status
}
</script>
