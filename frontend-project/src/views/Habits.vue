<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-6">
    <div class="bg-white rounded-2xl shadow-lg p-8 w-full max-w-3xl">
      <h1 class="text-3xl font-bold text-center mb-6">全部习惯列表</h1>

      <form @submit.prevent="applyHabits" class="space-y-4">
        <ul class="space-y-3">
          <li
            v-for="(habit, index) in habits"
            :key="index"
            class="flex items-center space-x-4"
          >
            <input
              type="checkbox"
              :value="habit.habitname"
              v-model="selectedHabits"
              class="w-5 h-5 text-blue-500 rounded focus:ring-blue-400"
            />
            <div class="text-lg">
              <p><strong>习惯名称：</strong>{{ habit.habitname }}</p>
              <p><strong>设备名称：</strong>{{ habit.devicename }}</p>
              <p><strong>设备类型：</strong>{{ habit.devicetype }}</p>
              <p><strong>所属用户：</strong>{{ habit.username }}</p>
            </div>
          </li>
        </ul>

        <div class="flex justify-around mt-6">
          <button
            type="submit"
            class="px-6 py-3 bg-green-500 text-white rounded-full shadow-md hover:bg-green-600 transition"
          >
            应用习惯
          </button>
          <button
            type="button"
            @click="deleteHabits"
            class="px-6 py-3 bg-red-500 text-white rounded-full shadow-md hover:bg-red-600 transition"
          >
            删除习惯
          </button>
          <button
            type="button"
            @click="showAddHabit = true"
            class="px-6 py-3 bg-blue-500 text-white rounded-full shadow-md hover:bg-blue-600 transition"
          >
            新增习惯
          </button>
        </div>
      </form>
    </div>

    <!-- 新增习惯弹窗 -->
    <div
      v-if="showAddHabit"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
    >
      <div class="bg-white rounded-2xl p-6 w-full max-w-lg space-y-4">
        <h2 class="text-2xl font-bold mb-4 text-center">新增习惯</h2>

        <!-- 设备选择 -->
        <select v-model="selectedDevice" @change="handleDeviceChange" class="w-full p-2 border rounded">
          <option disabled value="">请选择设备</option>
          <option
            v-for="device in allDevices"
            :key="device.id"
            :value="device"
          >
            {{ device.name }}（{{ device.type_name }}）
          </option>
        </select>

        <input v-model="newHabit.habitname" type="text" placeholder="习惯名称" class="w-full p-2 border rounded" />
        <input v-model="newHabit.brightness" type="number" placeholder="灯光亮度（可选）" class="w-full p-2 border rounded" />
        <input v-model="newHabit.temperature" type="number" placeholder="空调温度（可选）" class="w-full p-2 border rounded" />

        <!-- 模式选择（根据设备类型） -->
        <div v-if="availableModes.length > 0">
          <select v-model="newHabit.mode" class="w-full p-2 border rounded">
            <option disabled value="">请选择模式</option>
            <option v-for="mode in availableModes" :key="mode" :value="mode">{{ mode }}</option>
          </select>
        </div>

        <div class="flex justify-around mt-4">
          <button @click="addHabit" class="px-4 py-2 bg-green-500 text-white rounded-full hover:bg-green-600">添加</button>
          <button @click="showAddHabit = false" class="px-4 py-2 bg-gray-500 text-white rounded-full hover:bg-gray-600">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { API_BASE_URL } from '../main'

const habits = ref([])
const selectedHabits = ref([])
const allDevices = ref([])

const showAddHabit = ref(false)
const selectedDevice = ref('')
const newHabit = ref({
  devicename: '',
  devicetype: '',
  habitname: '',
  brightness: null,
  temperature: null,
  mode: ''
})

const deviceModes = {
  AirConditioner: ['cool', 'heat', 'auto', 'dry', 'fan'],
  Washer: ['standard', 'quick', 'delicate', 'heavy', 'wool'],
  Sweeper: ['auto', 'spot', 'edge', 'single_room', 'mop']
}

