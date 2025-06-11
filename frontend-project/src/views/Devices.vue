<template>
  <div class="devices-container">
    <h2 class="title">{{ titleMap[filter] }}</h2>

    <div class="top-actions">
      <button @click="goToAddDevice" class="top-btn add-btn">添加设备</button>
      <button @click="goToDeleteDevice" class="top-btn del-btn">删除设备</button>
    </div>

    <div class="device-grid">
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
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

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
        const response = await axios.get('{API_BASE_URL}home/devices/') // 确保路径和后端一致
        if (response.data.status === 'success') {
          // 后端返回的是设备类别数组，扁平化为设备列表
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
      // 后端传过来的类型映射为前端类型
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
      // 图标路径映射
      return `/icons/${iconName}.png`
    },
    goToAddDevice() {
      this.$router.push({ name: 'AddDevice' })
    },
    goToDeleteDevice() {
      this.$router.push({ name: 'DeleteDevice' })
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
        }
      })
    }
  },
  mounted() {
    this.fetchDevices()
  }
}
</script>

<style scoped>
/* 顶部操作按钮 */
.top-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-bottom: 20px;
}

.top-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  color: white;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.add-btn {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.del-btn {
  background: linear-gradient(135deg, #ff6a6a, #ff4e50);
}

.del-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

</style>
