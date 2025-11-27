<template>
  <div class="h-full flex flex-col p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Задачи</h1>
      <button @click="showCreateModal = true" class="btn-primary flex items-center">
        <PlusIcon class="w-5 h-5 mr-2" />
        Новая задача
      </button>
    </div>
    
    <!-- Фильтры по типу задач -->
    <div class="mb-4 flex gap-2">
      <button
        @click="filterType = 'all'"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-colors',
          filterType === 'all' 
            ? 'bg-primary-600 text-white' 
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
        ]"
      >
        Все ({{ tasks.length }})
      </button>
      <button
        @click="filterType = 'assigned'"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-colors',
          filterType === 'assigned' 
            ? 'bg-primary-600 text-white' 
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
        ]"
      >
        Назначенные мне ({{ assignedToMe.length }})
      </button>
      <button
        @click="filterType = 'created'"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-colors',
          filterType === 'created' 
            ? 'bg-primary-600 text-white' 
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
        ]"
      >
        Созданные мной ({{ createdByMe.length }})
      </button>
    </div>
    
    <!-- Filters -->
    <div class="mb-6 flex items-center space-x-4">
      <div class="flex-1">
        <div class="relative">
          <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Поиск задач..."
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>
      </div>
      
      <select
        v-model="sortBy"
        class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
      >
        <option value="date">По дате создания</option>
        <option value="priority">По приоритету</option>
        <option value="status">По статусу</option>
        <option value="deadline">По дедлайну</option>
      </select>
      
      <select
        v-model="filterStatus"
        class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
      >
        <option value="">Все статусы</option>
        <option value="todo">К выполнению</option>
        <option value="in_progress">В работе</option>
        <option value="review">На проверке</option>
        <option value="done">Выполнено</option>
      </select>
      
      <select
        v-model="filterPriority"
        class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
      >
        <option value="">Все приоритеты</option>
        <option value="low">Низкий</option>
        <option value="medium">Средний</option>
        <option value="high">Высокий</option>
        <option value="urgent">Срочный</option>
      </select>
    </div>
    
    <!-- Tasks Grid -->
    <div class="flex-1 overflow-auto">
      <div v-if="filteredTasks.length === 0" class="text-center py-12">
        <ClipboardDocumentListIcon class="w-16 h-16 mx-auto text-gray-400 mb-4" />
        <p class="text-gray-500 mb-4">Нет задач</p>
        <button @click="showCreateModal = true" class="btn-primary">
          Создать первую задачу
        </button>
      </div>
      
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="task in filteredTasks"
          :key="task.id"
          class="card p-4 hover:shadow-md transition-shadow cursor-pointer"
          @click="viewTask(task)"
        >
          <div class="flex items-start justify-between mb-3">
            <span
              :class="[
                'px-2 py-1 text-xs font-medium rounded',
                getPriorityClass(task.priority)
              ]"
            >
              {{ getPriorityLabel(task.priority) }}
            </span>
            
            <Menu as="div" class="relative">
              <MenuButton @click.stop class="p-1 hover:bg-gray-100 rounded transition-colors">
                <EllipsisVerticalIcon class="w-5 h-5 text-gray-600" />
              </MenuButton>
              
              <transition
                enter-active-class="transition duration-100 ease-out"
                enter-from-class="transform scale-95 opacity-0"
                enter-to-class="transform scale-100 opacity-100"
                leave-active-class="transition duration-75 ease-in"
                leave-from-class="transform scale-100 opacity-100"
                leave-to-class="transform scale-95 opacity-0"
              >
                <MenuItems class="absolute right-0 mt-2 w-48 origin-top-right bg-white rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none z-10">
                  <div class="p-1">
                    <MenuItem v-slot="{ active }">
                      <button
                        @click.stop="editTask(task)"
                        :class="[
                          active ? 'bg-gray-100' : '',
                          'group flex items-center w-full px-3 py-2 text-sm text-gray-900 rounded-md'
                        ]"
                      >
                        <PencilIcon class="w-4 h-4 mr-2" />
                        Редактировать
                      </button>
                    </MenuItem>
                    <MenuItem v-slot="{ active }">
                      <button
                        @click.stop="deleteTask(task.id)"
                        :class="[
                          active ? 'bg-red-50 text-red-600' : 'text-gray-900',
                          'group flex items-center w-full px-3 py-2 text-sm rounded-md'
                        ]"
                      >
                        <TrashIcon class="w-4 h-4 mr-2" />
                        Удалить
                      </button>
                    </MenuItem>
                  </div>
                </MenuItems>
              </transition>
            </Menu>
          </div>
          
          <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ task.title }}</h3>
          <p v-if="task.description" class="text-sm text-gray-600 mb-3 line-clamp-2">
            {{ task.description }}
          </p>
          
          <div class="flex items-center justify-between text-sm">
            <span
              :class="[
                'px-2 py-1 rounded',
                getStatusClass(task.status)
              ]"
            >
              {{ getStatusLabel(task.status) }}
            </span>
            
            <span v-if="task.due_date" class="text-gray-500 flex items-center">
              <CalendarIcon class="w-4 h-4 mr-1" />
              {{ formatDate(task.due_date) }}
            </span>
          </div>
          
          <div v-if="task.tags?.length" class="mt-3 flex flex-wrap gap-1">
            <span
              v-for="tag in task.tags"
              :key="tag"
              class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded"
            >
              {{ tag }}
            </span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Create Task Modal -->
    <CreateTaskModal
      :show="showCreateModal"
      :preselected-assignee="preselectedAssignee"
      @close="showCreateModal = false"
      @created="handleTaskCreated"
    />
    
    <!-- Edit Task Modal -->
    <EditTaskModal
      :show="showEditModal"
      :task="selectedTask"
      @close="showEditModal = false"
      @updated="handleTaskUpdated"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import websocket from '@/services/websocket'
