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
        <div class="flex min-h-full items-center justify-center p-0 sm:p-4">
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel class="w-full h-full sm:h-auto sm:max-w-md transform overflow-hidden sm:rounded-2xl bg-white dark:bg-gray-800 shadow-xl transition-all flex flex-col">
              <!-- Заголовок -->
              <div class="flex items-center justify-between p-4 sm:p-6 border-b border-gray-200 dark:border-gray-700">
                <DialogTitle as="h3" class="text-lg font-semibold text-gray-900 dark:text-gray-100">
                  Создать чат
                </DialogTitle>
                <button
                  @click="$emit('close')"
                  class="sm:hidden p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
                >
                  <XMarkIcon class="w-6 h-6 text-gray-600 dark:text-gray-400" />
                </button>
              </div>
              
              <!-- Содержимое с прокруткой -->
              <div class="flex-1 overflow-y-auto p-4 sm:p-6">
              <form @submit.prevent="handleSubmit" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Тип чата
                  </label>
                  <select v-model="formData.type" required class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600">
                    <option value="">Выберите тип</option>
                    <option value="private">Личный чат</option>
                    <option value="group">Групповой чат</option>
                  </select>
                </div>
                
                <div v-if="formData.type === 'group'">
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Название чата
                  </label>
                  <input
                    v-model="formData.name"
                    type="text"
                    required
                    class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600"
                    placeholder="Введите название чата"
                  />
                </div>
                
                <div v-if="formData.type === 'group'">
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Участники ({{ formData.members.length }} выбрано)
                  </label>
                  
                  <!-- Поиск участников -->
                  <div class="relative mb-3">
                    <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <input
                      v-model="searchQuery"
                      type="text"
                      placeholder="Поиск участников..."
                      class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600 pl-10 w-full"
                    />
                  </div>
                  
                  <div class="border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 max-h-60 overflow-y-auto">
                    <div v-if="filteredUsers.length === 0" class="p-4 text-center text-gray-500 dark:text-gray-400 text-sm">
                      Пользователи не найдены
                    </div>
                    <div
                      v-for="user in filteredUsers"
                      :key="user.id"
                      class="flex items-center p-3 hover:bg-gray-50 dark:hover:bg-gray-600 cursor-pointer"
                      @click="toggleMember(user.id)"
                    >
                      <input
                        type="checkbox"
                        :checked="formData.members.includes(user.id)"
                        class="w-4 h-4 text-primary-600 border-gray-300 dark:border-gray-600 rounded focus:ring-primary-500"
                        @click.stop="toggleMember(user.id)"
                      />
                      <div class="ml-3 flex-1">
                        <p class="text-sm font-medium text-gray-900 dark:text-gray-100">
                          {{ user.first_name }} {{ user.last_name }}
                        </p>
                        <p class="text-xs text-gray-500 dark:text-gray-400">@{{ user.username }}</p>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div v-if="formData.type === 'private'">
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Пользователь
                  </label>
                  
                  <!-- Поиск пользователя -->
                  <div class="relative mb-3">
                    <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <input
                      v-model="searchQuery"
                      type="text"
                      placeholder="Поиск пользователя..."
                      class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600 pl-10 w-full"
                    />
                  </div>
                  
                  <div class="border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 max-h-60 overflow-y-auto">
                    <div v-if="filteredUsers.length === 0" class="p-4 text-center text-gray-500 dark:text-gray-400 text-sm">
                      Пользователи не найдены
                    </div>
                    <button
                      v-for="user in filteredUsers"
                      :key="user.id"
                      type="button"
                      @click="formData.user = user.id"
                      :class="[
                        'w-full flex items-center p-3 hover:bg-gray-50 dark:hover:bg-gray-600 text-left transition-colors',
                        formData.user === user.id ? 'bg-primary-50 dark:bg-primary-900' : ''
                      ]"
                    >
                      <div v-if="user.avatar_url" class="w-10 h-10 rounded-full overflow-hidden">
                        <img :src="`http://localhost:8000${user.avatar_url}`" alt="Avatar" class="w-full h-full object-cover" />
                      </div>
                      <div v-else class="w-10 h-10 rounded-full bg-primary-600 flex items-center justify-center text-white font-semibold">
                        {{ user.first_name?.[0] }}{{ user.last_name?.[0] }}
                      </div>
                      
                      <div class="ml-3 flex-1">
                        <p class="text-sm font-medium text-gray-900 dark:text-gray-100">
                          {{ user.first_name }} {{ user.last_name }}
                        </p>
                        <p class="text-xs text-gray-500 dark:text-gray-400">@{{ user.username }}</p>
                      </div>
                      
                      <CheckIcon v-if="formData.user === user.id" class="w-5 h-5 text-primary-600 dark:text-primary-400" />
                    </button>
                  </div>
                </div>
                
              </form>
              </div>
              
              <!-- Футер с кнопками -->
              <div class="p-4 sm:p-6 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
                <div class="flex space-x-3">
                  <button
                    type="button"
                    @click="handleSubmit"
                    :disabled="loading || !isFormValid"
                    class="flex-1 btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {{ loading ? 'Создание...' : 'Создать' }}
                  </button>
                  <button type="button" @click="$emit('close')" class="flex-1 btn-secondary">
                    Отмена
                  </button>
                </div>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import api from '@/services/api'
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle
} from '@headlessui/vue'
import { CheckIcon, MagnifyingGlassIcon, XMarkIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'created'])

