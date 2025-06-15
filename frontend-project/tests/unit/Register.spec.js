import { mount, flushPromises } from '@vue/test-utils'
import Register from '@/views/Register.vue'
import axios from 'axios'

// Mock axios
jest.mock('axios')

describe('Register.vue', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(Register, {
      global: {
        mocks: {
          $router: {
            push: jest.fn(),
            go: jest.fn(),
          },
        },
      },
    })
  })

  afterEach(() => {
    jest.clearAllMocks()
  })

  it('should show error if passwords do not match', async () => {
    await wrapper.find('#username').setValue('testuser')
    await wrapper.find('#phone').setValue('1234567890')
    await wrapper.find('#age').setValue('25')
    await wrapper.find('#password').setValue('password123')
    await wrapper.find('#confirmPassword').setValue('wrongpassword')

    await wrapper.find('form').trigger('submit.prevent')
    await flushPromises()

    expect(wrapper.text()).toContain('两次输入的密码不一致')
  })

  it('should call API and navigate to login on success', async () => {
    // mock axios response
    axios.post.mockResolvedValueOnce({
      data: { status: 'success' }
    })

    await wrapper.find('#username').setValue('testuser')
    await wrapper.find('#phone').setValue('1234567890')
    await wrapper.find('#age').setValue('25')
    await wrapper.find('#password').setValue('password123')
    await wrapper.find('#confirmPassword').setValue('password123')

    await wrapper.find('form').trigger('submit.prevent')
    await flushPromises()

    expect(axios.post).toHaveBeenCalled()
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/login')
  })

  it('should show error if API fails', async () => {
    axios.post.mockRejectedValueOnce({
      response: {
        data: {
          message: '用户已存在'
        }
      }
    })

    await wrapper.find('#username').setValue('existinguser')
    await wrapper.find('#phone').setValue('1234567890')
    await wrapper.find('#age').setValue('30')
    await wrapper.find('#password').setValue('123456')
    await wrapper.find('#confirmPassword').setValue('123456')

    await wrapper.find('form').trigger('submit.prevent')
    await flushPromises()

    expect(wrapper.text()).toContain('用户已存在')
  })
})
