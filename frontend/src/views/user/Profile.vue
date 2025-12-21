<template>
  <div class="profile-container">
    <el-row :gutter="20">
      <el-col :xs="24" :sm="24" :md="16" :lg="16">
        <el-card class="profile-card">
          <template #header>
            <div class="card-header">
              <span>Profile Information</span>
            </div>
          </template>

          <el-form
            ref="profileFormRef"
            :model="profileForm"
            :rules="profileRules"
            label-width="140px"
            label-position="right"
          >
            <el-form-item label="Username" prop="username">
              <el-input
                v-model="profileForm.username"
                placeholder="Username"
                disabled
                :prefix-icon="User"
              />
            </el-form-item>

            <el-form-item label="Phone Number" prop="phoneNo">
              <el-input
                v-model="profileForm.phoneNo"
                placeholder="Enter phone number"
                :prefix-icon="Phone"
              />
            </el-form-item>

            <el-form-item label="ID Number" prop="idno">
              <el-input
                v-model="profileForm.idno"
                placeholder="Enter ID number"
                :prefix-icon="CreditCard"
                disabled
              />
            </el-form-item>

            <el-form-item label="Real Name" prop="realName">
              <el-input
                v-model="profileForm.realName"
                placeholder="Enter your real name"
                :prefix-icon="UserFilled"
              />
            </el-form-item>

            <el-form-item label="City" prop="cityId">
              <el-select
                v-model="profileForm.cityId"
                placeholder="Select city"
                style="width: 100%"
              >
                <el-option
                  v-for="city in cities"
                  :key="city.id"
                  :label="city.name"
                  :value="city.id"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="Address" prop="address">
              <el-input
                v-model="profileForm.address"
                type="textarea"
                placeholder="Enter your address"
                :rows="3"
              />
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                @click="handleUpdateProfile"
                :loading="loading"
                :icon="DocumentCopy"
              >
                Save Changes
              </el-button>
              <el-button @click="handleResetProfile">Cancel</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="24" :md="8" :lg="8">
        <el-card class="stats-card">
          <template #header>
            <div class="card-header">
              <span>Account Stats</span>
            </div>
          </template>

          <div class="stats-content">
            <div class="stat-item">
              <div class="stat-label">Service Requests</div>
              <div class="stat-value">{{ accountStats.serviceRequests }}</div>
            </div>
            <el-divider />
            <div class="stat-item">
              <div class="stat-label">Service Responses</div>
              <div class="stat-value">{{ accountStats.serviceResponses }}</div>
            </div>
            <el-divider />
            <div class="stat-item">
              <div class="stat-label">Completed Services</div>
              <div class="stat-value">{{ accountStats.completedServices }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :xs="24" :sm="24" :md="16" :lg="16">
        <el-card class="password-card">
          <template #header>
            <div class="card-header">
              <span>Change Password</span>
            </div>
          </template>

          <el-form
            ref="passwordFormRef"
            :model="passwordForm"
            :rules="passwordRules"
            label-width="140px"
            label-position="right"
          >
            <el-form-item label="Old Password" prop="currentPassword">
              <el-input
                v-model="passwordForm.currentPassword"
                type="password"
                placeholder="Enter old password"
                :prefix-icon="Lock"
                show-password
              />
            </el-form-item>

            <el-form-item label="New Password" prop="newPassword">
              <el-input
                v-model="passwordForm.newPassword"
                type="password"
                placeholder="At least 6 characters, 2+ digits"
                :prefix-icon="Lock"
                show-password
              />
            </el-form-item>

            <el-form-item label="Confirm Password" prop="confirmPassword">
              <el-input
                v-model="passwordForm.confirmPassword"
                type="password"
                placeholder="Enter new password again"
                :prefix-icon="Lock"
                show-password
              />
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                @click="handleChangePassword"
                :loading="passwordLoading"
                :icon="Edit"
              >
                Change Password
              </el-button>
              <el-button @click="handleResetPassword">Cancel</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  User,
  Phone,
  CreditCard,
  UserFilled,
  DocumentCopy,
  Lock,
  Edit
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { getUserProfile, updateUserProfile, changePassword } from '@/api/user'
import { CITIES } from '@/utils/constants'

const userStore = useUserStore()
const profileFormRef = ref(null)
const passwordFormRef = ref(null)

const loading = ref(false)
const passwordLoading = ref(false)
const cities = ref(CITIES)

const profileForm = reactive({
  username: '',
  phoneNo: '',
  idno: '',
  realName: '',
  cityId: null,
  address: ''
})

const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const accountStats = reactive({
  serviceRequests: 0,
  serviceResponses: 0,
  completedServices: 0
})

const validateNewPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('Please enter new password'))
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
  } else if (value !== passwordForm.newPassword) {
    callback(new Error('Passwords do not match'))
  } else {
    callback()
  }
}

