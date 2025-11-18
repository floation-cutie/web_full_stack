import request from '@/utils/request'

export const login = (data) => {
  return request({
    url: '/api/v1/auth/login',
    method: 'post',
    data
  })
}

export const register = (data) => {
  return request({
    url: '/api/v1/auth/register',
    method: 'post',
    data
  })
}

export const logout = () => {
  return request({
    url: '/api/v1/auth/logout',
    method: 'post'
  })
}

export const getCurrentUser = () => {
  return request({
    url: '/api/v1/auth/me',
    method: 'get'
  })
}
