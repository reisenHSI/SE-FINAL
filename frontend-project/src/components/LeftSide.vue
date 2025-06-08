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
  width: 180px;
  background-color: #f0f8ff;
  padding: 20px;
  border-right: 1px solid #d0e3f1;
  height: 100%;
}

.nav-title {
  font-size: 18px;
  color: #2a6ecf;
  margin-bottom: 16px;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-list li {
  padding: 10px 12px;
  margin-bottom: 8px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.nav-list li:hover {
  background-color: #d7ebff;
}

.nav-list li.active {
  background-color: #2a6ecf;
  color: white;
}
</style>
