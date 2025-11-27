# Новые фичи чата: Голосовые сообщения, Поиск, Закрепленные сообщения

## ✅ Бэкенд (Готово)

### Изменения в БД:
- Добавлено поле `is_pinned` в таблицу `messages`
- Миграция применена

### API Endpoints:
1. **POST** `/api/messages/{message_id}/pin` - Закрепить сообщение
2. **DELETE** `/api/messages/{message_id}/pin` - Открепить сообщение  
3. **GET** `/api/messages/chat/{chat_id}/pinned` - Получить закрепленные сообщения
4. **GET** `/api/messages/search?query=...&chat_id=...` - Поиск по сообщениям (уже был)
5. **POST** `/api/messages/upload` - Загрузка файлов (включая аудио)

## 🔨 Фронтенд (В процессе)

### Установленные пакеты:
- `vue-audio-recorder` - для записи голосовых сообщений
- `emoji-picker-element` - новый emoji picker

### Что нужно реализовать в ChatDetailView.vue:

#### 1. Голосовые сообщения

```vue
<template>
  <!-- Кнопка записи голосового сообщения -->
  <button
    v-if="!isRecording"
    @click="startRecording"
    class="p-2 text-gray-600 hover:text-red-600 rounded-lg"
    title="Записать голосовое сообщение"
  >
    <MicrophoneIcon class="w-6 h-6" />
  </button>
  
  <!-- Индикатор записи -->
  <div v-else class="flex items-center space-x-2 px-4 py-2 bg-red-50 rounded-lg">
    <div class="w-3 h-3 bg-red-600 rounded-full animate-pulse"></div>
    <span class="text-sm text-red-600">{{ recordingTime }}</span>
    <button @click="stopRecording" class="p-1 hover:bg-red-100 rounded">
      <StopIcon class="w-5 h-5 text-red-600" />
    </button>
    <button @click="cancelRecording" class="p-1 hover:bg-red-100 rounded">
      <XMarkIcon class="w-5 h-5 text-red-600" />
    </button>
  </div>
  
  <!-- Отображение голосового сообщения -->
  <div v-if="message.message_type === 'AUDIO'" class="flex items-center space-x-2">
    <button @click="toggleAudioPlay(message)" class="p-2 bg-primary-100 rounded-full">
      <PlayIcon v-if="!isPlaying(message.id)" class="w-5 h-5 text-primary-600" />
      <PauseIcon v-else class="w-5 h-5 text-primary-600" />
    </button>
    <div class="flex-1 h-1 bg-gray-200 rounded-full">
      <div class="h-full bg-primary-600 rounded-full" :style="{width: getAudioProgress(message.id) + '%'}"></div>
    </div>
    <span class="text-xs text-gray-500">{{ formatAudioDuration(message) }}</span>
  </div>
</template>

<script setup>
let mediaRecorder = null
let audioChunks = []
const isRecording = ref(false)
const recordingTime = ref('0:00')
let recordingInterval = null
let recordingStartTime = 0

async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder = new MediaRecorder(stream)
    audioChunks = []
    
    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data)
    }
    
    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/webm' })
      await sendAudioMessage(audioBlob)
      stream.getTracks().forEach(track => track.stop())
    }
    
    mediaRecorder.start()
    isRecording.value = true
    recordingStartTime = Date.now()
    
    recordingInterval = setInterval(() => {
      const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000)
      const minutes = Math.floor(elapsed / 60)
      const seconds = elapsed % 60
      recordingTime.value = `${minutes}:${seconds.toString().padStart(2, '0')}`
    }, 1000)
  } catch (error) {
    console.error('Error starting recording:', error)
    alert('Не удалось получить доступ к микрофону')
  }
}

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop()
    isRecording.value = false
    clearInterval(recordingInterval)
    recordingTime.value = '0:00'
  }
}

function cancelRecording() {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop()
    audioChunks = []
    isRecording.value = false
    clearInterval(recordingInterval)
    recordingTime.value = '0:00'
  }
}

async function sendAudioMessage(audioBlob) {
  try {
    const formData = new FormData()
    formData.append('file', audioBlob, `voice_${Date.now()}.webm`)
    formData.append('chat_id', route.params.id)
    
    const response = await api.post('/messages/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    // Отправляем сообщение с аудио
    await api.post('/messages/', {
      chat_id: parseInt(route.params.id),
      content: '',
      message_type: 'AUDIO',
      attachment: {
        file_name: response.data.file_name,
        file_path: response.data.file_path,
        file_type: 'audio/webm',
        file_size: audioBlob.size
      }
    })
    
    await loadMessages()
  } catch (error) {
    console.error('Error sending audio:', error)
  }
}
</script>
```

#### 2. Поиск по сообщениям

