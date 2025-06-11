<template>
  <div class="flex flex-col items-center justify-center h-screen bg-blue-100">
    <!-- 设备信息 -->
    <div class="text-center mb-6">
      <h1 class="text-3xl font-bold mb-2">{{ device.name }}</h1>
      <p class="text-lg">设备类型: {{ device.type }}</p>
    </div>

    <!-- 窗帘动画 -->
    <div class="relative w-3/4 h-1/2 overflow-hidden border-4 border-blue-400 rounded-xl bg-white shadow-lg">
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
    <button
      @click="toggleCurtain"
      class="mt-8 px-6 py-3 bg-blue-500 text-white rounded-full shadow-lg transform transition active:scale-95"
    >
      {{ isOpen ? '关闭窗帘' : '打开窗帘' }}
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const route = useRoute()
const deviceName = route.query.device_name

const device = ref({})
const isOpen = ref(false)

const fetchCurtain = async () => {
  try {
    const response = await axios.get('/curtain/', { params: { device_name: deviceName } })
    if (response.data.status === 'success') {
      device.value = response.data.device
      isOpen.value = response.data.device.status === '1'
    } else {
      alert(response.data.message)
    }
  } catch (error) {
    console.error(error)
    alert('获取设备信息失败')
  }
}

const toggleCurtain = async () => {
  try {
    const newStatus = isOpen.value ? '0' : '1'
    const response = await axios.post('/curtain/', { device_name: deviceName, new_status: newStatus })

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

onMounted(() => {
  fetchCurtain()
})
</script>

<style scoped>
/* 动态窗帘效果已经由 tailwind transition 配合 width 实现，无需额外 CSS */
</style>
