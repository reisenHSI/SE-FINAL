import { mount, flushPromises } from '@vue/test-utils'
import Habits from '@/views/Habits.vue'
import axios from 'axios'

// 模拟 Vue Router
jest.mock('vue-router', () => ({
  createWebHashHistory: jest.fn(),
  createRouter: jest.fn(() => ({
    push: jest.fn()
  })),
  useRoute: jest.fn(() => ({
    path: '/habits'
  })),
  useRouter: jest.fn(() => ({
    push: jest.fn()
  }))
}))

// 模拟 axios
jest.mock('axios')

// 抑制主应用挂载相关的警告
jest.mock('@/main.js', () => ({
  mount: jest.fn()
}))

describe('Habits.vue', () => {
  let wrapper
  const mockHabits = [
    {
      habitname: '早晨灯光',
      devicename: '卧室灯',
      devicetype: 'Light',
      brightness: 80
    }
  ]

  beforeEach(async () => {
    // 模拟 localStorage
    Storage.prototype.getItem = jest.fn(() => 'testuser')

    // 配置 axios 响应
    axios.post.mockImplementation((url) => {
      if (url.includes('/home/habits/')) {
        return Promise.resolve({ data: { result: mockHabits } })
      }
      if (url.includes('/home/devices/light/')) {
        return Promise.resolve({ data: { status: 'success' } })
      }
      return Promise.resolve({ data: {} })
    })

    // 挂载组件
    wrapper = mount(Habits, {
      global: {
        mocks: {
          $route: { path: '/habits' },
          $router: { push: jest.fn() }
        }
      },
      data() {
        return {
          selectedHabits: []
        }
      }
    })

    await flushPromises()
  })

  afterEach(() => {
    jest.clearAllMocks()
  })

  it('正确渲染组件', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('显示习惯列表', () => {
    const habits = wrapper.findAll('li')
    expect(habits.length).toBe(mockHabits.length)
    expect(habits[0].text()).toContain('早晨灯光')
  })

  describe('应用习惯', () => {
    it('未选择时显示警告', async () => {
      window.alert = jest.fn()
      await wrapper.find('form').trigger('submit.prevent')
      expect(window.alert).toHaveBeenCalledWith('请先选择要应用的习惯')
    })

    it('成功应用习惯', async () => {
      window.alert = jest.fn()
      wrapper.vm.selectedHabits = ['早晨灯光']
      await wrapper.find('form').trigger('submit.prevent')
      await flushPromises()

      expect(axios.post).toHaveBeenCalledWith(
        expect.stringContaining('/home/devices/light/'),
        expect.objectContaining({
          device_name: '卧室灯',
          new_brightness: 80
        })
      )
      expect(window.alert).toHaveBeenCalledWith('习惯已成功应用')
    })
  })
})