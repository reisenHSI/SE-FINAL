<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-blue-100 to-white p-4">
    <!-- 设备信息 -->
    <div class="text-center mb-6">
      <h1 class="text-3xl font-bold mb-2">{{ device.name }}</h1>
      <p class="text-lg text-gray-700">{{ device.type }}</p>
      <p class="text-lg text-gray-700">当前温度: {{ device.temperature }}°C</p>
      <p class="text-lg text-gray-700">当前模式: {{ device.mode }}</p>
    </div>

    <!-- 空调显示区域 -->
    <div class="relative flex items-center justify-center w-full mb-10" style="height: 50vh;">
      <!-- 空调图标 -->
      <div
        :class="[
          'transition-all duration-500 ease-in-out flex flex-col items-center justify-center text-9xl',
          device.status === '1' ? 'text-blue-400' : 'text-gray-400'
        ]"
      >
        ❄️
        <!-- 吹风动画 -->
        <div v-if="device.status === '1'" class="mt-4 flex space-x-2">
          <div class="w-2 h-10 bg-blue-300 animate-wind"></div>
          <div class="w-2 h-10 bg-blue-300 animate-wind delay-200"></div>
          <div class="w-2 h-10 bg-blue-300 animate-wind delay-400"></div>
        </div>
      </div>
    </div>

    <!-- 拟真遥控器 -->
    <div class="bg-gray-800 rounded-3xl p-6 text-white shadow-lg flex flex-col items-center space-y-4">
      <!-- 开关按钮 -->
      <button
        @click="togglePower"
        class="w-24 h-12 bg-red-500 rounded-full text-lg font-semibold shadow-md active:scale-95 transition transform"
      >
        {{ device.status === '1' ? '关闭' : '开启' }}
      </button>

      <!-- 温度调节 -->
      <div class="flex items-center space-x-4">
        <button
          @click="changeTemperature(device.temperature - 1)"
          class="w-12 h-12 bg-gray-600 rounded-full text-2xl active:scale-95 transition transform"
        >-</button>
        <span class="text-2xl">{{ device.temperature }}°C</span>
        <button
          @click="changeTemperature(device.temperature + 1)"
          class="w-12 h-12 bg-gray-600 rounded-full text-2xl active:scale-95 transition transform"
        >+</button>
      </div>

      <!-- 模式切换 -->
      <div class="flex space-x-4">
        <button
          v-for="mode in device.valid_modes"
          :key="mode"
          @click="changeMode(mode)"
          :class="[
            'px-4 py-2 rounded-full text-sm font-semibold active:scale-95 transition transform',
            device.mode === mode ? 'bg-green-400' : 'bg-gray-600'
          ]"
        >
          {{ modeLabels[mode] }}
        </button>
      </div>

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
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'
import { API_BASE_URL } from "../../main";

const route = useRoute()
const deviceName = route.query.name || '默认空调设备'

const device = ref({
  id: null,
  name: '',
  type: '',
  status: '0',
  temperature: 24,
  mode: 'cool',
  valid_modes: [],
  controls: {}
})

const modeLabels = {
  cool: '制冷',
  heat: '制热',
  dry: '除湿'
}

const fetchDeviceInfo = async () => {
  try {
    const response = await axios.post(`${API_BASE_URL}/home/devices/airConditioner/`, {
      username: localStorage.getItem('username'),
      device_name: deviceName })
    if (response.data.status === 'success') {
      device.value = response.data.device
    } else {
      alert(response.data.message)
    }
  } catch (error) {
    alert('获取设备信息失败')
  }
}

const togglePower = async () => {
  try {
    const newStatus = device.value.status === '1' ? '0' : '1'
    const response = await axios.post(`${API_BASE_URL}/home/devices/airConditioner/`, {
      username: localStorage.getItem('username'),
      device_name: device.value.name,
      new_status: newStatus
    })
    if (response.data.status === 'success') {
      device.value.status = newStatus
    } else {
      alert(response.data.message)
    }
  } catch (error) {
    alert('切换状态失败')
  }
}

const changeTemperature = async (newTemp) => {
  if (newTemp < 16 || newTemp > 30) return alert('温度必须在 16-30℃')
  try {
    const response = await axios.post(`${API_BASE_URL}/home/devices/airConditioner/`, {
      username: localStorage.getItem('username'),
      device_name: device.value.name,
      new_temperature: newTemp
    })
    if (response.data.status === 'success') {
      device.value.temperature = newTemp
    } else {
      alert(response.data.message)
    }
  } catch (error) {
    alert('调整温度失败')
  }
}

const changeMode = async (mode) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/home/devices/airConditioner/`, {
      username: localStorage.getItem('username'),
      device_name: device.value.name,
      new_mode: mode })
    if (response.data.status === 'success') {
      device.value.mode = mode
    } else {
      alert(response.data.message)
    }
  } catch (error) {
    alert('切换模式失败')
  }
}

const renameDevice = async () => {
  const newName = prompt('请输入新的设备名称', device.value.name)
  if (!newName) return
  try {
    const response = await axios.post(`${API_BASE_URL}/home/devices/airConditioner/`, {
      username: localStorage.getItem('username'),
      device_name: device.value.name,
      new_name: newName
    })
    if (response.data.status === 'success') {
      device.value.name = newName
      alert('重命名成功')
    } else {
      alert(response.data.message)
    }
  } catch (error) {
    alert('重命名失败')
  }
}

onMounted(() => {
  fetchDeviceInfo()
})
</script>

<style scoped>
@keyframes wind {
  0% { transform: translateY(0); opacity: 1; }
  50% { transform: translateY(20px); opacity: 0.5; }
  100% { transform: translateY(0); opacity: 1; }
}

.animate-wind {
  animation: wind 1s infinite;
}

.delay-200 {
  animation-delay: 0.2s;
}

.delay-400 {
  animation-delay: 0.4s;
}
</style>
