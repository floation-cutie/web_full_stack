<template>
  <div class="create-response-page">
    <el-card v-loading="requestLoading" class="request-card">
      <template #header>
        <h3>服务请求信息</h3>
      </template>

      <el-descriptions v-if="requestDetail" :column="2" border>
        <el-descriptions-item label="服务类型">
          {{ requestDetail.service_type_name }}
        </el-descriptions-item>
        <el-descriptions-item label="发布者">
          {{ requestDetail.publisher_name }}
        </el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">
          {{ requestDetail.desc }}
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <h2>提交服务响应</h2>
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
        <el-form-item label="响应标题" prop="responseTitle">
          <el-input
            v-model="form.responseTitle"
            placeholder="请输入响应标题"
            maxlength="50"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="响应描述" prop="responseContent">
          <el-input
            v-model="form.responseContent"
            type="textarea"
            :rows="5"
            placeholder="请详细描述您的服务能力和计划"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="图片/视频">
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
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getNeedDetail } from '@/api/serviceRequest'
import { createResponse } from '@/api/serviceResponse'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const formRef = ref(null)
const loading = ref(false)
const requestLoading = ref(false)
const requestDetail = ref(null)

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
  responseTitle: '',
  responseContent: '',
  fileList: '' // Will be populated with uploaded filenames
})

const rules = {
  responseTitle: [
    { required: true, message: 'Please enter response title', trigger: 'blur' },
    { min: 5, max: 50, message: 'Title length must be 5-50 characters', trigger: 'blur' }
  ],
  responseContent: [
    { required: true, message: 'Please enter response content', trigger: 'blur' },
    { min: 10, max: 500, message: 'Content length must be 10-500 characters', trigger: 'blur' }
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
  form.fileList = uploadedFiles.value.map(file => file.name).join(',')
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
      title: form.responseTitle,
      desc: form.responseContent,
      file_list: form.fileList
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
  fileList.value = []
  uploadedFiles.value = []
  form.fileList = ''
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
