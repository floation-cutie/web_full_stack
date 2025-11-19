export const SERVICE_TYPES = [
  { id: 1, name: '水电维修', value: 'plumbing' },
  { id: 2, name: '养老服务', value: 'elderly_care' },
  { id: 3, name: '保洁服务', value: 'cleaning' },
  { id: 4, name: '医疗护理', value: 'medical' },
  { id: 5, name: '送餐服务', value: 'meals' },
  { id: 6, name: '出行陪伴', value: 'transportation' }
]

export const SERVICE_REQUEST_STATUS = {
  PUBLISHED: 0,
  CANCELLED: -1
}

export const RESPONSE_STATUS = {
  PENDING: 0,
  ACCEPTED: 1,
  REJECTED: 2,
  CANCELLED: 3
}

export const RESPONSE_STATUS_TEXT = {
  0: '待处理',
  1: '已接受',
  2: '已拒绝',
  3: '已取消'
}

export const RESPONSE_STATUS_TYPE = {
  0: 'warning',
  1: 'success',
  2: 'info',
  3: 'info'
}

export const CITIES = [
  { id: 110100, name: '北京市' },
  { id: 310100, name: '上海市' },
  { id: 440100, name: '广州市' },
  { id: 440300, name: '深圳市' },
  { id: 330100, name: '杭州市' },
  { id: 510100, name: '成都市' },
  { id: 420100, name: '武汉市' },
  { id: 610100, name: '西安市' }
]

export const PAGE_SIZES = [10, 20, 50, 100]
export const DEFAULT_PAGE_SIZE = 10
