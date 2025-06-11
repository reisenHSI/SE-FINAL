<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-200 p-4">
    <!-- 设备信息 -->
    <div class="text-center mb-6">
      <h1 class="text-3xl font-bold mb-2">{{ device.name }}</h1>
      <p class="text-lg text-gray-700">{{ device.type }}</p>
      <p class="text-lg text-gray-700">当前亮度: {{ device.brightness }}%</p>
    </div>

    <!-- 灯泡 -->
    <div class="flex items-center justify-center w-full mb-10" style="height: 50vh;">
      <div
        :class="[
          'transition-all duration-500 ease-in-out rounded-full shadow-lg flex items-center justify-center',
          device.status === '1' ? 'bg-yellow-400' : 'bg-gray-400'
        ]"
        style="width: 50%; height: 100%;"
      >
        <!-- 灯泡图标 -->
        <div
          :class="[
            'text-[10rem] transition-transform duration-500',
            device.status === '1' ? 'scale-110 brightness-125' : 'scale-90 brightness-75'
          ]"
        >
          💡
        </div>
      </div>
    </div>

    <!-- 控制按钮 -->
    <div class="flex flex-col items-center space-y-6">
      <!-- 拨动开关按钮 -->
      <div class="flex items-center space-x-4">
        <span class="text-xl font-semibold">{{ device.status === '1' ? '开' : '关' }}</span>
        <div
          class="w-16 h-8 flex items-center bg-gray-300 rounded-full p-1 cursor-pointer transition-colors duration-300"
          :class="device.status === '1' ? 'bg-green-400' : 'bg-gray-400'"
          @click="toggleLight"
        >
          <div
            class="bg-white w-6 h-6 rounded-full shadow-md transform transition-transform duration-300"
            :class="device.status === '1' ? 'translate-x-8' : 'translate-x-0'"
          ></div>
        </div>
      </div>

      <!-- 调整亮度按钮 -->
      <button
        class="px-6 py-3 bg-blue-500 text-white rounded-full text-lg hover:bg-blue-600 transition"
        @click="changeBrightness"
      >
        调整亮度
      </button>

      <!-- 重命名按钮 -->
      <button
        class="px-6 py-3 bg-yellow-500 text-white rounded-full text-lg hover:bg-yellow-600 transition"
        @click="renameDevice"
      >
        重命名设备
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const route = useRoute()
const deviceName = route.query.device_name || '默认设备名'

const device = ref({
  id: null,
  name: '',
  type: '',
  status: '0',
  brightness: 0,
})

// 获取设备信息
const fetchDeviceInfo = async () => {
  try {
    const response = await axios.get('/light/', { params: { device_name: deviceName } })
    if (response.data.status === 'success') {
      device.value = response.data.device
    } else {
      alert(response.data.message)
    }
  } catch (error) {
    alert('获取设备信息失败')
  }
}

// 切换灯泡状态
const toggleLight = async () => {
  try {
    const newStatus = device.value.status === '1' ? '0' : '1'
    const response = await axios.post('/light/', { device_name: device.value.name, new_status: newStatus })
    if (response.data.status === 'success') {
      device.value.status = newStatus
    } else {
      alert(response.data.message)
    }
  } catch (error) {
    alert('切换状态失败')
  }
}

// 调整亮度
const changeBrightness = async () => {
  const newBrightness = prompt('请输入新的亮度（0-100）', device.value.brightness)
  if (newBrightness === null) return
  const brightnessValue = parseInt(newBrightness)

  if (isNaN(brightnessValue) || brightnessValue < 0 || brightnessValue > 100) {
    alert('亮度必须是 0 到 100 的整数')
    return
  }

  try {
    const response = await axios.post('/light/', { device_name: device.value.name, new_brightness: brightnessValue })
    if (response.data.status === 'success') {
      device.value.brightness = brightnessValue
    } else {
      alert(response.data.message)
    }
  } catch (error) {
    alert('调整亮度失败')
  }
}

// 重命名设备
const renameDevice = async () => {
  const newName = prompt('请输入新的设备名称', device.value.name)
  if (!newName) return

  try {
    const response = await axios.post('/light/', { device_name: device.value.name, new_name: newName })
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
/* 可以添加额外细节样式，这里主要用的是 Tailwind 动画 */
</style>
