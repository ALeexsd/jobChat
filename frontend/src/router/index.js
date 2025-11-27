import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/RegisterView.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('@/views/MainView.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Main',
        redirect: '/chats'
      },
      {
        path: 'chats',
        name: 'Chats',
        component: () => import('@/views/ChatsView.vue')
      },
      {
        path: 'chats/:id',
        name: 'ChatDetail',
        component: () => import('@/views/ChatDetailView.vue')
      },
      {
        path: 'tasks',
        name: 'Tasks',
        component: () => import('@/views/TasksView.vue')
      },
      {
        path: 'routes',
        name: 'Routes',
        component: () => import('@/views/RoutesView.vue')
      },
      {
        path: 'notes',
        name: 'Notes',
        component: () => import('@/views/NotesView.vue')
      },
      {
        path: 'vacations',
        name: 'Vacations',
        component: () => import('@/views/VacationsView.vue')
      },
      {
        path: 'employees',
        name: 'Employees',
        component: () => import('@/views/EmployeesView.vue')
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/ProfileView.vue')
      },
      {
        path: 'users/:id',
        name: 'UserProfile',
        component: () => import('@/views/UserProfileView.vue')
      },
      {
        path: 'admin',
        name: 'Admin',
        redirect: '/admin/dashboard',
        meta: { requiresAdmin: true }
      },
      {
        path: 'admin/dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/AdminDashboard.vue'),
        meta: { requiresAdmin: true }
      },
      {
        path: 'admin/users',
        name: 'AdminUsers',
        component: () => import('@/views/admin/AdminUsers.vue'),
        meta: { requiresAdmin: true }
      },
      {
        path: 'admin/vacations',
        name: 'AdminVacations',
        component: () => import('@/views/admin/AdminVacations.vue'),
        meta: { requiresAdmin: true }
      },
      {
        path: 'admin/tasks',
        name: 'AdminTasks',
        component: () => import('@/views/admin/AdminTasks.vue'),
        meta: { requiresAdmin: true }
      },
      {
        path: 'admin/routes',
        name: 'AdminRoutes',
        component: () => import('@/views/admin/AdminRoutes.vue'),
        meta: { requiresAdmin: true }
      },
      {
        path: 'admin/notes',
        name: 'AdminNotes',
        component: () => import('@/views/admin/AdminNotes.vue'),
        meta: { requiresAdmin: true }
      },
      {
        path: 'admin/chats',
        name: 'AdminChats',
        component: () => import('@/views/admin/AdminChats.vue'),
        meta: { requiresAdmin: true }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (!to.meta.requiresAuth && authStore.isAuthenticated) {
    next('/')
  } else if (to.meta.requiresAdmin && authStore.user?.role !== 'admin') {
    // Если требуется роль админа, но пользователь не админ
    next('/')
  } else {
    next()
  }
})

export default router
