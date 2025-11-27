<template>
  <div class="h-full overflow-auto p-6 bg-gray-50 dark:bg-gray-900">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">Управление чатами</h1>

      <div class="grid gap-4">
        <div v-for="chat in chats" :key="chat.id" class="card dark:bg-gray-800 dark:border-gray-700 p-4">
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-2">
                <h3 class="font-semibold text-gray-900 dark:text-gray-100">
                  {{ chat.is_group ? chat.name : 'Личный чат' }}
                </h3>
                <span
                  v-if="chat.is_group"
                  class="px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200"
                >
                  Группа
                </span>
              </div>
              <div class="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                <p>Участников: {{ chat.participants?.length || 0 }}</p>
                <p>Создан: {{ formatDate(chat.created_at) }}</p>
                <p v-if="chat.last_message">Последнее сообщение: {{ formatDate(chat.last_message.created_at) }}</p>
              </div>
            </div>
            <button @click="deleteChat(chat.id)" class="text-red-600 hover:text-red-700 p-2">
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

const chats = ref([])

onMounted(() => {
  loadChats()
})

async function loadChats() {
  try {
    const response = await api.get('/chats/')
    chats.value = response.data
  } catch (error) {
    console.error('Load chats error:', error)
  }
}

async function deleteChat(id) {
  if (!confirm('Удалить чат?')) return
  try {
    await api.delete(`/chats/${id}`)
    await loadChats()
  } catch (error) {
    console.error('Delete chat error:', error)
  }
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>