```vue
<template>
  <!-- Кнопка поиска в header -->
  <button @click="showSearch = !showSearch" class="p-2 hover:bg-gray-100 rounded-lg">
    <MagnifyingGlassIcon class="w-5 h-5" />
  </button>
  
  <!-- Панель поиска -->
  <div v-if="showSearch" class="absolute top-16 left-0 right-0 bg-white border-b p-4 z-10">
    <div class="flex items-center space-x-2">
      <input
        v-model="searchQuery"
        @input="handleSearch"
        type="text"
        placeholder="Поиск в сообщениях..."
        class="flex-1 px-4 py-2 border rounded-lg"
      />
      <button @click="showSearch = false" class="p-2 hover:bg-gray-100 rounded-lg">
        <XMarkIcon class="w-5 h-5" />
      </button>
    </div>
    
    <!-- Результаты поиска -->
    <div v-if="searchResults.length > 0" class="mt-4 max-h-60 overflow-y-auto">
      <div
        v-for="result in searchResults"
        :key="result.id"
        @click="scrollToMessage(result.id)"
        class="p-3 hover:bg-gray-50 rounded-lg cursor-pointer"
      >
        <p class="text-sm">{{ result.content }}</p>
        <span class="text-xs text-gray-500">{{ formatTime(result.created_at) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
const showSearch = ref(false)
const searchQuery = ref('')
const searchResults = ref([])
let searchTimeout = null

async function handleSearch() {
  if (searchTimeout) clearTimeout(searchTimeout)
  
  if (!searchQuery.value) {
    searchResults.value = []
    return
  }
  
  searchTimeout = setTimeout(async () => {
    try {
      const response = await api.get('/messages/search', {
        params: {
          query: searchQuery.value,
          chat_id: route.params.id
        }
      })
      searchResults.value = response.data
    } catch (error) {
      console.error('Search error:', error)
    }
  }, 300)
}

function scrollToMessage(messageId) {
  const element = document.getElementById(`message-${messageId}`)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'center' })
    element.classList.add('bg-yellow-100')
    setTimeout(() => element.classList.remove('bg-yellow-100'), 2000)
  }
  showSearch.value = false
}
</script>
```

#### 3. Закрепленные сообщения

```vue
<template>
  <!-- Панель закрепленных сообщений -->
  <div v-if="pinnedMessages.length > 0" class="bg-primary-50 border-b p-3">
    <div class="flex items-center justify-between">
      <div class="flex items-center space-x-2">
        <PushPinIcon class="w-5 h-5 text-primary-600" />
        <div class="flex-1">
          <p class="text-sm font-medium text-primary-900">Закрепленное сообщение</p>
          <p class="text-sm text-primary-700 truncate">{{ pinnedMessages[0].content }}</p>
        </div>
      </div>
      <button @click="scrollToMessage(pinnedMessages[0].id)" class="p-1 hover:bg-primary-100 rounded">
        <ChevronDownIcon class="w-5 h-5 text-primary-600" />
      </button>
    </div>
  </div>
  
  <!-- Меню сообщения - добавить опцию закрепления -->
  <MenuItem v-slot="{ active }">
    <button
      @click="togglePinMessage(message)"
      :class="[
        active ? 'bg-gray-100' : '',
        'group flex items-center w-full px-3 py-2 text-sm'
      ]"
    >
      <PushPinIcon class="w-5 h-5 mr-2" />
      {{ message.is_pinned ? 'Открепить' : 'Закрепить' }}
    </button>
  </MenuItem>
  
  <!-- Индикатор закрепленного сообщения -->
  <div v-if="message.is_pinned" class="absolute top-0 right-0 p-1">
    <PushPinIcon class="w-4 h-4 text-primary-600" />
  </div>
</template>

<script setup>
const pinnedMessages = ref([])

async function loadPinnedMessages() {
  try {
    const response = await api.get(`/messages/chat/${route.params.id}/pinned`)
    pinnedMessages.value = response.data
  } catch (error) {
    console.error('Load pinned messages error:', error)
  }
}

async function togglePinMessage(message) {
  try {
    if (message.is_pinned) {
      await api.delete(`/messages/${message.id}/pin`)
      message.is_pinned = false
    } else {
      await api.post(`/messages/${message.id}/pin`)
      message.is_pinned = true
    }
    await loadPinnedMessages()
  } catch (error) {
    console.error('Toggle pin error:', error)
  }
}

onMounted(async () => {
  await loadPinnedMessages()
})
</script>
```

### Необходимые иконки из Heroicons:
- MicrophoneIcon
- StopIcon  
- PlayIcon
- PauseIcon
- MagnifyingGlassIcon
- PushPinIcon
- ChevronDownIcon

## 🚀 Следующие шаги:

1. Перезапустить бэкенд: `docker-compose restart backend`
2. Интегрировать код выше в ChatDetailView.vue
3. Добавить стили для новых компонентов
4. Протестировать все фичи
