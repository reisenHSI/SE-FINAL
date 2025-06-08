// src/router/index.js
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
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/devices', component: Devices },
  { path: '/devices/light', component: Light },
  { path: '/devices/curtain', component: Curtain },
  { path: '/devices/air', component: AirConditioner },
  { path: '/devices/washing-machine', component: WashingMachine },
  { path: '/devices/robotvacuum', component: RobotVacuum }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router