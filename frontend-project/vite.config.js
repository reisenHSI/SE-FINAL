import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,       // 你可以自定义开发服务器端口
    open: true,       // 启动后自动打开浏览器
  },
  resolve: {
    alias: {
      '@': '/src'     // 配置路径别名，方便导入src下的文件
    }
  }
})
