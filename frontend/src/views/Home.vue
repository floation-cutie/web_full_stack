<template>
  <div class="home-page">
    <div class="welcome-section">
      <el-card class="welcome-card">
        <h1>欢迎来到好服务</h1>
        <p>与您的社区连接，高效对接服务需求与响应</p>
      </el-card>
    </div>


    <el-row :gutter="20" class="action-cards">
      <el-col :xs="24" :sm="12" :md="4">
        <el-card class="action-card" shadow="hover" @click="router.push('/needs/create')">
          <el-icon :size="48" color="#409EFF"><Plus /></el-icon>
          <h3>发布需求</h3>
          <p>填写发布服务需求信息</p>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="4">
        <el-card class="action-card" shadow="hover" @click="router.push('/needs')">
          <el-icon :size="48" color="#67C23A"><Document /></el-icon>
          <h3>我的需求</h3>
          <p>查看我的服务请求</p>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="4">
        <el-card class="action-card" shadow="hover" @click="router.push('/responses')">
          <el-icon :size="48" color="#E6A23C"><ChatDotRound /></el-icon>
          <h3>我的响应</h3>
          <p>查看我的服务响应</p>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="4" v-if="isAdmin">
        <el-card class="action-card" shadow="hover" @click="router.push('/stats')">
          <el-icon :size="48" color="#F56C6C"><DataAnalysis /></el-icon>
          <h3>数据统计</h3>
          <p>查看服务统计数据</p>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="4">
        <el-card class="action-card" shadow="hover" @click="router.push('/browse-needs')">
          <el-icon :size="48" color="#909399"><Search /></el-icon>
          <h3>浏览需求</h3>
          <p>查找服务需求信息</p>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="4">
        <el-card class="action-card" shadow="hover" @click="router.push('/profile')">
          <el-icon :size="48" color="#409EFF"><User /></el-icon>
          <h3>我的资料</h3>
          <p>管理您的个人资料</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { computed } from 'vue'
import {
  Plus,
  Document,
  ChatDotRound,
  DataAnalysis,
  Search,
  User
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

// 计算属性：检查当前用户是否为管理员
const isAdmin = computed(() => {
  return userStore.userInfo?.userlvl === 'admin'
})
</script>

<style scoped>
.home-page {
  padding: 20px;
}

.welcome-section {
  margin-bottom: 30px;
}

.welcome-card {
  text-align: center;
  padding: 40px;
}

.welcome-card h1 {
  font-size: 32px;
  color: #303133;
  margin-bottom: 12px;
}

.welcome-card p {
  font-size: 16px;
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
  margin-bottom: 20px;
}

.action-card:hover {
  transform: translateY(-5px);
}

.action-card h3 {
  margin: 16px 0 8px;
  font-size: 18px;
  color: #303133;
}

.action-card p {
  color: #909399;
  font-size: 14px;
}
</style>
