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
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { API_BASE_URL } from '../main'

const habits = ref([])
const selectedHabits = ref([])

// 获取全部习惯列表
const fetchHabits = async () => {
  try {
    console.log(localStorage.getItem('username'))
    const response = await axios.post(`${API_BASE_URL}/home/habits/`, {
      username: localStorage.getItem('username')
    })
    habits.value = response.data.result
  } catch (error) {
    console.error('获取习惯失败', error)
    alert('获取习惯失败')
  }
}

// 应用习惯
const applyHabits = async () => {
  if (selectedHabits.value.length === 0) {
    alert('请先选择要应用的习惯')
    return
  }

  try {
    const response = await axios.post(`${API_BASE_URL}/home/habits/apply/`, {
      habits: selectedHabits.value
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

// 删除习惯
const deleteHabits = async () => {
  if (selectedHabits.value.length === 0) {
    alert('请先选择要删除的习惯')
    return
  }

  try {
    const response = await axios.post(`${API_BASE_URL}/home/habits/delete/`, {
      habits: selectedHabits.value
    })

    if (response.status === 200) {
      alert('习惯已成功删除')
      habits.value = habits.value.filter(
        habit => !selectedHabits.value.includes(habit.habitname)
      )
      selectedHabits.value = []
    } else {
      alert('删除习惯失败')
    }
  } catch (error) {
    console.error('删除习惯失败', error)
    alert('删除习惯失败')
  }
}

// 页面加载时获取所有习惯
onMounted(() => {
  fetchHabits()
})
</script>

<style scoped>
/* 样式已由 Tailwind 完整处理，无需额外 CSS */
</style>
