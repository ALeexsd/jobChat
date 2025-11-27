# 🔔 Система звуковых уведомлений

## Функционал

1. **Глобальное включение/выключение звуков**
2. **Выбор звука уведомления** (ICQ, Telegram, WhatsApp, Default)
3. **Регулировка громкости**
4. **Отключение звука для отдельных чатов**
5. **Загрузка пользовательских звуков**
6. **Воспроизведение при новых сообщениях**

## Добавление звуковых файлов

### Шаг 1: Скачать звуки

Скачайте звуковые файлы и поместите их в `frontend/public/sounds/`:

- `icq.mp3` - классический звук ICQ "Uh-oh!"
- `telegram.mp3` - звук Telegram
- `whatsapp.mp3` - звук WhatsApp
- `default.mp3` - стандартный звук

### Шаг 2: Где найти звуки

**ICQ звук:**
- Поиск: "ICQ uh oh sound effect download"
- Или использовать: https://www.myinstants.com/en/instant/icq-uh-oh/

**Telegram звук:**
- Извлечь из приложения Telegram
- Или найти: "telegram notification sound download"

**WhatsApp звук:**
- Извлечь из приложения WhatsApp
- Или найти: "whatsapp notification sound download"

### Шаг 3: Конвертация (если нужно)

Если звуки в другом формате, конвертируйте в MP3:
```bash
ffmpeg -i input.wav -codec:a libmp3lame -qscale:a 2 output.mp3
```

## Структура файлов

```
frontend/
├── public/
│   └── sounds/
│       ├── icq.mp3
│       ├── telegram.mp3
│       ├── whatsapp.mp3
│       └── default.mp3
├── src/
│   └── composables/
│       └── useNotificationSounds.js
```

## Использование в коде

### В ChatDetailView.vue

```javascript
import { useNotificationSounds } from '@/composables/useNotificationSounds'

const { playSound, soundSettings } = useNotificationSounds()

// При получении нового сообщения
websocket.on('new_message', (data) => {
  if (data.message.sender_id !== authStore.user?.id) {
    playSound(data.chat_id)
  }
})
```

### В ProfileView.vue

```vue
<template>
  <!-- Секция звуковых уведомлений -->
  <div class="border rounded-lg">
    <button @click="toggleSection('sounds')">
      <SpeakerWaveIcon />
      <span>Звуковые уведомления</span>
    </button>
    
    <div v-show="expandedSections.sounds">
      <!-- Включение/выключение -->
      <label class="flex items-center">
        <input type="checkbox" v-model="soundSettings.enabled" @change="saveSettings" />
        <span>Включить звуки</span>
      </label>
      
      <!-- Выбор звука -->
      <select v-model="soundSettings.selectedSound" @change="saveSettings">
        <option value="icq">ICQ (Uh-oh!)</option>
        <option value="telegram">Telegram</option>
        <option value="whatsapp">WhatsApp</option>
        <option value="default">По умолчанию</option>
      </select>
      
      <!-- Громкость -->
      <input 
        type="range" 
        min="0" 
        max="1" 
        step="0.1"
        v-model.number="soundSettings.volume"
        @change="saveSettings"
      />
      
      <!-- Тест звука -->
      <button @click="playSound()">Проверить звук</button>
      
      <!-- Загрузка своего звука -->
      <input type="file" accept="audio/*" @change="uploadCustomSound" />
    </div>
  </div>
</template>
```

### В ChatDetailView.vue - отключение для чата

```vue
<template>
  <!-- В меню чата -->
  <MenuItem>
    <button @click="toggleChatSound">
      <SpeakerWaveIcon v-if="!isChatMuted" />
      <SpeakerXMarkIcon v-else />
      {{ isChatMuted ? 'Включить звук' : 'Отключить звук' }}
    </button>
  </MenuItem>
</template>

<script setup>
const { soundSettings, saveSettings } = useNotificationSounds()

const isChatMuted = computed(() => {
  return soundSettings.value.mutedChats.includes(parseInt(route.params.id))
})

function toggleChatSound() {
  const chatId = parseInt(route.params.id)
  const index = soundSettings.value.mutedChats.indexOf(chatId)
  
  if (index > -1) {
    soundSettings.value.mutedChats.splice(index, 1)
  } else {
    soundSettings.value.mutedChats.push(chatId)
  }
  
  saveSettings()
}
</script>
```

## Настройки в localStorage

```json
{
  "enabled": true,
  "selectedSound": "telegram",
  "volume": 0.7,
  "mutedChats": [1, 5, 12]
}
```

## Проверка разрешений

Система автоматически проверяет:
1. Разрешение на уведомления (Notification API)
2. Возможность воспроизведения звука (autoplay policy)

## Временные звуки (для тестирования)

Если нет звуковых файлов, можно использовать Web Audio API для генерации звуков:

```javascript
function generateBeep() {
  const audioContext = new (window.AudioContext || window.webkitAudioContext)()
  const oscillator = audioContext.createOscillator()
  const gainNode = audioContext.createGain()
  
  oscillator.connect(gainNode)
  gainNode.connect(audioContext.destination)
  
  oscillator.frequency.value = 800
  oscillator.type = 'sine'
  
  gainNode.gain.setValueAtTime(0.3, audioContext.currentTime)
  gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5)
  
  oscillator.start(audioContext.currentTime)
  oscillator.stop(audioContext.currentTime + 0.5)
}
```

## Следующие шаги

1. ✅ Создан composable `useNotificationSounds.js`
2. ✅ Создана папка `public/sounds/`
3. ⏳ Добавить звуковые файлы
4. ⏳ Интегрировать в ProfileView.vue
5. ⏳ Интегрировать в ChatDetailView.vue
6. ⏳ Добавить кнопку отключения звука в меню чата
