<template>
  <div class="container">
    <div class="register-card">
      <h2 class="title">注册账号</h2>
      <form @submit.prevent="register">
        <div class="form-group">
          <label for="username">用户名</label>
          <input v-model="username" type="text" id="username" required />
        </div>
        <div class="form-group">
          <label for="password">电话</label>
          <input v-model="phone" type="text" id="phone" required />
        </div>
        <div class="form-group">
          <label for="password">年龄</label>
          <input v-model="age" type="number" id="age" required />
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input v-model="password" type="password" id="password" required />
        </div>
        <div class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input v-model="confirmPassword" type="password" id="confirmPassword" required />
        </div>

        <button type="submit" class="register-button">注册</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import {API_BASE_URL} from "../main";

export default {
  name: 'Register',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      errorMessage: "",
      phone: "",
      age: 0,
      isSubmitting: false
    }
  },
  methods: {
    async register() {
      this.isSubmitting = true;
      this.errorMessage = "";

      try {
        const response = await axios.post(`${API_BASE_URL}register/`, {
          phone: this.phone,
          username: this.username,
          password: this.password,
          age: this.age,
        });

        // 处理返回的信息
        if (response.data.status === 'success') {
          this.$router.push("/login");  // 跳转到登陆界面
        } else {
          this.errorMessage = response.data.message;
        }
      } catch (error) {
        console.error("Register error:", error);
        this.errorMessage = error.response.data.message || "注册时发生错误，请稍后再试。";
      } finally {
        this.isSubmitting = false;  // 提交完毕
      }
    }
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

.register-card {
  background-color: #ffffff;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 450px;
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

.register-button {
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

.register-button:hover {
  background-color: #1f5eb7;
}
</style>
