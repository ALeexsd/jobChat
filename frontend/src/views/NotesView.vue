<template>
  <div class="h-full flex flex-col p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Заметки</h1>
      <button @click="showCreateModal = true" class="btn-primary flex items-center">
        <PlusIcon class="w-5 h-5 mr-2" />
        Новая заметка
      </button>
    </div>
    
    <!-- Search -->
    <div class="mb-6">
      <div class="relative">
        <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Поиск заметок..."
          class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
        />
      </div>
    </div>
    
    <!-- Notes Grid -->
    <div class="flex-1 overflow-auto">
      <div v-if="filteredNotes.length === 0" class="text-center py-12">
        <DocumentTextIcon class="w-16 h-16 mx-auto text-gray-400 mb-4" />
        <p class="text-gray-500 mb-4">Нет заметок</p>
        <button @click="showCreateModal = true" class="btn-primary">
          Создать первую заметку
        </button>
      </div>
      
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <div
          v-for="note in filteredNotes"
          :key="note.id"
          class="card p-4 hover:shadow-md transition-shadow cursor-pointer relative"
          @click="viewNote(note)"
        >
          <div v-if="note.is_pinned" class="absolute top-2 right-2">
            <StarIcon class="w-5 h-5 text-yellow-500 fill-current" />
          </div>
          
          <h3 class="text-lg font-semibold text-gray-900 mb-2 pr-6">{{ note.title }}</h3>
          <p class="text-sm text-gray-600 mb-3 line-clamp-3">{{ note.content }}</p>
          
          <div class="flex items-center justify-between text-xs text-gray-500 mb-2">
            <span>{{ formatDate(note.created_at) }}</span>
            <span
              v-if="note.priority"
              :class="[
                'px-2 py-1 rounded',
                getPriorityClass(note.priority)
              ]"
            >
              {{ getPriorityLabel(note.priority) }}
            </span>
          </div>
          
          <div v-if="note.tags?.length" class="flex flex-wrap gap-1">
            <span
              v-for="tag in note.tags"
              :key="tag"
              class="px-2 py-1 bg-primary-50 text-primary-700 text-xs rounded"
            >
              {{ tag }}
            </span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Create Note Modal -->
    <CreateNoteModal
      :show="showCreateModal"
      @close="showCreateModal = false"
      @created="handleNoteCreated"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import CreateNoteModal from '@/components/CreateNoteModal.vue'
import {
  PlusIcon,
  MagnifyingGlassIcon,
  DocumentTextIcon,
  StarIcon
} from '@heroicons/vue/24/outline'

const notes = ref([])
const searchQuery = ref('')
const showCreateModal = ref(false)

const filteredNotes = computed(() => {
  if (!searchQuery.value) return notes.value
  
  return notes.value.filter(note =>
    note.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    note.content.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    note.tags?.some(tag => tag.toLowerCase().includes(searchQuery.value.toLowerCase()))
  )
})

onMounted(() => {
  loadNotes()
})

async function loadNotes() {
  try {
    const response = await api.get('/notes')
    notes.value = response.data
  } catch (error) {
    console.error('Load notes error:', error)
  }
}

function handleNoteCreated() {
  loadNotes()
}

function viewNote(note) {
  console.log('View note:', note)
}

function getPriorityClass(priority) {
  const classes = {
    low: 'bg-gray-100 text-gray-700',
    medium: 'bg-yellow-100 text-yellow-700',
    high: 'bg-red-100 text-red-700'
  }
  return classes[priority] || classes.medium
}

function getPriorityLabel(priority) {
  const labels = {
    low: 'Низкий',
    medium: 'Средний',
    high: 'Высокий'
  }
  return labels[priority] || priority
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('ru-RU')
}
</script>
