<template>
  <div class="h-full overflow-auto p-6 bg-gray-50 dark:bg-gray-900">
    <div class="max-w-7xl mx-auto">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Управление отпусками</h1>
        <div class="flex gap-3">
          <select v-model="filterStatus" class="input">
            <option value="">Все статусы</option>
            <option value="pending">Ожидает</option>
            <option value="approved">Одобрено</option>
            <option value="rejected">Отклонено</option>
          </select>
        </div>
      </div>

      <div class="grid gap-4">
        <div v-for="vacation in filteredVacations" :key="vacation.id" class="card dark:bg-gray-800 dark:border-gray-700 p-6">
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-3">
                <div class="w-12 h-12 rounded-full bg-blue-600 flex items-center justify-center text-white font-semibold">
                  {{ vacation.user_name?.[0] || '?' }}
                </div>
                <div>
                  <h3 class="font-semibold text-gray-900 dark:text-gray-100">{{ vacation.user_name || 'Неизвестный пользователь' }}</h3>
                  <p class="text-sm text-gray-600 dark:text-gray-400">ID пользователя: {{ vacation.user_id }}</p>
                </div>
              </div>
              
              <div class="space-y-2 text-sm">
                <div class="flex items-center gap-2">
                  <CalendarIcon class="w-5 h-5 text-gray-400" />
                  <span class="text-gray-900 dark:text-gray-100">
                    {{ formatDate(vacation.start_date) }} - {{ formatDate(vacation.end_date) }}
                  </span>
                  <span class="text-gray-600 dark:text-gray-400">
                    ({{ calculateDays(vacation.start_date, vacation.end_date) }} дней)
                  </span>
                </div>
                
                <div v-if="vacation.reason" class="flex items-start gap-2">
                  <DocumentTextIcon class="w-5 h-5 text-gray-400 mt-0.5" />
                  <span class="text-gray-600 dark:text-gray-400">{{ vacation.reason }}</span>
                </div>
                
                <div class="flex items-center gap-2">
                  <span
                    :class="[
                      'px-3 py-1 rounded-full text-xs font-medium',
                      vacation.status === 'approved' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' :
                      vacation.status === 'rejected' ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200' :
                      'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                    ]"
                  >
                    {{ getStatusText(vacation.status) }}
                  </span>
                  <span class="text-xs text-gray-500 dark:text-gray-400">
                    Создано: {{ formatDate(vacation.created_at) }}
                  </span>
                </div>
              </div>
            </div>
            
            <div class="flex items-center gap-2 ml-4">
              <button
                v-if="vacation.status === 'pending'"
                @click="updateStatus(vacation.id, 'approved')"
                class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg text-sm font-medium transition-colors"
              >
                Одобрить
              </button>
              <button
                v-if="vacation.status === 'pending'"
                @click="updateStatus(vacation.id, 'rejected')"
                class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg text-sm font-medium transition-colors"
              >
                Отклонить
              </button>
              <button
                @click="deleteVacation(vacation.id)"
                class="p-2 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                title="Удалить"
              >
                <TrashIcon class="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>

        <div v-if="filteredVacations.length === 0" class="text-center py-12">
          <CalendarIcon class="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <p class="text-gray-600 dark:text-gray-400">Заявки на отпуск не найдены</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import { CalendarIcon, DocumentTextIcon, TrashIcon } from '@heroicons/vue/24/outline'

const vacations = ref([])
const filterStatus = ref('')

const filteredVacations = computed(() => {
  if (!filterStatus.value) return vacations.value
  return vacations.value.filter(v => v.status === filterStatus.value)
})

onMounted(() => {
  loadVacations()
})

async function loadVacations() {
  try {
    const response = await api.get('/vacations/')
    vacations.value = response.data
  } catch (error) {
    console.error('Load vacations error:', error)
  }
}

async function updateStatus(id, status) {
  try {
    await api.put(`/vacations/${id}`, { status })
    await loadVacations()
  } catch (error) {
    console.error('Update vacation status error:', error)
    alert('Ошибка при обновлении статуса')
  }
}

async function deleteVacation(id) {
  if (!confirm('Удалить заявку на отпуск?')) return
  try {
    await api.delete(`/vacations/${id}`)
    await loadVacations()
  } catch (error) {
    console.error('Delete vacation error:', error)
    alert('Ошибка при удалении заявки')
  }
}

function formatDate(date) {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

function calculateDays(startDate, endDate) {
  if (!startDate || !endDate) return 0
  const start = new Date(startDate)
  const end = new Date(endDate)
  const diffTime = Math.abs(end - start)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays + 1
}

function getStatusText(status) {
  const statuses = {
    pending: 'Ожидает одобрения',
    approved: 'Одобрено',
    rejected: 'Отклонено'
  }
  return statuses[status] || status
}
</script>
