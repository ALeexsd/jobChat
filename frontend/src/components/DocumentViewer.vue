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
        <div class="fixed inset-0 bg-black bg-opacity-90" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-hidden">
        <div class="flex min-h-full items-center justify-center p-4">
          <TransitionChild
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel class="w-full max-w-6xl h-[90vh] transform overflow-hidden rounded-2xl bg-white dark:bg-gray-800 shadow-xl transition-all flex flex-col">
              <!-- Header -->
              <div class="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
                <DialogTitle class="text-lg font-semibold text-gray-900 dark:text-gray-100 truncate flex-1 mr-4">
                  {{ fileName }}
                </DialogTitle>
                
                <div class="flex items-center gap-2">
                  <!-- PDF Controls -->
                  <div v-if="fileType === 'pdf'" class="flex items-center gap-2 mr-4">
                    <button
                      @click="zoomOut"
                      :disabled="scale <= 0.5"
                      class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                      title="Уменьшить"
                    >
                      <MinusIcon class="w-5 h-5 text-gray-700 dark:text-gray-300" />
                    </button>
                    
                    <span class="text-sm text-gray-700 dark:text-gray-300 min-w-[60px] text-center">
                      {{ Math.round(scale * 100) }}%
                    </span>
                    
                    <button
                      @click="zoomIn"
                      :disabled="scale >= 3"
                      class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                      title="Увеличить"
                    >
                      <PlusIcon class="w-5 h-5 text-gray-700 dark:text-gray-300" />
                    </button>
                    
                    <div class="w-px h-6 bg-gray-300 dark:bg-gray-600 mx-2"></div>
                    
                    <button
                      @click="previousPage"
                      :disabled="currentPage <= 1"
                      class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      <ChevronLeftIcon class="w-5 h-5 text-gray-700 dark:text-gray-300" />
                    </button>
                    
                    <input
                      v-model.number="currentPage"
                      type="number"
                      :min="1"
                      :max="totalPages"
                      class="w-12 text-center text-sm bg-transparent border border-gray-300 dark:border-gray-600 rounded px-1 py-1 text-gray-700 dark:text-gray-300"
                    />
                    <span class="text-sm text-gray-700 dark:text-gray-300">
                      / {{ totalPages }}
                    </span>
                    
                    <button
                      @click="nextPage"
                      :disabled="currentPage >= totalPages"
                      class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      <ChevronRightIcon class="w-5 h-5 text-gray-700 dark:text-gray-300" />
                    </button>
                    
                    <div class="w-px h-6 bg-gray-300 dark:bg-gray-600 mx-2"></div>
                    
                    <button
                      @click="rotateLeft"
                      class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                      title="Повернуть влево"
                    >
                      <ArrowPathIcon class="w-5 h-5 text-gray-700 dark:text-gray-300 transform -scale-x-100" />
                    </button>
                    
                    <button
                      @click="rotateRight"
                      class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                      title="Повернуть вправо"
                    >
                      <ArrowPathIcon class="w-5 h-5 text-gray-700 dark:text-gray-300" />
                    </button>
                  </div>
                  
                  <!-- Action Buttons -->
                  <button
                    v-if="fileType === 'pdf'"
                    @click="printDocument"
                    class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                    title="Печать"
                  >
                    <PrinterIcon class="w-5 h-5 text-gray-700 dark:text-gray-300" />
                  </button>
                  
                  <button
                    v-if="canEdit"
                    @click="toggleEditMode"
                    :class="[
                      'p-2 rounded-lg transition-colors',
                      isEditMode
                        ? 'bg-primary-600 text-white hover:bg-primary-700'
                        : 'hover:bg-gray-100 dark:hover:bg-gray-700'
                    ]"
                    title="Редактировать"
                  >
                    <PencilSquareIcon class="w-5 h-5" :class="isEditMode ? 'text-white' : 'text-gray-700 dark:text-gray-300'" />
                  </button>
                  
                  <!-- Download Button -->
                  <a
                    :href="fileUrl"
                    download
                    class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                    title="Скачать"
                  >
                    <ArrowDownTrayIcon class="w-5 h-5 text-gray-700 dark:text-gray-300" />
                  </a>
                  
                  <!-- Close Button -->
                  <button
                    @click="$emit('close')"
                    class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                  >
                    <XMarkIcon class="w-5 h-5 text-gray-700 dark:text-gray-300" />
                  </button>
                </div>
              </div>
              
              <!-- Content -->
              <div class="flex-1 overflow-auto bg-gray-100 dark:bg-gray-900 p-4">
                <!-- Loading -->
                <div v-if="loading" class="flex items-center justify-center h-full">
                  <div class="text-center">
                    <div class="w-16 h-16 border-4 border-primary-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                    <p class="text-gray-600 dark:text-gray-400">Загрузка документа...</p>
                  </div>
                </div>
                
                <!-- Error -->
                <div v-else-if="error" class="flex items-center justify-center h-full">
                  <div class="text-center">
                    <ExclamationCircleIcon class="w-16 h-16 text-red-500 mx-auto mb-4" />
                    <p class="text-red-600 dark:text-red-400 mb-2">Ошибка загрузки документа</p>
                    <p class="text-sm text-gray-600 dark:text-gray-400">{{ error }}</p>
                  </div>
                </div>
                
                <!-- PDF Viewer -->
                <div v-else-if="fileType === 'pdf'" class="flex justify-center">
                  <div 
                    :style="{ 
                      transform: `scale(${scale}) rotate(${rotation}deg)`,
                      transformOrigin: 'center top',
                      transition: 'transform 0.2s ease'
                    }"
                  >
                    <VuePdfEmbed
                      v-if="pdfSource"
                      :source="pdfSource"
                      :page="currentPage"
                      @rendered="handlePdfRendered"
                      @loaded="handlePdfLoaded"
                      @rendering-failed="handlePdfError"
                      class="shadow-lg"
                    />
                  </div>
                </div>
                
                <!-- Word Viewer -->
                <div v-else-if="fileType === 'word'" class="max-w-4xl mx-auto bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
                  <div
                    v-if="!isEditMode"
                    v-html="wordContent"
                    class="prose dark:prose-invert max-w-none"
                  ></div>
                  <div
                    v-else
                    contenteditable="true"
                    @input="onContentEdit"
                    v-html="wordContent"
                    class="prose dark:prose-invert max-w-none outline-none border-2 border-primary-500 rounded p-4"
                  ></div>
                </div>
                
                <!-- Unsupported -->
                <div v-else class="flex items-center justify-center h-full">
                  <div class="text-center">
                    <DocumentIcon class="w-16 h-16 text-gray-400 mx-auto mb-4" />
                    <p class="text-gray-600 dark:text-gray-400 mb-4">Предпросмотр недоступен для этого типа файла</p>
                    <a
                      :href="fileUrl"
                      download
                      class="btn-primary inline-flex items-center"
                    >
                      <ArrowDownTrayIcon class="w-5 h-5 mr-2" />
                      Скачать файл
                    </a>
                  </div>
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
import { ref, watch, computed } from 'vue'
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle
} from '@headlessui/vue'
import {
  XMarkIcon,
  ArrowDownTrayIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  DocumentIcon,
  ExclamationCircleIcon,
  PlusIcon,
  MinusIcon,
  ArrowPathIcon,
  PrinterIcon,
  PencilSquareIcon
} from '@heroicons/vue/24/outline'
import VuePdfEmbed from 'vue-pdf-embed'
import mammoth from 'mammoth'

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  fileUrl: {
    type: String,
    required: true
  },
  fileName: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['close'])

