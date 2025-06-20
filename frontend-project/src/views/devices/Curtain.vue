<template>
  <div class="flex flex-col items-center justify-center h-screen bg-blue-100">
    <!-- 返回按钮 -->
    <div class="w-full max-w-md px-4 py-2 flex justify-start">
      <button
        @click="goBack"
        class="px-4 py-2 bg-gray-300 hover:bg-gray-400 rounded-lg shadow-sm"
      >
        返回
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center text-gray-500 text-xl mt-10">
      正在加载设备信息...
    </div>

    <!-- 设备信息 -->
    <div class="text-center mb-6">
      <h1 class="text-3xl font-bold mb-2">{{ device.name }}</h1>
      <p class="text-lg">设备类型: {{ device.type }}</p>
    </div>

    <!-- 窗帘动画 -->
    <div v-if="!loading" class="relative w-3/4 h-1/2 overflow-hidden border-4 border-blue-400 rounded-xl bg-white shadow-lg">
      <div
        class="absolute top-0 left-0 h-full bg-blue-300 transition-all duration-1000"
        :style="{ width: isOpen ? '0%' : '50%' }"
      ></div>
      <div
        class="absolute top-0 right-0 h-full bg-blue-300 transition-all duration-1000"
        :style="{ width: isOpen ? '0%' : '50%' }"
      ></div>
    </div>

    <!-- 控制按钮 -->
    <div v-if="!loading" class="flex flex-col items-center space-y-6 mt-8">
      <button
        @click="toggleCurtain"
        class="px-6 py-3 bg-blue-500 text-white rounded-full shadow-lg transform transition active:scale-95"
      >
        {{ isOpen ? '关闭窗帘' : '打开窗帘' }}
      </button>

      <!-- 重命名输入框 -->
      <div class="w-full flex flex-col items-center">
        <label class="text-lg font-semibold mb-2">重命名设备</label>
        <div class="flex w-full space-x-4">
          <input
            type="text"
            v-model="newDeviceName"
            placeholder="输入新设备名称"
            class="flex-1 p-2 rounded-lg border border-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            class="px-4 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 transition shadow"
            @click="renameDevice"
          >
            确认
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { API_BASE_URL } from "../../main";
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const deviceName = route.query.name || '默认设备名'
const loading = ref(true)

const device = ref({})
const isOpen = ref(false)
const newDeviceName = ref('')

const fetchCurtain = async () => {
  try {
    const response = await axios.post(`${API_BASE_URL}/home/devices/curtain/`, {
      username: localStorage.getItem('username'),
      device_name: deviceName
    })
    if (response.data.status === 'success') {
      device.value = response.data.device
      isOpen.value = response.data.device.status === 1
    } else {
      alert(response.data.message)
    }
  } catch (error) {
    console.error(error)
    alert('获取设备信息失败')
  } finally {
    loading.value = false
  }
}

const toggleCurtain = async () => {
  try {
    const newStatus = isOpen.value ? '0' : '1'
    console.log(`newStatus:${newStatus}`)
    const response = await axios.post(`${API_BASE_URL}/home/devices/curtain/`, {
      username: localStorage.getItem('username'),
      device_name: deviceName,
      new_status: newStatus
    })

    if (response.data.status === 'success') {
      isOpen.value = !isOpen.value
    } else {
      alert(response.data.message)
    }
  } catch (error) {
    console.error(error)
    alert('操作失败')
  }
}

// 重命名设备
const renameDevice = async () => {
  if (!newDeviceName.value.trim()) {
    alert('设备名称不能为空')
    return
  }

  try {
    const response = await axios.post(`${API_BASE_URL}/home/devices/curtain/`, {
      username: localStorage.getItem('username'),
      device_name: deviceName,
      new_name: newDeviceName.value
    })
    if (response.data.status === 'success') {
      device.value.name = newDeviceName.value
      alert('重命名成功')
      newDeviceName.value = ''
    } else {
      alert(response.data.message)
    }
  } catch (error) {
    alert('重命名失败')
  }
}
const goBack = () => {
  router.push({ name: 'Home' });
}
onMounted(() => {
  fetchCurtain()
})
</script>

<style scoped>
/* 动态窗帘效果已用 tailwind transition 实现，无需额外 CSS */
</style>
