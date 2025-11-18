import request from '@/utils/request'

export const getMyNeeds = (params) => {
  return request({
    url: '/api/v1/service-requests/my-needs',
    method: 'get',
    params
  })
}

export const createNeed = (data) => {
  return request({
    url: '/api/v1/service-requests',
    method: 'post',
    data
  })
}

export const getNeedDetail = (id) => {
  return request({
    url: `/api/v1/service-requests/${id}`,
    method: 'get'
  })
}

export const updateNeed = (id, data) => {
  return request({
    url: `/api/v1/service-requests/${id}`,
    method: 'put',
    data
  })
}

export const deleteNeed = (id) => {
  return request({
    url: `/api/v1/service-requests/${id}`,
    method: 'delete'
  })
}

export const cancelNeed = (id) => {
  return request({
    url: `/api/v1/service-requests/${id}/cancel`,
    method: 'post'
  })
}

export const getNeedResponses = (id, params) => {
  return request({
    url: `/api/v1/service-requests/${id}/responses`,
    method: 'get',
    params
  })
}

export const getAllNeeds = (params) => {
  return request({
    url: '/api/v1/service-requests',
    method: 'get',
    params
  })
}
