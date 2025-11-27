<template>
  <div class="h-full overflow-auto p-6 bg-gray-50 dark:bg-gray-900">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">Управление заметками</h1>

      <div class="grid gap-4">
        <div v-for="note in notes" :key="note.id" class="card dark:bg-gray-800 dark:border-gray-700 p-4">
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <h3 class="font-semibold text-gray-900 dark:text-gray-100 mb-2">{{ note.title }}</h3>
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">{{ note.content }}</p>
              <div class="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
                <span>Автор: {{ note.author_name }}</span>
                <span>{{ formatDate(note.created_at) }}</span>
              </div>
            </div>
            <button @click="deleteNote(note.id)" class="text-red-600 hover:text-red-700 p-2">
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

const notes = ref([])

onMounted(() => {
  loadNotes()
})

async function loadNotes() {
  try {
    const response = await api.get('/notes/')
    notes.value = response.data
  } catch (error) {
    console.error('Load notes error:', error)
  }
}

async function deleteNote(id) {
  if (!confirm('Удалить заметку?')) return
  try {
    await api.delete(`/notes/${id}`)
    await loadNotes()
  } catch (error) {
    console.error('Delete note error:', error)
  }
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('ru-RU')
}
</script>
