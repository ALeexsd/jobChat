<template>
  <div class="h-screen flex overflow-hidden bg-gray-100 dark:bg-gray-900">
    <!-- Mobile Menu Button -->
    <button
      @click="sidebarCollapsed = !sidebarCollapsed"
      class="lg:hidden fixed top-4 left-4 z-50 p-2 bg-white rounded-lg shadow-lg"
    >
      <component :is="sidebarCollapsed ? Bars3Icon : XMarkIcon" class="w-6 h-6" />
    </button>

    <!-- Mobile Overlay -->
    <div
      v-if="!sidebarCollapsed"
      @click="sidebarCollapsed = true"
      class="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-30"
    ></div>

    <!-- Sidebar -->
    <div 
      :class="[
        'bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col transition-all duration-300',
        'fixed lg:relative inset-y-0 left-0 z-40',
        sidebarCollapsed ? '-translate-x-full lg:translate-x-0 lg:w-16' : 'translate-x-0 w-64'
      ]"
    >
      <!-- Logo -->
      <div class="h-16 flex items-center justify-center border-b border-gray-200 dark:border-gray-700">
        <h1 v-if="!sidebarCollapsed" class="text-xl font-bold text-primary-600 dark:text-primary-400">
          Мессенджер
        </h1>
        <span v-else class="text-2xl">💬</span>
      </div>
      
      <!-- Navigation -->
      <nav class="flex-1 overflow-y-auto py-4">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-primary-50 dark:hover:bg-gray-700 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
          active-class="bg-primary-50 dark:bg-gray-700 text-primary-600 dark:text-primary-400 border-r-4 border-primary-600 dark:border-primary-400"
        >
          <component :is="item.icon" class="w-6 h-6" />
          <span v-if="!sidebarCollapsed" class="ml-3">{{ item.label }}</span>
        </router-link>
      </nav>
      
      <!-- User Profile -->
      <div class="border-t border-gray-200 dark:border-gray-700 p-4">
        <Menu as="div" class="relative">
          <MenuButton class="flex items-center justify-center w-full hover:bg-gray-50 dark:hover:bg-gray-700 rounded-lg p-2 transition-colors">
            <!-- Свернутое меню - иконка профиля -->
            <div v-if="sidebarCollapsed" class="w-10 h-10 flex items-center justify-center mx-auto">
              <UserCircleIcon class="w-10 h-10 text-gray-600 dark:text-gray-400" />
            </div>
            <!-- Развернутое меню - аватар -->
            <template v-else>
              <div v-if="user?.avatar_url" class="w-10 h-10 rounded-full overflow-hidden">
                <img :src="`http://localhost:8000${user.avatar_url}`" alt="Avatar" class="w-full h-full object-cover" />
              </div>
              <div v-else class="w-10 h-10 rounded-full bg-primary-600 flex items-center justify-center text-white font-semibold">
                {{ userInitials }}
              </div>
              <div class="ml-3 text-left flex-1">
                <p class="text-sm font-medium text-gray-900 dark:text-gray-100">{{ user?.first_name }} {{ user?.last_name }}</p>
                <p class="text-xs text-gray-500 dark:text-gray-400">{{ user?.position || 'Сотрудник' }}</p>
              </div>
            </template>
          </MenuButton>
          
          <transition
            enter-active-class="transition duration-100 ease-out"
            enter-from-class="transform scale-95 opacity-0"
            enter-to-class="transform scale-100 opacity-100"
            leave-active-class="transition duration-75 ease-in"
            leave-from-class="transform scale-100 opacity-100"
            leave-to-class="transform scale-95 opacity-0"
          >
            <MenuItems class="absolute bottom-full left-0 mb-2 w-56 origin-bottom-left bg-white dark:bg-gray-800 rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
              <div class="p-1">
                <MenuItem v-slot="{ active }">
                  <router-link
                    to="/profile"
                    :class="[
                      active ? 'bg-primary-50 dark:bg-gray-700 text-primary-600 dark:text-primary-400' : 'text-gray-900 dark:text-gray-100',
                      'group flex items-center w-full px-3 py-2 text-sm rounded-md'
                    ]"
                  >
                    <UserCircleIcon class="w-5 h-5 mr-2" />
                    Профиль
                  </router-link>
                </MenuItem>
                <MenuItem v-slot="{ active }">
                  <button
                    @click="handleLogout"
                    :class="[
                      active ? 'bg-red-50 dark:bg-red-900 text-red-600 dark:text-red-400' : 'text-gray-900 dark:text-gray-100',
                      'group flex items-center w-full px-3 py-2 text-sm rounded-md'
                    ]"
                  >
                    <ArrowRightOnRectangleIcon class="w-5 h-5 mr-2" />
                    Выйти
                  </button>
                </MenuItem>
              </div>
            </MenuItems>
          </transition>
        </Menu>
      </div>
      
      <!-- Toggle Button (Desktop only) -->
      <button
        @click="sidebarCollapsed = !sidebarCollapsed"
        class="hidden lg:flex absolute top-20 -right-3 w-6 h-6 bg-white border border-gray-200 rounded-full items-center justify-center hover:bg-gray-50 transition-colors"
      >
        <ChevronLeftIcon v-if="!sidebarCollapsed" class="w-4 h-4 text-gray-600" />
        <ChevronRightIcon v-else class="w-4 h-4 text-gray-600" />
      </button>
    </div>
    
    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Header -->
      <header class="h-16 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between px-6 lg:px-6 pl-16 lg:pl-6">
        <h2 class="text-xl font-semibold text-gray-900 dark:text-gray-100">{{ currentPageTitle }}</h2>
        
        <div class="flex items-center space-x-4">
          <!-- Theme Toggle (только на десктопе) -->
          <button
            @click="themeStore.toggleTheme()"
            class="hidden lg:flex p-2 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            title="Переключить тему"
          >
            <MoonIcon v-if="!themeStore.isDark" class="w-6 h-6" />
            <SunIcon v-else class="w-6 h-6" />
          </button>
          
          <!-- Notifications -->
          <Menu as="div" class="relative">
            <MenuButton class="relative p-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
              <BellIcon class="w-6 h-6" />
              <span v-if="unreadNotifications > 0 && notifications.length > 0" class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
            </MenuButton>
            
            <transition
              enter-active-class="transition duration-100 ease-out"
              enter-from-class="transform scale-95 opacity-0"
              enter-to-class="transform scale-100 opacity-100"
              leave-active-class="transition duration-75 ease-in"
              leave-from-class="transform scale-100 opacity-100"
              leave-to-class="transform scale-95 opacity-0"
            >
              <MenuItems class="absolute right-0 mt-2 w-80 origin-top-right bg-white dark:bg-gray-800 rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none z-[60]">
                <div class="p-4">
                  <h3 class="text-sm font-semibold text-gray-900 dark:text-gray-100 mb-3">Уведомления</h3>
                  <div v-if="notifications.length === 0" class="text-center py-8 text-gray-500 dark:text-gray-400">
                    Нет уведомлений
                  </div>
                  <div v-else class="space-y-2">
                    <div
                      v-for="notification in notifications"
                      :key="notification.id"
                      class="p-3 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-lg cursor-pointer"
                    >
                      <p class="text-sm text-gray-900 dark:text-gray-100">{{ notification.message }}</p>
                      <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">{{ formatTime(notification.created_at) }}</p>
                    </div>
                  </div>
                </div>
              </MenuItems>
            </transition>
          </Menu>
        </div>
      </header>
      
      <!-- Page Content -->
      <main :class="[
        'flex-1 overflow-auto',
        route.path.startsWith('/chats/') ? 'pb-0' : 'pb-16 lg:pb-0'
      ]">
        <router-view />
      </main>
    </div>
    
    <!-- Mobile Bottom Navigation (скрыт в чатах) -->
    <nav v-if="!route.path.startsWith('/chats/')" class="lg:hidden fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 z-50">
      <div class="flex justify-around items-center h-16">
        <router-link
          to="/chats"
          class="flex flex-col items-center justify-center flex-1 h-full"
          :class="route.path.startsWith('/chats') ? 'text-primary-600 dark:text-primary-400' : 'text-gray-600 dark:text-gray-400'"
        >
          <ChatBubbleLeftRightIcon class="w-6 h-6" />
          <span class="text-xs mt-1">Чаты</span>
        </router-link>
        
        <router-link
          to="/tasks"
          class="flex flex-col items-center justify-center flex-1 h-full"
          :class="route.path === '/tasks' ? 'text-primary-600 dark:text-primary-400' : 'text-gray-600 dark:text-gray-400'"
        >
          <ClipboardDocumentListIcon class="w-6 h-6" />
          <span class="text-xs mt-1">Задачи</span>
        </router-link>
        
        <router-link
          to="/notes"
          class="flex flex-col items-center justify-center flex-1 h-full"
          :class="route.path === '/notes' ? 'text-primary-600 dark:text-primary-400' : 'text-gray-600 dark:text-gray-400'"
        >
          <DocumentTextIcon class="w-6 h-6" />
          <span class="text-xs mt-1">Заметки</span>
        </router-link>
        
        <router-link
          to="/profile"
          class="flex flex-col items-center justify-center flex-1 h-full"
          :class="route.path === '/profile' ? 'text-primary-600 dark:text-primary-400' : 'text-gray-600 dark:text-gray-400'"
        >
          <UserCircleIcon class="w-6 h-6" />
          <span class="text-xs mt-1">Профиль</span>
        </router-link>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import websocket from '@/services/websocket'
