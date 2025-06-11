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
export default {
  name: "DeleteDevices",
  data() {
    return {
      deviceId: this.$route.query.id || "",
      deviceName: this.$route.query.name || "未知设备"
    };
  },
  methods: {
    confirmDelete() {
      // 这里写调用后端删除设备的代码
      alert(`已删除设备: ${this.deviceName} (ID: ${this.deviceId})`);

      // 删除成功后跳转回设备列表
      this.$router.push({ name: "Devices" });
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
