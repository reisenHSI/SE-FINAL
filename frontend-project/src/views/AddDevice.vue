<template>
  <div class="add-device">
    <h1>添加设备</h1>
    <form @submit.prevent="addDevice">
      <div>
        <label for="device_name">设备名称:</label>
        <input type="text" id="device_name" v-model="deviceName" required />
      </div>
      <div>
        <label for="device_type">设备类型:</label>
        <select id="device_type" v-model="deviceType" required>
          <option value="Light">灯</option>
          <option value="AirConditioner">空调</option>
          <option value="Curtain">窗帘</option>
          <option value="WashingMachine">洗衣机</option>
          <option value="RobotVacuum">扫地机</option>
        </select>
      </div>
      <button type="submit">添加</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      deviceName: "",
      deviceType: "",
    };
  },
  methods: {
    async addDevice() {
      try {
        const response = await fetch("/add_device/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            device_name: this.deviceName,
            device_type: this.deviceType,
          }),
        });
        if (response.ok) {
          alert("设备添加成功");
          this.deviceName = "";
          this.deviceType = "";
        } else {
          alert("设备添加失败");
        }
      } catch (error) {
        console.error("添加设备失败", error);
      }
    },
  },
};
</script>

<style>
/* ...样式代码... */
</style>
