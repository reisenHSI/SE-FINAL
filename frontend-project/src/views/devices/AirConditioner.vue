<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-blue-100 to-white p-4">
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
    <div v-else class="text-center mb-6">
      <h1 class="text-3xl font-bold mb-2">{{ device.name }}</h1>
      <p class="text-lg text-gray-700">{{ device.type }}</p>
      <p class="text-lg text-gray-700">当前温度: {{ device.temperature }}°C</p>
      <p class="text-lg text-gray-700">当前模式: {{ device.mode }}</p>
    </div>

    <!-- 空调显示区域 -->
    <div v-if="!loading" class="relative flex items-center justify-center w-full mb-10" style="height: 50vh;">
      <!-- 空调图标 -->
      <div
        :class="[
          'transition-all duration-500 ease-in-out flex flex-col items-center justify-center text-9xl',
          device.status === STATUS_ON ? modeColors[device.mode].icon : 'text-gray-400'
        ]"
      >
        {{ modeIcons[device.mode] }}
        <!-- 吹风动画 -->
        <div v-if="device.status === STATUS_ON" class="mt-4 flex space-x-2">
          <div :class="['w-2 h-10', modeColors[device.mode].wind, 'animate-wind']"></div>
          <div :class="['w-2 h-10', modeColors[device.mode].wind, 'animate-wind delay-200']"></div>
          <div :class="['w-2 h-10', modeColors[device.mode].wind, 'animate-wind delay-400']"></div>
        </div>
      </div>
    </div>

    <!-- 拟真遥控器 -->
    <div v-if="!loading" class="bg-gray-800 rounded-3xl p-6 text-white shadow-lg flex flex-col items-center space-y-4">
      <!-- 开关按钮 -->
      <button
        @click="togglePower"
        class="w-24 h-12 bg-red-500 rounded-full text-lg font-semibold shadow-md active:scale-95 transition transform"
      >
        {{ device.status === STATUS_ON ? '关闭' : '开启' }}
      </button>

      <!-- 温度调节 -->
      <div class="flex items-center space-x-4">
        <button
          @click="changeTemperature(device.temperature - 1)"
          :disabled="device.temperature <= MIN_TEMP"
          class="w-12 h-12 bg-gray-600 rounded-full text-2xl active:scale-95 transition transform disabled:opacity-50 disabled:cursor-not-allowed"
        >-</button>
        <span class="text-2xl">{{ device.temperature }}°C</span>
        <button
          @click="changeTemperature(device.temperature + 1)"
          :disabled="device.temperature >= MAX_TEMP"
          class="w-12 h-12 bg-gray-600 rounded-full text-2xl active:scale-95 transition transform disabled:opacity-50 disabled:cursor-not-allowed"
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

      <!-- 重命名输入框（按钮在输入框内部） -->
      <div class="w-full flex flex-col items-center mt-4">
        <label class="text-lg font-semibold mb-2">重命名设备</label>
        <div class="relative w-full max-w-md">
          <input
            type="text"
            v-model="newDeviceName"
            placeholder="输入新设备名称"
            class="w-full p-2 pr-16 rounded-lg border border-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            class="absolute right-2 top-1/2 transform -translate-y-1/2 px-3 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600 transition"
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
import { useRoute, useRouter } from 'vue-router'
import { API_BASE_URL } from '../../main'

const route = useRoute()
const router = useRouter()

const deviceName = route.query.name || '默认空调设备'

const STATUS_ON = '1'
const STATUS_OFF = '0'
const MIN_TEMP = 16
const MAX_TEMP = 30

const loading = ref(true)

const device = ref({
  id: null,
  name: '',
  type: '',
  status: STATUS_OFF,
  temperature: 24,
  mode: 'cool',
  valid_modes: [],
  controls: {}
})

const newDeviceName = ref('')

const modeLabels = {
  cool: '制冷',
  heat: '制热',
  auto: '自动',
  dry: '除湿',
  fan: '送风'
}

const modeIcons = {
  cool: '❄️',
  heat: '🔥',
  dry: '💧',
  auto: '🌈',
  fan: '🌀'
}

const modeColors = {
  cool: { icon: 'text-blue-400', wind: 'bg-blue-300' },
  heat: { icon: 'text-red-400', wind: 'bg-red-300' },
  dry: { icon: 'text-teal-400', wind: 'bg-teal-300' },
  auto: { icon: 'text-purple-400', wind: 'bg-purple-300' },
  fan: { icon: 'text-yellow-400', wind: 'bg-yellow-300' }
}

const fetchDeviceInfo = async () => {
  try {
    const response = await axios.post(`${API_BASE_URL}/home/devices/airConditioner/`, {
      username: localStorage.getItem('username'),
      device_name: deviceName
    })
    if (response.data.status === 'success') {
      const fetchedDevice = response.data.device
      // 强制转换类型，确保 status 是字符串
      fetchedDevice.status = String(fetchedDevice.status)
      device.value = fetchedDevice
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

const togglePower = async () => {
  try {
    const newStatus = device.value.status === STATUS_ON ? STATUS_OFF : STATUS_ON
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
    console.error(error)
    alert('切换状态失败')
  }
}

const changeTemperature = async (newTemp) => {
  if (newTemp < MIN_TEMP || newTemp > MAX_TEMP) {
    alert(`温度必须在 ${MIN_TEMP}-${MAX_TEMP}℃`)
    return
  }
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
    console.error(error)
    alert('调整温度失败')
  }
}

const changeMode = async (mode) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/home/devices/airConditioner/`, {
      username: localStorage.getItem('username'),
      device_name: device.value.name,
      new_mode: mode
    })
    if (response.data.status === 'success') {
      device.value.mode = mode
    } else {
      alert(response.data.message)
    }
  } catch (error) {
    console.error(error)
    alert('切换模式失败')
  }
}

const renameDevice = async () => {
  if (!newDeviceName.value.trim()) {
    alert('设备名称不能为空')
    return
  }
  try {
    const response = await axios.post(`${API_BASE_URL}/home/devices/airConditioner/`, {
      username: localStorage.getItem('username'),
      device_name: device.value.name,
      new_name: newDeviceName.value
    })
    if (response.data.status === 'success') {
      device.value.name = newDeviceName.value
      router.replace({ query: { name: newDeviceName.value } })
      alert('重命名成功')
      newDeviceName.value = ''
    } else {
      alert(response.data.message)
    }
  } catch (error) {
    console.error(error)
    alert('重命名失败')
  }
}

const goBack = () => {
  router.push({ name: 'Home' })
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
