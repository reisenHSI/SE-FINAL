import { mount, flushPromises } from '@vue/test-utils'
import AirConditioner from '@/views/devices/AirConditioner.vue'
import axios from 'axios'

// 1. 完整模拟 Vue Router
jest.mock('vue-router', () => ({
  createWebHashHistory: jest.fn(),
  createRouter: jest.fn(() => ({
    push: jest.fn(),
    replace: jest.fn()
  })),
  useRoute: jest.fn(() => ({
    query: { name: '客厅空调' },
    path: '/air-conditioner'
  })),
  useRouter: jest.fn(() => ({
    push: jest.fn(),
    replace: jest.fn()
  }))
}))

// 2. 模拟 axios
jest.mock('axios')

// 3. 模拟主应用挂载
jest.mock('@/main.js', () => ({}))

describe('AirConditioner.vue', () => {
  let wrapper
  const mockRouterPush = jest.fn()
  const mockDeviceData = {
    id: 1,
    name: '客厅空调',
    type: 'AirConditioner',
    status: '1',
    temperature: 24,
    mode: 'cool',
    valid_modes: ['cool', 'heat', 'auto', 'dry', 'fan'],
    controls: {}
  }

  beforeEach(async () => {
    // 4. 重置所有mock
    jest.clearAllMocks()

    // 5. 设置路由mock返回值
    require('vue-router').useRouter.mockReturnValue({
      push: mockRouterPush,
      replace: jest.fn()
    })

    // 6. 模拟localStorage
    Storage.prototype.getItem = jest.fn(() => 'testuser')

    // 7. 配置axios响应
    axios.post.mockImplementation((url) => {
      if (url.includes('/airConditioner/')) {
        return Promise.resolve({
          data: {
            status: 'success',
            device: mockDeviceData
          }
        })
      }
      return Promise.resolve({ data: {} })
    })

    // 8. 挂载组件
    wrapper = mount(AirConditioner, {
      global: {
        mocks: {
          $route: {
            query: { name: '客厅空调' },
            path: '/air-conditioner'
          },
          $router: {
            push: mockRouterPush,
            replace: jest.fn()
          }
        }
      }
    })

    await flushPromises()
  })

  afterEach(() => {
    jest.clearAllMocks()
  })

  // 9. 基础渲染测试
  it('正确渲染组件', () => {
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.find('h1').exists()).toBe(true)
  })

  // 10. 设备信息显示测试
  it('加载完成后显示设备信息', async () => {
    await flushPromises()
    expect(wrapper.find('h1').text()).toBe('客厅空调')
    expect(wrapper.text()).toContain('当前温度: 24°C')
    expect(wrapper.text()).toContain('当前模式: cool')
  })

  // 11. 开关控制测试
  describe('开关控制', () => {
    it('点击开关按钮发送正确请求', async () => {
      await flushPromises()
      const powerButton = wrapper.find('button.bg-red-500')
      await powerButton.trigger('click')

      expect(axios.post).toHaveBeenCalledWith(
        expect.stringContaining('/airConditioner/'),
        expect.objectContaining({
          username: 'testuser',
          device_name: '客厅空调',
          new_status: '0'
        })
      )
    })
  })

  // 12. 温度控制测试
  describe('温度控制', () => {
    it('增加温度', async () => {
      await flushPromises()
      const buttons = wrapper.findAll('button')
      const plusButton = buttons.find(b => b.text() === '+')
      await plusButton.trigger('click')

      expect(axios.post).toHaveBeenCalledWith(
        expect.stringContaining('/airConditioner/'),
        expect.objectContaining({
          new_temperature: 25
        })
      )
    })
  })

  // 13. 模式切换测试
  describe('模式切换', () => {
    it('切换为制热模式', async () => {
      await flushPromises()
      const buttons = wrapper.findAll('button')
      const heatButton = buttons.find(b => b.text() === '制热')
      await heatButton.trigger('click')

      expect(axios.post).toHaveBeenCalledWith(
        expect.stringContaining('/airConditioner/'),
        expect.objectContaining({
          new_mode: 'heat'
        })
      )
    })
  })

  // 14. 设备重命名测试
  describe('设备重命名', () => {
    it('成功重命名设备', async () => {
      await flushPromises()
      const newName = '主卧空调'

      await wrapper.find('input[type="text"]').setValue(newName)
      await wrapper.find('button.bg-yellow-500').trigger('click')

      expect(axios.post).toHaveBeenCalledWith(
        expect.stringContaining('/airConditioner/'),
        expect.objectContaining({
          new_name: newName
        })
      )
    })
  })

  // 15. 返回按钮测试
  it('点击返回按钮跳转到首页', async () => {
    await flushPromises()
    const buttons = wrapper.findAll('button')
    const backButton = buttons.find(b => b.text() === '返回')
    await backButton.trigger('click')

    expect(mockRouterPush).toHaveBeenCalledWith({ name: 'Home' })
  })
})