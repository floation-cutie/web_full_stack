<template>
  <div class="edit-response-page">
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
          <h2>编辑服务响应</h2>
          <div>
            <el-button @click="handleDelete" type="danger" :loading="deleteLoading">
              删除
            </el-button>
            <el-button @click="router.back()">返回</el-button>
          </div>
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
        <el-form-item label="Title" prop="title">
          <el-input
            v-model="form.title"
            placeholder="请输入响应标题"
            maxlength="50"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="描述" prop="desc">
          <el-input
            v-model="form.desc"
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
                jpg/png/gif/mp4/avi/mov/wmv 文件，单个文件不超过 10MB，最多上传 5 个文件。
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
            更新响应
          </el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button @click="router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getNeedDetail } from '@/api/serviceRequest'
import { getResponseDetail, updateResponse, deleteResponse } from '@/api/serviceResponse'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const formRef = ref(null)
const loading = ref(false)
const deleteLoading = ref(false)
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
  title: '',
  desc: '',
  file_list: ''
})

const rules = {
  title: [
    { required: true, message: 'Please enter response title', trigger: 'blur' },
    { min: 1, max: 50, message: 'Title length must be 1-50 characters', trigger: 'blur' }
  ],
  desc: [
    { required: true, message: 'Please enter response description', trigger: 'blur' },
    { min: 10, max: 500, message: 'Description length must be 10-500 characters', trigger: 'blur' }
  ],
  file_list: [
    { max: 400, message: 'File list cannot exceed 400 characters', trigger: 'blur' }
  ]
}

// 获取视频类型
const getVideoType = (url) => {
  const extension = url.split('.').pop().toLowerCase()
  const videoTypes = {
    mp4: 'video/mp4',
    avi: 'video/avi',
    mov: 'video/quicktime',
    wmv: 'video/x-ms-wmv'
  }
  return videoTypes[extension] || 'video/mp4'
}

// 更新表单中的文件列表
const updateFileList = () => {
  form.file_list = uploadedFiles.value.map(file => file.name).join(',')
}

// 上传成功回调
const handleUploadSuccess = (response, uploadFile, uploadFiles) => {
  if (response.code === 200) {
    // 构造完整的URL用于预览
    const fullUrl = `${import.meta.env.VITE_API_BASE_URL}${response.data.url}`
    
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
    ElMessage.error('File size exceeds 10MB limit!')
    return false
  }
  
  return true
}

const loadRequestDetail = async () => {
  requestLoading.value = true
  try {
    // Get the service request details associated with this response
    const responseRes = await getResponseDetail(route.params.id)
    const requestId = responseRes.data.sr_id
    const res = await getNeedDetail(requestId)
    requestDetail.value = res.data
  } catch (error) {
    ElMessage.error('Failed to load request details')
  } finally {
    requestLoading.value = false
  }
}

const loadData = async () => {
  try {
    const res = await getResponseDetail(route.params.id)
    form.title = res.data.title || ''
    form.desc = res.data.desc || ''
    form.file_list = res.data.file_list || ''
    
    // 如果已有文件列表，初始化上传组件
    if (res.data.file_list) {
      const fileNames = res.data.file_list.split(',').filter(name => name.trim() !== '')
      for (const fileName of fileNames) {
        // 构造文件URL
        const fileUrl = `${import.meta.env.VITE_API_BASE_URL}/api/v1/files/${fileName}`
        
        // 判断文件类型（简化版）
        const isImage = /\.(jpg|jpeg|png|gif)$/i.test(fileName)
        const isVideo = /\.(mp4|avi|mov|wmv)$/i.test(fileName)
        const fileType = isImage ? 'image' : isVideo ? 'video' : 'other'
        
        // 添加到已上传文件列表
        uploadedFiles.value.push({
          name: fileName,
          url: fileUrl,
          type: fileType
        })
        
        // 添加到文件列表用于显示
        fileList.value.push({
          name: fileName,
          url: fileUrl
        })
      }
    }
    
    // Load request details
    await loadRequestDetail()
  } catch (error) {
    ElMessage.error('Failed to load response details')
    router.back()
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
    await updateResponse(route.params.id, {
      title: form.title,
      desc: form.desc,
      file_list: form.file_list
    })
    ElMessage.success('Response updated successfully')
    router.push('/responses')
  } catch (error) {
    ElMessage.error('Failed to update response')
  } finally {
    loading.value = false
  }
}

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm(
      'Are you sure you want to permanently delete this response? This action cannot be undone.',
      'Confirm Delete',
      {
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }
    )
    
    deleteLoading.value = true
    try {
      await deleteResponse(route.params.id)
      ElMessage.success('Response deleted successfully')
      router.push('/responses')
    } catch (error) {
      ElMessage.error('Failed to delete response')
    } finally {
      deleteLoading.value = false
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Failed to delete response')
    }
  }
}

const handleReset = () => {
  formRef.value?.resetFields()
  fileList.value = []
  uploadedFiles.value = []
  form.file_list = ''
  
  // 重新加载原始数据
  loadData()
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.edit-response-page {
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

/* 图片预览容器 */
.image-preview-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.image-preview-item {
  position: relative;
}

.preview-image {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
}

/* 视频预览容器 */
.video-preview-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.video-preview-item {
  position: relative;
}

.preview-video {
  width: 200px;
  height: 150px;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
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
  
  .card-header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
  
  .preview-image,
  .preview-video {
    width: 100px;
    height: 100px;
  }
}
</style>