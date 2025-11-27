<template>
  <TransitionRoot appear :show="show" as="template">
    <Dialog as="div" @close="closeModal" class="relative z-50">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black/75" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-end sm:items-center justify-center sm:p-4">
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 translate-y-full sm:scale-95"
            enter-to="opacity-100 translate-y-0 sm:scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 translate-y-0 sm:scale-100"
            leave-to="opacity-0 translate-y-full sm:scale-95"
          >
            <DialogPanel class="w-full max-h-[90vh] sm:max-w-2xl bg-white dark:bg-gray-800 rounded-t-3xl sm:rounded-3xl shadow-xl flex flex-col overflow-hidden">
              <!-- Header -->
              <div class="flex items-center justify-between px-5 py-4 border-b border-gray-100 dark:border-gray-700">
                <DialogTitle as="h3" class="text-lg font-bold text-gray-900 dark:text-gray-100">
                  {{ editMode ? 'Редактировать' : 'Новый маршрут' }}
                </DialogTitle>
                <button @click="closeModal" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 p-2">
                  <XMarkIcon class="w-6 h-6" />
                </button>
              </div>
              
              <!-- Content -->
              <form @submit.prevent="handleSubmit" class="flex-1 overflow-y-auto p-5 space-y-5">
                <!-- Date -->
                <div>
                  <label class="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-2">Дата поездки</label>
                  <input
                    v-model="formData.start_date"
                    type="date"
                    required
                    class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-xl text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
                
                <!-- Driver -->
                <div>
                  <label class="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-2">Назначить</label>
                  <select 
                    v-model="formData.driver_id" 
                    class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-xl text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option :value="null">Не назначен</option>
                    <option v-for="user in users" :key="user.id" :value="user.id">
                      {{ user.first_name }} {{ user.last_name }}
                    </option>
                  </select>
                </div>
                
                <!-- Points -->
                <div>
                  <label class="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-3">Точки маршрута</label>
                  <div class="space-y-3">
                    <div 
                      v-for="(point, index) in routePoints" 
                      :key="index" 
                      class="bg-gray-50 dark:bg-gray-700/50 rounded-2xl p-4"
                    >
                      <!-- Header -->
                      <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center gap-2">
                          <div 
                            :class="[
                              'w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm border-2',
                              index === 0 
                                ? 'bg-white dark:bg-gray-800 border-green-500 text-green-600' 
                                : 'bg-white dark:bg-gray-800 border-red-500 text-red-600'
                            ]"
                          >
                            {{ index + 1 }}
                          </div>
                          <span class="text-sm font-semibold text-gray-700 dark:text-gray-300">Точка маршрута</span>
                        </div>
                        <button
                          v-if="routePoints.length > 1"
                          type="button"
                          @click="removePoint(index)"
                          class="text-gray-400 hover:text-red-500 p-1"
                        >
                          <TrashIcon class="w-5 h-5" />
                        </button>
                      </div>
                      
                      <!-- Fields -->
                      <div class="space-y-3">
                        <div>
                          <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1.5">Адрес</label>
                          <input
                            v-model="point.address"
                            type="text"
                            class="w-full px-3 py-2.5 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-xl text-sm text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                            placeholder="Улица, дом, город"
                          />
                        </div>
                        
                        <div class="grid grid-cols-2 gap-3">
                          <div>
                            <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1.5">ФИО</label>
                            <input
                              v-model="point.fullName"
                              type="text"
                              class="w-full px-3 py-2.5 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-xl text-sm text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                              placeholder="Иванов И.И."
                            />
                          </div>
                          
                          <div>
                            <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1.5">Номер телефона</label>
                            <input
                              v-model="point.phone"
                              type="tel"
                              class="w-full px-3 py-2.5 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-xl text-sm text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                              placeholder="+7 (XXX) XXX-XX-XX"
                            />
                          </div>

                          <div>
                            <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1.5">Описание задачи</label>
                            <textarea
                              v-model="point.description"
                              rows="2"
                              class="w-full px-3 py-2.5 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-xl text-sm text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                              placeholder="Доставить/Забрать груз, особенности"
                            ></textarea>
                          </div>

                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Add button -->
                  <button
                    type="button"
                    @click="addPoint"
                    class="mt-3 w-full py-3 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl text-sm font-medium text-gray-500 dark:text-gray-400 hover:border-primary-500 hover:text-primary-600 hover:bg-primary-50 dark:hover:bg-primary-900/10 flex items-center justify-center gap-2"
                  >
                    <PlusIcon class="w-5 h-5" />
                    Добавить точку
                  </button>
                </div>
              </form>
              
              <!-- Footer -->
              <div class="flex gap-3 px-5 py-4 border-t border-gray-100 dark:border-gray-700">
                <button 
                  type="button" 
                  @click="closeModal" 
                  class="flex-1 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 font-medium py-3 rounded-xl"
                >
                  Отмена
                </button>
                <button 
                  type="button" 
                  @click="handleSubmit" 
                  :disabled="loading" 
                  class="flex-1 bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-medium py-3 rounded-xl"
                >
                  {{ loading ? 'Сохранение...' : (editMode ? 'Сохранить' : 'Создать') }}
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import api from '@/services/api'
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle
} from '@headlessui/vue'
import { PlusIcon, TrashIcon, XMarkIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  editMode: {
    type: Boolean,
    default: false
  },
  routeData: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'created', 'updated'])

