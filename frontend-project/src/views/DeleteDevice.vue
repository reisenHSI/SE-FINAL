<template>
  <div class="delete-device">
    <h1>删除设备</h1>
    <form @submit.prevent="deleteDevices">
      <ul>
        <li v-for="device in devices" :key="device.device_name">
          <input type="checkbox" :value="device.name" v-model="selectedDevices" />
          {{ device.name }} ({{ device.type }})
        </li>
      </ul>
      <button type="submit">删除</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      devices: [],
      selectedDevices: [],
    };
  },
  async created() {
    try {
      const response = await fetch("/delete_device/");
      const result = await response.json();
      this.devices = result.devices;
    } catch (error) {
      console.error("获取设备列表失败", error);
    }
  },
  methods: {
    async deleteDevices() {
      try {
        const response = await fetch("/delete_device/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ device_name: this.selectedDevices }),
        });
        if (response.ok) {
          alert("设备删除成功");
          this.devices = this.devices.filter(device => !this.selectedDevices.includes(device.name));
          this.selectedDevices = [];
        } else {
          alert("设备删除失败");
        }
      } catch (error) {
        console.error("删除设备失败", error);
      }
    },
  },
};
</script>

<style>
/* ...样式代码... */
</style>
