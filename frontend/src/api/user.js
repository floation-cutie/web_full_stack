import request from '@/utils/request'

export const getUserProfile = () => {
  return request({
    url: '/api/v1/users/profile',
    method: 'get'
  })
}

export const updateUserProfile = (data) => {
  return request({
    url: '/api/v1/users/profile',
    method: 'put',
    data
  })
}

export const changePassword = (data) => {
  return request({
    url: '/api/v1/users/change-password',
    method: 'post',
    data
  })
}

export const getCities = () => {
  return request({
    url: '/api/v1/cities',
    method: 'get'
  })
}

export const getServiceTypes = () => {
  return request({
    url: '/api/v1/service-types',
    method: 'get'
  })
}
