import { createRouter, createWebHashHistory } from 'vue-router'

import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import Devices from '@/views/Devices.vue'
import Light from '@/views/devices/Light.vue'
import Curtain from '@/views/devices/Curtain.vue'
import AirConditioner from '@/views/devices/AirConditioner.vue'
import WashingMachine from '@/views/devices/WashingMachine.vue'
import RobotVacuum from '@/views/devices/RobotVacuum.vue'
/*
const routes = [
  {
    path: '/',
    redirect: () => {
      const isLoggedIn = localStorage.getItem('token')
      console.log('是否已登录:', isLoggedIn)
      return isLoggedIn === 'true' ? '/home' : '/login'
    }
  },
  { path: '/home', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/devices', name: 'Devices', component: Devices },
  { path: '/devices/light', name: 'Light', component: Light },
  { path: '/devices/curtain', name: 'Curtain', component: Curtain },
  { path: '/devices/air', name: 'AirConditioner', component: AirConditioner },
  { path: '/devices/washing-machine', name: 'WashingMachine', component: WashingMachine },
  { path: '/devices/robotvacuum', name: 'RobotVacuum', component: RobotVacuum },

    // 防止路径不匹配导致页面空白
  { path: '/:catchAll(.*)', redirect: '/login' },
]*/

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})


export default router