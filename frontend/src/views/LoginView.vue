<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-500 to-purple-600 px-4">
    <div class="max-w-md w-full">
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-white mb-2">Корпоративный мессенджер</h1>
        <p class="text-primary-100">Войдите в свой аккаунт</p>
      </div>
      
      <div class="card p-8">
        <form @submit.prevent="handleLogin" class="space-y-6">
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
              placeholder="Введите имя пользователя"
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
              class="input"
              placeholder="Введите пароль"
            />
          </div>
          
          <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {{ error }}
          </div>
          
          <button
            type="submit"
            :disabled="loading"
            class="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">Вход...</span>
            <span v-else>Войти</span>
          </button>
        </form>
        
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            Нет аккаунта?
            <router-link to="/register" class="text-primary-600 hover:text-primary-700 font-medium">
              Зарегистрироваться
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
  password: ''
})

const loading = ref(false)
const error = ref('')

async function handleLogin() {
  if (!formData.value.username || !formData.value.password) {
    error.value = 'Заполните все поля'
    return
  }
  
  loading.value = true
  error.value = ''
  
  try {
    console.log('Attempting login with:', formData.value)
    await authStore.login(formData.value)
    router.push('/')
  } catch (err) {
    console.error('Login failed:', err)
    error.value = err.response?.data?.detail || 'Ошибка входа'
  } finally {
    loading.value = false
  }
}
</script>
