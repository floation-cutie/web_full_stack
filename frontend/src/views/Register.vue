<template>
  <div class="register-container">
    <div class="register-box">
      <div class="register-header">
        <el-icon :size="48" color="#409EFF"><House /></el-icon>
        <h1>GoodServices</h1>
        <p>Community Service Platform</p>
      </div>

      <el-card class="register-card">
        <template #header>
          <div class="card-header">
            <span>Register</span>
          </div>
        </template>

        <el-form
          ref="registerFormRef"
          :model="registerForm"
          :rules="registerRules"
          label-position="top"
          @submit.prevent="handleRegister"
        >
          <el-form-item label="Username" prop="username">
            <el-input
              v-model="registerForm.username"
              placeholder="Enter username (3-20 characters)"
              size="large"
              :prefix-icon="User"
            />
          </el-form-item>

          <el-form-item label="Real Name" prop="bname">
            <el-input
              v-model="registerForm.bname"
              placeholder="Enter real name"
              size="large"
              :prefix-icon="User"
            />
          </el-form-item>

          <el-form-item label="Password" prop="password">
            <el-input
              v-model="registerForm.password"
              type="password"
              placeholder="At least 6 characters, 2+ digits"
              size="large"
              :prefix-icon="Lock"
              show-password
            />
          </el-form-item>

          <el-form-item label="Confirm Password" prop="confirmPassword">
            <el-input
              v-model="registerForm.confirmPassword"
              type="password"
              placeholder="Enter password again"
              size="large"
              :prefix-icon="Lock"
              show-password
            />
          </el-form-item>

          <el-form-item label="Phone Number" prop="phoneNo">
            <el-input
              v-model="registerForm.phoneNo"
              placeholder="Enter phone number"
              size="large"
              :prefix-icon="Phone"
            />
          </el-form-item>

          <el-form-item label="ID Type" prop="ctype">
            <el-select
              v-model="registerForm.ctype"
              placeholder="Select ID type"
              size="large"
              style="width: 100%"
            >
              <el-option label="ID Card" value="身份证" />
              <el-option label="Passport" value="护照" />
              <el-option label="Other" value="其他" />
            </el-select>
          </el-form-item>

          <el-form-item label="ID Number" prop="idno">
            <el-input
              v-model="registerForm.idno"
              placeholder="Enter ID number"
              size="large"
              :prefix-icon="CreditCard"
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              style="width: 100%"
              @click="handleRegister"
            >
              Register
            </el-button>
          </el-form-item>

          <div class="register-footer">
            <span>Already have an account?</span>
            <el-link type="primary" @click="router.push('/login')">
              Login now
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
import { User, Lock, House, Phone, CreditCard } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const registerFormRef = ref(null)
const loading = ref(false)

const registerForm = reactive({
  username: '',
  bname: '',
  password: '',
  confirmPassword: '',
  phoneNo: '',
  ctype: '',
  idno: ''
})

const validatePassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('Please enter password'))
  } else if (value.length < 6) {
    callback(new Error('Password must be at least 6 characters'))
  } else {
    const digitCount = (value.match(/\d/g) || []).length
    if (digitCount < 2) {
      callback(new Error('Password must contain at least 2 digits'))
    } else {
      callback()
    }
  }
}

const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('Please confirm password'))
  } else if (value !== registerForm.password) {
    callback(new Error('Passwords do not match'))
  } else {
    callback()
  }
}

const registerRules = {
  username: [
    { required: true, message: 'Please enter username', trigger: 'blur' },
    { min: 3, max: 20, message: 'Username length must be 3-20 characters', trigger: 'blur' }
  ],
  bname: [
    { required: true, message: 'Please enter real name', trigger: 'blur' },
    { min: 2, max: 50, message: 'Real name length must be 2-50 characters', trigger: 'blur' }
  ],
  password: [
    { required: true, validator: validatePassword, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ],
  phoneNo: [
    { required: true, message: 'Please enter phone number', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: 'Invalid phone number format', trigger: 'blur' }
  ],
  ctype: [
    { required: true, message: 'Please select ID type', trigger: 'change' }
  ],
  idno: [
    { required: true, message: 'Please enter ID number', trigger: 'blur' },
    { min: 6, max: 50, message: 'ID number length must be 6-50 characters', trigger: 'blur' }
  ]
}

const handleRegister = async () => {
  if (!registerFormRef.value) return

  try {
    await registerFormRef.value.validate()
  } catch {
    return
  }

  loading.value = true
  try {
    await userStore.register({
      uname: registerForm.username,
      bname: registerForm.bname,
      bpwd: registerForm.password,
      phoneNo: registerForm.phoneNo,
      ctype: registerForm.ctype,
      idno: registerForm.idno
    })
    ElMessage.success('Registration successful, please login')
    router.push('/login')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || 'Registration failed')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.register-box {
  width: 100%;
  max-width: 480px;
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
  color: #fff;
}

.register-header h1 {
  font-size: 36px;
  margin: 16px 0 8px;
  font-weight: bold;
}

.register-header p {
  font-size: 16px;
  opacity: 0.9;
}

.register-card {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.card-header {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.register-footer {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #606266;
}

.register-footer span {
  margin-right: 8px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #303133;
}

@media (max-width: 480px) {
  .register-header h1 {
    font-size: 28px;
  }

  .register-box {
    max-width: 100%;
  }
}
</style>
