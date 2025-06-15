import { mount, flushPromises } from '@vue/test-utils'
import Curtain from '@/views/devices/Curtain.vue'
import axios from 'axios'

// 完整模拟 vue-router
jest.mock('vue-router', () => ({
  createWebHashHistory: jest.fn(),
  createRouter: jest.fn(),
  useRoute: jest.fn(() => ({
    query: { name: '客厅窗帘' }
  })),
  useRouter: jest.fn(() => ({
    push: jest.fn()
  }))
}))

// 模拟主应用入口文件
jest.mock('@/main.js', () => ({}))

// 模拟 axios
jest.mock('axios')

// 模拟 localStorage
const localStorageMock = {
  getItem: jest.fn(() => 'testuser')
}
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock
})

// 模拟全局 alert
global.alert = jest.fn()

describe('Curtain.vue', () => {
  let wrapper
  const mockDeviceData = {
    id: 1,
    name: '客厅窗帘',
    type: 'Curtain',
    status: '0',
    controls: {}
  }

  beforeEach(async () => {
    jest.clearAllMocks()

    axios.post.mockImplementation((url) => {
      if (url.includes('/home/devices/curtain/')) {
        return Promise.resolve({
          data: {
            status: 'success',
            device: mockDeviceData
          }
        })
      }
      return Promise.resolve({ data: {} })
    })

    wrapper = mount(Curtain, {
      global: {
        mocks: {
          $route: {
            query: { name: '客厅窗帘' }
          },
          $router: {
            push: jest.fn()
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
    expect(wrapper.find('h1').text()).toBe('客厅窗帘')
    expect(wrapper.text()).toContain('设备类型: Curtain')
  })

  describe('窗帘控制', () => {
    it('初始状态为关闭', async () => {
      expect(wrapper.vm.isOpen).toBe(false)
      const toggleButton = wrapper.findAll('button').find(btn =>
        btn.text().match(/打开|关闭/)
      )
      expect(toggleButton.exists()).toBe(true)
      expect(toggleButton.text()).toContain('打开')
    })

    it('点击按钮切换窗帘状态', async () => {
      axios.post.mockClear()
      axios.post.mockResolvedValueOnce({
        data: {
          status: 'success',
          device: { ...mockDeviceData, status: '1' }
        }
      })

      const toggleButton = wrapper.findAll('button').find(btn =>
        btn.text().match(/打开|关闭/)
      )
      await toggleButton.trigger('click')

      expect(axios.post).toHaveBeenCalledWith(
        expect.stringContaining('/home/devices/curtain/'),
        expect.objectContaining({
          new_status: '1'
        })
      )

      await flushPromises()
      expect(wrapper.vm.isOpen).toBe(true)
    })
  })

  it('显示正确的窗帘动画状态', async () => {
    const curtains = wrapper.findAll('.bg-blue-300')
    expect(curtains[0].attributes('style')).toContain('width: 50%')
    expect(curtains[1].attributes('style')).toContain('width: 50%')

    wrapper.vm.isOpen = true
    await wrapper.vm.$nextTick()

    expect(curtains[0].attributes('style')).toContain('width: 0%')
    expect(curtains[1].attributes('style')).toContain('width: 0%')
  })

  describe('设备重命名', () => {
    it('成功重命名设备', async () => {
      const newName = '主卧窗帘'
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
      expect(global.alert).toHaveBeenCalledWith('重命名成功')
    })

    it('空名称时显示警告', async () => {
      axios.post.mockClear()
      await wrapper.find('input[type="text"]').setValue('')
      await wrapper.find('.bg-yellow-500').trigger('click')

      expect(global.alert).toHaveBeenCalledWith('设备名称不能为空')
      expect(axios.post).not.toHaveBeenCalled()
    })
  })
})