<template>
  <div class="h-full flex flex-col p-6">
    <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">Сотрудники</h1>
    
    <!-- Search -->
    <div class="mb-6">
      <div class="relative">
        <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Поиск сотрудников..."
          class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-gray-800 dark:text-gray-100"
        />
      </div>
    </div>
    
    <!-- Employees List -->
    <div class="flex-1 overflow-auto">
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
        <p class="text-gray-600 dark:text-gray-400">Загрузка...</p>
      </div>
      
      <div v-else-if="filteredEmployees.length === 0" class="text-center py-12">
        <UserGroupIcon class="w-16 h-16 mx-auto text-gray-400 mb-4" />
        <p class="text-gray-500 dark:text-gray-400">Сотрудники не найдены</p>
      </div>
      
      <div v-else class="space-y-2">
        <div
          v-for="employee in filteredEmployees"
          :key="employee.id"
          @click="goToProfile(employee.id)"
          class="card dark:bg-gray-800 dark:border-gray-700 p-4 hover:shadow-md transition-shadow cursor-pointer"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center flex-1 min-w-0">
              <!-- Avatar -->
              <div v-if="employee.avatar_url" class="w-12 h-12 rounded-full overflow-hidden flex-shrink-0">
                <img :src="`http://localhost:8000${employee.avatar_url}`" alt="Avatar" class="w-full h-full object-cover" />
              </div>
              <div v-else class="w-12 h-12 rounded-full bg-primary-600 flex items-center justify-center text-white font-semibold flex-shrink-0">
                {{ getInitials(employee) }}
              </div>
              
              <!-- Info -->
              <div class="ml-4 flex-1 min-w-0">
                <div class="flex items-center">
                  <h3 class="text-base font-semibold text-gray-900 dark:text-gray-100 truncate">
                    {{ employee.first_name }} {{ employee.last_name }}
                  </h3>
                  <!-- Status -->
                  <div class="flex items-center ml-3">
                    <div :class="[
                      'w-2 h-2 rounded-full',
                      employee.status === 'online' ? 'bg-green-500' : 
                      employee.status === 'away' ? 'bg-yellow-500' : 
                      'bg-gray-400'
                    ]" :title="getStatusLabel(employee.status)"></div>
                  </div>
                </div>
                <div class="flex items-center mt-1 space-x-3">
                  <p class="text-sm text-gray-600 dark:text-gray-400">@{{ employee.username }}</p>
                  <p v-if="employee.position" class="text-sm text-gray-500 dark:text-gray-500">
                    {{ employee.position }}
                  </p>
                </div>
              </div>
            </div>
            
            <!-- Action Button -->
            <button
              @click.stop="createChat(employee)"
              class="ml-4 btn-primary flex items-center flex-shrink-0"
            >
              <ChatBubbleLeftRightIcon class="w-5 h-5 mr-2" />
              Написать
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import {
  MagnifyingGlassIcon,
  UserGroupIcon,
  ChatBubbleLeftRightIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const employees = ref([])
const searchQuery = ref('')
const loading = ref(true)

const filteredEmployees = computed(() => {
  if (!searchQuery.value) return employees.value
  
  const query = searchQuery.value.toLowerCase()
  return employees.value.filter(emp => 
    emp.first_name.toLowerCase().includes(query) ||
    emp.last_name.toLowerCase().includes(query) ||
    emp.username.toLowerCase().includes(query) ||
    (emp.position && emp.position.toLowerCase().includes(query))
  )
})

onMounted(async () => {
  await loadEmployees()
})

async function loadEmployees() {
  loading.value = true
  try {
    const response = await api.get('/users')
    employees.value = response.data
  } catch (error) {
    console.error('Load employees error:', error)
  } finally {
    loading.value = false
  }
}

function getInitials(employee) {
  return `${employee.first_name?.[0] || ''}${employee.last_name?.[0] || ''}`
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

function goToProfile(userId) {
  router.push(`/users/${userId}`)
}

async function createChat(employee) {
  try {
    const response = await api.post('/chats/', {
      name: `${employee.first_name} ${employee.last_name}`,
      chat_type: 'private',
      member_ids: [employee.id]
    })
    
    router.push(`/chats/${response.data.id}`)
  } catch (error) {
    console.error('Create chat error:', error)
    alert('Ошибка создания чата: ' + (error.response?.data?.detail || error.message))
  }
}
</script>
