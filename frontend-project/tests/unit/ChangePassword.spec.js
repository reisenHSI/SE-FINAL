import { mount } from '@vue/test-utils'
import ChangePassword from '@/views/ChangePassword.vue'
import axios from 'axios'
import flushPromises from 'flush-promises'

// 模拟 axios
jest.mock('axios')

describe('ChangePassword.vue', () => {
  const pushMock = jest.fn()

  const wrapperFactory = () =>
    mount(ChangePassword, {
      global: {
        mocks: {
          $router: {
            push: pushMock
          }
        }
      }
    })

  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('表单应正常渲染', () => {
    const wrapper = wrapperFactory()
    expect(wrapper.find('input#username').exists()).toBe(true)
    expect(wrapper.find('input#old_password').exists()).toBe(true)
    expect(wrapper.find('input#new_password').exists()).toBe(true)
    expect(wrapper.find('input#confirm_new_password').exists()).toBe(true)
  })

  it('新密码与确认密码不一致时应显示错误', async () => {
    const wrapper = wrapperFactory()

    await wrapper.setData({
      username: 'testuser',
      oldPassword: 'old123',
      newPassword: 'new123',
      confirmNewPassword: 'new456'
    })

    await wrapper.find('form').trigger('submit.prevent')
    expect(wrapper.text()).toContain('新密码和确认密码不一致')
  })

  it('提交成功后跳转到登录页', async () => {
    axios.post.mockResolvedValue({
      data: {
        status: 'success',
        message: '修改成功'
      }
    })

    window.alert = jest.fn()

    const wrapper = wrapperFactory()
    await wrapper.setData({
      username: 'testuser',
      oldPassword: 'old123',
      newPassword: 'new123',
      confirmNewPassword: 'new123'
    })

    await wrapper.find('form').trigger('submit.prevent')
    await flushPromises()

    expect(axios.post).toHaveBeenCalledWith(
      expect.stringContaining('/change_password/'),
      {
        username: 'testuser',
        old_password: 'old123',
        new_password: 'new123',
        confirm_new_password: 'new123'
      },
      { withCredentials: true }
    )

    expect(window.alert).toHaveBeenCalledWith('修改成功')
    expect(pushMock).toHaveBeenCalledWith('/login')
  })

  it('提交失败后显示后端返回的错误', async () => {
    axios.post.mockResolvedValue({
      data: {
        status: 'fail',
        message: '原密码错误'
      }
    })

    const wrapper = wrapperFactory()
    await wrapper.setData({
      username: 'testuser',
      oldPassword: 'wrongold',
      newPassword: 'newpass',
      confirmNewPassword: 'newpass'
    })

    await wrapper.find('form').trigger('submit.prevent')
    await flushPromises()

    expect(wrapper.text()).toContain('原密码错误')
  })

  it('网络错误时显示默认错误信息', async () => {
    axios.post.mockRejectedValue({
      response: {
        data: { message: '服务器异常' }
      }
    })

    const wrapper = wrapperFactory()
    await wrapper.setData({
      username: 'testuser',
      oldPassword: 'old123',
      newPassword: 'new123',
      confirmNewPassword: 'new123'
    })

    await wrapper.find('form').trigger('submit.prevent')
    await flushPromises()

    expect(wrapper.text()).toContain('服务器异常')
  })

  it('点击返回跳转到登录页', async () => {
    const wrapper = wrapperFactory()
    await wrapper.find('.back-link').trigger('click')
    expect(pushMock).toHaveBeenCalledWith('/login')
  })
})