const loading = ref(false)
const users = ref([])
const searchQuery = ref('')

const formData = ref({
  name: '',
  type: '',
  members: [],
  user: null
})

// Фильтрация пользователей по поиску
const filteredUsers = computed(() => {
  if (!searchQuery.value) return users.value
  
  const query = searchQuery.value.toLowerCase()
  return users.value.filter(user => {
    const fullName = `${user.first_name} ${user.last_name}`.toLowerCase()
    const username = user.username.toLowerCase()
    return fullName.includes(query) || username.includes(query)
  })
})

// Валидация формы
const isFormValid = computed(() => {
  if (!formData.value.type) return false
  
  if (formData.value.type === 'group') {
    return formData.value.name && formData.value.members.length > 0
  }
  
  if (formData.value.type === 'private') {
    return formData.value.user !== null
  }
  
  return false
})

watch(() => props.show, (newValue) => {
  if (newValue) {
    loadUsers()
    searchQuery.value = ''
  } else {
    resetForm()
  }
})

// Очистка поиска при смене типа чата
watch(() => formData.value.type, () => {
  searchQuery.value = ''
})

onMounted(() => {
  if (props.show) {
    loadUsers()
  }
})

async function loadUsers() {
  try {
    const response = await api.get('/users/')
    users.value = response.data
  } catch (error) {
    console.error('Load users error:', error)
  }
}

function toggleMember(userId) {
  const index = formData.value.members.indexOf(userId)
  if (index > -1) {
    formData.value.members.splice(index, 1)
  } else {
    formData.value.members.push(userId)
  }
}

async function handleSubmit() {
  loading.value = true
  
  try {
    let chatName = formData.value.name
    
    // Для личного чата автоматически берем имя пользователя
    if (formData.value.type === 'private' && formData.value.user) {
      const user = users.value.find(u => u.id === formData.value.user)
      if (user) {
        chatName = `${user.first_name} ${user.last_name}`
      }
    }
    
    const chatData = {
      name: chatName,
      chat_type: formData.value.type,
      member_ids: formData.value.type === 'group' 
        ? formData.value.members 
        : [formData.value.user]
    }
    
    await api.post('/chats', chatData)
    emit('created')
    emit('close')
  } catch (error) {
    console.error('Create chat error:', error)
    alert('Ошибка создания чата: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

function resetForm() {
  formData.value = {
    name: '',
    type: '',
    members: [],
    user: null
  }
  searchQuery.value = ''
}
</script>
