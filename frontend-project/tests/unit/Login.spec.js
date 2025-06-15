import { mount } from '@vue/test-utils'
import Login from '@/views/Login.vue'
import axios from 'axios'

jest.mock('axios')

describe('Login.vue', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(Login, {
      global: {
        mocks: {
          $router: { push: jest.fn() }
        }
      }
    })
  })

  it('渲染登录表单', () => {
    expect(wrapper.find('input#username').exists()).toBe(true)
    expect(wrapper.find('input#password').exists()).toBe(true)
  })

  it('登录成功后跳转到 /home', async () => {
    axios.post.mockResolvedValue({ data: { status: 'success' } })

    await wrapper.find('#username').setValue('admin')
    await wrapper.find('#password').setValue('123456')
    await wrapper.find('form').trigger('submit.prevent')

    expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/home')
  })
})
