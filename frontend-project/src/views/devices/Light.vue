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

    <!-- 控制区域 -->
    <div class="flex flex-col items-center space-y-8 w-full max-w-md">
      <!-- 拨动开关 -->
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

      <!-- 亮度滑块 -->
      <div class="w-full flex flex-col items-center">
        <label class="text-lg font-semibold mb-2">调整亮度</label>
        <input
          type="range"
          min="0"
          max="100"
          v-model="sliderBrightness"
          @change="changeBrightness"
          class="w-full accent-blue-500 cursor-pointer"
        />
        <span class="mt-2 text-gray-700">{{ sliderBrightness }}%</span>
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
import { API_BASE_URL } from "../../main";
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const route = useRoute()
const deviceName = route.query.name || '默认设备名'

const device = ref({
  id: null,
  name: '',
  type: '',
  status: '0',
  brightness: 0,
})

const sliderBrightness = ref(0)
const newDeviceName = ref('')

// 获取设备信息
const fetchDeviceInfo = async () => {
  try {
    const response = await axios.post(`${API_BASE_URL}/home/devices/light/`, { device_name: deviceName })
    if (response.data.status === 'success') {
      device.value = response.data.device
      sliderBrightness.value = device.value.brightness
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
    const response = await axios.post(`${API_BASE_URL}/home/devices/light/`, {
      device_name: deviceName,
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

// 调整亮度
const changeBrightness = async () => {
  try {
    const response = await axios.post(`${API_BASE_URL}/home/devices/light/`, {
      device_name: deviceName,
      new_brightness: sliderBrightness.value
    })
    if (response.data.status === 'success') {
      device.value.brightness = sliderBrightness.value
    } else {
      alert(response.data.message)
    }
  } catch (error) {
    alert('调整亮度失败')
  }
}

// 重命名设备
const renameDevice = async () => {
  if (!newDeviceName.value.trim()) {
    alert('设备名称不能为空')
    return
  }

  try {
    const response = await axios.post(`${API_BASE_URL}/home/devices/light/`, {
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

onMounted(() => {
  fetchDeviceInfo()
})
</script>

<style scoped>
/* 美化滑块兼容所有浏览器 */
input[type="range"] {
  -webkit-appearance: none; /* Chrome */
  appearance: none;
  height: 6px;
  background: #d1d5db; /* gray-300 */
  border-radius: 3px;
  outline: none;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  background: #3b82f6; /* blue-500 */
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.5);
  transition: background 0.3s;
}

input[type="range"]::-webkit-slider-thumb:hover {
  background: #2563eb; /* blue-600 */
}

input[type="range"]::-moz-range-thumb {
  width: 20px;
  height: 20px;
  background: #3b82f6; /* blue-500 */
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.5);
  transition: background 0.3s;
}

input[type="range"]::-moz-range-thumb:hover {
  background: #2563eb; /* blue-600 */
}

/* 输入框聚焦高亮 */
input[type="text"]:focus {
  border-color: #3b82f6; /* blue-500 */
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.4); /* blue-500 shadow */
  outline: none;
}

</style>
