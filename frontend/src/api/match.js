import request from '@/utils/request'

export const acceptResponse = (response_id) => {
  return request({
    url: `/api/v1/match/accept/${response_id}`,
    method: 'post'
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