const profileRules = {
  phoneNo: [
    { required: true, message: 'Please enter phone number', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: 'Invalid phone number format', trigger: 'blur' }
  ],
  realName: [
    { required: false, message: 'Please enter real name', trigger: 'blur' }
  ],
  cityId: [
    { required: false, message: 'Please select city', trigger: 'change' }
  ]
}

const passwordRules = {
  currentPassword: [
    { required: true, message: 'Please enter current password', trigger: 'blur' },
    { min: 6, message: 'Password must be at least 6 characters', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, validator: validateNewPassword, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

onMounted(async () => {
  await loadProfileData()
})

const loadProfileData = async () => {
  try {
    const res = await getUserProfile()
    const data = res.data || res

    profileForm.username = data.username || userStore.userInfo?.username || ''
    profileForm.phoneNo = data.phone_no || data.phoneNo || ''
    profileForm.idno = data.idno || ''
    profileForm.realName = data.real_name || data.realName || ''
    profileForm.cityId = data.city_id || data.cityId || null
    profileForm.address = data.address || ''

    accountStats.serviceRequests = data.service_requests_count || 0
    accountStats.serviceResponses = data.service_responses_count || 0
    accountStats.completedServices = data.completed_services_count || 0
  } catch (error) {
    ElMessage.error('Failed to load profile data')
  }
}

const handleUpdateProfile = async () => {
  if (!profileFormRef.value) return

  try {
    await profileFormRef.value.validate()
  } catch {
    return
  }

  loading.value = true
  try {
    await updateUserProfile({
      phone_no: profileForm.phoneNo,
      real_name: profileForm.realName,
      city_id: profileForm.cityId,
      address: profileForm.address
    })
    ElMessage.success('Profile updated successfully')
    await loadProfileData()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || 'Failed to update profile')
  } finally {
    loading.value = false
  }
}

const handleResetProfile = () => {
  loadProfileData()
}

const handleChangePassword = async () => {
  if (!passwordFormRef.value) return

  try {
    await passwordFormRef.value.validate()
  } catch {
    return
  }

  passwordLoading.value = true
  try {
    await changePassword({
      old_password: passwordForm.currentPassword,
      new_password: passwordForm.newPassword
    })
    ElMessage.success('Password changed successfully')
    handleResetPassword()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || 'Failed to change password')
  } finally {
    passwordLoading.value = false
  }
}

const handleResetPassword = () => {
  passwordForm.currentPassword = ''
  passwordForm.newPassword = ''
  passwordForm.confirmPassword = ''
  if (passwordFormRef.value) {
    passwordFormRef.value.clearValidate()
  }
}
</script>

<style scoped>
.profile-container {
  padding: 20px;
}

.card-header {
  font-weight: bold;
  font-size: 16px;
  color: #303133;
}

.profile-card,
.password-card {
  margin-bottom: 20px;
}

.stats-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.stats-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
}

.stat-item {
  text-align: center;
  padding: 10px 0;
}

.stat-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #409EFF;
}

:deep(.el-divider--horizontal) {
  margin: 10px 0;
}

@media (max-width: 768px) {
  .profile-container {
    padding: 10px;
  }

  :deep(.el-form) {
    --el-form-label-width: 100px;
  }

  .stats-card {
    margin-top: 20px;
  }
}
</style>
