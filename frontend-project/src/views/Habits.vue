<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-6">
    <div class="bg-white rounded-2xl shadow-lg p-8 w-full max-w-xl">
      <h1 class="text-3xl font-bold text-center mb-6">一键开启习惯</h1>

      <form @submit.prevent="applyHabits" class="space-y-4">
        <ul class="space-y-3">
          <li
            v-for="habit in habits"
            :key="habit.habit_id"
            class="flex items-center space-x-4"
          >
            <input
              type="checkbox"
              :value="habit.habit_id"
              v-model="selectedHabits"
              class="w-5 h-5 text-blue-500 rounded focus:ring-blue-400"
            />
            <span class="text-lg">{{ habit.username }} 的习惯</span>
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

// 获取习惯列表
const fetchHabits = async () => {
  try {
    const response = await axios.post(`${API_BASE_URL}/home/habits/`)
    if (response.data.status === 'success') {
      habits.value = response.data.user_habits
    } else {
      alert(response.data.message)
    }
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
    const response = await axios.post(`${API_BASE_URL}/home/habits/`, {
      habit_ids: selectedHabits.value
    })

    if (response.data.status === 'success') {
      alert('习惯已成功应用')
      selectedHabits.value = []
    } else {
      alert(response.data.message)
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
      habit_ids: selectedHabits.value
    })

    if (response.data.status === 'success') {
      alert('习惯已成功删除')
      // 前端同步删除
      habits.value = habits.value.filter(
        habit => !selectedHabits.value.includes(habit.habit_id)
      )
      selectedHabits.value = []
    } else {
      alert(response.data.message)
    }
  } catch (error) {
    console.error('删除习惯失败', error)
    alert('删除习惯失败')
  }
}

onMounted(() => {
  fetchHabits()
})
</script>

<style scoped>
/* 样式已由 Tailwind 完整处理，无需额外 CSS */
</style>
