import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('accessToken'))
  const refreshToken = ref(localStorage.getItem('refreshToken'))

  const isAuthenticated = computed(() => !!accessToken.value)

  async function login(credentials) {
    try {
      console.log('Login credentials:', credentials)
      const response = await api.post('/auth/login', credentials)
      console.log('Login response:', response.data)
      accessToken.value = response.data.access_token
      refreshToken.value = response.data.refresh_token
      
      localStorage.setItem('accessToken', accessToken.value)
      localStorage.setItem('refreshToken', refreshToken.value)
      
      await fetchUser()
      return true
    } catch (error) {
      console.error('Login error:', error)
      console.error('Error response:', error.response?.data)
      throw error
    }
  }

  async function register(userData) {
    try {
      await api.post('/auth/register', userData)
      return await login({ username: userData.username, password: userData.password })
    } catch (error) {
      console.error('Register error:', error)
      throw error
    }
  }

  async function fetchUser() {
    try {
      const response = await api.get('/users/me')
      user.value = response.data
    } catch (error) {
      console.error('Fetch user error:', error)
    }
  }

  function logout() {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
  }

  async function refreshAccessToken() {
    try {
      const response = await api.post('/auth/refresh', {
        refresh_token: refreshToken.value
      })
      accessToken.value = response.data.access_token
      refreshToken.value = response.data.refresh_token
      
      localStorage.setItem('accessToken', accessToken.value)
      localStorage.setItem('refreshToken', refreshToken.value)
      
      return true
    } catch (error) {
      logout()
      return false
    }
  }

  async function checkAuth() {
    if (accessToken.value) {
      try {
        await fetchUser()
      } catch (error) {
        console.error('Check auth error:', error)
        logout()
      }
    }
  }

  return {
    user,
    accessToken,
    isAuthenticated,
    login,
    register,
    logout,
    fetchUser,
    refreshAccessToken,
    checkAuth
  }
})
