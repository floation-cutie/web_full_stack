import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import MainLayout from '@/layouts/MainLayout.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: MainLayout,
    redirect: '/home',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'home',
        name: 'Home',
        component: () => import('@/views/Home.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'needs',
        name: 'MyNeeds',
        component: () => import('@/views/needs/MyNeeds.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'needs/create',
        name: 'CreateNeed',
        component: () => import('@/views/needs/CreateNeed.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'needs/:id',
        name: 'NeedDetail',
        component: () => import('@/views/needs/NeedDetail.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'needs/edit/:id',
        name: 'EditNeed',
        component: () => import('@/views/needs/EditNeed.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'browse-needs',
        name: 'BrowseNeeds',
        component: () => import('@/views/needs/BrowseNeeds.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'responses',
        name: 'MyResponses',
        component: () => import('@/views/responses/MyResponses.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'responses/create/:needId',
        name: 'CreateResponse',
        component: () => import('@/views/responses/CreateResponse.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'responses/edit/:id',
        name: 'EditResponse',
        component: () => import('@/views/responses/EditResponse.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'stats',
        name: 'Statistics',
        component: () => import('@/views/stats/Statistics.vue'),
        meta: { requiresAuth: true, requiresAdmin: true }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/user/Profile.vue'),
        meta: { requiresAuth: true }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  if (to.meta.requiresAuth && !userStore.token) {
    next('/login')
  } else if (to.meta.requiresAdmin && userStore.userInfo?.userlvl !== 'admin') {
    // 如果路由需要管理员权限但用户不是管理员，重定向到首页
    next('/home')
  } else if (to.path === '/login' && userStore.token) {
    next('/home')
  } else {
    next()
  }
})

export default router
