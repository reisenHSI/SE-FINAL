<template>
  <footer class="footer">
    <p>智慧生活，从这里开始。</p>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
.footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 50px;

  background-color: #5690d0;
  color: #666;
  text-align: center;
  line-height: 50px;
  font-size: 14px;
  border-top: 1px solid #d0e3f1;
  z-index: 100;
}
</style>
