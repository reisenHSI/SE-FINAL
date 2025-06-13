<template>
  <div class="container">
    <div class="change-password-card">
      <h2 class="title">修改密码</h2>

      <form @submit.prevent="changePassword" class="space-y-6">
        <div class="form-group">
          <label for="username">用户名</label>
          <input v-model="username" type="text" id="username" required />
        </div>

        <div class="form-group">
          <label for="old_password">当前密码</label>
          <input v-model="oldPassword" type="password" id="old_password" required />
        </div>

        <div class="form-group">
          <label for="new_password">新密码</label>
          <input v-model="newPassword" type="password" id="new_password" required />
        </div>

        <div class="form-group">
          <label for="confirm_new_password">确认新密码</label>
          <input v-model="confirmNewPassword" type="password" id="confirm_new_password" required />
        </div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <button type="submit" class="change-button" :disabled="isSubmitting">
          {{ isSubmitting ? '提交中...' : '确认修改' }}
        </button>
      </form>

      <div class="back-link" @click="goBack">返回登录</div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { API_BASE_URL } from "../main";

export default {
  name: "ChangePassword",
  data() {
    return {
      username: "",
      oldPassword: "",
      newPassword: "",
      confirmNewPassword: "",
      isSubmitting: false,
      errorMessage: "",
    };
  },
  methods: {
    async changePassword() {
      this.errorMessage = "";

      if (this.newPassword !== this.confirmNewPassword) {
        this.errorMessage = "新密码和确认密码不一致";
        return;
      }

      this.isSubmitting = true;

      try {
        const response = await axios.post(`${API_BASE_URL}change_password`, {
          username: this.username,
          old_password: this.oldPassword,
          new_password: this.newPassword,
          confirm_new_password: this.confirmNewPassword
        }, { withCredentials: true });

        if (response.data.status === "success") {
          alert(response.data.message);
          this.$router.push("/login");
        } else {
          this.errorMessage = response.data.message || "密码修改失败";
        }
      } catch (error) {
        console.error("修改密码失败:", error);
        this.errorMessage = error.response?.data?.message || "请求失败，请稍后再试";
      } finally {
        this.isSubmitting = false;
      }
    },
    goBack() {
      this.$router.push("/login");
    },
  },
  mounted() {
    console.log("ChangePassword 页面已加载");
  }
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100vw;
  height: 100vh;
  background: linear-gradient(to right, #e0f2ff, #f1f5ff);
}

.change-password-card {
  background-color: #ffffff;
  padding: 40px;
  border-radius: 24px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.change-password-card:hover {
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
  margin-bottom: 16px;
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

.change-button {
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

.change-button:hover {
  opacity: 0.9;
}

.change-button:active {
  transform: scale(0.98);
}

.error-message {
  color: #ef4444;
  font-size: 14px;
  margin-bottom: 12px;
}

.back-link {
  margin-top: 24px;
  font-size: 14px;
  color: #2563eb;
  cursor: pointer;
  font-weight: bold;
  transition: color 0.2s;
}

.back-link:hover {
  color: #1d4ed8;
}
</style>
