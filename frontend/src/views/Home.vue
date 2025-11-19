<template>
  <div class="home-page">
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
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import {
  Plus,
  Document,
  ChatDotRound,
  DataAnalysis
} from '@element-plus/icons-vue'

const router = useRouter()
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
