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
            <DialogPanel class="w-full max-w-2xl transform overflow-hidden rounded-2xl bg-white dark:bg-gray-800 shadow-xl transition-all">
              <div class="border-b border-gray-200 dark:border-gray-700 px-6 py-4">
                <DialogTitle as="h3" class="text-lg font-semibold text-gray-900 dark:text-gray-100">
                  Настройки группы
                </DialogTitle>
              </div>
              
              <div class="max-h-[70vh] overflow-y-auto">
                <!-- Group Info -->
                <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                  <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100 mb-4">Информация о группе</h4>
                  
                  <div class="space-y-4">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Название группы
                      </label>
                      <input
                        v-model="groupName"
                        type="text"
                        class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600"
                        placeholder="Введите название группы"
                      />
                    </div>
                    
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Описание группы
                      </label>
                      <textarea
                        v-model="groupDescription"
                        rows="3"
                        class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600"
                        placeholder="Описание группы (необязательно)"
                      ></textarea>
                    </div>
                  </div>
                </div>
                
                <!-- Members -->
                <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                  <div class="flex items-center justify-between mb-4">
                    <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100">
                      Участники ({{ members.length }})
                    </h4>
                    <button @click="showAddMember = true" class="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-800 dark:hover:text-primary-300">
                      + Добавить участника
                    </button>
                  </div>
                  
                  <div class="space-y-2 max-h-60 overflow-y-auto">
                    <div
                      v-for="member in members"
                      :key="member.id"
                      class="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700"
                    >
                      <div class="flex items-center">
                        <div v-if="member.avatar_url" class="w-10 h-10 rounded-full overflow-hidden">
                          <img :src="`http://localhost:8000${member.avatar_url}`" alt="Avatar" class="w-full h-full object-cover" />
                        </div>
                        <div v-else class="w-10 h-10 rounded-full bg-primary-600 flex items-center justify-center text-white font-semibold">
                          {{ member.first_name?.[0] }}{{ member.last_name?.[0] }}
                        </div>
                        
                        <div class="ml-3">
                          <p class="text-sm font-medium text-gray-900 dark:text-gray-100">
                            {{ member.first_name }} {{ member.last_name }}
                          </p>
                          <p class="text-xs text-gray-500 dark:text-gray-400">@{{ member.username }}</p>
                        </div>
                      </div>
                      
                      <div class="flex items-center space-x-2">
                        <select
                          v-model="member.role"
                          @change="updateMemberRole(member)"
                          class="text-xs px-2 py-1 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                        >
                          <option value="member">Участник</option>
                          <option value="admin">Администратор</option>
                        </select>
                        
                        <button
                          v-if="member.role !== 'admin' || members.filter(m => m.role === 'admin').length > 1"
                          @click="removeMember(member.id)"
                          class="p-1 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded"
                        >
                          <XMarkIcon class="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Add Member Section -->
                <div v-if="showAddMember" class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700/50">
                  <div class="flex items-center justify-between mb-3">
                    <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100">Добавить участника</h4>
                    <button @click="showAddMember = false" class="text-gray-500 hover:text-gray-700 dark:hover:text-gray-300">
                      <XMarkIcon class="w-5 h-5" />
                    </button>
                  </div>
                  
                  <div class="relative mb-3">
                    <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <input
                      v-model="searchQuery"
                      type="text"
                      placeholder="Поиск пользователей..."
                      class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                    />
                  </div>
                  
                  <div v-if="filteredUsers.length > 0" class="space-y-2 max-h-40 overflow-y-auto">
                    <button
                      v-for="user in filteredUsers"
                      :key="user.id"
                      @click="addMember(user)"
                      class="w-full flex items-center p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 text-left"
                    >
                      <div v-if="user.avatar_url" class="w-8 h-8 rounded-full overflow-hidden">
                        <img :src="`http://localhost:8000${user.avatar_url}`" alt="Avatar" class="w-full h-full object-cover" />
                      </div>
                      <div v-else class="w-8 h-8 rounded-full bg-primary-600 flex items-center justify-center text-white text-sm font-semibold">
                        {{ user.first_name?.[0] }}{{ user.last_name?.[0] }}
                      </div>
                      
                      <div class="ml-3">
                        <p class="text-sm font-medium text-gray-900 dark:text-gray-100">
                          {{ user.first_name }} {{ user.last_name }}
                        </p>
                        <p class="text-xs text-gray-500 dark:text-gray-400">@{{ user.username }}</p>
                      </div>
                    </button>
                  </div>
                </div>
                
                <!-- Danger Zone -->
                <div class="px-6 py-4">
                  <h4 class="text-sm font-medium text-red-600 dark:text-red-400 mb-4">Опасная зона</h4>
                  <button
                    @click="leaveGroup"
                    class="w-full px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                  >
                    Покинуть группу
                  </button>
                </div>
              </div>
              
              <div class="border-t border-gray-200 dark:border-gray-700 px-6 py-4 flex space-x-3">
                <button @click="saveSettings" :disabled="saving" class="flex-1 btn-primary disabled:opacity-50">
                  {{ saving ? 'Сохранение...' : 'Сохранить' }}
                </button>
                <button @click="$emit('close')" class="flex-1 btn-secondary">
                  Отмена
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
import { ref, computed, watch, onMounted } from 'vue'
import api from '@/services/api'
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle
} from '@headlessui/vue'
import { XMarkIcon, MagnifyingGlassIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  chatId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['close', 'updated', 'left'])

