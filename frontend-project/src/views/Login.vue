<template>
  <div class="container">
    <div class="login-card">
      <h2 class="title">登录</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="username">用户名</label>
          <input v-model="username" type="text" id="username" required />
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input v-model="password" type="password" id="password" required />
        </div>
        <button type="submit" class="login-button">登录</button>
      </form>

      <div class="register-hint">
        还未有账号？
        <span class="register-link" @click="goToRegister">注册</span>
      </div>
    </div>
  </div>
</template>

<script>

import axios from "axios";
import {API_BASE_URL} from "../main";

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      isSubmitting: false,
      errorMessage: '',
    }
  },
  methods: {
    async login() {
      this.isSubmitting = true;
      this.errorMessage = '';

      try {
        const response = await axios.post(`${API_BASE_URL}login/`, {
          username: this.username,
          password: this.password
        },{withCredentials:true,});

        // 处理请求返回的信息
        if (response.data.status === 'success') {
          localStorage.setItem('token', 'true');
          localStorage.setItem('username', this.username)
          this.$router.push('/home');  // 跳转到home界面
        } else {
          this.errorMessage = response.data.message;
        }
      } catch (error) {
        console.error('登录失败:', error);
        this.errorMessage = error.response.data.message || '未知错误';
      } finally {
        this.isSubmitting = false;
      }
    },

    goToRegister() {
      this.$router.push('/register');
    }
  },
  mounted() {
    console.log('Login 页面已加载')
  }
}
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #e6f0fa;
}

.login-card {
  background-color: #ffffff;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.title {
  text-align: center;
  color: #2a6ecf;
  margin-bottom: 24px;
  font-size: 24px;
  font-weight: bold;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 16px;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

input:focus {
  border-color: #5aa0ff;
  outline: none;
}

.login-button {
  width: 100%;
  padding: 12px;
  background-color: #2a6ecf;
  color: white;
  font-size: 16px;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-button:hover {
  background-color: #1f5eb7;
}
</style>