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
                Создать заметку
              </DialogTitle>
              
              <form @submit.prevent="handleSubmit" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Заголовок</label>
                  <input
                    v-model="formData.title"
                    type="text"
                    required
                    class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600"
                    placeholder="Введите заголовок заметки"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Содержание</label>
                  <textarea
                    v-model="formData.content"
                    rows="6"
                    required
                    class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600"
                    placeholder="Содержание заметки"
                  ></textarea>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Категория</label>
                  <select v-model="formData.category" class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600">
                    <option :value="null">Без категории</option>
                    <option value="work">Работа</option>
                    <option value="personal">Личное</option>
                    <option value="ideas">Идеи</option>
                    <option value="meetings">Встречи</option>
                    <option value="projects">Проекты</option>
                  </select>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Теги</label>
                  <input
                    v-model="tagsInput"
                    type="text"
                    class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600"
                    placeholder="Введите теги через запятую"
                    @blur="updateTags"
                  />
                  <div v-if="formData.tags.length" class="mt-2 flex flex-wrap gap-2">
                    <span
                      v-for="(tag, index) in formData.tags"
                      :key="index"
                      class="px-2 py-1 bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 text-sm rounded flex items-center"
                    >
                      {{ tag }}
                      <button
                        type="button"
                        @click="removeTag(index)"
                        class="ml-2 text-primary-600 dark:text-primary-400 hover:text-primary-800 dark:hover:text-primary-200"
                      >
                        ×
                      </button>
                    </span>
                  </div>
                </div>
                
                <div class="flex items-center">
                  <input
                    id="is_pinned"
                    v-model="formData.is_pinned"
                    type="checkbox"
                    class="w-4 h-4 text-primary-600 border-gray-300 dark:border-gray-600 rounded focus:ring-primary-500"
                  />
                  <label for="is_pinned" class="ml-2 text-sm text-gray-700 dark:text-gray-300">
                    Закрепить заметку
                  </label>
                </div>
                
                <div class="flex space-x-3 mt-6">
                  <button type="submit" :disabled="loading" class="flex-1 btn-primary disabled:opacity-50">
                    {{ loading ? 'Создание...' : 'Создать' }}
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
const tagsInput = ref('')

const formData = ref({
  title: '',
  content: '',
  category: null,
  tags: [],
  is_pinned: false
})

watch(() => props.show, (newValue) => {
  if (!newValue) {
    resetForm()
  }
})

async function handleSubmit() {
  loading.value = true
  
  try {
    const noteData = {
      title: formData.value.title,
      content: formData.value.content,
      category: formData.value.category || null,
      tags: formData.value.tags.join(', '),
      is_pinned: formData.value.is_pinned
    }
    
    await api.post('/notes', noteData)
    emit('created')
    emit('close')
  } catch (error) {
    console.error('Create note error:', error)
    alert('Ошибка создания заметки: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

function updateTags() {
  if (tagsInput.value.trim()) {
    const newTags = tagsInput.value.split(',').map(tag => tag.trim()).filter(tag => tag)
    formData.value.tags = [...new Set([...formData.value.tags, ...newTags])]
    tagsInput.value = ''
  }
}

function removeTag(index) {
  formData.value.tags.splice(index, 1)
}

function resetForm() {
  formData.value = {
    title: '',
    content: '',
    category: null,
    tags: [],
    is_pinned: false
  }
  tagsInput.value = ''
}
</script>
