<template>
  <div class="device-details">
    <h1>{{ device.name }} 详情</h1>
    <p>设备类型: {{ device.type }}</p>
    <p>设备状态: {{ device.status === 1 ? "开启" : "关闭" }}</p>
    <div v-if="device.type === 'Light'">
      <label for="brightness">亮度:</label>
      <input
        type="range"
        id="brightness"
        v-model="brightness"
        min="0"
        max="100"
        @change="updateBrightness"
      />
      <span>{{ brightness }}</span>
    </div>
    <div v-if="device.type === 'AirConditioner'">
      <label for="temperature">温度:</label>
      <input
        type="number"
        id="temperature"
        v-model="temperature"
        @change="updateTemperature"
      />
      <p>模式: {{ mode }}</p>
      <button @click="setMode('cool')">制冷</button>
      <button @click="setMode('heat')">制热</button>
      <button @click="setMode('dry')">除湿</button>
    </div>
    <button @click="toggleDevice">
      {{ device.status === 1 ? "关闭设备" : "开启设备" }}
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      device: {},
      brightness: 100,
      temperature: 25,
      mode: "cool",
    };
  },
  async created() {
    const deviceId = this.$route.params.id;
    try {
      const response = await fetch(`/device_details/${deviceId}/`);
      const result = await response.json();
      this.device = result.device;
      if (this.device.type === "Light") {
        this.brightness = this.device.brightness;
      } else if (this.device.type === "AirConditioner") {
        this.temperature = this.device.temperature;
        this.mode = this.device.mode;
      }
    } catch (error) {
      console.error("获取设备详情失败", error);
    }
  },
  methods: {
    async toggleDevice() {
      const action = this.device.status === 1 ? "turn_off" : "turn_on";
      try {
        const response = await fetch(`/${action}/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ device_id: this.device.id }),
        });
        if (response.ok) {
          this.device.status = this.device.status === 1 ? 0 : 1;
        } else {
          alert("操作失败");
        }
      } catch (error) {
        console.error("设备操作失败", error);
      }
    },
    async updateBrightness() {
      try {
        const response = await fetch("/set_brightness/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            device_id: this.device.id,
            brightness: this.brightness,
          }),
        });
        if (!response.ok) {
          alert("亮度更新失败");
        }
      } catch (error) {
        console.error("亮度更新失败", error);
      }
    },
    async updateTemperature() {
      try {
        const response = await fetch("/aircondition_set_temperature/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            device_id: this.device.id,
            temperature: this.temperature,
          }),
        });
        if (!response.ok) {
          alert("温度更新失败");
        }
      } catch (error) {
        console.error("温度更新失败", error);
      }
    },
    async setMode(newMode) {
      try {
        const response = await fetch("/aircondition_set_mode/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            device_id: this.device.id,
            mode: newMode,
          }),
        });
        if (response.ok) {
          this.mode = newMode;
        } else {
          alert("模式更新失败");
        }
      } catch (error) {
        console.error("模式更新失败", error);
      }
    },
  },
};
</script>

<style>
/* ...样式代码... */
</style>
