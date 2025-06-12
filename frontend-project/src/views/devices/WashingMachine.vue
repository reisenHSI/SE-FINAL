<template>
  <div v-if="isLoaded" class="flex flex-col items-center justify-center h-screen bg-gray-100">
    <!-- 设备信息 -->
    <div class="text-center mb-6">
      <h1 class="text-3xl font-bold mb-2">{{ device.name }}</h1>
      <p class="text-lg">当前模式: {{ device.mode }}</p>
      <p class="text-lg" v-if="device.remaining_time !== null">剩余时间: {{ device.remaining_time }} 分钟</p>
    </div>

    <!-- 洗衣机滚筒动画 -->
    <div class="relative w-48 h-48 border-8 border-gray-500 rounded-full flex items-center justify-center bg-white shadow-lg overflow-hidden">
      <div
        class="w-40 h-40 rounded-full border-4 border-blue-400"
        :class="{ 'animate-spin': isRunning, 'animate-none': !isRunning }"
      ></div>
    </div>

    <!-- 控制按钮 -->
    <div class="mt-8 flex flex-wrap justify-center gap-4" v-if="device.controls">
      <button
        @click="toggleWashingMachine"
        class="px-6 py-3 bg-blue-500 text-white rounded-full shadow-lg transform transition active:scale-95"
      >
        {{ isRunning ? '停止洗衣机' : '启动洗衣机' }}
      </button>

      <select
        v-model="selectedMode"
        @change="changeMode"
        class="px-4 py-2 border rounded-lg"
        :disabled="!device.controls.can_change_mode"
      >
        <option v-for="mode in device.valid_modes" :key="mode" :value="mode">{{ mode }}</option>
      </select>

      <button
        @click="renameDevice"
        v-if="device.controls.can_rename"
        class="px-6 py-3 bg-green-500 text-white rounded-full shadow-lg transform transition active:scale-95"
      >
        修改设备名称
      </button>
    </div>
  </div>

  <!-- 加载中状态 -->
  <div v-else class="flex items-center justify-center h-screen bg-gray-100">
    <p class="text-lg text-gray-500">加载中...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { API_BASE_URL } from "../../main";
import axios from 'axios'
import { useRoute } from 'vue-router'

const route = useRoute()
const deviceName = route.query.name

const device = ref({})
const isRunning = ref(false)
const selectedMode = ref('')
const isLoaded = ref(false)

const fetchWashingMachine = async () => {
  try {
    const response = await axios.post(`${API_BASE_URL}/home/devices/washingmachine/`, {
      username: localStorage.getItem('username'),
      device_name: deviceName
    })

    if (response.data.status === 'success') {
      device.value = response.data.device
      isRunning.value = response.data.device.status === '1'
      selectedMode.value = response.data.device.mode
    } else {
      alert(response.data.message)
    }
  } catch (error) {
    console.error(error)
    alert('获取设备信息失败')
  } finally {
    isLoaded.value = true
  }
}

const toggleWashingMachine = async () => {
  try {
    const newStatus = isRunning.value ? '0' : '1'
    const response = await axios.post(`${API_BASE_URL}/home/devices/washingmachine/`, {
      username: localStorage.getItem('username'),
      device_name: deviceName,
      new_status: newStatus
    })

    if (response.data.status === 'success') {
      isRunning.value = !isRunning.value
    } else {
      alert(response.data.message)
    }
  } catch (error) {
    console.error(error)
    alert('操作失败')
  }
}

const changeMode = async () => {
  try {
    const response = await axios.post(`${API_BASE_URL}/home/devices/washingmachine/`, {
      username: localStorage.getItem('username'),
      device_name: deviceName,
      new_mode: selectedMode.value
    })

    if (response.data.status === 'success') {
      device.value.mode = selectedMode.value
    } else {
      alert(response.data.message)
    }
  } catch (error) {
    console.error(error)
    alert('切换模式失败')
  }
}

const renameDevice = async () => {
  const newName = prompt('请输入新的设备名称', device.value.name)
  if (newName && newName.trim() !== '') {
    try {
      const response = await axios.post(`${API_BASE_URL}/home/devices/washingmachine/`, {
        username: localStorage.getItem('username'),
        device_name: deviceName,
        new_name: newName
      })

      if (response.data.status === 'success') {
        device.value.name = newName
      } else {
        alert(response.data.message)
      }
    } catch (error) {
      console.error(error)
      alert('重命名失败')
    }
  }
}

onMounted(() => {
  fetchWashingMachine()
})
</script>

<style scoped>
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

.animate-none {
  animation: none;
}
</style>

