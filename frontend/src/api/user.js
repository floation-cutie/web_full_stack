import request from '@/utils/request'

export const getUserProfile = () => {
  return request({
    url: '/api/v1/users/me',
    method: 'get'
  })
}

export const updateUserProfile = (data) => {
  return request({
    url: '/api/v1/users/me',
    method: 'put',
    data
  })
}

export const changePassword = (data) => {
  return request({
    url: '/api/v1/users/me/password',
    method: 'put',
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