import CreateTaskModal from '@/components/CreateTaskModal.vue'
import EditTaskModal from '@/components/EditTaskModal.vue'
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'
import {
  PlusIcon,
  MagnifyingGlassIcon,
  ClipboardDocumentListIcon,
  EllipsisVerticalIcon,
  PencilIcon,
  TrashIcon,
  CalendarIcon
} from '@heroicons/vue/24/outline'

const route = useRoute()
const authStore = useAuthStore()

const tasks = ref([])
const searchQuery = ref('')
const filterStatus = ref('')
const filterPriority = ref('')
const filterType = ref(localStorage.getItem('taskFilter') || 'all')
const sortBy = ref(localStorage.getItem('taskSort') || 'date')
const showCreateModal = ref(false)
const showEditModal = ref(false)
const preselectedAssignee = ref(null)
const selectedTask = ref(null)

// Вычисляемые свойства для фильтрации
const currentUserId = computed(() => authStore.user?.id)

const assignedToMe = computed(() => 
  tasks.value.filter(task => 
    task.assignees?.some(a => a.user_id === currentUserId.value)
  )
)

const createdByMe = computed(() => 
  tasks.value.filter(task => task.created_by_id === currentUserId.value)
)

const filteredTasks = computed(() => {
  let result = tasks.value
  
  // Фильтрация по типу (все/назначенные/созданные)
  if (filterType.value === 'assigned') {
    result = assignedToMe.value
  } else if (filterType.value === 'created') {
    result = createdByMe.value
  }
  
  // Фильтрация по поиску
  result = result.filter(task => {
    const matchesSearch = !searchQuery.value ||
      task.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      task.description?.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesStatus = !filterStatus.value || task.status === filterStatus.value
    const matchesPriority = !filterPriority.value || task.priority === filterPriority.value
    
    return matchesSearch && matchesStatus && matchesPriority
  })
  
  // Сортировка
  return result.sort((a, b) => {
    if (sortBy.value === 'date') {
      return new Date(b.created_at) - new Date(a.created_at)
    } else if (sortBy.value === 'priority') {
      const priorities = { urgent: 4, high: 3, medium: 2, low: 1 }
      return (priorities[b.priority] || 0) - (priorities[a.priority] || 0)
    } else if (sortBy.value === 'status') {
      return a.status.localeCompare(b.status)
    } else if (sortBy.value === 'deadline') {
      if (!a.deadline) return 1
      if (!b.deadline) return -1
      return new Date(a.deadline) - new Date(b.deadline)
    }
    return 0
  })
})