const availableModes = ref([])

const fetchHabits = async () => {
  try {
    const response = await axios.post(`${API_BASE_URL}/home/habits/`, {
      username: localStorage.getItem('username')
    })
    habits.value = response.data.result
  } catch (error) {
    console.error('获取习惯失败', error)
    alert('获取习惯失败')
  }
}

const fetchDevices = async () => {
  try {
    const response = await axios.post(`${API_BASE_URL}home/devices/`, { username: localStorage.getItem('username') })
    if (response.status === 200) {
      const deviceCategories = response.data.device_categories
      // 展平成一个设备列表，带上 type 和 type_name
      allDevices.value = deviceCategories.flatMap(category =>
        category.devices.map(device => ({
          ...device,
          type: category.type,
          type_name: category.type_name
        }))
      )
    }
  } catch (error) {
    console.error('获取设备失败', error)
    alert('获取设备失败')
  }
}

const handleDeviceChange = () => {
  if (selectedDevice.value) {
    newHabit.value.devicename = selectedDevice.value.name
    newHabit.value.devicetype = selectedDevice.value.type
    // 联动模式
    availableModes.value = deviceModes[selectedDevice.value.type] || []
  }
}

const applyHabits = async () => {
  if (selectedHabits.value.length === 0) {
    alert('请先选择要应用的习惯')
    return
  }

  try {
    const response = await axios.post(`${API_BASE_URL}/home/habits/exec_habit/`, {
      username: localStorage.getItem('username'),
      habitname: selectedHabits.value
    })

    if (response.status === 200) {
      alert('习惯已成功应用')
      selectedHabits.value = []
    } else {
      alert('应用习惯失败')
    }
  } catch (error) {
    console.error('应用习惯失败', error)
    alert('应用习惯失败')
  }
}

const deleteHabits = async () => {
  if (selectedHabits.value.length === 0) {
    alert('请先选择要删除的习惯')
    return
  }

  try {
    const username = localStorage.getItem('username')

    // 遍历每个选中的习惯，依次请求删除
    for (const habitName of selectedHabits.value) {
      // 查找当前习惯对应的 devicename
      const habit = habits.value.find(h => h.habitname === habitName)
      if (!habit) continue // 如果找不到习惯，跳过
      console.log(habit)
      await axios.post(`${API_BASE_URL}/home/habits/delete_habit/`, {
        username: localStorage.getItem('username'),
        habitname: habit.habitname
      })
    }

    alert('习惯已成功删除')

    // 更新本地列表
    habits.value = habits.value.filter(
      habit => !selectedHabits.value.includes(habit.habitname)
    )
    selectedHabits.value = []

  } catch (error) {
    console.error('删除习惯失败', error)
    alert('删除习惯失败')
  }
}

const addHabit = async () => {
  if (!newHabit.value.devicename || !newHabit.value.devicetype) {
    alert('请先选择设备')
    return
  }

  try {
    console.log(newHabit.value.devicename, newHabit.value.devicetype, newHabit.value.habitname)
    const response = await axios.post(`${API_BASE_URL}/home/habits/add_habit/`, {
      username: localStorage.getItem('username'),
      devicename: newHabit.value.devicename,
      devicetype: newHabit.value.devicetype,
      habitname: newHabit.value.habitname,
      brightness: newHabit.value.brightness,
      temperature: newHabit.value.temperature,
      mode: newHabit.value.mode
    })

    if (response.status === 200) {
      alert('习惯添加成功')
      showAddHabit.value = false
      fetchHabits()
      newHabit.value = { devicename: '', devicetype: '', habitname: '', brightness: null, temperature: null, mode: '' }
      selectedDevice.value = ''
      availableModes.value = []
    } else {
      alert('习惯添加失败')
    }
  } catch (error) {
    console.error('添加习惯失败', error)
    alert('添加习惯失败')
  }
}

onMounted(() => {
  fetchHabits()
  fetchDevices()
})
</script>

<style scoped>
/* 样式已由 Tailwind 完整处理，无需额外 CSS */
</style>
