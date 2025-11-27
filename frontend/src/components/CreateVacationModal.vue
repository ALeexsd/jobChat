<template>
  <TransitionRoot appear :show="show" as="template">
    <Dialog as="div" @close="$emit('close')" class="relative z-50">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black bg-opacity-25" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4">
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel class="w-full max-w-2xl transform overflow-hidden rounded-2xl bg-white dark:bg-gray-800 p-6 shadow-xl transition-all">
              <DialogTitle as="h3" class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
                Подать заявку на отпуск
              </DialogTitle>
              
              <form @submit.prevent="handleSubmit" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Тип отпуска</label>
                  <select v-model="formData.type" required class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600">
                    <option value="vacation">Отпуск</option>
                    <option value="sick_leave">Больничный</option>
                    <option value="personal">Личный день</option>
                  </select>
                </div>
                
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Дата начала</label>
                    <input
                      v-model="formData.start_date"
                      type="date"
                      required
                      class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600"
                    />
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Дата окончания</label>
                    <input
                      v-model="formData.end_date"
                      type="date"
                      required
                      class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600"
                    />
                  </div>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Причина</label>
                  <textarea
                    v-model="formData.reason"
                    rows="3"
                    class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600"
                    placeholder="Укажите причину (необязательно)"
                  ></textarea>
                </div>
                
                <div class="flex space-x-3 mt-6">
                  <button type="submit" :disabled="loading" class="flex-1 btn-primary disabled:opacity-50">
                    {{ loading ? 'Отправка...' : 'Подать заявку' }}
                  </button>
                  <button type="button" @click="$emit('close')" class="flex-1 btn-secondary">
                    Отмена
                  </button>
                </div>
              </form>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { ref, watch } from 'vue'
import api from '@/services/api'
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle
} from '@headlessui/vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'created'])

const loading = ref(false)

const formData = ref({
  type: 'vacation',
  start_date: '',
  end_date: '',
  reason: ''
})

watch(() => props.show, (newValue) => {
  if (!newValue) {
    resetForm()
  }
})

async function handleSubmit() {
  loading.value = true
  
  try {
    const vacationData = {
      vacation_type: formData.value.type,
      start_date: formData.value.start_date,
      end_date: formData.value.end_date,
      comment: formData.value.reason || null
    }
    
    await api.post('/vacations', vacationData)
    emit('created')
    emit('close')
  } catch (error) {
    console.error('Create vacation error:', error)
    alert('Ошибка создания заявки: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

function resetForm() {
  formData.value = {
    type: 'vacation',
    start_date: '',
    end_date: '',
    reason: ''
  }
}
</script>
