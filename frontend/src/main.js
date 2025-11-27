import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './assets/main.css'
import { registerSW } from './registerSW'
// import { createYmaps } from 'vue-yandex-maps' // Отключено - пакет не установлен

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Яндекс.Карты (отключено из-за проблем с API ключом)
// app.use(createYmaps({
//   apikey: '65137eb7-838c-4f8e-ad4a-dd0d8c5423d7',
//   lang: 'ru_RU'
// }))

app.mount('#app')

// Регистрация Service Worker
registerSW()
