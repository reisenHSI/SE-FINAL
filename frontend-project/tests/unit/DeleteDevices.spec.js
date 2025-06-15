import { mount } from '@vue/test-utils'
import DeleteDevices from '@/views/DeleteDevice.vue'
import axios from 'axios'
import { nextTick } from 'vue'

// 模拟 axios
jest.mock('axios')

describe('DeleteDevices.vue', () => {
  const pushMock = jest.fn()
  const backMock = jest.fn()
  const messageMock = {
    success: jest.fn(),
    error: jest.fn(),
  }

  const wrapperFactory = (options = {}) => {
    return mount(DeleteDevices, {
      global: {
        mocks: {
          $router: {
            push: pushMock,
            back: backMock,
          },
          $message: messageMock,
          $route: {
            query: {
              id: '123',
              name: '测试设备',
            },
          },
        },
      },
      ...options,
    })
  }

  beforeEach(() => {
    jest.clearAllMocks()
    localStorage.setItem('username', 'testuser')
  })

  it('渲染设备信息', () => {
    const wrapper = wrapperFactory()
    expect(wrapper.text()).toContain('测试设备')
    expect(wrapper.text()).toContain('ID: 123')
  })

  it('点击取消按钮会返回上一页', async () => {
    const wrapper = wrapperFactory()
    await wrapper.find('.btn-cancel').trigger('click')
    expect(backMock).toHaveBeenCalled()
  })

  it('点击确认删除按钮发送请求并成功处理', async () => {
    axios.post.mockResolvedValue({
      data: {
        status: 'success',
      },
    })

    const wrapper = wrapperFactory()
    await wrapper.find('.btn-delete').trigger('click')
    await nextTick()

    expect(axios.post).toHaveBeenCalledWith(
      expect.stringContaining('/delete_device/'),
      {
        device_name: '测试设备',
        username: 'testuser',
      },
      { withCredentials: true }
    )

    expect(messageMock.success).toHaveBeenCalledWith(
      '已成功删除设备: 测试设备 (ID: 123)'
    )
    expect(pushMock).toHaveBeenCalledWith({ name: 'Home' })
  })

  it('点击确认删除按钮请求失败时显示错误信息', async () => {
    axios.post.mockResolvedValue({
      data: {
        status: 'fail',
        message: '设备不存在',
      },
    })

    const wrapper = wrapperFactory()
    await wrapper.find('.btn-delete').trigger('click')
    await nextTick()

    expect(messageMock.error).toHaveBeenCalledWith('设备不存在')
    expect(pushMock).not.toHaveBeenCalled()
  })

  it('点击确认删除按钮请求异常时捕获错误', async () => {
    axios.post.mockRejectedValue({
      response: {
        data: { message: '服务器异常' },
      },
    })

    const wrapper = wrapperFactory()
    await wrapper.find('.btn-delete').trigger('click')
    await nextTick()

    expect(messageMock.error).toHaveBeenCalledWith('服务器异常')
  })
})