onMounted(() => {
  loadTasks()
  
  // Проверяем, есть ли параметр assignee в query
  if (route.query.assignee) {
    preselectedAssignee.value = parseInt(route.query.assignee)
    showCreateModal.value = true
  }
  
  // Подписываемся на уведомления о задачах
  console.log('📋 TasksView: Subscribing to task_assigned events')
  websocket.on('task_assigned', handleTaskAssigned)
  
  // Проверяем подключение WebSocket
  console.log('📋 TasksView: WebSocket connected:', websocket.isConnected())
})

onUnmounted(() => {
  // Отписываемся от уведомлений
  websocket.off('task_assigned', handleTaskAssigned)
})

// Следим за изменениями query параметров
watch(() => route.query.assignee, (newAssignee) => {
  if (newAssignee) {
    preselectedAssignee.value = parseInt(newAssignee)
    showCreateModal.value = true
  }
})

// Сохраняем выбранный фильтр и сортировку
watch(filterType, (newFilter) => {
  localStorage.setItem('taskFilter', newFilter)
})

watch(sortBy, (newSort) => {
  localStorage.setItem('taskSort', newSort)
})

// Обработчик уведомления о назначении задачи
async function handleTaskAssigned(data) {
  console.log('🎯 TasksView: Task assigned event received!', data)
  
  // Обновляем список задач (звук и уведомление обрабатываются в MainView)
  console.log('🔄 Reloading tasks')
  await loadTasks()
}

async function loadTasks() {
  try {
    const response = await api.get('/tasks')
    tasks.value = response.data
  } catch (error) {
    console.error('Load tasks error:', error)
  }
}

function handleTaskCreated() {
  loadTasks()
}

function viewTask(task) {
  console.log('View task:', task)
}

function editTask(task) {
  selectedTask.value = task
  showEditModal.value = true
}

async function handleTaskUpdated() {
  await loadTasks()
}

async function deleteTask(id) {
  if (!confirm('Удалить задачу?')) return
  
  try {
    await api.delete(`/tasks/${id}`)
    loadTasks()
  } catch (error) {
    console.error('Delete task error:', error)
  }
}

function getPriorityClass(priority) {
  const classes = {
    low: 'bg-gray-100 text-gray-700',
    medium: 'bg-yellow-100 text-yellow-700',
    high: 'bg-orange-100 text-orange-700',
    urgent: 'bg-red-100 text-red-700'
  }
  return classes[priority] || classes.medium
}

function getPriorityLabel(priority) {
  const labels = {
    low: 'Низкий',
    medium: 'Средний',
    high: 'Высокий',
    urgent: 'Срочный'
  }
  return labels[priority] || priority
}

function getStatusClass(status) {
  const classes = {
    todo: 'bg-gray-100 text-gray-700',
    in_progress: 'bg-blue-100 text-blue-700',
    review: 'bg-purple-100 text-purple-700',
    done: 'bg-green-100 text-green-700'
  }
  return classes[status] || classes.todo
}

function getStatusLabel(status) {
  const labels = {
    todo: 'К выполнению',
    in_progress: 'В работе',
    review: 'На проверке',
    done: 'Выполнено'
  }
  return labels[status] || status
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('ru-RU')
}
</script>
