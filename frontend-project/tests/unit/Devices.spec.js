import { mount, flushPromises } from '@vue/test-utils'
import Devices from '@/views/Devices.vue'
import axios from 'axios'
import { nextTick } from 'vue'

jest.mock('axios')

const mockRouterPush = jest.fn()

const createWrapper = async (devicesData = [], filter = 'all') => {
  axios.post.mockResolvedValue({
    data: {
      status: 'success',
      device_categories: devicesData,
    },
  })

  const wrapper = mount(Devices, {
    props: { filter },
    global: {
      mocks: {
        $router: {
          push: mockRouterPush,
        },
        $message: {
          error: jest.fn(),
        },
        localStorage: {
          getItem: () => 'test-user',
        },
      },
    },
  })

  await flushPromises()
  return wrapper
}

describe('Devices.vue', () => {
  afterEach(() => {
    jest.clearAllMocks()
  })

  it('should display "当前没有设备" if devices list is empty', async () => {
    const wrapper = await createWrapper([])

    expect(wrapper.text()).toContain('当前没有设备')
  })

  it('should render devices correctly', async () => {
    const devicesData = [
      {
        type: 'Light',
        icon: 'light-icon',
        devices: [
          { id: 1, name: '灯1' },
          { id: 2, name: '灯2' },
        ],
      },
    ]

    const wrapper = await createWrapper(devicesData)

    expect(wrapper.findAll('.device-row').length).toBe(2)
    expect(wrapper.text()).toContain('灯1')
    expect(wrapper.text()).toContain('灯2')
  })

  it('should filter devices by type', async () => {
    const devicesData = [
      {
        type: 'Light',
        icon: 'light-icon',
        devices: [{ id: 1, name: '灯1' }],
      },
      {
        type: 'Curtain',
        icon: 'curtain-icon',
        devices: [{ id: 2, name: '窗帘1' }],
      },
    ]

    const wrapper = await createWrapper(devicesData, 'curtain')

    const deviceNames = wrapper.findAll('.device-name').map(d => d.text())
    expect(deviceNames).toEqual(['窗帘1'])
  })

  it('should call router.push when clicking "添加设备"', async () => {
    const wrapper = await createWrapper([])

    await wrapper.find('.add-btn').trigger('click')
    expect(mockRouterPush).toHaveBeenCalledWith({ name: 'AddDevice' })
  })

  it('should call router.push with correct query when clicking 删除按钮', async () => {
    const devicesData = [
      {
        type: 'Light',
        icon: 'light-icon',
        devices: [{ id: 1, name: '灯1' }],
      },
    ]
    const wrapper = await createWrapper(devicesData)

    await wrapper.find('.delete-btn').trigger('click')
    expect(mockRouterPush).toHaveBeenCalledWith({
      name: 'DeleteDevice',
      query: { id: 1, name: '灯1' },
    })
  })

  it('should show error message for unknown device type when clicking 控制', async () => {
    const errorMock = jest.fn()
    const wrapper = await mount(Devices, {
      props: { filter: 'all' },
      data() {
        return {
          devices: [
            {
              id: 999,
              name: '未知设备',
              type: 'unknown',
              icon: 'unknown-icon',
            },
          ],
        }
      },
      global: {
        mocks: {
          $router: { push: mockRouterPush },
          $message: { error: errorMock },
        },
      },
    })

    await wrapper.find('.control-btn').trigger('click')
    expect(errorMock).toHaveBeenCalledWith('暂不支持该设备类型！')
  })
})
