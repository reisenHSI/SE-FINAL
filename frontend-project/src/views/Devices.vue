<template>
  <div class="devices-container">
    <h2 class="title">{{ titleMap[filter] }}</h2>
    <div class="device-grid">
      <div
        class="device-card"
        v-for="device in filteredDevices"
        :key="device.id"
      >
        <img :src="device.icon" class="device-icon" alt="icon" />
        <p class="device-name">{{ device.name }}</p>
        <p class="device-info">类型：{{ typeMap[device.type] }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Devices',
  props: {
    filter: {
      type: String,
      default: 'all'
    }
  },
  data() {
    return {
      devices: [
        { id: 1, type: 'light', name: '客厅灯 A', icon: '/icons/light.png' },
        { id: 2, type: 'light', name: '卧室灯 B', icon: '/icons/light.png' },
        { id: 3, type: 'curtain', name: '窗帘 1 号', icon: '/icons/curtain.png' },
        { id: 4, type: 'air', name: '空调 A', icon: '/icons/air.png' },
        { id: 5, type: 'air', name: '空调 B', icon: '/icons/air.png' },
        { id: 6, type: 'washing', name: '洗衣机 A', icon: '/icons/washing.png' },
        { id: 7, type: 'robot', name: '扫地机器人 1', icon: '/icons/robot.png' },
        { id: 8, type: 'robot', name: '扫地机器人 2', icon: '/icons/robot.png' }
      ],
      titleMap: {
        all: '全部设备',
        light: '灯光设备',
        curtain: '窗帘设备',
        air: '空调设备',
        washing: '洗衣机设备',
        robot: '扫地机器人'
      },
      typeMap: {
        light: '灯光',
        curtain: '窗帘',
        air: '空调',
        washing: '洗衣机',
        robot: '扫地机器人'
      }
    }
  },
  computed: {
    filteredDevices() {
      if (this.filter === 'all') return this.devices
      return this.devices.filter(d => d.type === this.filter)
    }
  }
}
</script>

<style scoped>
.devices-container {
  flex: 1;
  padding: 20px;
  background-color: #f8fbff;
}

.title {
  font-size: 20px;
  color: #2a6ecf;
  margin-bottom: 20px;
}

.device-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 20px;
}

.device-card {
  background-color: #ffffff;
  border: 1px solid #d0e3f1;
  border-radius: 10px;
  padding: 16px;
  text-align: center;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
  transition: transform 0.2s ease;
}

.device-card:hover {
  transform: translateY(-4px);
}

.device-icon {
  width: 60px;
  height: 60px;
  margin-bottom: 10px;
}

.device-name {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.device-info {
  font-size: 14px;
  color: #666;
}
</style>
