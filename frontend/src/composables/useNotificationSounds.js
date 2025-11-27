import { ref, computed } from 'vue'

// Автоматическое определение доступных звуков из папки
const availableSounds = ref([
  { id: 'telegram', name: 'Telegram', path: '/sounds/telegram.mp3' },
  { id: 'telegram-iphone', name: 'Telegram iPhone', path: '/sounds/telegram-iphone.mp3' },
  { id: 'icq', name: 'ICQ', path: '/sounds/icq.mp3' },
  { id: 'icq2', name: 'ICQ 2', path: '/sounds/icq2.mp3' }
])

// Для обратной совместимости
const SOUNDS = computed(() => {
  const soundsMap = { custom: null }
  availableSounds.value.forEach(sound => {
    soundsMap[sound.id] = sound.path
  })
  return soundsMap
})

// Настройки звуков из localStorage
const soundSettings = ref({
  enabled: true,
  selectedSound: 'telegram', // По умолчанию telegram.mp3
  volume: 0.7,
  mutedChats: [] // ID чатов с отключенным звуком
})

// Загрузка настроек
function loadSettings() {
  const saved = localStorage.getItem('soundSettings')
  if (saved) {
    soundSettings.value = { ...soundSettings.value, ...JSON.parse(saved) }
  } else {
    // Если настроек нет, сохраняем дефолтные
    saveSettings()
  }
}

// Сохранение настроек
function saveSettings() {
  localStorage.setItem('soundSettings', JSON.stringify(soundSettings.value))
}

// Генерация звука через Web Audio API (временное решение)
function generateBeep(type = 'telegram') {
  try {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)()
    const oscillator = audioContext.createOscillator()
    const gainNode = audioContext.createGain()
    
    oscillator.connect(gainNode)
    gainNode.connect(audioContext.destination)
    
    // Разные звуки для разных типов
    switch(type) {
      case 'telegram':
        oscillator.frequency.value = 800
        oscillator.type = 'sine'
        gainNode.gain.setValueAtTime(soundSettings.value.volume * 0.3, audioContext.currentTime)
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3)
        oscillator.start(audioContext.currentTime)
        oscillator.stop(audioContext.currentTime + 0.3)
        break
      case 'icq':
        oscillator.frequency.value = 600
        oscillator.type = 'square'
        gainNode.gain.setValueAtTime(soundSettings.value.volume * 0.2, audioContext.currentTime)
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2)
        oscillator.start(audioContext.currentTime)
        oscillator.stop(audioContext.currentTime + 0.2)
        break
      case 'whatsapp':
        oscillator.frequency.value = 1000
        oscillator.type = 'sine'
        gainNode.gain.setValueAtTime(soundSettings.value.volume * 0.25, audioContext.currentTime)
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.25)
        oscillator.start(audioContext.currentTime)
        oscillator.stop(audioContext.currentTime + 0.25)
        break
      default:
        oscillator.frequency.value = 700
        oscillator.type = 'sine'
        gainNode.gain.setValueAtTime(soundSettings.value.volume * 0.3, audioContext.currentTime)
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.4)
        oscillator.start(audioContext.currentTime)
        oscillator.stop(audioContext.currentTime + 0.4)
    }
  } catch (err) {
    console.log('Audio generation error:', err)
  }
}

// Воспроизведение звука
function playSound(chatId = null) {
  // Проверка глобального отключения
  if (!soundSettings.value.enabled) return
  
  // Проверка отключения для конкретного чата
  if (chatId && soundSettings.value.mutedChats.includes(chatId)) return
  
  // Если выбран пользовательский звук
  if (soundSettings.value.selectedSound === 'custom') {
    const customSound = localStorage.getItem('customSound')
    if (customSound) {
      const audio = new Audio(customSound)
      audio.volume = soundSettings.value.volume
      audio.play().catch(err => {
        console.log('Custom sound play error:', err)
        generateBeep('default')
      })
      return
    }
  }
  
  // Пробуем загрузить файл, если не получается - генерируем звук
  const soundUrl = SOUNDS.value[soundSettings.value.selectedSound]
  if (soundUrl) {
    const audio = new Audio(soundUrl)
    audio.volume = soundSettings.value.volume
    audio.play().catch(err => {
      console.log('Sound file not found, using generated sound')
      generateBeep(soundSettings.value.selectedSound)
    })
  } else {
    generateBeep(soundSettings.value.selectedSound)
  }
}

// Функция для добавления нового звука (если пользователь добавит файл в папку)
function addSound(id, name, path) {
  if (!availableSounds.value.find(s => s.id === id)) {
    availableSounds.value.push({ id, name, path })
    saveAvailableSounds()
  }
}

// Сохранение списка звуков в localStorage
function saveAvailableSounds() {
  localStorage.setItem('availableSounds', JSON.stringify(availableSounds.value))
}

// Загрузка списка звуков из localStorage
function loadAvailableSounds() {
  const saved = localStorage.getItem('availableSounds')
  if (saved) {
    try {
      const parsed = JSON.parse(saved)
      if (Array.isArray(parsed) && parsed.length > 0) {
        availableSounds.value = parsed
      }
    } catch (e) {
      console.log('Error loading available sounds:', e)
    }
  }
}

// Сканирование папки sounds для обнаружения новых файлов
async function scanSoundsFolder() {
  try {
    // Пробуем загрузить известные звуки
    const knownSounds = [
      'telegram.mp3',
      'telegram-iphone.mp3',
      'icq.mp3',
      'icq2.mp3',
      'whatsapp.mp3',
      'default.mp3'
    ]
    
    const foundSounds = []
    
    for (const filename of knownSounds) {
      try {
        const response = await fetch(`/sounds/${filename}`, { method: 'HEAD' })
        if (response.ok) {
          const id = filename.replace('.mp3', '')
          const name = id.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')
          foundSounds.push({ id, name, path: `/sounds/${filename}` })
        }
      } catch (e) {
        // Файл не найден, пропускаем
      }
    }
    
    if (foundSounds.length > 0) {
      availableSounds.value = foundSounds
      saveAvailableSounds()
    }
  } catch (error) {
    console.log('Error scanning sounds folder:', error)
  }
}

// Инициализация
loadAvailableSounds()
scanSoundsFolder() // Сканируем при загрузке

// Инициализация
loadSettings()

export function useNotificationSounds() {
  return {
    soundSettings,
    SOUNDS,
    availableSounds,
    playSound,
    saveSettings,
    loadSettings,
    addSound,
    scanSoundsFolder
  }
}
