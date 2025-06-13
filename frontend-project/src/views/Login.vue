<template>
  <div class="container">
    <div class="login-card">
      <h2 class="title">欢迎登录</h2>

      <form @submit.prevent="login" class="space-y-6">
        <div class="form-group">
          <label for="username">用户名</label>
          <input v-model="username" type="text" id="username" required />
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <input v-model="password" type="password" id="password" required />
        </div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <button type="submit" class="login-button" :disabled="isSubmitting">
          {{ isSubmitting ? '登录中...' : '登录' }}
        </button>
      </form>

      <div class="options">
        <span class="option-link" @click="goToReset">点击修改密码</span>
      </div>

      <div class="register-hint">
        还没有账号？
        <span class="register-link" @click="goToRegister">立即注册</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { API_BASE_URL } from "../main";

export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
      isSubmitting: false,
      errorMessage: "",
    };
  },
  methods: {
    async login() {
      this.isSubmitting = true;
      this.errorMessage = "";

      try {
        const response = await axios.post(
          `${API_BASE_URL}login/`,
          { username: this.username, password: this.password },
          { withCredentials: true }
        );

        if (response.data.status === "success") {
          localStorage.setItem("token", "true");
          localStorage.setItem("username", this.username);
          this.$router.push("/home");
        } else {
          this.errorMessage = response.data.message;
        }
      } catch (error) {
        console.error("登录失败:", error);
        this.errorMessage = error.response?.data?.message || "未知错误";
      } finally {
        this.isSubmitting = false;
      }
    },
    goToRegister() {
      this.$router.push("/register");
    },
    goToReset() {
      this.$router.push('changePassword');
    },
  },
  mounted() {
    console.log("Login 页面已加载");
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100vw;           /* 保证横向全屏 */
  height: 100vh;          /* 保证纵向全屏 */
  background: linear-gradient(to right, #e0f2ff, #f1f5ff);
}

.login-card {
  background-color: #ffffff;
  padding: 40px;
  border-radius: 24px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.login-card:hover {
  transform: scale(1.02);
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.15);
}

.title {
  color: #2563eb;
  margin-bottom: 24px;
  font-size: 32px;
  font-weight: bold;
}

.form-group {
  text-align: left;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font-size: 16px;
  box-sizing: border-box;
  transition: border-color 0.2s, box-shadow 0.2s;
}

input:focus {
  border-color: #60a5fa;
  box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.4);
  outline: none;
}

.login-button {
  width: 100%;
  padding: 14px;
  background: linear-gradient(to right, #3b82f6, #2563eb);
  color: white;
  font-size: 18px;
  font-weight: bold;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.1s;
}

.login-button:hover {
  opacity: 0.9;
}

.login-button:active {
  transform: scale(0.98);
}

.options {
  margin-top: 16px;
}

.option-link {
  color: #2563eb;
  cursor: pointer;
  font-size: 14px;
  transition: color 0.2s;
}

.option-link:hover {
  color: #1d4ed8;
}

.register-hint {
  margin-top: 24px;
  font-size: 14px;
  color: #555;
}

.register-link {
  color: #2563eb;
  margin-left: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: color 0.2s;
}

.register-link:hover {
  color: #1d4ed8;
}

.error-message {
  color: #ef4444;
  font-size: 14px;
  margin-bottom: 12px;
}

</style>
