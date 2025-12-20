<template>
  <el-container class="layout-container">
    <el-header class="layout-header">
      <div class="header-content">
        <div class="logo">
          <el-icon><Service /></el-icon>
          <span>GoodServices</span>
        </div>
        <el-menu
          :default-active="activeMenu"
          mode="horizontal"
          :ellipsis="false"
          @select="handleMenuSelect"
        >
          <el-menu-item index="/home">
            <el-icon><HomeFilled /></el-icon>
            <span>Dashboard</span>
          </el-menu-item>
          <el-menu-item index="/needs">
            <el-icon><Document /></el-icon>
            <span>My Needs</span>
          </el-menu-item>
          <el-menu-item index="/responses">
            <el-icon><ChatDotRound /></el-icon>
            <span>My Responses</span>
          </el-menu-item>
          <el-menu-item index="/browse-needs">
            <el-icon><Search /></el-icon>
            <span>Browse Needs</span>
          </el-menu-item>
          <el-menu-item index="/stats">
            <el-icon><DataAnalysis /></el-icon>
            <span>Statistics</span>
          </el-menu-item>
        </el-menu>
        <div class="user-info">
          <el-dropdown @command="handleCommand">
            <span class="user-dropdown">
              <el-icon><User /></el-icon>
              <span>{{ userStore.userInfo.uname || 'User' }}</span>
              <el-icon><CaretBottom /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>
                  Profile
                </el-dropdown-item>
                <el-dropdown-item command="logout" divided>
                  <el-icon><SwitchButton /></el-icon>
                  Logout
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </el-header>
    <el-main class="layout-main">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessageBox } from 'element-plus'
import {
  Service,
  HomeFilled,
  Document,
  ChatDotRound,
  DataAnalysis,
  User,
  CaretBottom,
  SwitchButton,
  Search
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const activeMenu = computed(() => {
  return '/' + route.path.split('/')[1]
})

const handleMenuSelect = (index) => {
  router.push(index)
}

const handleCommand = async (command) => {
  if (command === 'profile') {
    router.push('/profile')
  } else if (command === 'logout') {
    try {
      await ElMessageBox.confirm(
        'Are you sure you want to logout?',
        'Confirm Logout',
        {
          confirmButtonText: 'Logout',
          cancelButtonText: 'Cancel',
          type: 'warning'
        }
      )
      userStore.logout()
      router.push('/login')
    } catch {
      // User cancelled
    }
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.layout-header {
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  padding: 0 20px;
}

.header-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.logo {
  display: flex;
  align-items: center;
  margin-right: 40px;
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
}

.logo .el-icon {
  margin-right: 8px;
  font-size: 24px;
}

.el-menu {
  flex: 1;
  border: none;
}

.user-info {
  margin-left: auto;
}

.user-dropdown {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 0 12px;
}

.user-dropdown span {
  margin: 0 4px;
}

.layout-main {
  background: #f0f2f5;
  overflow-y: auto;
}
</style>
