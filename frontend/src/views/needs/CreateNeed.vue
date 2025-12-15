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
        <el-form-item label="Service Title" prop="sr_title">
          <el-input
            v-model="form.sr_title"
            placeholder="Please enter service request title (e.g., Need plumbing repair)"
            maxlength="80"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="Service Type" prop="stype_id">
          <el-select v-model="form.stype_id" placeholder="Please select service type" style="width: 100%">
            <el-option
              v-for="type in serviceTypes"
              :key="type.id"
              :label="type.name"
              :value="type.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="City" prop="cityID">
          <el-select v-model="form.cityID" placeholder="Please select city" style="width: 100%">
            <el-option
              v-for="city in cities"
              :key="city.id"
              :label="city.name"
              :value="city.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="Description" prop="desc">
          <el-input
            v-model="form.desc"
            type="textarea"
            :rows="5"
            placeholder="Please describe your service request in detail"
            maxlength="300"
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
import { SERVICE_TYPES, CITIES } from '@/utils/constants'

const router = useRouter()
const formRef = ref(null)
const loading = ref(false)
const serviceTypes = ref(SERVICE_TYPES)
const cities = ref(CITIES)

const form = reactive({
  sr_title: '',
  stype_id: null,
  cityID: null,
  desc: '',
  file_list: '' // Default to empty string as per schema
})

const rules = {
  sr_title: [
    { required: true, message: 'Please enter service title', trigger: 'blur' },
    { min: 3, max: 80, message: 'Title length must be 3-80 characters', trigger: 'blur' }
  ],
  stype_id: [
    { required: true, message: 'Please select service type', trigger: 'change' }
  ],
  cityID: [
    { required: true, message: 'Please select city', trigger: 'change' }
  ],
  desc: [
    { required: true, message: 'Please enter description', trigger: 'blur' },
    { min: 10, max: 300, message: 'Description length must be 10-300 characters', trigger: 'blur' }
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
      sr_title: form.sr_title,
      stype_id: form.stype_id,
      cityID: form.cityID,
      desc: form.desc,
      file_list: form.file_list,
      ps_begindate: new Date().toISOString()
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
