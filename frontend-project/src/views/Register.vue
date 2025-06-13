<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-blue-100">
    <div class="bg-white p-10 rounded-3xl shadow-2xl w-full max-w-md transition-transform transform hover:scale-[1.01]">
      <h2 class="text-4xl font-bold text-center text-blue-600 mb-8">创建账号</h2>

      <form @submit.prevent="register" class="space-y-6">
        <!-- 用户名 -->
        <div>
          <label class="block text-gray-700 mb-2" for="username">用户名</label>
          <input
            v-model="username"
            id="username"
            type="text"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
          />
        </div>

        <!-- 电话 -->
        <div>
          <label class="block text-gray-700 mb-2" for="phone">电话</label>
          <input
            v-model="phone"
            id="phone"
            type="text"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
          />
        </div>

        <!-- 年龄 -->
        <div>
          <label class="block text-gray-700 mb-2" for="age">年龄</label>
          <input
            v-model="age"
            id="age"
            type="number"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
          />
        </div>

        <!-- 密码 -->
        <div>
          <label class="block text-gray-700 mb-2" for="password">密码</label>
          <input
            v-model="password"
            id="password"
            type="password"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
          />
        </div>

        <!-- 确认密码 -->
        <div>
          <label class="block text-gray-700 mb-2" for="confirmPassword">确认密码</label>
          <input
            v-model="confirmPassword"
            id="confirmPassword"
            type="password"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
          />
        </div>

        <!-- 邀请码 -->
        <div>
          <label class="block text-gray-700 mb-2" for="inviteCode">邀请码 <span class="text-gray-400">(选填)</span></label>
          <input
            v-model="inviteCode"
            id="inviteCode"
            type="text"
            placeholder="可选，输入邀请码"
            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
          />
        </div>

        <!-- 错误提示 -->
        <div v-if="errorMessage" class="text-red-500 text-center text-sm">
          {{ errorMessage }}
        </div>

        <!-- 注册按钮 -->
        <button
          type="submit"
          :disabled="isSubmitting"
          class="w-full py-3 bg-gradient-to-r from-blue-500 to-blue-400 text-white rounded-xl font-semibold text-lg hover:opacity-90 active:scale-95 transition"
        >
          {{ isSubmitting ? '注册中...' : '注册' }}
        </button>

        <!-- 返回按钮 -->
        <button
          type="button"
          @click="goBack"
          class="w-full py-3 mt-4 border border-blue-400 text-blue-600 rounded-xl font-semibold hover:bg-blue-50 active:scale-95 transition"
        >
          返回
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { API_BASE_URL } from "../main";

export default {
  name: 'Register',
  data() {
    return {
      username: '',
      phone: '',
      age: '',
      password: '',
      confirmPassword: '',
      inviteCode: '',
      errorMessage: "",
      isSubmitting: false
    }
  },
  methods: {
    async register() {
      this.isSubmitting = true;
      this.errorMessage = "";

      if (this.password !== this.confirmPassword) {
        this.errorMessage = "两次输入的密码不一致。";
        this.isSubmitting = false;
        return;
      }

      try {
        const response = await axios.post(`${API_BASE_URL}register/`, {
          phone: this.phone,
          username: this.username,
          password: this.password,
          age: this.age,
          registration_code: this.inviteCode
        }, { withCredentials: true });

        if (response.data.status === 'success') {
          this.$router.push("/login");
        } else {
          this.errorMessage = response.data.message;
        }
      } catch (error) {
        console.error("Register error:", error);
        this.errorMessage = error.response?.data?.message || "注册时发生错误，请稍后再试。";
      } finally {
        this.isSubmitting = false;
      }
    },
    goBack() {
      this.$router.go(-1);
    }
  }
}
</script>

<style scoped>
/* Tailwind 已经足够美观，无需额外 CSS */
</style>

