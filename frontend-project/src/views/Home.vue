<template>
  <div class="home-container">
    <Header />

    <div class="main-section">
      <LeftSide @filter-change="filterDevice" />
      <Devices :filter="currentFilter" />
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
</style>