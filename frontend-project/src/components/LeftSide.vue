<template>
  <aside class="left-side">
    <h3 class="nav-title">设备导航</h3>
    <ul class="nav-list">
      <li
        v-for="item in navItems"
        :key="item.value"
        :class="{ active: activeItem === item.value }"
        @click="selectItem(item.value)"
      >
        {{ item.label }}
      </li>
    </ul>
  </aside>
</template>

<script>
export default {
  name: 'LeftSide',
  data() {
    return {
      activeItem: 'all',
      navItems: [
        { label: '全部设备', value: 'all' },
        { label: '灯光', value: 'light' },
        { label: '窗帘', value: 'curtain' },
        { label: '空调', value: 'air' },
        { label: '洗衣机', value: 'washing' },
        { label: '扫地机器人', value: 'robot' }
      ]
    }
  },
  methods: {
    selectItem(value) {
      this.activeItem = value
      this.$emit('filter-change', value) // 通知父组件进行设备过滤
    }
  }
}
</script>

<style scoped>
.left-side {
  width: 220px;
  background: linear-gradient(to bottom, #e0f0ff, #ffffff);
  padding: 24px;
  border-right: 1px solid #d0e3f1;
  height: 100vh;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
  border-top-right-radius: 16px;
  border-bottom-right-radius: 16px;
}

.nav-title {
  font-size: 22px;
  color: #2563eb;
  font-weight: bold;
  margin-bottom: 24px;
  text-align: center;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.nav-list li {
  padding: 12px 16px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  color: #333;
  transition: all 0.3s ease;
  text-align: center;
}

.nav-list li:hover {
  background-color: #d7ebff;
  transform: translateX(4px);
}

.nav-list li.active {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  color: white;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transform: translateX(4px);
}
</style>
