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
import Logs from '@/views/Logs.vue'
import AddDevice from "@/views/AddDevice.vue";
import DeleteDevice from "@/views/DeleteDevice.vue";
import Habits from "@/views/Habits.vue"

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
  { path: '/logs', name: 'Logs', component: Logs},
  { path: '/devices', name: 'Devices', component: Devices },
  { path: '/devices/light', name: 'Light', component: Light },
  { path: '/AddDevice' , name: "AddDevice", component: AddDevice },
  { path: '/DeleteDevice' , name: "DeleteDevice", component: DeleteDevice },
  { path: '/devices/curtain', name: 'Curtain', component: Curtain },
  { path: '/devices/air', name: 'AirConditioner', component: AirConditioner },
  { path: '/devices/washing-machine', name: 'WashingMachine', component: WashingMachine },
  { path: '/devices/robotvacuum', name: 'RobotVacuum', component: RobotVacuum },
  { path: '/habits', name: 'Habits', component: Habits },


    // 防止路径不匹配导致页面空白
  { path: '/:catchAll(.*)', redirect: '/login' },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})


export default router