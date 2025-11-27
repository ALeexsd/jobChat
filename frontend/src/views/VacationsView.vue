<template>
  <div class="h-full flex flex-col p-6 bg-white dark:bg-gray-900">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Отпуска</h1>
      <button @click="showCreateModal = true" class="btn-primary flex items-center">
        <PlusIcon class="w-5 h-5 mr-2" />
        Подать заявление
      </button>
    </div>
    
    <!-- Vacations List -->
    <div class="flex-1 overflow-auto">
      <div v-if="vacations.length === 0" class="text-center py-12">
        <CalendarDaysIcon class="w-16 h-16 mx-auto text-gray-400 mb-4" />
        <p class="text-gray-500 dark:text-gray-400 mb-4">Нет заявок на отпуск</p>
        <button @click="showCreateModal = true" class="btn-primary">
          Подать первую заявку
        </button>
      </div>
      
      <div v-else class="space-y-4">
        <div
          v-for="vacation in vacations"
          :key="vacation.id"
          class="card dark:bg-gray-800 dark:border-gray-700 p-4 hover:shadow-md transition-shadow"
        >
          <div class="flex items-start justify-between mb-3">
            <div class="flex-1">
              <div class="flex items-center space-x-3 mb-2">
                <span :class="['px-2 py-1 rounded-full text-xs font-medium', getStatusColor(vacation.status)]">
                  {{ getStatusLabel(vacation.status) }}
                </span>
                
                <span :class="['px-2 py-1 rounded-full text-xs font-medium', getTypeColor(vacation.vacation_type)]">
                  {{ getTypeLabel(vacation.vacation_type) }}
                </span>
              </div>
              
              <div class="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                <p><strong>Период:</strong> {{ formatDate(vacation.start_date) }} - {{ formatDate(vacation.end_date) }}</p>
                <p><strong>Дней:</strong> {{ getDaysDifference(vacation.start_date, vacation.end_date) }}</p>
                <p v-if="vacation.comment"><strong>Комментарий:</strong> {{ vacation.comment }}</p>
              </div>
            </div>
            
            <button
              v-if="vacation.status === 'pending'"
              @click="cancelVacation(vacation.id)"
              class="text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 p-1"
            >
              <TrashIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Create Modal -->
    <CreateVacationModal
      :show="showCreateModal"
      @close="showCreateModal = false"
      @created="handleVacationCreated"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import { PlusIcon, CalendarDaysIcon, TrashIcon } from '@heroicons/vue/24/outline'
import CreateVacationModal from '@/components/CreateVacationModal.vue'

const showCreateModal = ref(false)
const vacations = ref([])

onMounted(() => {
  loadVacations()
})

async function loadVacations() {
  try {
    const response = await api.get('/vacations')
    vacations.value = response.data
  } catch (error) {
    console.error('Load vacations error:', error)
  }
}

async function handleVacationCreated() {
  await loadVacations()
}

async function cancelVacation(id) {
  if (!confirm('Отменить заявление?')) return
  
  try {
    await api.delete(`/vacations/${id}`)
    await loadVacations()
  } catch (error) {
    console.error('Cancel vacation error:', error)
  }
}

function getStatusColor(status) {
  const colors = {
    pending: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300',
    approved: 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300',
    rejected: 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300'
  }
  return colors[status] || 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
}

function getStatusLabel(status) {
  const labels = {
    pending: 'На рассмотрении',
    approved: 'Одобрено',
    rejected: 'Отклонено'
  }
  return labels[status] || status
}

function getTypeColor(type) {
  const colors = {
    vacation: 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300',
    sick_leave: 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300',
    personal: 'bg-indigo-100 text-indigo-700 dark:bg-indigo-900 dark:text-indigo-300'
  }
  return colors[type] || 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
}

function getTypeLabel(type) {
  const labels = {
    vacation: 'Отпуск',
    sick_leave: 'Больничный',
    personal: 'Личный день'
  }
  return labels[type] || type
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('ru-RU')
}

function getDaysDifference(startDate, endDate) {
  const start = new Date(startDate)
  const end = new Date(endDate)
  const diffTime = Math.abs(end - start)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1
  return diffDays
}
</script>