const loading = ref(false)
const error = ref(null)
const currentPage = ref(1)
const totalPages = ref(0)
const wordContent = ref('')
const scale = ref(1)
const rotation = ref(0)
const isEditMode = ref(false)
const editedContent = ref('')
const pdfSource = ref(null)

const canEdit = computed(() => {
  return fileType.value === 'word'
})

const fileType = computed(() => {
  const fileName = props.fileName.toLowerCase()
  if (fileName.endsWith('.pdf')) return 'pdf'
  if (fileName.endsWith('.doc') || fileName.endsWith('.docx')) return 'word'
  return 'unknown'
})

watch(() => props.show, async (newVal) => {
  if (newVal) {
    await loadDocument()
    // Добавляем обработчик клавиатуры
    window.addEventListener('keydown', handleKeyPress)
  } else {
    // Reset state
    currentPage.value = 1
    totalPages.value = 0
    wordContent.value = ''
    error.value = null
    scale.value = 1
    rotation.value = 0
    pdfSource.value = null
    // Удаляем обработчик клавиатуры
    window.removeEventListener('keydown', handleKeyPress)
  }
})

watch(() => props.fileUrl, async (newUrl) => {
  if (newUrl && props.show) {
    await loadDocument()
  }
})

async function loadDocument() {
  loading.value = true
  error.value = null
  
  try {
    if (fileType.value === 'word') {
      await loadWordDocument()
    } else if (fileType.value === 'pdf') {
      await loadPdfDocument()
    }
  } catch (err) {
    console.error('Error loading document:', err)
    error.value = err.message || 'Не удалось загрузить документ'
  } finally {
    loading.value = false
  }
}

async function loadPdfDocument() {
  try {
    // Проверяем доступность файла
    const response = await fetch(props.fileUrl, { method: 'HEAD' })
    if (!response.ok) {
      throw new Error('Файл не найден или недоступен')
    }
    
    // Загружаем PDF
    pdfSource.value = props.fileUrl
  } catch (err) {
    console.error('Error loading PDF:', err)
    throw new Error('Не удалось загрузить PDF документ')
  }
}

async function loadWordDocument() {
  try {
    const response = await fetch(props.fileUrl)
    const arrayBuffer = await response.arrayBuffer()
    
    const result = await mammoth.convertToHtml({ arrayBuffer })
    wordContent.value = result.value
    
    if (result.messages.length > 0) {
      console.warn('Word conversion warnings:', result.messages)
    }
  } catch (err) {
    throw new Error('Не удалось загрузить Word документ')
  }
}

