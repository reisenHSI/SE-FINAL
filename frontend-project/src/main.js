// main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// 引入 Element Plus（Vue 3 版本）
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 引入 Axios
import axios from 'axios'

// 创建 axios 实例
export const API_BASE_URL = 'http://localhost:8000/api/'
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 创建 Vue 应用实例
const app = createApp(App)

// 使用插件
app.use(router)
app.use(ElementPlus)

// 全局挂载 axios 实例
app.config.globalProperties.$api = apiClient

// 挂载应用
app.mount('#app')
