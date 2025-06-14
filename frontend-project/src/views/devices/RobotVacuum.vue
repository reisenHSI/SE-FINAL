<template>
  <div class="flex flex-col items-center justify-center h-screen bg-gray-100" v-if="isLoaded">
    <!-- 返回按钮 -->
    <div class="w-full max-w-md px-4 py-2 flex justify-start">
      <button
        @click="goBack"
        class="px-4 py-2 bg-gray-300 hover:bg-gray-400 rounded-lg shadow-sm"
      >
        返回
      </button>
    </div>
    <!-- 设备信息 -->
    <div class="text-center mb-6">
      <h1 class="text-3xl font-bold mb-2">{{ device.name }}</h1>
      <p class="text-lg">当前模式: {{ device.mode }}</p>
      <p class="text-lg" v-if="device.electricity !== null">电量: {{ device.electricity }}%</p>
      <p class="text-lg" v-if="device.sweeparea !== null">已清扫面积: {{ device.sweeparea }} ㎡</p>
    </div>

    <!-- 扫地机器人动画 -->
    <div class="relative w-40 h-40 border-8 border-gray-500 rounded-full flex items-center justify-center bg-white shadow-lg overflow-hidden">
      <div
        class="w-32 h-32 rounded-full border-4 border-green-400"
        :class="{ 'animate-spin': isRunning, 'animate-none': !isRunning }"
      ></div>
    </div>

    <!-- 控制按钮 -->
    <div class="mt-8 flex flex-wrap justify-center gap-4">
      <button
        @click="toggleRobot"
        class="px-6 py-3 bg-blue-500 text-white rounded-full shadow-lg transform transition active:scale-95"
      >
        {{ isRunning ? '停止清扫' : '启动清扫' }}
      </button>

      <select
        v-model="selectedMode"
        @change="changeMode"
        class="px-4 py-2 border rounded-lg"
      >
        <option v-for="mode in device.valid_modes" :key="mode" :value="mode">{{ mode }}</option>
      </select>

      <!-- 重命名输入框（包裹在边框内） -->
      <div class="w-full flex flex-col items-center mt-4">
        <label class="text-lg font-semibold mb-2">重命名设备</label>
        <div class="flex w-full max-w-md border border-gray-400 rounded-lg overflow-hidden">
          <input
            type="text"
            v-model="newDeviceName"
            placeholder="输入新设备名称"
            class="flex-1 p-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            class="px-4 bg-yellow-500 text-white hover:bg-yellow-600 transition"
            @click="renameDevice"
          >
            确认
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- 加载中状态 -->
  <div v-else class="flex items-center justify-center h-screen bg-gray-100">
    <p class="text-lg text-gray-500">加载中...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { API_BASE_URL } from "../../main";

const route = useRoute()
const router = useRouter()

const deviceName = route.query.name

const device = ref({})
const isRunning = ref(false)
const selectedMode = ref('')
const newDeviceName = ref('')
const isLoaded = ref(false)

const fetchRobotVacuum = async () => {
  try {
    const response = await axios.post(`${API_BASE_URL}/home/devices/robotvacuum/`, {
      username: localStorage.getItem('username'),
      device_name: deviceName
    })
    if (response.data.status === 'success') {
      console.log(response.data)
      device.value = response.data.device
      console.log(device.value)
      isRunning.value = response.data.device.status === 1
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

const toggleRobot = async () => {
  try {
    const newStatus = isRunning.value ? '0' : '1'
    const response = await axios.post(`${API_BASE_URL}/home/devices/robotvacuum/`, {
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
    const response = await axios.post(`${API_BASE_URL}/home/devices/robotvacuum/`, {
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
  if (newDeviceName.value && newDeviceName.value.trim() !== '') {
    try {
      const response = await axios.post(`${API_BASE_URL}/home/devices/robotvacuum/`, {
        username: localStorage.getItem('username'),
        device_name: deviceName,
        new_name: newDeviceName.value
      })

      if (response.data.status === 'success') {
        device.value.name = newDeviceName.value
        newDeviceName.value = ''
      } else {
        alert(response.data.message)
      }
    } catch (error) {
      console.error(error)
      alert('重命名失败')
    }
  } else {
    alert('设备名称不能为空')
  }
}

// 这里改成组合式 API 的写法，不用 this
const goBack = () => {
  router.push({ name: 'Home' });
}

onMounted(() => {
  fetchRobotVacuum()
})
</script>
