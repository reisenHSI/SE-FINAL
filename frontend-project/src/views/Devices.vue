<template>
  <div class="devices-container">
    <h2 class="title">{{ titleMap[filter] }}</h2>

    <div class="top-actions">
      <button @click="goToAddDevice" class="top-btn add-btn">添加设备</button>
    </div>

    <!-- 设备为空时显示 -->
    <div v-if="filteredDevices.length === 0" class="no-devices">
      当前没有设备
    </div>

    <div v-else class="device-grid">
      <div
        class="device-row"
        v-for="device in filteredDevices"
        :key="device.id"
      >
        <!-- 设备信息区域 -->
        <div class="device-card">
          <img :src="device.icon" class="device-icon" alt="icon" />
          <p class="device-name">{{ device.name }}</p>
          <p class="device-info">类型：{{ typeMap[device.type] }}</p>
        </div>

        <!-- 操作按钮区域 -->
        <div class="device-actions">
          <button @click="goToControlDevice(device)" class="action-btn control-btn">
            控制
          </button>
          <button @click="goToDeleteDevice(device.id, device.name)" class="action-btn delete-btn">
            删除
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { API_BASE_URL } from "../main";

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
      devices: [],
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
  },
  methods: {
    async fetchDevices() {
      try {
        const response = await axios.post(`${API_BASE_URL}home/devices/`, { username: localStorage.getItem('username') })

        if (response.data.status === 'success') {
          let deviceList = []
          response.data.device_categories.forEach(category => {
            category.devices.forEach(device => {
              deviceList.push({
                id: device.id,
                name: device.name,
                type: this.mapBackendType(category.type),
                icon: this.getIconPath(category.icon)
              })
            })
          })
          this.devices = deviceList
        } else {
          this.$message.error(response.data.message || '设备获取失败')
        }
      } catch (error) {
        this.$message.error('设备获取失败，请检查网络')
      }
    },
    mapBackendType(type) {
      const typeMap = {
        Light: 'light',
        Curtain: 'curtain',
        AirConditioner: 'air',
        WashingMachine: 'washing',
        Robotvacuum: 'robot'
      }
      return typeMap[type] || 'unknown'
    },
    getIconPath(iconName) {
      return `/public/icons/${iconName}.png`
    },
    goToAddDevice() {
      this.$router.push({ name: 'AddDevice' })
    },
    goToDeleteDevice(deviceId, deviceName) {
      this.$router.push({
        name: 'DeleteDevice',
        query: { id: deviceId, name: deviceName }
      })
    },
    goToControlDevice(device) {
      const routeMap = {
        light: 'Light',
        air: 'AirConditioner',
        curtain: 'Curtain',
        washing: 'WashingMachine',
        robot: 'RobotVacuum'
      }

      const routeName = routeMap[device.type]
      if (!routeName) {
        this.$message.error('暂不支持该设备类型！')
        return
      }

      this.$router.push({
        name: routeName,
        query: {
          id: device.id,
          name: device.name
        },
      })
    }
  },
  mounted() {
    this.fetchDevices()
  }
}
</script>

<style scoped>
.devices-container {
  padding: 20px;
}

.title {
  text-align: center;
  font-size: 28px;
  color: #2a6ecf;
  margin-bottom: 20px;
}

/* 顶部操作按钮 */
.top-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-bottom: 20px;
}

.top-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 16px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  color: white;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.add-btn {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
}

.del-btn {
  background: linear-gradient(135deg, #ff6a6a, #ff4e50);
}

.top-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
}

/* 设备网格 */
.device-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.device-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  background-color: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.device-card {
  display: flex;
  align-items: center;
  gap: 16px;
}

.device-icon {
  width: 60px;
  height: 60px;
}

.device-name {
  font-size: 18px;
  font-weight: bold;
}

.device-info {
  color: #555;
  margin-top: 4px;
}

.device-actions .action-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 10px;
  background-color: #2a6ecf;
  color: white;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.device-actions .action-btn:hover {
  background-color: #1f5eb7;
}

/* 无设备提示样式 */
.no-devices {
  text-align: center;
  font-size: 18px;
  color: #888;
  margin-top: 50px;
}
</style>
