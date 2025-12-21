import request from '@/utils/request'

export const getMonthlyStats = (params) => {
  return request({
    url: '/api/v1/stats/monthly',
    method: 'get',
    params
  })
}

export const getDashboardStats = () => {
  return request({
    url: '/api/v1/stats/dashboard',
    method: 'get'
  })
}

export const getServiceTypeStats = (params) => {
  return request({
    url: '/api/v1/stats/service-types',
    method: 'get',
    params
  })
}

export const getCityStats = (params) => {
  return request({
    url: '/api/v1/stats/cities',
    method: 'get',
    params
  })
}
