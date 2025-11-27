<template>
  <div class="h-full overflow-auto p-6 bg-gray-50 dark:bg-gray-900">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">Управление маршрутами</h1>

      <div class="grid gap-4">
        <div v-for="route in routes" :key="route.id" class="card dark:bg-gray-800 dark:border-gray-700 p-4">
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <h3 class="font-semibold text-gray-900 dark:text-gray-100 mb-2">{{ route.name }}</h3>
              <div class="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                <p>Откуда: {{ route.start_location }}</p>
                <p>Куда: {{ route.end_location }}</p>
                <p>Дата: {{ formatDate(route.date) }}</p>
                <p>Создатель: {{ route.creator_name }}</p>
              </div>
            </div>
            <button @click="deleteRoute(route.id)" class="text-red-600 hover:text-red-700 p-2">
              <TrashIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import { TrashIcon } from '@heroicons/vue/24/outline'

const routes = ref([])

onMounted(() => {
  loadRoutes()
})

async function loadRoutes() {
  try {
    const response = await api.get('/routes/')
    routes.value = response.data
  } catch (error) {
    console.error('Load routes error:', error)
  }
}

async function deleteRoute(id) {
  if (!confirm('Удалить маршрут?')) return
  try {
    await api.delete(`/routes/${id}`)
    await loadRoutes()
  } catch (error) {
    console.error('Delete route error:', error)
  }
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('ru-RU')
}
</script>
