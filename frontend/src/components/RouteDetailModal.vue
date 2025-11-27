<template>
  <TransitionRoot :show="show" as="template">
    <Dialog @close="$emit('close')" class="relative z-50">
      <TransitionChild
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
        <div class="flex min-h-full items-center justify-center p-4">
          <TransitionChild
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel class="w-full max-w-2xl max-h-[90vh] bg-white dark:bg-gray-800 rounded-2xl shadow-xl flex flex-col overflow-hidden">
              <!-- Header -->
              <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                <DialogTitle class="text-xl font-bold text-gray-900 dark:text-gray-100">
                  Детали маршрута
                </DialogTitle>
                <button 
                  @click="$emit('close')" 
                  class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
                >
                  <XMarkIcon class="w-6 h-6" />
                </button>
              </div>
              
              <!-- Content -->
              <div v-if="route" class="flex-1 overflow-y-auto">
                <!-- Info Card -->
                <div class="px-6 py-5 bg-gray-50 dark:bg-gray-700/30 border-b border-gray-200 dark:border-gray-700">
                  <div class="flex justify-between items-center">
                    <div>
                      <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Всего точек</p>
                      <p class="text-3xl font-bold text-gray-900 dark:text-gray-100">{{ route.locations?.length || 0 }}</p>
                    </div>
                    <div class="text-right">
                      <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Дата</p>
                      <p class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ formatDateFull(route.date) }}</p>
                    </div>
                  </div>
                </div>
                
                <!-- Assignees -->
                <div v-if="route.assignees && route.assignees.length" class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                  <h4 class="text-xs font-medium text-gray-500 dark:text-gray-400 mb-3">НАЗНАЧЕНО</h4>
                  <div class="space-y-2">
                    <div
                      v-for="assignee in route.assignees"
                      :key="assignee.id"
                      class="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-700/30 rounded-lg"
                    >
                      <div class="w-10 h-10 rounded-full bg-primary-600 flex items-center justify-center text-white font-bold text-sm">
                        {{ getUserInitials(assignee.user) }}
                      </div>
                      <div class="flex-1">
                        <p class="font-medium text-sm text-gray-900 dark:text-gray-100">
                          {{ assignee.user?.first_name || 'Без имени' }} {{ assignee.user?.last_name || '' }}
                        </p>
                        <a 
                          v-if="assignee.user?.phone"
                          :href="`tel:${assignee.user.phone}`"
                          class="text-xs text-gray-500 dark:text-gray-400 hover:text-primary-600"
                        >
                          {{ assignee.user.phone }}
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Locations -->
                <div v-if="route.locations && route.locations.length" class="px-6 py-5">
                  <div class="relative pl-14">
                    <!-- Vertical Line -->
                    <div class="absolute left-[26px] top-0 bottom-0 w-px bg-gray-300 dark:bg-gray-600"></div>
                    
                    <div class="space-y-4">
                      <div
                        v-for="(location, index) in sortedLocations"
                        :key="location.id"
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
                          <!-- Top section -->
                          <div class="flex items-start justify-between gap-4 mb-3">
                            <div class="flex-1">
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
                              <button class="w-10 h-10 rounded-xl bg-gray-200 dark:bg-gray-600 flex items-center justify-center text-gray-500 dark:text-gray-400">
                                <MapPinIcon class="w-5 h-5" />
                              </button>
                              <a 
                                v-if="location.contact_phone"
                                :href="`tel:${location.contact_phone}`"
                                class="w-10 h-10 rounded-xl bg-green-100 dark:bg-green-900/30 flex items-center justify-center hover:bg-green-200"
                              >
                                <span class="text-xl">📞</span>
                              </a>
                            </div>
                          </div>
                          
                          <!-- Description at bottom -->
                          <div v-if="location.description && location.description !== location.name" class="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
                            <p class="text-sm text-gray-400 dark:text-gray-500">
                              {{ location.description }}
                            </p>
                          </div>
                          
                          <!-- Status -->
                          <div v-if="canUpdateLocation" class="mt-3">
                            <select
                              v-model="location.status"
                              @change="updateLocationStatus(location.id, location.status)"
                              class="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300"
                            >
                              <option value="pending">Ожидает</option>
                              <option value="in_transit">В пути</option>
                              <option value="arrived">Прибыл</option>
                              <option value="completed">Завершено</option>
                            </select>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Footer -->
              <div class="flex gap-3 px-6 py-4 border-t border-gray-200 dark:border-gray-700">
                <button
                  @click="$emit('close')"
                  class="flex-1 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 font-medium py-2.5 rounded-lg"
                >
                  Закрыть
                </button>
                <button
                  v-if="canEdit"
                  @click="handleEdit"
                  class="flex-1 bg-primary-600 hover:bg-primary-700 text-white font-medium py-2.5 rounded-lg"
                >
                  Редактировать
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
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle
} from '@headlessui/vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'
import { MapPinIcon } from '@heroicons/vue/24/solid'

const props = defineProps({
  show: Boolean,
  route: Object
})

const emit = defineEmits(['close', 'edit', 'updated'])

const authStore = useAuthStore()

const canEdit = computed(() => {
  return props.route?.created_by_id === authStore.user?.id
})

const canUpdateLocation = computed(() => {
  if (!props.route) return false
  const isCreator = props.route.created_by_id === authStore.user?.id
  const isAssignee = props.route.assignees?.some(a => a.user_id === authStore.user?.id)
  return isCreator || isAssignee
})

const sortedLocations = computed(() => {
  if (!props.route?.locations) return []
  return [...props.route.locations].sort((a, b) => a.order - b.order)
})

async function updateLocationStatus(locationId, status) {
  try {
    await api.patch(`/routes/${props.route.id}/locations/${locationId}/status`, null, {
      params: { status }
    })
    emit('updated')
  } catch (error) {
    console.error('Update location status error:', error)
    alert('Ошибка при обновлении статуса точки')
  }
}

function handleEdit() {
  emit('edit', props.route)
}

function getUserInitials(user) {
  if (!user) return '?'
  const first = user.first_name?.[0] || ''
  const last = user.last_name?.[0] || ''
  return (first + last).toUpperCase() || '?'
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
