import request from '@/utils/request'

export const getMonthlyStats = (params) => {
  return request({
    url: '/api/v1/statistics/monthly',
    method: 'get',
    params
  })
}

export const getDashboardStats = () => {
  return request({
    url: '/api/v1/statistics/dashboard',
    method: 'get'
  })
}

export const getServiceTypeStats = (params) => {
  return request({
    url: '/api/v1/statistics/service-types',
    method: 'get',
    params
  })
}

export const getCityStats = (params) => {
  return request({
    url: '/api/v1/statistics/cities',
    method: 'get',
    params
  })
}
