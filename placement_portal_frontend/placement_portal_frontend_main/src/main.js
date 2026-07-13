import { createApp } from 'vue'
import { createPinia } from "pinia"
import App from './App.vue'
import router from './router/index.js'


import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import { useAuthStore } from './stores/AuthStore.js'





const app = createApp(App)

const pinia =createPinia()
app.use(pinia)

const authStore = useAuthStore()

await authStore.initAuth()  

app.use(router)
app.mount('#app')
