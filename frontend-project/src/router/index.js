import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Devices from '../views/Devices.vue'
import Light from '../views/devices/Light.vue'
import Curtain from '../views/devices/Curtain.vue'
import AirConditioner from '../views/devices/AirConditioner.vue'
import WashingMachine from '../views/devices/WashingMachine.vue'
import RobotVacuum from '../views/devices/RobotVacuum.vue'

const routes = [
  {
    path: '/',
    name: 'Root',
    // 根据是否登录决定主页面是哪里
    beforeEnter: (to, from, next) => {
      const isLoggedIn = localStorage.getItem('token') // 登陆状态
      if (isLoggedIn) {
        next('/home')
      } else {
        next('/login')
      }
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
  { path: '/devices/robotvacuum', name: 'RobotVacuum', component: RobotVacuum }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router