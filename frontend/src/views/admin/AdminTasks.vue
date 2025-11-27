<template>
  <div class="h-full overflow-auto p-6 bg-gray-50 dark:bg-gray-900">
    <div class="max-w-7xl mx-auto">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Управление задачами</h1>
        <div class="flex gap-3">
          <select v-model="filterStatus" class="input">
            <option value="">Все статусы</option>
            <option value="pending">В ожидании</option>
            <option value="in_progress">В работе</option>
            <option value="completed">Завершено</option>
          </select>
        </div>
      </div>

      <div class="grid gap-4">
        <div v-for="task in filteredTasks" :key="task.id" class="card dark:bg-gray-800 dark:border-gray-700 p-4">
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <h3 class="font-semibold text-gray-900 dark:text-gray-100 mb-2">{{ task.title }}</h3>
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">{{ task.description }}</p>
              <div class="flex items-center gap-4 text-sm">
                <span class="text-gray-600 dark:text-gray-400">
                  Исполнитель: {{ task.assigned_to_name || 'Не назначен' }}
                </span>
                <span
                  :class="[
                    'px-2 py-1 rounded-full text-xs font-medium',
                    task.status === 'completed' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' :
                    task.status === 'in_progress' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200' :
                    'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
                  ]"
                >
                  {{ getStatusText(task.status) }}
                </span>
              </div>
            </div>
            <button @click="deleteTask(task.id)" class="text-red-600 hover:text-red-700 p-2">
              <TrashIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import { TrashIcon } from '@heroicons/vue/24/outline'

const tasks = ref([])
const filterStatus = ref('')

const filteredTasks = computed(() => {
  if (!filterStatus.value) return tasks.value
  return tasks.value.filter(t => t.status === filterStatus.value)
})

onMounted(() => {
  loadTasks()
})

async function loadTasks() {
  try {
    const response = await api.get('/tasks/')
    tasks.value = response.data
  } catch (error) {
    console.error('Load tasks error:', error)
  }
}

async function deleteTask(id) {
  if (!confirm('Удалить задачу?')) return
  try {
    await api.delete(`/tasks/${id}`)
    await loadTasks()
  } catch (error) {
    console.error('Delete task error:', error)
  }
}

function getStatusText(status) {
  const statuses = {
    pending: 'В ожидании',
    in_progress: 'В работе',
    completed: 'Завершено'
  }
  return statuses[status] || status
}
</script>
