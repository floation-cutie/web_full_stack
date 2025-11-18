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
  { id: 1, name: '北京', value: 'beijing' },
  { id: 2, name: '上海', value: 'shanghai' },
  { id: 3, name: '广州', value: 'guangzhou' },
  { id: 4, name: '深圳', value: 'shenzhen' },
  { id: 5, name: '杭州', value: 'hangzhou' },
  { id: 6, name: '成都', value: 'chengdu' },
  { id: 7, name: '武汉', value: 'wuhan' },
  { id: 8, name: '西安', value: 'xian' }
]

export const PAGE_SIZES = [10, 20, 50, 100]
export const DEFAULT_PAGE_SIZE = 10