const groupName = ref('')
const groupDescription = ref('')
const members = ref([])
const allUsers = ref([])
const searchQuery = ref('')
const showAddMember = ref(false)
const saving = ref(false)

const filteredUsers = computed(() => {
  if (!searchQuery.value) return []
  
  const memberIds = members.value.map(m => m.id)
  return allUsers.value.filter(user => {
    if (memberIds.includes(user.id)) return false
    
    const query = searchQuery.value.toLowerCase()
    return (
      user.first_name.toLowerCase().includes(query) ||
      user.last_name.toLowerCase().includes(query) ||
      user.username.toLowerCase().includes(query)
    )
  })
})

watch(() => props.show, (newValue) => {
  if (newValue) {
    loadChatData()
    loadUsers()
  }
})

async function loadChatData() {
  try {
    const response = await api.get(`/chats/${props.chatId}/`)
    groupName.value = response.data.name
    groupDescription.value = response.data.description || ''
    
    // Загружаем участников
    const membersResponse = await api.get(`/chats/${props.chatId}/members/`)
    members.value = membersResponse.data
  } catch (error) {
    console.error('Load chat data error:', error)
  }
}

async function loadUsers() {
  try {
    const response = await api.get('/users/')
    allUsers.value = response.data
  } catch (error) {
    console.error('Load users error:', error)
  }
}

async function addMember(user) {
  try {
    await api.post(`/chats/${props.chatId}/members/`, {
      user_id: user.id
    })
    
    members.value.push({
      ...user,
      role: 'member'
    })
    
    searchQuery.value = ''
    showAddMember.value = false
  } catch (error) {
    console.error('Add member error:', error)
    alert('Ошибка добавления участника')
  }
}

async function removeMember(userId) {
  if (!confirm('Удалить участника из группы?')) return
  
  try {
    await api.delete(`/chats/${props.chatId}/members/${userId}/`)
    members.value = members.value.filter(m => m.id !== userId)
  } catch (error) {
    console.error('Remove member error:', error)
    alert('Ошибка удаления участника')
  }
}

async function updateMemberRole(member) {
  try {
    await api.patch(`/chats/${props.chatId}/members/${member.id}/`, {
      role: member.role
    })
  } catch (error) {
    console.error('Update member role error:', error)
    alert('Ошибка обновления роли')
  }
}

async function saveSettings() {
  saving.value = true
  
  try {
    await api.patch(`/chats/${props.chatId}/`, {
      name: groupName.value,
      description: groupDescription.value
    })
    
    emit('updated')
    emit('close')
  } catch (error) {
    console.error('Save settings error:', error)
    alert('Ошибка сохранения настроек')
  } finally {
    saving.value = false
  }
}

async function leaveGroup() {
  if (!confirm('Вы уверены, что хотите покинуть группу?')) return
  
  try {
    await api.post(`/chats/${props.chatId}/leave/`)
    emit('left')
    emit('close')
  } catch (error) {
    console.error('Leave group error:', error)
    alert('Ошибка выхода из группы')
  }
}
</script>
