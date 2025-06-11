<template>
  <div class="add-device-container">
    <h2>添加设备 - {{ deviceTypeName }}</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="deviceName">设备名称：</label>
        <input
          id="deviceName"
          v-model="deviceName"
          type="text"
          placeholder="请输入设备名称"
          required
        />
      </div>

      <div class="form-group">
        <label for="deviceType">设备类型：</label>
        <input
          id="deviceType"
          v-model="deviceType"
          type="text"
          readonly
        />
      </div>

      <button type="submit">添加设备</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "AddDevices",
  data() {
    return {
      deviceType: this.$route.query.type || "未知类型",
      deviceName: ""
    };
  },
  computed: {
    deviceTypeName() {
      const map = {
        light: "灯光",
        curtain: "窗帘",
        air: "空调",
        washing: "洗衣机",
        robot: "扫地机器人"
      };
      return map[this.deviceType] || this.deviceType;
    }
  },
  methods: {
    submitForm() {
      if (!this.deviceName.trim()) {
        alert("设备名称不能为空");
        return;
      }

      // 这里写调用后端接口的代码
      alert(`添加设备: ${this.deviceName} (${this.deviceType})`);

      // 提交成功后可以跳转回设备列表
      this.$router.push({ name: "Devices", query: { filter: this.deviceType } });
    }
  }
};
</script>

<style scoped>
.add-device-container {
  max-width: 400px;
  margin: 40px auto;
  padding: 20px;
  background: #f8fbff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(42, 110, 207, 0.2);
}

h2 {
  color: #2a6ecf;
  margin-bottom: 20px;
  text-align: center;
}

.form-group {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 6px;
  font-weight: 600;
  color: #333;
}

input[type="text"] {
  padding: 8px 12px;
  border: 1px solid #d0e3f1;
  border-radius: 6px;
  font-size: 16px;
}

input[readonly] {
  background-color: #eee;
  cursor: not-allowed;
}

button {
  width: 100%;
  padding: 12px 0;
  background-color: #2a6ecf;
  border: none;
  border-radius: 8px;
  color: white;
  font-weight: 700;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button:hover {
  background-color: #1e4aad;
}
</style>
