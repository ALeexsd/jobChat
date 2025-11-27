<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-500 to-purple-600 px-4 py-12">
    <div class="max-w-md w-full">
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-white mb-2">Регистрация</h1>
        <p class="text-primary-100">Создайте новый аккаунт</p>
      </div>
      
      <div class="card p-8">
        <form @submit.prevent="handleRegister" class="space-y-4">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
              Имя пользователя
            </label>
            <input
              id="username"
              v-model="formData.username"
              type="text"
              required
              class="input"
              placeholder="username"
            />
          </div>
          
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              Пароль
            </label>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              required
              minlength="6"
              class="input"
              placeholder="Минимум 6 символов"
            />
          </div>
          
          <div>
            <label for="confirm_password" class="block text-sm font-medium text-gray-700 mb-2">
              Подтвердите пароль
            </label>
            <input
              id="confirm_password"
              v-model="formData.confirm_password"
              type="password"
              required
              class="input"
              placeholder="Повторите пароль"
            />
          </div>
          
          <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
            {{ error }}
          </div>
          
          <button
            type="submit"
            :disabled="loading"
            class="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">Регистрация...</span>
            <span v-else>Зарегистрироваться</span>
          </button>
        </form>
        
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            Уже есть аккаунт?
            <router-link to="/login" class="text-primary-600 hover:text-primary-700 font-medium">
              Войти
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const formData = ref({
  username: '',
  password: '',
  confirm_password: ''
})

const loading = ref(false)
const error = ref('')

async function handleRegister() {
  if (formData.value.password !== formData.value.confirm_password) {
    error.value = 'Пароли не совпадают'
    return
  }
  
  if (formData.value.password.length < 6) {
    error.value = 'Пароль должен быть минимум 6 символов'
    return
  }
  
  loading.value = true
  error.value = ''
  
  try {
    await authStore.register({
      username: formData.value.username,
      password: formData.value.password,
      first_name: formData.value.username, // Используем username как имя по умолчанию
      last_name: ''
    })
    router.push('/login')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка регистрации'
  } finally {
    loading.value = false
  }
}
</script>
