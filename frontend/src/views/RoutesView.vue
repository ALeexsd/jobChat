<template>
  <div class="h-full flex flex-col bg-gray-50 dark:bg-gray-900">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 px-6 py-4 border-b border-gray-200 dark:border-gray-700">
      <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Маршруты</h1>
        <button 
          @click="showCreateModal = true" 
          class="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition-colors flex items-center gap-2"
        >
          <PlusIcon class="w-5 h-5" />
          <span>Новый</span>
        </button>
      </div>
    </div>
    
    <!-- Tabs -->
    <div class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
      <div class="flex px-6">
        <button
          @click="activeTab = 'all'"
          :class="[
            'px-4 py-3 text-sm font-medium border-b-2 transition-colors',
            activeTab === 'all'
              ? 'border-primary-600 text-primary-600 dark:text-primary-400'
              : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
          ]"
        >
          Все
        </button>
        <button
          @click="activeTab = 'assigned'"
          :class="[
            'px-4 py-3 text-sm font-medium border-b-2 transition-colors',
            activeTab === 'assigned'
              ? 'border-primary-600 text-primary-600 dark:text-primary-400'
              : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
          ]"
        >
          Мои
        </button>
      </div>
    </div>
    
    <!-- Routes List -->
    <div class="flex-1 overflow-auto p-6">
      <div v-if="filteredRoutes.length === 0" class="flex flex-col items-center justify-center py-20">
        <MapIcon class="w-16 h-16 text-gray-300 dark:text-gray-600 mb-4" />
        <p class="text-gray-400 dark:text-gray-500 text-sm mb-6">Нет маршрутов</p>
        <button 
          @click="showCreateModal = true" 
          class="bg-primary-600 hover:bg-primary-700 text-white px-6 py-2.5 rounded-lg text-sm font-medium"
        >
          Создать маршрут
        </button>
      </div>
      
      <div v-else class="max-w-4xl mx-auto space-y-6">
        <div
          v-for="route in filteredRoutes"
          :key="route.id"
          class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden"
        >
          <!-- Header -->
          <div class="px-6 py-4 bg-gray-50 dark:bg-gray-700/30 border-b border-gray-200 dark:border-gray-700">
            <div class="flex justify-between items-center">
              <div class="flex items-center gap-4">
                <div>
                  <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">ВСЕГО ТОЧЕК</p>
                  <p class="text-2xl font-bold text-gray-900 dark:text-gray-100">{{ route.locations?.length || 0 }}</p>
                </div>
              </div>
              <div class="text-right">
                <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">ДАТА</p>
                <p class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ formatDateFull(route.date) }}</p>
              </div>
            </div>
          </div>
          
          <!-- Points -->
          <div v-if="route.locations && route.locations.length" class="p-6">
            <div class="relative pl-14">
              <!-- Vertical Line -->
              <div class="absolute left-[26px] top-0 bottom-0 w-px bg-gray-300 dark:bg-gray-600"></div>
              
              <div class="space-y-4">
                <div
                  v-for="(location, index) in route.locations"
                  :key="index"
                  class="relative"
                >
                  <!-- Number Badge -->
                  <div 
                    :class="[
                      'absolute -left-14 w-[52px] h-[52px] rounded-xl flex items-center justify-center font-bold text-xl border-[3px] bg-white dark:bg-gray-800',
                      index === 0 
                        ? 'border-green-500 text-green-600 dark:text-green-400' 
                        : 'border-red-500 text-red-600 dark:text-red-400'
                    ]"
                  >
                    {{ index + 1 }}
                  </div>
                  
                  <!-- Card -->
                  <div class="bg-gray-50 dark:bg-gray-700/30 rounded-xl p-4">
                    <!-- Top section with icons -->
                    <div class="flex items-start justify-between gap-4 mb-3">
                      <div class="flex-1 min-w-0">
                        <p class="text-xs text-gray-400 dark:text-gray-500 mb-2">{{ formatDateShort(route.date) }}</p>
                        <h5 class="text-base font-semibold text-gray-900 dark:text-gray-100 mb-3">
                          {{ location.name }}
                        </h5>
                        <p v-if="location.contact_name" class="text-sm text-gray-700 dark:text-gray-300 mb-1">
                          {{ location.contact_name }}
                        </p>
                        <p v-if="location.contact_phone" class="text-sm text-gray-400 dark:text-gray-500">
                          {{ location.contact_phone }}
                        </p>
                      </div>
                      
                      <!-- Actions -->
                      <div class="flex gap-2">
                        <button 
                          v-if="location.latitude && location.longitude"
                          @click.stop="openNavigator(location)"
                          class="w-10 h-10 rounded-xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-blue-600 dark:text-blue-400 hover:bg-blue-200 dark:hover:bg-blue-900/50 transition-colors"
                          title="Открыть в навигаторе"
                        >
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                          </svg>
                        </button>
                        <a 
                          v-if="location.contact_phone"
                          :href="`tel:${location.contact_phone}`"
                          @click.stop
                          class="w-10 h-10 rounded-xl bg-green-100 dark:bg-green-900/30 flex items-center justify-center text-green-600 dark:text-green-400 hover:bg-green-200 dark:hover:bg-green-900/50 transition-colors"
                          title="Позвонить"
                        >
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                          </svg>
                        </a>
                        <button 
                          v-if="isRouteAuthor(route)"
                          @click.stop="handleEdit(route)"
                          class="w-10 h-10 rounded-xl bg-gray-200 dark:bg-gray-600 flex items-center justify-center text-gray-600 dark:text-gray-400 hover:bg-gray-300 dark:hover:bg-gray-500 transition-colors"
                          title="Редактировать"
                        >
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </button>
                      </div>
                    </div>
                    
                    <!-- Description at bottom -->
                    <div v-if="location.description && location.description !== location.name" class="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
                      <p class="text-sm text-gray-400 dark:text-gray-500">
                        {{ location.description }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <CreateRouteModal
      :show="showCreateModal"
      :edit-mode="editMode"
      :route-data="editingRoute"
      @close="closeCreateModal"
      @created="handleRouteCreated"
      @updated="handleRouteUpdated"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import websocket from '@/services/websocket'
import { PlusIcon, MapIcon } from '@heroicons/vue/24/outline'
import CreateRouteModal from '@/components/CreateRouteModal.vue'

const authStore = useAuthStore()
const showCreateModal = ref(false)
const editMode = ref(false)
const editingRoute = ref(null)
const routes = ref([])
const activeTab = ref('all')

const filteredRoutes = computed(() => {
  let filtered = routes.value
  
  if (activeTab.value === 'assigned') {
    filtered = filtered.filter(route => 
      route.assignees?.some(assignee => assignee.user_id === authStore.user?.id)
    )
  }
  
  return filtered
})

onMounted(() => {
  loadRoutes()
  websocket.on('route_assigned', handleRouteAssigned)
})

onUnmounted(() => {
  websocket.off('route_assigned', handleRouteAssigned)
})

async function handleRouteAssigned() {
  await loadRoutes()
}

async function loadRoutes() {
  try {
    const response = await api.get('/routes')
    routes.value = response.data
  } catch (error) {
    console.error('Load routes error:', error)
  }
}

async function handleRouteCreated() {
  await loadRoutes()
}

async function handleRouteUpdated() {
  await loadRoutes()
}

function handleEdit(route) {
  editMode.value = true
  editingRoute.value = route
  showCreateModal.value = true
}

function closeCreateModal() {
  showCreateModal.value = false
  editMode.value = false
  editingRoute.value = null
}

function isRouteAuthor(route) {
  return route.created_by_id === authStore.user?.id
}

function openNavigator(location) {
  if (location.latitude && location.longitude) {
    // Открываем Яндекс.Карты с координатами
    const url = `https://yandex.ru/maps/?pt=${location.longitude},${location.latitude}&z=16&l=map`
    window.open(url, '_blank')
  }
}

function formatDateFull(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('ru-RU', { 
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  }) + ' г.'
}

function formatDateShort(dateStr) {
  const date = new Date(dateStr)
  const formatted = date.toLocaleDateString('ru-RU', { 
    day: 'numeric',
    month: 'short'
  })
  return formatted.replace('.', '').toUpperCase()
}
</script>
