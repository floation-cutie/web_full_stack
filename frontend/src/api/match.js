import request from '@/utils/request'

export const acceptResponse = (data) => {
  return request({
    url: '/api/v1/matches/accept',
    method: 'post',
    data
  })
}

export const getMyMatches = (params) => {
  return request({
    url: '/api/v1/matches/my-matches',
    method: 'get',
    params
  })
}

export const getMatchDetail = (id) => {
  return request({
    url: `/api/v1/matches/${id}`,
    method: 'get'
  })
}
