<template>
  <div class="edit-need-page">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <h2>Edit Service Request</h2>
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

        <el-form-item label="Images/Videos">
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
            <el-button type="primary">Click to upload</el-button>
            <template #tip>
              <div class="el-upload__tip">
                jpg/png/gif/mp4/avi/mov/wmv files with a size less than 10MB, up to 5 files
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
          <el-button type="primary" :loading="submitting" @click="handleSubmit">
            Update Request
          </el-button>
          <el-button @click="handleReset">Reset</el-button>
          <el-button @click="router.back()">Cancel</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getNeedDetail, updateNeed } from '@/api/serviceRequest'
import { SERVICE_TYPES, CITIES } from '@/utils/constants'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const formRef = ref(null)
const loading = ref(false)
const submitting = ref(false)
const serviceTypes = ref(SERVICE_TYPES)
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

// 加载已有服务请求数据
const loadRequestData = async () => {
  loading.value = true
  try {
    const res = await getNeedDetail(route.params.id)
    const requestData = res.data
    
    // 填充表单数据
    form.sr_title = requestData.sr_title
    form.stype_id = requestData.stype_id
    form.cityID = requestData.cityID
    form.desc = requestData.desc
    form.file_list = requestData.file_list || ''
    
    // 处理已有的文件
    if (requestData.file_list) {
      const fileNames = requestData.file_list.split(',')
      for (const fileName of fileNames) {
        if (fileName) {
          const fullUrl = `${import.meta.env.VITE_API_BASE_URL}/api/v1/files/${fileName}`
          const ext = fileName.split('.').pop().toLowerCase()
          const fileType = ['jpg', 'jpeg', 'png', 'gif'].includes(ext) ? 'image' : 'video'
          
          uploadedFiles.value.push({
            name: fileName,
            url: fullUrl,
            type: fileType
          })
          
          // 添加到文件列表用于显示
          fileList.value.push({
            name: fileName,
            url: fullUrl
          })
        }
      }
    }
  } catch (error) {
    ElMessage.error('Failed to load request data')
    router.back()
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
  } catch {
    return
  }

  submitting.value = true
  try {
    await updateNeed(route.params.id, {
      sr_title: form.sr_title,
      stype_id: form.stype_id,
      cityID: form.cityID,
      desc: form.desc,
      file_list: form.file_list
    })
    ElMessage.success('Service request updated successfully')
    router.push(`/needs/${route.params.id}`)
  } catch (error) {
    ElMessage.error('Failed to update request: ' + (error.message || 'Unknown error'))
  } finally {
    submitting.value = false
  }
}

const handleReset = () => {
  formRef.value?.resetFields()
  fileList.value = []
  uploadedFiles.value = []
  form.file_list = ''
  
  // 重新加载原始数据
  loadRequestData()
}

// 组件挂载时加载数据
onMounted(() => {
  loadRequestData()
  
  // 强制更新组件以确保上传按钮显示
  nextTick(() => {
    // 组件已正确挂载
  })
})
</script>

<style scoped>
.edit-need-page {
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
</style>