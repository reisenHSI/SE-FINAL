import { mount, flushPromises } from '@vue/test-utils'
import AddDevices from '@/views/AddDevice.vue'

describe('AddDevices.vue', () => {
  let wrapper
  const mockRouter = {
    push: jest.fn()
  }
  const mockAxios = {
    post: jest.fn(),
    defaults: {
      baseURL: 'http://127.0.0.1:8000/'
    }
  }

  beforeEach(() => {
    document.body.innerHTML = '<div id="app"></div>'
    Storage.prototype.getItem = jest.fn(() => 'testuser')

    wrapper = mount(AddDevices, {
      global: {
        mocks: {
          $router: mockRouter,
          $axios: mockAxios
        }
      }
    })
  })

  afterEach(() => {
    jest.clearAllMocks()
    document.body.innerHTML = ''
  })

  it('正确渲染表单', () => {
    expect(wrapper.find('h2').text()).toBe('添加设备')
    expect(wrapper.find('#deviceName').exists()).toBe(true)
    expect(wrapper.find('#deviceType').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').text()).toBe('添加设备')
    expect(wrapper.find('button.back-btn').text()).toBe('返回主页')
  })

  it('显示所有设备类型选项', () => {
    const options = wrapper.findAll('#deviceType option')
    expect(options).toHaveLength(6)
    expect(options[1].text()).toBe('灯光')
    expect(options[1].attributes('value')).toBe('Light')
  })

  it('设备名称为空时显示警告', async () => {
    window.alert = jest.fn()
    await wrapper.find('#deviceName').setValue('')
    await wrapper.find('form').trigger('submit.prevent')
    expect(window.alert).toHaveBeenCalledWith('设备名称不能为空')
    expect(mockAxios.post).not.toHaveBeenCalled()
  })

  it('成功提交时使用正确数据调用API', async () => {
    mockAxios.post.mockResolvedValueOnce({
      data: { status: 'success' }
    })

    window.alert = jest.fn()

    await wrapper.find('#deviceName').setValue('Test Device')
    await wrapper.find('#deviceType').setValue('Light')
    await wrapper.find('form').trigger('submit.prevent')
    await flushPromises()

    expect(mockAxios.post).toHaveBeenCalledWith(
      'http://127.0.0.1:8000/home/add_delete/add_device/',
      {
        device_name: 'Test Device',
        device_type: 'Light',
        username: 'testuser'
      }
    )
    expect(window.alert).toHaveBeenCalledWith('设备添加成功！')
    expect(mockRouter.push).toHaveBeenCalledWith({ name: 'Home' })
  })

  it('网络错误时显示通用错误', async () => {
    mockAxios.post.mockRejectedValueOnce(new Error('Network Error'))
    window.alert = jest.fn()

    await wrapper.find('#deviceName').setValue('Test Device')
    await wrapper.find('#deviceType').setValue('AirConditioner')
    await wrapper.find('form').trigger('submit.prevent')
    await flushPromises()

    expect(window.alert).toHaveBeenCalledWith('添加设备失败，请稍后重试')
  })

  it('点击返回按钮导航到主页', async () => {
    await wrapper.find('.back-btn').trigger('click')
    expect(mockRouter.push).toHaveBeenCalledWith({ name: 'Home' })
  })
})