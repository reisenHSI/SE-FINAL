import { mount, flushPromises } from '@vue/test-utils'
import RobotVacuum from '@/views/devices/RobotVacuum.vue'
import axios from 'axios'

// 1. 完全隔离路由依赖 - 修复createWebHashHistory错误
jest.mock('vue-router', () => ({
  createWebHashHistory: jest.fn(() => ({
    path: '/',
    fullPath: '/',
    href: '/'
  })),
  createRouter: jest.fn(() => ({
    push: jest.fn(),
    replace: jest.fn()
  })),
  useRoute: jest.fn(() => ({
    query: { name: '客厅扫地机器人' }
  })),
  useRouter: jest.fn(() => ({
    push: jest.fn()
  }))
}))

// 2. 模拟主应用入口文件
jest.mock('@/main.js', () => ({}))

// 3. 模拟axios
jest.mock('axios')

// 4. 模拟localStorage
const localStorageMock = {
  getItem: jest.fn(() => 'testuser')
}
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock
})

// 5. 模拟全局alert
global.alert = jest.fn()

describe('RobotVacuum.vue', () => {
  let wrapper
  const mockDeviceData = {
    id: 1,
    name: '客厅扫地机器人',
    type: 'RobotVacuum',
    status: '0',
    mode: 'standard',
    electricity: 80,
    sweeparea: 25,
    valid_modes: ['standard', 'turbo', 'quiet']
  }

  beforeEach(async () => {
    jest.clearAllMocks()

    // 6. 配置axios响应
    axios.post.mockImplementation((url) => {
      if (url.includes('/robotvacuum/')) {
        return Promise.resolve({
          data: {
            status: 'success',
            device: mockDeviceData
          }
        })
      }
      return Promise.resolve({ data: {} })
    })

    // 7. 挂载组件 - 提供完整的模拟路由
    wrapper = mount(RobotVacuum, {
      global: {
        mocks: {
          $route: {
            query: { name: '客厅扫地机器人' },
            path: '/robotvacuum'
          },
          $router: {
            push: jest.fn(),
            replace: jest.fn()
          }
        }
      }
    })

    await flushPromises()
  })

  it('正确渲染组件', () => {
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.find('h1').exists()).toBe(true)
  })

  it('加载完成后显示设备信息', async () => {
    await flushPromises()
    expect(wrapper.find('h1').text()).toBe('客厅扫地机器人')
    expect(wrapper.text()).toContain('当前模式: standard')
    expect(wrapper.text()).toContain('电量: 80%')
    expect(wrapper.text()).toContain('已清扫面积: 25 ㎡')
  })

  describe('扫地机器人控制', () => {
    it('初始状态为停止', async () => {
      await flushPromises()
      expect(wrapper.vm.isRunning).toBe(false)
      const toggleButton = wrapper.find('.bg-blue-500')
      expect(toggleButton.text()).toContain('启动清扫')
    })

    it('点击按钮切换清扫状态', async () => {
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
        expect.stringContaining('/robotvacuum/'),
        expect.objectContaining({
          new_status: '1'
        })
      )

      await flushPromises()
      expect(wrapper.vm.isRunning).toBe(true)
    })
  })

  describe('模式切换', () => {
    it('显示所有有效模式选项', async () => {
      await flushPromises()
      const options = wrapper.findAll('option')
      expect(options.length).toBe(3)
      expect(options[0].text()).toBe('standard')
      expect(options[1].text()).toBe('turbo')
      expect(options[2].text()).toBe('quiet')
    })

    it('切换模式发送正确请求', async () => {
      await flushPromises()

      axios.post.mockResolvedValueOnce({
        data: {
          status: 'success',
          device: { ...mockDeviceData, mode: 'turbo' }
        }
      })

      const select = wrapper.find('select')
      await select.setValue('turbo')
      await select.trigger('change')

      expect(axios.post).toHaveBeenCalledWith(
        expect.stringContaining('/robotvacuum/'),
        expect.objectContaining({
          new_mode: 'turbo'
        })
      )
    })
  })

  describe('设备重命名', () => {
    it('成功重命名设备', async () => {
      await flushPromises()

      const newName = '主卧扫地机器人'
      await wrapper.find('input[type="text"]').setValue(newName)

      axios.post.mockResolvedValueOnce({
        data: {
          status: 'success',
          device: { ...mockDeviceData, name: newName }
        }
      })

      await wrapper.find('.bg-yellow-500').trigger('click')
      await flushPromises()

      expect(wrapper.find('h1').text()).toBe(newName)
    })

    it('空名称时显示警告', async () => {
      await flushPromises()

      axios.post.mockClear()
      await wrapper.find('input[type="text"]').setValue('')
      await wrapper.find('.bg-yellow-500').trigger('click')

      expect(global.alert).toHaveBeenCalledWith('设备名称不能为空')
      expect(axios.post).not.toHaveBeenCalled()
    })
  })

  it('显示正确的清扫动画状态', async () => {
    await flushPromises()

    // 初始状态为停止
    expect(wrapper.find('.animate-none').exists()).toBe(true)

    // 切换为运行状态
    wrapper.vm.isRunning = true
    await wrapper.vm.$nextTick()

    expect(wrapper.find('.animate-spin').exists()).toBe(true)
  })
})