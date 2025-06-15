import { mount, flushPromises } from '@vue/test-utils'
import WashingMachine from '@/views/devices/WashingMachine.vue'
import axios from 'axios'

// 模拟 vue-router
jest.mock('vue-router', () => ({
  createWebHashHistory: jest.fn(),
  createRouter: jest.fn(),
  useRoute: jest.fn(() => ({
    query: { name: '客厅洗衣机' }
  })),
  useRouter: jest.fn(() => ({
    push: jest.fn(),
    replace: jest.fn()
  }))
}))

// 模拟主应用入口文件
jest.mock('@/main.js', () => ({}))

// 模拟axios
jest.mock('axios')

// 模拟localStorage
const localStorageMock = {
  getItem: jest.fn(() => 'testuser')
}
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock
})

// 模拟全局alert
global.alert = jest.fn()

describe('WashingMachine.vue', () => {
  let wrapper
  const mockDeviceData = {
    name: '客厅洗衣机',
    mode: 'standard',
    status: '0',
    remaining_time: 45,
    valid_modes: ['standard', 'quick', 'delicate']
  }

  beforeEach(async () => {
    jest.clearAllMocks()

    // 配置axios响应
    axios.post.mockImplementation((url) => {
      if (url.includes('/washingMachine/')) {
        return Promise.resolve({
          data: {
            status: 'success',
            device: mockDeviceData
          }
        })
      }
      return Promise.resolve({ data: {} })
    })

    wrapper = mount(WashingMachine, {
      global: {
        mocks: {
          $route: {
            query: { name: '客厅洗衣机' },
            path: '/washingMachine'
          },
          $router: {
            push: jest.fn(),
            replace: jest.fn()
          }
        }
      }
    })
  })

  it('正确渲染组件', () => {
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.find('h1').exists()).toBe(true)
  })

  it('加载完成后显示设备信息', async () => {
    await flushPromises()
    expect(wrapper.vm.isLoaded).toBe(true)
    expect(wrapper.find('h1').text()).toBe('客厅洗衣机')
    expect(wrapper.text()).toContain('当前模式: standard')
    expect(wrapper.text()).toContain('剩余时间: 45 分钟')
  })

  it('显示正确的洗衣机动画状态', async () => {
    await flushPromises()

    // 初始状态为停止
    expect(wrapper.find('.animate-none').exists()).toBe(true)

    // 切换为运行状态
    wrapper.vm.isRunning = true
    await wrapper.vm.$nextTick()

    expect(wrapper.find('.animate-spin').exists()).toBe(true)
  })

  describe('洗衣机控制', () => {
    it('初始状态为停止', async () => {
      await flushPromises()
      expect(wrapper.vm.isRunning).toBe(false)
      const toggleButton = wrapper.find('.bg-blue-500')
      expect(toggleButton.text()).toContain('启动洗衣机')
    })

    it('点击按钮切换洗衣机状态', async () => {
      await flushPromises()

      axios.post.mockResolvedValueOnce({
        data: {
          status: 'success',
          device: { ...mockDeviceData, status: '1' }
        }
      })

      const toggleButton = wrapper.find('.bg-blue-500')
      await toggleButton.trigger('click')

      expect(axios.post).toHaveBeenCalledWith(
        expect.stringContaining('/washingMachine/'),
        expect.objectContaining({
          new_status: '1'
        })
      )

      await flushPromises()
      expect(wrapper.vm.isRunning).toBe(true)
      expect(toggleButton.text()).toContain('停止洗衣机')
    })
  })

  describe('模式切换', () => {
    it('显示所有有效模式选项', async () => {
      await flushPromises()
      const options = wrapper.findAll('option')
      expect(options.length).toBe(3)
      expect(options[0].text()).toBe('standard')
      expect(options[1].text()).toBe('quick')
      expect(options[2].text()).toBe('delicate')
    })

    it('切换模式发送正确请求', async () => {
      await flushPromises()

      axios.post.mockResolvedValueOnce({
        data: {
          status: 'success',
          device: { ...mockDeviceData, mode: 'quick' }
        }
      })

      const select = wrapper.find('select')
      await select.setValue('quick')
      await select.trigger('change')

      expect(axios.post).toHaveBeenCalledWith(
        expect.stringContaining('/washingMachine/'),
        expect.objectContaining({
          new_mode: 'quick'
        })
      )
    })
  })

  describe('设备重命名', () => {
    beforeEach(async () => {
      await flushPromises()
    })

    it('空名称时显示警告', async () => {
      axios.post.mockClear()
      await wrapper.find('input[type="text"]').setValue('')
      await wrapper.find('.bg-green-500').trigger('click')

      expect(global.alert).toHaveBeenCalledWith('设备名称不能为空')
      expect(axios.post).not.toHaveBeenCalled()
    })
  })
})
