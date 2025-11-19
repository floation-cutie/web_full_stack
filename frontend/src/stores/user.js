import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginApi, register as registerApi } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || '{}'))

  const isLoggedIn = computed(() => !!token.value)

  async function login(credentials) {
    console.log('Store: Attempting login', credentials.username)
    const res = await loginApi(credentials)
    console.log('Store: Login response received', res)
    // Axios interceptor returns response.data, so res = { code, message, data: {...} }
    token.value = res.data.token
    userInfo.value = res.data.user_info
    console.log('Store: Token set:', token.value ? 'YES' : 'NO')
    console.log('Store: User info set:', userInfo.value)
    localStorage.setItem('token', token.value)
    localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
  }

  async function register(userData) {
    const res = await registerApi(userData)
    return res
  }

  function logout() {
    token.value = ''
    userInfo.value = {}
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    login,
    register,
    logout
  }
})
