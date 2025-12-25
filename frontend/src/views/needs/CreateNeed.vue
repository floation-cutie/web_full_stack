<template>
  <div class="create-need-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>发布服务请求</h2>
          <el-button @click="router.back()">返回</el-button>
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
        <el-form-item label="服务标题" prop="sr_title">
          <el-input
            v-model="form.sr_title"
            placeholder="请输入服务请求标题 (例如：需要水电维修)"
            maxlength="80"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="服务类型" prop="stype_id">
          <el-select v-model="form.stype_id" placeholder="请选择服务类型" style="width: 100%">
            <el-option
              v-for="type in serviceTypes"
              :key="type.id"
              :label="type.name"
              :value="type.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="城市" prop="cityID">
          <el-select v-model="form.cityID" placeholder="请选择城市" style="width: 100%">
            <el-option
              v-for="city in cities"
              :key="city.id"
              :label="city.name"
              :value="city.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="描述" prop="desc">
          <el-input
            v-model="form.desc"
            type="textarea"
            :rows="5"
            placeholder="请详细描述您的服务请求"
            maxlength="300"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="上传附件">
          <el-upload
            v-model:file-list="fileList"
            class="upload-demo"
            action="/api/v1/files/upload"
            :headers="uploadHeaders"
            :on-success="handleUploadSuccess"
            :on-error="handleUploadError"
            :on-remove="handleRemoveFile"
            :before-upload="beforeUpload"
            multiple
            :limit="5"
            :auto-upload="true"
          >
            <el-button type="primary">点击上传</el-button>
            <template #tip>
              <div class="el-upload__tip">
                jpg/png/gif/mp4/avi/mov/wmv 文件，单个文件不超过 10MB，最多上传 5 个文件
              </div>
            </template>
          </el-upload>
        </el-form-item>

        <!-- 预览已上传的图片 -->
        <el-form-item v-if="imagePreviews.length > 0" label="Image Previews">
          <div class="image-preview-container">
            <div v-for="(preview, index) in imagePreviews" :key="index" class="image-preview-item">
              <img :src="preview.url" :alt="preview.name" class="preview-image" />
            </div>
          </div>
        </el-form-item>

        <!-- 预览已上传的视频 -->
        <el-form-item v-if="videoPreviews.length > 0" label="Video Previews">
          <div class="video-preview-container">
            <div v-for="(preview, index) in videoPreviews" :key="index" class="video-preview-item">
              <video controls class="preview-video">
                <source :src="preview.url" :type="getVideoType(preview.url)">
                Your browser does not support the video tag.
              </video>
            </div>
          </div>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">
            发布需求
          </el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button @click="router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { createNeed } from '@/api/serviceRequest'
import { getCities, getServiceTypes } from '@/api/user'
import { CITIES } from '@/utils/constants'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref(null)
const loading = ref(false)
const serviceTypes = ref([])
const cities = ref(CITIES)

// 文件上传相关
const fileList = ref([])
const uploadedFiles = ref([])

// 上传头部信息
const uploadHeaders = computed(() => {
  return {
    Authorization: `Bearer ${userStore.token}`
  }
})

// 图片预览
const imagePreviews = computed(() => {
  return uploadedFiles.value.filter(file => file.type === 'image')
})

// 视频预览
const videoPreviews = computed(() => {
  return uploadedFiles.value.filter(file => file.type === 'video')
})

const form = reactive({
  sr_title: '',
  stype_id: null,
  cityID: null,
  desc: '',
  file_list: '' // Will be populated with uploaded filenames
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

// 上传成功回调
const handleUploadSuccess = (response, uploadFile, uploadFiles) => {
  if (response.code === 200) {
    // 构造完整的URL用于预览
    const fullUrl = `${import.meta.env.VITE_API_BASE_URL}${response.data.url}`;
    
    // 添加到已上传文件列表
    uploadedFiles.value.push({
      name: response.data.filename,
      url: fullUrl,
      type: response.data.type
    })
    
    // 更新表单中的文件列表
    updateFileList()
    
    ElMessage.success('File uploaded successfully')
  } else {
    ElMessage.error(response.message || 'File upload failed')
    // 从文件列表中移除失败的文件
    fileList.value = fileList.value.filter(file => file.uid !== uploadFile.uid)
  }
}

// 上传失败回调
const handleUploadError = (error, uploadFile, uploadFiles) => {
  ElMessage.error('File upload failed')
  // 从文件列表中移除失败的文件
  fileList.value = fileList.value.filter(file => file.uid !== uploadFile.uid)
}

// 移除文件回调
const handleRemoveFile = (uploadFile, uploadFiles) => {
  // 从已上传文件列表中移除
  uploadedFiles.value = uploadedFiles.value.filter(file => file.name !== uploadFile.name)
  
  // 更新表单中的文件列表
  updateFileList()
  
  ElMessage.success('File removed successfully')
}

// 上传前检查
const beforeUpload = (rawFile) => {
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'video/mp4', 'video/avi', 'video/mov', 'video/wmv']
  const maxSize = 10 * 1024 * 1024 // 10MB
  
  if (!allowedTypes.includes(rawFile.type)) {
    ElMessage.error('Unsupported file type!')
    return false
  }
  
  if (rawFile.size > maxSize) {
    ElMessage.error('File size exceeds 10MB!')
    return false
  }
  
  return true
}

// 获取视频类型
const getVideoType = (url) => {
  // 从完整URL中提取文件名
  const filename = url.split('/').pop();
  const ext = filename.split('.').pop().toLowerCase()
  const typeMap = {
    'mp4': 'video/mp4',
    'avi': 'video/avi',
    'mov': 'video/quicktime',
    'wmv': 'video/x-ms-wmv'
  }
  return typeMap[ext] || 'video/mp4'
}

// 更新表单中的文件列表
const updateFileList = () => {
  form.file_list = uploadedFiles.value.map(file => file.name).join(',')
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
  fileList.value = []
  uploadedFiles.value = []
  form.file_list = ''
}

// 组件挂载时确保正确初始化
onMounted(async () => {
  // 获取服务类型数据
  try {
    const res = await getServiceTypes()
    serviceTypes.value = res.data || []
  } catch (error) {
    ElMessage.error('Failed to load service types')
  }
  
  // 强制更新组件以确保上传按钮显示
  nextTick(() => {
    // 组件已正确挂载
  })
})
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

.image-preview-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.image-preview-item {
  width: 150px;
  height: 150px;
  overflow: hidden;
  border-radius: 4px;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-preview-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.video-preview-item {
  width: 200px;
}

.preview-video {
  width: 100%;
  height: 150px;
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
  
  .image-preview-item {
    width: 100px;
    height: 100px;
  }
  
  .video-preview-item {
    width: 100%;
  }
  
  .preview-video {
    height: 120px;
  }
}
</style>
