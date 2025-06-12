<template>
  <div class="home-container">
    <Header />

    <div class="main-section">
      <LeftSide @filter-change="filterDevice" />
      <div class="devices-wrapper">
        <Devices :filter="currentFilter" />
      </div>
    </div>

    <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import Devices from '@/views/Devices.vue'
import LeftSide from '@/components/LeftSide.vue'

export default {
  name: 'Home',
  components: { Header, Footer, Devices, LeftSide },
  data() {
    return {
      currentFilter: 'all'
    }
  },
  methods: {
    filterDevice(type) {
      this.currentFilter = type
    }
  }
}
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.main-section {
  display: flex;
  flex: 1;
}

/* 左侧菜单固定宽度 */
.main-section > :first-child {
  width: 200px; /* 你可以根据实际需要调整宽度 */
  border-right: 1px solid #e0e0e0;
}

/* Devices 区域包裹器，保证 Devices 居中 */
.devices-wrapper {
  flex: 1;
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: flex-start; /* 顶部对齐 */
  padding: 40px 20px;
  overflow-y: auto; /* 防止内容溢出 */
}
</style>