import { useNotificationSounds } from '@/composables/useNotificationSounds'
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'
import {
  ChatBubbleLeftRightIcon,
  ClipboardDocumentListIcon,
  DocumentTextIcon,
  CalendarDaysIcon,
  MapIcon,
  UserCircleIcon,
  UserGroupIcon,
  BellIcon,
  ArrowRightOnRectangleIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  Bars3Icon,
  XMarkIcon,
  MoonIcon,
  SunIcon,
  Cog6ToothIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const themeStore = useThemeStore()

// Sidebar collapsed by default on mobile
const sidebarCollapsed = ref(window.innerWidth < 1024)

// Загружаем уведомления и счетчик из localStorage при инициализации
const savedNotifications = localStorage.getItem('notifications')
const notifications = ref(savedNotifications ? JSON.parse(savedNotifications) : [])

const savedCount = localStorage.getItem('unreadNotifications')
const unreadNotifications = ref(savedCount ? parseInt(savedCount) : 0)

// Сохраняем уведомления в localStorage
const saveNotifications = () => {
  localStorage.setItem('notifications', JSON.stringify(notifications.value))
}

// Сохраняем счетчик в localStorage при изменении
const updateUnreadCount = (count) => {
  unreadNotifications.value = count
  localStorage.setItem('unreadNotifications', count.toString())
}

// WebSocket подключение и статус онлайн/офлайн
onMounted(() => {
  // Подключаемся к WebSocket при входе в приложение
  if (authStore.isAuthenticated) {
    websocket.connect()
    
    // Устанавливаем статус онлайн при подключении
    websocket.on('connected', () => {
      websocket.updateStatus('online')
    })
    
    // Глобальные обработчики уведомлений
    const { playSound } = useNotificationSounds()
    
    // Уведомления о новых сообщениях (глобально)
    websocket.on('new_message', (data) => {
      // Воспроизводим звук если сообщение от другого пользователя
      if (data.message.sender_id !== authStore.user?.id) {
        // Проверяем, не находимся ли мы уже в этом чате
        const isInCurrentChat = route.name === 'chat-detail' && route.params.id === String(data.chat_id)
        
        // Показываем уведомления ТОЛЬКО если НЕ в этом чате
        if (!isInCurrentChat) {
          playSound()
          
          // Показываем браузерное уведомление
          if ('Notification' in window && Notification.permission === 'granted') {
            new Notification('Новое сообщение', {
              body: data.message.content?.substring(0, 100) || 'Вложение',
              icon: '/logo.png',
              tag: `message-${data.message.id}`
            })
          }
          
          // Добавляем уведомление в список
          notifications.value.unshift({
            id: `message-${data.message.id}`,
            type: 'message',
            message: data.message.content?.substring(0, 100) || 'Новое сообщение',
            created_at: new Date().toISOString(),
            chat_id: data.chat_id
          })
          
          // Ограничиваем количество уведомлений
          if (notifications.value.length > 50) {
            notifications.value = notifications.value.slice(0, 50)
          }
          
          // Сохраняем уведомления
          saveNotifications()
          
          // Увеличиваем счетчик непрочитанных
          updateUnreadCount(unreadNotifications.value + 1)
        }
      }
    })
    
    // Уведомления о задачах (глобально)
    websocket.on('task_assigned', (data) => {
      playSound()
      
      if ('Notification' in window && Notification.permission === 'granted') {
        new Notification('Новая задача', {
          body: `Вам назначена задача: ${data.task_title}`,
          icon: '/logo.png',
          tag: `task-${data.task_id}`
        })
      }
      
      // Добавляем уведомление в список
      notifications.value.unshift({
        id: `task-${data.task_id}`,
        type: 'task',
        message: `Вам назначена задача: ${data.task_title}`,
        created_at: new Date().toISOString(),
        task_id: data.task_id
      })
      
      // Ограничиваем количество уведомлений
      if (notifications.value.length > 50) {
        notifications.value = notifications.value.slice(0, 50)
      }
      
      // Сохраняем уведомления
      saveNotifications()
      
      updateUnreadCount(unreadNotifications.value + 1)
    })
    
    // Уведомления о маршрутах (глобально)
    websocket.on('route_assigned', (data) => {
      playSound()
      
      if ('Notification' in window && Notification.permission === 'granted') {
        new Notification('Новый маршрут', {
          body: `Вам назначен маршрут: ${data.route_title}`,
          icon: '/logo.png',
          tag: `route-${data.route_id}`
        })
      }
      
      // Добавляем уведомление в список
      notifications.value.unshift({
        id: `route-${data.route_id}`,
        type: 'route',
        message: `Вам назначен маршрут: ${data.route_title}`,
        created_at: new Date().toISOString(),
        route_id: data.route_id
      })
      
      // Ограничиваем количество уведомлений
      if (notifications.value.length > 50) {
        notifications.value = notifications.value.slice(0, 50)
      }
      
      // Сохраняем уведомления
      saveNotifications()
      
      updateUnreadCount(unreadNotifications.value + 1)
    })
  }
  
  // Обработчики для автоматического определения статуса
  const handleVisibilityChange = () => {
    if (document.hidden) {
      // Страница скрыта - устанавливаем офлайн
      websocket.updateStatus('offline')
    } else {
      // Страница видима - устанавливаем онлайн
      websocket.updateStatus('online')
    }
  }
  
  const handleBeforeUnload = () => {
    // Перед закрытием страницы - устанавливаем офлайн
    websocket.updateStatus('offline')
  }
  
  // Слушаем события
  document.addEventListener('visibilitychange', handleVisibilityChange)
  window.addEventListener('beforeunload', handleBeforeUnload)
  
  // Очистка при размонтировании
  onBeforeUnmount(() => {
    document.removeEventListener('visibilitychange', handleVisibilityChange)
    window.removeEventListener('beforeunload', handleBeforeUnload)
  })
})

// Отслеживаем переход в чат для обнуления счетчика
watch(() => route.name, (newName, oldName) => {
  // Обнуляем счетчик ТОЛЬКО при переходе В чат (не при обновлении страницы)
  if (newName === 'chat-detail' && oldName && oldName !== 'chat-detail') {
    // Получаем ID чата из параметров
    const chatId = route.params.id
    
    // Удаляем уведомления для этого чата
    const beforeCount = notifications.value.length
    notifications.value = notifications.value.filter(n => n.chat_id !== parseInt(chatId))
    const afterCount = notifications.value.length
    
    // Сохраняем изменения
    saveNotifications()
    
    // Уменьшаем счетчик на количество удаленных уведомлений
    const removedCount = beforeCount - afterCount
    const newCount = Math.max(0, unreadNotifications.value - removedCount)
    updateUnreadCount(newCount)
  }
})

// Синхронизируем счетчик с реальным количеством уведомлений при загрузке
watch(() => notifications.value.length, (newLength) => {
  // Если уведомлений меньше чем счетчик, корректируем
  if (newLength < unreadNotifications.value) {
    updateUnreadCount(newLength)
  }
})

onBeforeUnmount(() => {
  // Устанавливаем офлайн перед отключением
  websocket.updateStatus('offline')
  // Отключаемся при выходе
  websocket.disconnect()
})

const user = computed(() => authStore.user)
const userInitials = computed(() => {
  if (!user.value) return '?'
  return `${user.value.first_name?.[0] || ''}${user.value.last_name?.[0] || ''}`
})

const menuItems = computed(() => {
  const items = [
    { path: '/chats', label: 'Чаты', icon: ChatBubbleLeftRightIcon },
    { path: '/employees', label: 'Сотрудники', icon: UserGroupIcon },
    { path: '/tasks', label: 'Задачи', icon: ClipboardDocumentListIcon },
    { path: '/notes', label: 'Заметки', icon: DocumentTextIcon },
    { path: '/vacations', label: 'Отпуска', icon: CalendarDaysIcon },
    { path: '/routes', label: 'Маршруты', icon: MapIcon }
  ]
  
  // Добавляем админ-панель только для администраторов
  if (user.value?.role === 'admin') {
    items.push({ path: '/admin', label: 'Администрирование', icon: Cog6ToothIcon })
  }
  
  return items
})

const currentPageTitle = computed(() => {
  const item = menuItems.value.find(item => route.path.startsWith(item.path))
  return item?.label || 'Главная'
})

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}

function formatTime(dateStr) {
  return new Date(dateStr).toLocaleString('ru-RU')
}
</script>