function handlePdfLoaded(pdf) {
  try {
    console.log('PDF loaded:', pdf)
    if (pdf && pdf.numPages) {
      totalPages.value = pdf.numPages
      loading.value = false
      error.value = null
    }
  } catch (err) {
    console.error('Error in handlePdfLoaded:', err)
  }
}

function handlePdfRendered(data) {
  try {
    console.log('PDF rendered:', data)
    // Если количество страниц еще не установлено
    if (totalPages.value === 0 && data) {
      if (typeof data === 'number') {
        // Иногда передается просто номер страницы
        return
      } else if (data && typeof data === 'object') {
        if (data.numPages) {
          totalPages.value = data.numPages
        } else if (data.pdfDocument && data.pdfDocument.numPages) {
          totalPages.value = data.pdfDocument.numPages
        } else if (data._pdfInfo && data._pdfInfo.numPages) {
          totalPages.value = data._pdfInfo.numPages
        }
      }
    }
    loading.value = false
    error.value = null
  } catch (err) {
    console.error('Error in handlePdfRendered:', err)
    handlePdfError(err)
  }
}

function handlePdfError(err) {
  console.error('PDF rendering error:', err)
  error.value = 'Не удалось отобразить PDF документ. Попробуйте скачать файл.'
  loading.value = false
}

function previousPage() {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

function zoomIn() {
  if (scale.value < 3) {
    scale.value = Math.min(3, scale.value + 0.25)
  }
}

function zoomOut() {
  if (scale.value > 0.5) {
    scale.value = Math.max(0.5, scale.value - 0.25)
  }
}

function rotateLeft() {
  rotation.value = (rotation.value - 90) % 360
}

function rotateRight() {
  rotation.value = (rotation.value + 90) % 360
}

function handleKeyPress(event) {
  if (!props.show) return
  
  // Не обрабатываем клавиши в режиме редактирования
  if (isEditMode.value) {
    if (event.key === 'Escape') {
      emit('close')
    }
    return
  }
  
  switch(event.key) {
    case 'Escape':
      emit('close')
      break
    case 'ArrowLeft':
      if (fileType.value === 'pdf') {
        event.preventDefault()
        previousPage()
      }
      break
    case 'ArrowRight':
      if (fileType.value === 'pdf') {
        event.preventDefault()
        nextPage()
      }
      break
    case '+':
    case '=':
      if (fileType.value === 'pdf') {
        event.preventDefault()
        zoomIn()
      }
      break
    case '-':
    case '_':
      if (fileType.value === 'pdf') {
        event.preventDefault()
        zoomOut()
      }
      break
    case 'p':
    case 'P':
      if (event.ctrlKey && fileType.value === 'pdf') {
        event.preventDefault()
        printDocument()
      }
      break
  }
}

function toggleEditMode() {
  isEditMode.value = !isEditMode.value
  if (isEditMode.value) {
    editedContent.value = wordContent.value
  }
}

function onContentEdit(event) {
  editedContent.value = event.target.innerHTML
}

async function printDocument() {
  if (fileType.value === 'pdf') {
    // Открываем PDF в новом окне для печати
    const printWindow = window.open(props.fileUrl, '_blank')
    if (printWindow) {
      printWindow.onload = () => {
        printWindow.print()
      }
    }
  } else if (fileType.value === 'word') {
    // Печать Word документа
    const printContent = isEditMode.value ? editedContent.value : wordContent.value
    const printWindow = window.open('', '_blank')
    if (printWindow) {
      printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
          <title>Печать - ${props.fileName}</title>
          <style>
            body {
              font-family: Arial, sans-serif;
              padding: 20px;
              max-width: 800px;
              margin: 0 auto;
            }
            @media print {
              body { padding: 0; }
            }
          </style>
        </head>
        <body>
          ${printContent}
        </body>
        </html>
      `)
      printWindow.document.close()
      printWindow.onload = () => {
        printWindow.print()
      }
    }
  }
}
</script>

<style scoped>
/* Стили для Word документов */
:deep(.prose) {
  @apply text-gray-900 dark:text-gray-100;
}

:deep(.prose h1) {
  @apply text-3xl font-bold mb-4 text-gray-900 dark:text-gray-100;
}

:deep(.prose h2) {
  @apply text-2xl font-bold mb-3 text-gray-900 dark:text-gray-100;
}

:deep(.prose h3) {
  @apply text-xl font-bold mb-2 text-gray-900 dark:text-gray-100;
}

:deep(.prose p) {
  @apply mb-4 text-gray-800 dark:text-gray-200;
}

:deep(.prose ul),
:deep(.prose ol) {
  @apply mb-4 ml-6;
}

:deep(.prose li) {
  @apply mb-2;
}

:deep(.prose a) {
  @apply text-primary-600 hover:text-primary-700 underline;
}

:deep(.prose strong) {
  @apply font-bold;
}

:deep(.prose em) {
  @apply italic;
}

:deep(.prose table) {
  @apply w-full border-collapse mb-4;
}

:deep(.prose th),
:deep(.prose td) {
  @apply border border-gray-300 dark:border-gray-600 px-4 py-2;
}

:deep(.prose th) {
  @apply bg-gray-100 dark:bg-gray-700 font-bold;
}
</style>
