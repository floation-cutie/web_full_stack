<template>
  <div class="create-response-page">
    <el-card v-loading="requestLoading" class="request-card">
      <template #header>
        <h3>Service Request Information</h3>
      </template>

      <el-descriptions v-if="requestDetail" :column="2" border>
        <el-descriptions-item label="Service Type">
          {{ requestDetail.service_type_name }}
        </el-descriptions-item>
        <el-descriptions-item label="Publisher">
          {{ requestDetail.publisher_name }}
        </el-descriptions-item>
        <el-descriptions-item label="Service Address" :span="2">
          {{ requestDetail.ps_address }}
        </el-descriptions-item>
        <el-descriptions-item label="Description" :span="2">
          {{ requestDetail.ps_content }}
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <h2>Submit Service Response</h2>
          <el-button @click="router.back()">Back</el-button>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="140px"
        label-position="right"
        style="max-width: 800px"
      >
        <el-form-item label="Response Content" prop="responseContent">
          <el-input
            v-model="form.responseContent"
            type="textarea"
            :rows="5"
            placeholder="Please describe your service capabilities and plan in detail"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="Contact Phone" prop="responsePhone">
          <el-input
            v-model="form.responsePhone"
            placeholder="Please enter your contact phone number"
            maxlength="20"
          />
        </el-form-item>

        <el-form-item label="Remarks" prop="responseRemark">
          <el-input
            v-model="form.responseRemark"
            type="textarea"
            :rows="3"
            placeholder="Any additional information (optional)"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">
            Submit Response
          </el-button>
          <el-button @click="handleReset">Reset</el-button>
          <el-button @click="router.back()">Cancel</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getNeedDetail } from '@/api/serviceRequest'
import { createResponse } from '@/api/serviceResponse'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const loading = ref(false)
const requestLoading = ref(false)
const requestDetail = ref(null)

const form = reactive({
  responseContent: '',
  responsePhone: '',
  responseRemark: ''
})

const rules = {
  responseContent: [
    { required: true, message: 'Please enter response content', trigger: 'blur' },
    { min: 10, max: 500, message: 'Content length must be 10-500 characters', trigger: 'blur' }
  ],
  responsePhone: [
    { required: true, message: 'Please enter contact phone', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: 'Invalid phone number format', trigger: 'blur' }
  ],
  responseRemark: [
    { max: 200, message: 'Remarks cannot exceed 200 characters', trigger: 'blur' }
  ]
}

const loadRequestDetail = async () => {
  requestLoading.value = true
  try {
    const res = await getNeedDetail(route.params.needId)
    requestDetail.value = res.data
  } catch (error) {
    ElMessage.error('Failed to load request details')
    router.back()
  } finally {
    requestLoading.value = false
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
  } catch {
    return
  }

  loading.value = true
  try {
    await createResponse({
      sr_id: route.params.needId,
      response_content: form.responseContent,
      response_phone: form.responsePhone,
      response_remark: form.responseRemark
    })
    ElMessage.success('Response submitted successfully')
    router.push('/responses')
  } catch (error) {
    ElMessage.error('Failed to submit response')
  } finally {
    loading.value = false
  }
}

const handleReset = () => {
  formRef.value?.resetFields()
}

onMounted(() => {
  loadRequestDetail()
})
</script>

<style scoped>
.create-response-page {
  padding: 20px;
}

.request-card {
  margin-bottom: 20px;
}

.request-card h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.form-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  font-size: 20px;
  color: #303133;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

@media (max-width: 768px) {
  :deep(.el-form) {
    max-width: 100%;
  }

  :deep(.el-form-item) {
    flex-direction: column;
    align-items: flex-start;
  }

  :deep(.el-form-item__label) {
    width: 100% !important;
    text-align: left;
    margin-bottom: 8px;
  }
}
</style>
