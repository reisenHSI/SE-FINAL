import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/index.css'


// 引入 Element Plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 全局 axios 实例
import axios from 'axios'
export const API_BASE_URL = 'http://127.0.0.1:8000/'

const app = createApp(App)

// 使用插件
app.use(router)
app.use(ElementPlus)

// 全局挂载 axios 实例
app.config.globalProperties.$axios = axios

// 挂载应用
app.mount('#app')
