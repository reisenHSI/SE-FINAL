<template>
  <header class="header">
    <div class="left">
      <h1 class="title">智能家居系统</h1>
    </div>
    <div class="right">
      <span class="username">欢迎，{{ username }}</span>
      <button @click="goHome">主页</button>
      <button @click="goToLogs">日志查询</button>
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
  background-color: #e6f1ff;
  padding: 12px 24px;
  border-bottom: 1px solid #bcd3ef;
}

.title {
  font-size: 22px;
  color: #2a6ecf;
  margin: 0;
}

.right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.username {
  margin-right: 10px;
  font-weight: bold;
  color: #333;
}

button {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  background-color: #162f60;
  color: white;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #0d3567;
}

.logout-btn {
  background-color: #ff5b5b;
}

.logout-btn:hover {
  background-color: #6a0202;
}
</style>