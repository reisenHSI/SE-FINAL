<template>
  <header class="header">
    <div class="left">
      <h1 class="title">智能家居系统</h1>
    </div>
    <div class="right">
      <span class="username">欢迎，{{ username }}</span>
      <button @click="goToLogs">日志查询</button>
      <button @click="goToHabits">个人习惯</button>
      <button @click="triggerOneKeyOpen">一键开启</button>
      <button class="logout-btn" @click="logout">退出登录</button>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header',
  data() {
    return {
      username: localStorage.getItem('username')
    }
  },
  methods: {
    logout() {
      // 清除 token 等登录信息
      localStorage.removeItem('token')
      this.$router.push('/login')
    },
    goHome() {
      this.$router.push('/home')
    },
    goToLogs() {
      this.$router.push('/logs')
    },
    goToHabits() {
      this.$router.push('/habits')
    },
    triggerOneKeyOpen() {
      // 你可以用 emit 或 Vuex 通知主组件执行操作
      this.$emit('one-key-open')
      alert('已发送一键开启指令')
    }
  }
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(to right, #4facfe, #00f2fe);
  padding: 16px 32px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-bottom-left-radius: 16px;
  border-bottom-right-radius: 16px;
}

.title {
  font-size: 28px;
  color: white;
  font-weight: bold;
  margin: 0;
}

.right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.username {
  margin-right: 16px;
  font-weight: bold;
  color: white;
  font-size: 16px;
}

button {
  padding: 10px 18px;
  border: none;
  border-radius: 12px;
  background: white;
  color: #2563eb;
  font-weight: bold;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

button:hover {
  background: #2563eb;
  color: white;
}

.logout-btn {
  background: linear-gradient(135deg, #ff6a6a, #ff4e50);
  color: white;
}

.logout-btn:hover {
  background: linear-gradient(135deg, #d84343, #c62828);
}
</style>
