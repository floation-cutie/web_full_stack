<template>
  <el-container class="home-container">
    <el-header class="header">
      <div class="header-content">
        <div class="logo">
          <el-icon :size="28"><House /></el-icon>
          <span class="logo-text">GoodServices</span>
        </div>
        <el-menu
          mode="horizontal"
          :default-active="activeMenu"
          class="nav-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="/home">Home</el-menu-item>
          <el-menu-item index="/needs">My Needs</el-menu-item>
          <el-menu-item index="/responses">My Responses</el-menu-item>
          <el-menu-item index="/stats">Statistics</el-menu-item>
        </el-menu>
        <div class="user-info">
          <el-dropdown @command="handleUserCommand">
            <span class="user-name">
              <el-icon><User /></el-icon>
              {{ userStore.userInfo.uname || 'User' }}
              <el-icon class="el-icon--right"><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">Profile</el-dropdown-item>
                <el-dropdown-item command="logout" divided>Logout</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </el-header>

    <el-main class="main-content">
      <div class="welcome-section">
        <el-card class="welcome-card">
          <h1>Welcome to GoodServices</h1>
          <p>Connect with your community for service needs and offers</p>
        </el-card>
      </div>

      <el-row :gutter="20" class="action-cards">
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="action-card" shadow="hover" @click="router.push('/needs/create')">
            <el-icon :size="48" color="#409EFF"><Plus /></el-icon>
            <h3>Publish Need</h3>
            <p>Post a service request</p>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="action-card" shadow="hover" @click="router.push('/needs')">
            <el-icon :size="48" color="#67C23A"><Document /></el-icon>
            <h3>My Needs</h3>
            <p>View my service requests</p>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="action-card" shadow="hover" @click="router.push('/responses')">
            <el-icon :size="48" color="#E6A23C"><ChatDotRound /></el-icon>
            <h3>My Responses</h3>
            <p>View my service responses</p>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="action-card" shadow="hover" @click="router.push('/stats')">
            <el-icon :size="48" color="#F56C6C"><DataAnalysis /></el-icon>
            <h3>Statistics</h3>
            <p>View service statistics</p>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  House,
  User,
  ArrowDown,
  Plus,
  Document,
  ChatDotRound,
  DataAnalysis
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const activeMenu = computed(() => router.currentRoute.value.path)

const handleMenuSelect = (index) => {
  router.push(index)
}

const handleUserCommand = async (command) => {
  if (command === 'profile') {
    router.push('/profile')
  } else if (command === 'logout') {
    try {
      await ElMessageBox.confirm('Are you sure you want to logout?', 'Confirm', {
        confirmButtonText: 'Logout',
        cancelButtonText: 'Cancel',
        type: 'warning'
      })
      userStore.logout()
      router.push('/login')
      ElMessage.success('Logged out successfully')
    } catch {
      // User cancelled
    }
  }
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.header {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 20px;
  font-weight: bold;
  color: #409EFF;
}

.nav-menu {
  flex: 1;
  border-bottom: none;
  margin: 0 40px;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-name {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-name:hover {
  background-color: #f5f7fa;
}

.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px 20px;
}

.welcome-section {
  margin-bottom: 40px;
}

.welcome-card {
  text-align: center;
  padding: 40px;
}

.welcome-card h1 {
  font-size: 36px;
  color: #303133;
  margin-bottom: 16px;
}

.welcome-card p {
  font-size: 18px;
  color: #909399;
}

.action-cards {
  margin-top: 20px;
}

.action-card {
  text-align: center;
  padding: 30px;
  cursor: pointer;
  transition: transform 0.3s;
}

.action-card:hover {
  transform: translateY(-5px);
}

.action-card h3 {
  margin: 16px 0 8px;
  font-size: 20px;
  color: #303133;
}

.action-card p {
  color: #909399;
  font-size: 14px;
}

@media (max-width: 768px) {
  .nav-menu {
    display: none;
  }

  .welcome-card h1 {
    font-size: 24px;
  }

  .action-cards {
    margin-top: 10px;
  }
}
</style>
