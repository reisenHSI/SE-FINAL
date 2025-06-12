<template>
  <div class="add-device-container">
    <h2>添加设备</h2>
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
        <select id="deviceType" v-model="deviceType" required>
          <option disabled value="">请选择设备类型</option>
          <option v-for="(name, type) in deviceTypes" :key="type" :value="type">
            {{ name }}
          </option>
        </select>
      </div>

      <button type="submit" class="submit-btn">添加设备</button>
    </form>
  </div>
</template>

<script>
import {API_BASE_URL} from "../main";

export default {
  name: "AddDevices",
  data() {
    return {
      deviceName: "",
      deviceType: "",
      deviceTypes: {
        Light: "灯光",
        Curtain: "窗帘",
        AirConditioner: "空调",
        WashingMachine: "洗衣机",
        Robotvacuum: "扫地机器人"
      }
    };
  },
  methods: {
    async submitForm() {
      if (!this.deviceName.trim()) {
        alert("设备名称不能为空");
        return;
      }

      try {
        console.log(localStorage.getItem('username'))
        // 向后端提交设备信息
        const response = await this.$axios.post(`${API_BASE_URL}home/add_delete/add_device/`, {
          device_name: this.deviceName,
          device_type: this.deviceType,
          username: localStorage.getItem('username')
        });

        if (response.data.status === 'success') {
          alert('设备添加成功！');
          this.$router.push({ name: 'Home'});
        } else {
          alert(`添加失败：${response.data.message}`);
        }
      } catch (error) {
        alert('添加设备失败，请稍后重试');
        console.error(error);
      }
    }
  }
};
</script>

<style scoped>
.add-device-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 20px;
  background-color: #f8fbff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #2a6ecf;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #333;
}

input, select {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #d0e3f1;
  border-radius: 8px;
  font-size: 16px;
}

input:focus, select:focus {
  outline: none;
  border-color: #2a6ecf;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
</style>

