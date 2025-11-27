import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'

export const useTaskStore = defineStore('task', () => {
  const tasks = ref([])
  const currentTask = ref(null)

  async function fetchTasks() {
    try {
      const response = await api.get('/tasks')
      tasks.value = response.data
    } catch (error) {
      console.error('Fetch tasks error:', error)
    }
  }

  async function fetchTask(taskId) {
    try {
      const response = await api.get(`/tasks/${taskId}`)
      currentTask.value = response.data
    } catch (error) {
      console.error('Fetch task error:', error)
    }
  }

  async function createTask(taskData) {
    try {
      const response = await api.post('/tasks', taskData)
      tasks.value.push(response.data)
      return response.data
    } catch (error) {
      console.error('Create task error:', error)
    }
  }

  async function updateTask(taskId, taskData) {
    try {
      const response = await api.put(`/tasks/${taskId}`, taskData)
      const index = tasks.value.findIndex(t => t.id === taskId)
      if (index !== -1) {
        tasks.value[index] = response.data
      }
      return response.data
    } catch (error) {
      console.error('Update task error:', error)
    }
  }

  async function addComment(taskId, content) {
    try {
      await api.post(`/tasks/${taskId}/comments`, { content })
      await fetchTask(taskId)
    } catch (error) {
      console.error('Add comment error:', error)
    }
  }

  return {
    tasks,
    currentTask,
    fetchTasks,
    fetchTask,
    createTask,
    updateTask,
    addComment
  }
})
