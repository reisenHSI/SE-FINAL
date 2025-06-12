<template>
  <div class="delete-device-container">
    <h2>删除设备</h2>
    <p>确定要删除设备吗？</p>
    <p class="device-info">{{ deviceName }} (ID: {{ deviceId }})</p>

    <div class="btn-group">
      <button @click="confirmDelete" class="btn-delete">确认删除</button>
      <button @click="cancel" class="btn-cancel">取消</button>
    </div>
  </div>
</template>



<script>
import axios from 'axios'
import { API_BASE_URL } from "../main";
export default {
  name: "DeleteDevices",
  data() {
    return {
      deviceId: this.$route.query.id || "",
      deviceName: this.$route.query.name || "未知设备"
    };
  },
  methods: {
    async confirmDelete() {
      try {
        console.log('1')
        const response = await axios.post(`${API_BASE_URL}home/add_delete/delete_device/`, {
          device_name: this.deviceName,
          username: localStorage.getItem('username')
        }, { withCredentials: true })

        console.log(response)
        if (response.data.status === 'success') {
          this.$message.success(`已成功删除设备: ${this.deviceName} (ID: ${this.deviceId})`)
          this.$router.push({ name: "Home" })
        } else {
          this.$message.error(response.data.message || '设备删除失败')
        }
      } catch (error) {
        console.error('删除设备失败:', error)
        this.$message.error(error.response?.data?.message || '删除设备时发生错误')
      }
    },
    cancel() {
      this.$router.back();
    }
  }
};
</script>

<style scoped>
.delete-device-container {
  max-width: 400px;
  margin: 40px auto;
  padding: 20px;
  background: #fff6f6;
  border-radius: 8px;
  border: 1px solid #e53e3e;
  box-shadow: 0 2px 8px rgba(229, 62, 62, 0.2);
  text-align: center;
}

h2 {
  color: #e53e3e;
  margin-bottom: 16px;
}

.device-info {
  font-weight: 600;
  color: #b82c2c;
  margin: 12px 0;
  font-size: 18px;
}

.btn-group {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 20px;
}

button {
  padding: 10px 20px;
  font-weight: 700;
  border-radius: 6px;
  cursor: pointer;
  border: none;
  font-size: 16px;
}

.btn-delete {
  background-color: #e53e3e;
  color: white;
}

.btn-delete:hover {
  background-color: #b82c2c;
}

.btn-cancel {
  background-color: #ccc;
  color: #333;
}

.btn-cancel:hover {
  background-color: #999;
}
</style>