const loading = ref(false)
const users = ref([])

const formData = ref({
  start_date: '',
  driver_id: null
})

const routePoints = ref([
  { description: '', address: '', fullName: '', phone: '' }
])

watch(() => props.show, (newValue) => {
  if (newValue) {
    loadUsers()
    if (props.editMode && props.routeData) {
      loadRouteData()
    }
  } else {
    resetForm()
  }
})

function loadRouteData() {
  if (!props.routeData) return
  
  const date = new Date(props.routeData.date)
  formData.value.start_date = date.toISOString().slice(0, 10)
  
  formData.value.driver_id = props.routeData.assignees?.[0]?.user_id || null
  
  if (props.routeData.locations && props.routeData.locations.length > 0) {
    routePoints.value = props.routeData.locations
      .sort((a, b) => a.order - b.order)
      .map(loc => ({
        description: loc.description || '',
        address: loc.address || '',
        fullName: loc.contact_name || '',
        phone: loc.contact_phone || ''
      }))
  }
}

onMounted(() => {
  if (props.show) {
    loadUsers()
  }
})

async function loadUsers() {
  try {
    const response = await api.get('/users')
    users.value = response.data
  } catch (error) {
    console.error('Load users error:', error)
  }
}

async function handleSubmit() {
  loading.value = true
  
  try {
    const locations = routePoints.value
      .filter(p => p.address.trim())
      .map((point, index) => ({
        name: point.address,
        address: point.address,
        description: point.description || null,
        contact_name: point.fullName || null,
        contact_phone: point.phone || null,
        order: index + 1
      }))
    
    if (locations.length === 0) {
      alert('Добавьте хотя бы одну точку маршрута')
      return
    }
    
    const routeTitle = locations[0].address || 'Маршрут'
    
    if (props.editMode && props.routeData) {
      const updateData = {
        title: routeTitle,
        description: `Маршрут из ${locations.length} точек`,
        date: formData.value.start_date,
        assignee_ids: formData.value.driver_id ? [formData.value.driver_id] : [],
        locations: locations
      }
      
      await api.put(`/routes/${props.routeData.id}`, updateData)
      emit('updated')
      closeModal()
    } else {
      const routeData = {
        title: routeTitle,
        description: `Маршрут из ${locations.length} точек`,
        date: formData.value.start_date,
        assignee_ids: formData.value.driver_id ? [formData.value.driver_id] : [],
        locations: locations
      }
      
      await api.post('/routes', routeData)
      emit('created')
      closeModal()
    }
  } catch (error) {
    console.error(props.editMode ? 'Update route error:' : 'Create route error:', error)
    alert(`Ошибка ${props.editMode ? 'обновления' : 'создания'} маршрута: ` + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

function addPoint() {
  routePoints.value.push({
    description: '',
    address: '',
    fullName: '',
    phone: ''
  })
}

function removePoint(index) {
  if (routePoints.value.length > 1) {
    routePoints.value.splice(index, 1)
  }
}

function closeModal() {
  emit('close')
}

function resetForm() {
  formData.value = {
    start_date: '',
    driver_id: null
  }
  
  routePoints.value = [
    { description: '', address: '', fullName: '', phone: '' }
  ]
}
</script>
