<template>
  <div class="create-need-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>Publish Service Request</h2>
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
        <el-form-item label="Service Type" prop="stypeId">
          <el-select v-model="form.stypeId" placeholder="Please select service type" style="width: 100%">
            <el-option
              v-for="type in serviceTypes"
              :key="type.id"
              :label="type.name"
              :value="type.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="Description" prop="psContent">
          <el-input
            v-model="form.psContent"
            type="textarea"
            :rows="5"
            placeholder="Please describe your service request in detail"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="Service Address" prop="psAddress">
          <el-input
            v-model="form.psAddress"
            placeholder="Please enter the service address"
            maxlength="200"
          />
        </el-form-item>

        <el-form-item label="Contact Phone" prop="psPhone">
          <el-input
            v-model="form.psPhone"
            placeholder="Please enter contact phone number"
            maxlength="20"
          />
        </el-form-item>

        <el-form-item label="Remarks" prop="psRemark">
          <el-input
            v-model="form.psRemark"
            type="textarea"
            :rows="3"
            placeholder="Any additional information (optional)"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">
            Publish Request
          </el-button>
          <el-button @click="handleReset">Reset</el-button>
          <el-button @click="router.back()">Cancel</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { createNeed } from '@/api/serviceRequest'
import { SERVICE_TYPES } from '@/utils/constants'

const router = useRouter()
const formRef = ref(null)
const loading = ref(false)
const serviceTypes = ref(SERVICE_TYPES)

const form = reactive({
  stypeId: null,
  psContent: '',
  psAddress: '',
  psPhone: '',
  psRemark: ''
})

const rules = {
  stypeId: [
    { required: true, message: 'Please select service type', trigger: 'change' }
  ],
  psContent: [
    { required: true, message: 'Please enter description', trigger: 'blur' },
    { min: 10, max: 500, message: 'Description length must be 10-500 characters', trigger: 'blur' }
  ],
  psAddress: [
    { required: true, message: 'Please enter service address', trigger: 'blur' },
    { min: 5, max: 200, message: 'Address length must be 5-200 characters', trigger: 'blur' }
  ],
  psPhone: [
    { required: true, message: 'Please enter contact phone', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: 'Invalid phone number format', trigger: 'blur' }
  ],
  psRemark: [
    { max: 200, message: 'Remarks cannot exceed 200 characters', trigger: 'blur' }
  ]
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
    await createNeed({
      stype_id: form.stypeId,
      ps_content: form.psContent,
      ps_address: form.psAddress,
      ps_phone: form.psPhone,
      ps_remark: form.psRemark
    })
    ElMessage.success('Service request published successfully')
    router.push('/needs')
  } catch (error) {
    ElMessage.error('Failed to publish request')
  } finally {
    loading.value = false
  }
}

const handleReset = () => {
  formRef.value?.resetFields()
}
</script>

<style scoped>
.create-need-page {
  padding: 20px;
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
