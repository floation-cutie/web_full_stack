import request from '@/utils/request'

export const getMyResponses = (params) => {
  return request({
    url: '/api/v1/service-responses/my',
    method: 'get',
    params
  })
}

export const createResponse = (data) => {
  return request({
    url: '/api/v1/service-responses',
    method: 'post',
    data
  })
}

export const getResponseDetail = (id) => {
  return request({
    url: `/api/v1/service-responses/${id}`,
    method: 'get'
  })
}

export const updateResponse = (id, data) => {
  return request({
    url: `/api/v1/service-responses/${id}`,
    method: 'put',
    data
  })
}

export const cancelResponse = (id) => {
  return request({
    url: `/api/v1/service-responses/${id}/cancel`,
    method: 'put'
  })
}
