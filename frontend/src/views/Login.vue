<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <el-icon :size="48" color="#409EFF"><House /></el-icon>
        <h1>GoodServices</h1>
        <p>Community Service Platform</p>
      </div>

      <el-card class="login-card">
        <template #header>
          <div class="card-header">
            <span>Login</span>
          </div>
        </template>

        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          label-position="top"
          @submit.prevent="handleLogin"
        >
          <el-form-item label="Username" prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="Enter your username"
              size="large"
              :prefix-icon="User"
            />
          </el-form-item>

          <el-form-item label="Password" prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="Enter your password"
              size="large"
              :prefix-icon="Lock"
              show-password
              @keyup.enter="handleLogin"
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              style="width: 100%"
              @click="handleLogin"
            >
              Login
            </el-button>
          </el-form-item>

          <div class="login-footer">
            <span>Don't have an account?</span>
            <el-link type="primary" @click="router.push('/register')">
              Register now
            </el-link>
          </div>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { User, Lock, House } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const loginFormRef = ref(null)
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const loginRules = {
  username: [
    { required: true, message: 'Please enter username', trigger: 'blur' },
    { min: 3, max: 20, message: 'Username length must be 3-20 characters', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Please enter password', trigger: 'blur' },
    { min: 6, message: 'Password must be at least 6 characters', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return

  try {
    await loginFormRef.value.validate()
  } catch {
    return
  }

  loading.value = true
  try {
    await userStore.login({
      username: loginForm.username,
      password: loginForm.password
    })
    console.log('Login successful, redirecting to /home')
    ElMessage.success('Login successful')
    await router.push('/home')
    console.log('Redirected to:', router.currentRoute.value.path)
  } catch (error) {
    console.error('Login error:', error)
    ElMessage.error(error.response?.data?.detail || error.message || 'Login failed')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-box {
  width: 100%;
  max-width: 420px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
  color: #fff;
}

.login-header h1 {
  font-size: 36px;
  margin: 16px 0 8px;
  font-weight: bold;
}

.login-header p {
  font-size: 16px;
  opacity: 0.9;
}

.login-card {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.card-header {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.login-footer {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #606266;
}

.login-footer span {
  margin-right: 8px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #303133;
}

@media (max-width: 480px) {
  .login-header h1 {
    font-size: 28px;
  }

  .login-box {
    max-width: 100%;
  }
}
</style>
