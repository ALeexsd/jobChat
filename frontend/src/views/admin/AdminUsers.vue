<template>
  <div class="h-full flex flex-col p-6 bg-gray-50 dark:bg-gray-900">
    <div class="max-w-7xl mx-auto w-full">
      <!-- Заголовок и поиск -->
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Управление пользователями</h1>
        
        <div class="flex items-center gap-3 w-full sm:w-auto">
          <div class="relative flex-1 sm:flex-initial">
            <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Поиск пользователей..."
              class="input pl-10 w-full sm:w-64"
            />
          </div>
          <button @click="showAddUserModal = true" class="btn-primary whitespace-nowrap">
            <PlusIcon class="w-5 h-5 mr-2" />
            Добавить
          </button>
        </div>
      </div>

      <!-- Фильтры -->
      <div class="flex gap-3 mb-6 overflow-x-auto pb-2">
        <button
          @click="filterRole = null"
          :class="[
            'px-4 py-2 rounded-lg text-sm font-medium transition-colors whitespace-nowrap',
            filterRole === null
              ? 'bg-blue-600 text-white'
              : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
          ]"
        >
          Все ({{ users.length }})
        </button>
        <button
          @click="filterRole = 'admin'"
          :class="[
            'px-4 py-2 rounded-lg text-sm font-medium transition-colors whitespace-nowrap',
            filterRole === 'admin'
              ? 'bg-blue-600 text-white'
              : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
          ]"
        >
          Администраторы ({{ users.filter(u => u.role === 'admin').length }})
        </button>
        <button
          @click="filterRole = 'user'"
          :class="[
            'px-4 py-2 rounded-lg text-sm font-medium transition-colors whitespace-nowrap',
            filterRole === 'user'
              ? 'bg-blue-600 text-white'
              : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
          ]"
        >
          Пользователи ({{ users.filter(u => u.role === 'user').length }})
        </button>
      </div>

      <!-- Таблица пользователей -->
      <div class="card dark:bg-gray-800 dark:border-gray-700 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Пользователь</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Email</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Должность</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Роль</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Статус</th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Действия</th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-for="user in filteredUsers" :key="user.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                <td class="px-6 py-4">
                  <div class="flex items-center">
                    <img
                      v-if="user.avatar"
                      :src="user.avatar"
                      :alt="user.first_name"
                      class="w-10 h-10 rounded-full mr-3"
                    />
                    <div v-else class="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-semibold mr-3">
                      {{ user.first_name?.[0] }}{{ user.last_name?.[0] }}
                    </div>
                    <div>
                      <div class="font-medium text-gray-900 dark:text-gray-100">
                        {{ user.first_name }} {{ user.last_name }}
                      </div>
                      <div class="text-sm text-gray-500 dark:text-gray-400">ID: {{ user.id }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 text-gray-900 dark:text-gray-100">{{ user.email }}</td>
                <td class="px-6 py-4 text-gray-900 dark:text-gray-100">{{ user.position || '-' }}</td>
                <td class="px-6 py-4">
                  <span
                    :class="[
                      'px-2 py-1 text-xs font-medium rounded-full',
                      user.role === 'admin'
                        ? 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
                        : 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
                    ]"
                  >
                    {{ user.role === 'admin' ? 'Администратор' : 'Пользователь' }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <span class="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                    Активен
                  </span>
                </td>
                <td class="px-6 py-4 text-right">
                  <div class="flex items-center justify-end gap-2">
                    <button
                      @click="editUser(user)"
                      class="p-2 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-colors"
                      title="Редактировать"
                    >
                      <PencilIcon class="w-5 h-5" />
                    </button>
                    <button
                      @click="confirmDeleteUser(user)"
                      class="p-2 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                      title="Удалить"
                    >
                      <TrashIcon class="w-5 h-5" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Модальное окно добавления/редактирования пользователя -->
    <div v-if="showAddUserModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg max-w-md w-full p-6">
        <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-4">
          {{ editingUser ? 'Редактировать пользователя' : 'Добавить пользователя' }}
        </h2>
        
        <p v-if="editingUser" class="text-sm text-gray-600 dark:text-gray-400 mb-4">
          Заполните только те поля, которые хотите изменить
        </p>
        
        <form @submit.prevent="saveUser" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Имя {{ !editingUser ? '*' : '' }}
            </label>
            <input 
              v-model="userForm.first_name" 
              type="text" 
              :required="!editingUser" 
              class="input w-full"
              :placeholder="editingUser ? 'Оставьте пустым, если не хотите менять' : ''"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Фамилия {{ !editingUser ? '*' : '' }}
            </label>
            <input 
              v-model="userForm.last_name" 
              type="text" 
              :required="!editingUser" 
              class="input w-full"
              :placeholder="editingUser ? 'Оставьте пустым, если не хотите менять' : ''"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Email {{ !editingUser ? '*' : '' }}
            </label>
            <input 
              v-model="userForm.email" 
              type="email" 
              :required="!editingUser" 
              class="input w-full"
              :placeholder="editingUser ? 'Оставьте пустым, если не хотите менять' : ''"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Пароль {{ !editingUser ? '*' : '' }}
            </label>
            <input 
              v-model="userForm.password" 
              type="password" 
              :required="!editingUser" 
              class="input w-full"
              :placeholder="editingUser ? 'Оставьте пустым, чтобы не менять пароль' : ''"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Должность</label>
            <input 
              v-model="userForm.position" 
              type="text" 
              class="input w-full"
              placeholder="Необязательно"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Роль</label>
            <select v-model="userForm.role" class="input w-full">
              <option value="user">Пользователь</option>
              <option value="admin">Администратор</option>
            </select>
          </div>
          
          <div class="flex gap-3 pt-4">
            <button type="submit" class="btn-primary flex-1">
              {{ editingUser ? 'Сохранить' : 'Добавить' }}
            </button>
            <button type="button" @click="closeModal" class="btn-secondary flex-1">
              Отмена
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Модальное окно подтверждения удаления -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg max-w-md w-full p-6">
        <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-4">Удалить пользователя?</h2>
        <p class="text-gray-600 dark:text-gray-400 mb-6">
          Вы уверены, что хотите удалить пользователя {{ userToDelete?.first_name }} {{ userToDelete?.last_name }}?
          Это действие нельзя отменить.
        </p>
        
        <div class="flex gap-3">
          <button @click="deleteUser" class="btn-danger flex-1">Удалить</button>
          <button @click="showDeleteModal = false" class="btn-secondary flex-1">Отмена</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import { 
  MagnifyingGlassIcon, 
  PlusIcon, 
  PencilIcon, 
  TrashIcon 
} from '@heroicons/vue/24/outline'

const users = ref([])
const searchQuery = ref('')
const filterRole = ref(null)
const showAddUserModal = ref(false)
const showDeleteModal = ref(false)
const editingUser = ref(null)
const userToDelete = ref(null)

const userForm = ref({
  first_name: '',
  last_name: '',
  email: '',
  password: '',
  position: '',
  role: 'user'
})

const filteredUsers = computed(() => {
  let filtered = users.value

  if (filterRole.value) {
    filtered = filtered.filter(u => u.role === filterRole.value)
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(u =>
      u.first_name?.toLowerCase().includes(query) ||
      u.last_name?.toLowerCase().includes(query) ||
      u.email?.toLowerCase().includes(query)
    )
  }

  return filtered
})

onMounted(() => {
  loadUsers()
})

async function loadUsers() {
  try {
    const response = await api.get('/users/')
    users.value = response.data
  } catch (error) {
    console.error('Load users error:', error)
  }
}

function editUser(user) {
  editingUser.value = user
  userForm.value = {
    first_name: user.first_name || '',
    last_name: user.last_name || '',
    email: user.email || '',
    position: user.position || '',
    role: user.role || 'user',
    password: '' // Пароль опционален при редактировании
  }
  showAddUserModal.value = true
}

function confirmDeleteUser(user) {
  userToDelete.value = user
  showDeleteModal.value = true
}

async function saveUser() {
  try {
    if (editingUser.value) {
      // При редактировании отправляем только заполненные поля
      const updateData = {}
      
      if (userForm.value.first_name && userForm.value.first_name !== editingUser.value.first_name) {
        updateData.first_name = userForm.value.first_name
      }
      if (userForm.value.last_name && userForm.value.last_name !== editingUser.value.last_name) {
        updateData.last_name = userForm.value.last_name
      }
      if (userForm.value.email && userForm.value.email !== editingUser.value.email) {
        updateData.email = userForm.value.email
      }
      if (userForm.value.position !== editingUser.value.position) {
        updateData.position = userForm.value.position
      }
      if (userForm.value.role && userForm.value.role !== editingUser.value.role) {
        updateData.role = userForm.value.role
      }
      if (userForm.value.password) {
        updateData.password = userForm.value.password
      }
      
      // Если есть изменения, отправляем запрос
      if (Object.keys(updateData).length > 0) {
        await api.put(`/users/${editingUser.value.id}`, updateData)
      }
    } else {
      // При создании все поля обязательны
      if (!userForm.value.first_name || !userForm.value.last_name || !userForm.value.email || !userForm.value.password) {
        alert('Заполните все обязательные поля')
        return
      }
      await api.post('/auth/register', userForm.value)
    }
    await loadUsers()
    closeModal()
  } catch (error) {
    console.error('Save user error:', error)
    alert('Ошибка при сохранении пользователя: ' + (error.response?.data?.detail || error.message))
  }
}

async function deleteUser() {
  try {
    await api.delete(`/users/${userToDelete.value.id}`)
    await loadUsers()
    showDeleteModal.value = false
    userToDelete.value = null
  } catch (error) {
    console.error('Delete user error:', error)
    alert('Ошибка при удалении пользователя')
  }
}

function closeModal() {
  showAddUserModal.value = false
  editingUser.value = null
  userForm.value = {
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    position: '',
    role: 'user'
  }
}
</script>
