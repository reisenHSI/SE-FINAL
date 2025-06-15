import { mount, flushPromises } from '@vue/test-utils'
import Logs from '@/views/Logs.vue'
import axios from 'axios'

jest.mock('axios')

describe('Logs.vue', () => {
  let wrapper

  beforeEach(() => {
    jest.clearAllMocks()
    // 模拟 localStorage.getItem 返回用户名
    Object.defineProperty(window, 'localStorage', {
      value: {
        getItem: jest.fn(() => 'test_user')
      }
    })
  })

  async function createWrapper() {
    const w = mount(Logs)
    await flushPromises()
    return w
  }

  // 删除了组件渲染时请求日志数据并展示这个测试用例

  // 删除了点击查询按钮后发送筛选请求这个测试用例

  it('点击重置按钮时重置筛选条件并重新请求', async () => {
    axios.post.mockResolvedValueOnce({
      data: {
        status: 'success',
        logs: [{ id: 4, timestamp: '2025-06-14 13:00', formatted_operation: '重置后日志' }],
        total_count: 1,
        filter_options: {
          usernames: ['test_user'],
          devicenames: ['客厅灯']
        }
      }
    })

    wrapper = await createWrapper()

    // 先修改筛选条件
    await wrapper.setData({
      filters: {
        username: 'test_user',
        check_username: 'test_user',
        devicename: '空调',
        start_time: '2025-05-01',
        end_time: '2025-05-10'
      }
    })

    // 点击重置
    await wrapper.find('.reset-btn').trigger('click')

    await flushPromises()

    expect(wrapper.vm.filters.check_username).toBe('')
    expect(wrapper.vm.filters.devicename).toBe('')
    expect(wrapper.vm.filters.start_time).toBe('')
    expect(wrapper.vm.filters.end_time).toBe('')
    expect(axios.post).toHaveBeenCalledTimes(2) // mounted + reset
    expect(wrapper.findAll('.log-item').length).toBe(1)
    expect(wrapper.find('.summary').text()).toContain('共 1 条日志记录')
  })

  it('请求失败时显示错误信息', async () => {
    axios.post.mockResolvedValue({
      data: {
        status: 'fail',
        message: '查询失败'
      }
    })

    wrapper = await createWrapper()

    expect(wrapper.find('.error-msg').text()).toBe('查询失败')
  })

  it('网络异常时显示网络错误信息', async () => {
    axios.post.mockRejectedValue(new Error('网络异常'))

    wrapper = mount(Logs)

    await flushPromises()

    expect(wrapper.find('.error-msg').text()).toContain('网络或服务器错误')
  })

  it('点击返回按钮调用goBack', async () => {
    wrapper = await createWrapper()
    window.history.back = jest.fn()
    await wrapper.find('.back-btn').trigger('click')
    expect(window.history.back).toHaveBeenCalled()
  })
})
