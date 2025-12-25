<template>
  <div class="need-detail-page">
    <el-card v-loading="loading" class="detail-card">
      <template #header>
        <div class="card-header">
          <h2>Service Request Details</h2>
          <div>
            <el-button 
              v-if="isMyRequest"
              type="primary" 
              @click="handleEdit"
            >
              Edit
            </el-button>
            <el-button 
              v-if="isMyRequest"
              type="danger" 
              @click="handleDelete"
            >
              Delete
            </el-button>
            <el-button @click="router.back()">Back</el-button>
          </div>
        </div>
      </template>

      <el-descriptions v-if="detail" :column="2" border>
        <el-descriptions-item label="Request ID">
          {{ detail.sr_id }}
        </el-descriptions-item>
        <el-descriptions-item label="Title" :span="2">
          {{ detail.sr_title }}
        </el-descriptions-item>
        <el-descriptions-item label="Service Type">
          {{ getServiceTypeName(detail.stype_id) }}
        </el-descriptions-item>
        <el-descriptions-item label="Status">
          <el-tag :type="detail.ps_state === 0 ? 'success' : 'info'">
            {{ detail.ps_state === 0 ? 'Published' : 'Cancelled' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="Start Date">
          {{ formatDateTime(detail.ps_begindate) }}
        </el-descriptions-item>
        <el-descriptions-item label="City">
          {{ getCityName(detail.cityID) }}
        </el-descriptions-item>
        <el-descriptions-item label="Description" :span="2">
          {{ detail.desc }}
        </el-descriptions-item>
        
        <!-- Display Images -->
        <el-descriptions-item label="Images" :span="2" v-if="imageFiles.length > 0">
          <div class="image-preview-container">
            <div v-for="(file, index) in imageFiles" :key="index" class="image-preview-item">
              <img :src="getFullImageUrl(file)" :alt="file" class="preview-image" />
            </div>
          </div>
        </el-descriptions-item>
        
        <!-- Display Videos -->
        <el-descriptions-item label="Videos" :span="2" v-if="videoFiles.length > 0">
          <div class="video-preview-container">
            <div v-for="(file, index) in videoFiles" :key="index" class="video-preview-item">
              <video controls class="preview-video">
                <source :src="getFullImageUrl(file)" :type="getVideoType(file)">
                Your browser does not support the video tag.
              </video>
            </div>
          </div>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card class="responses-card">
      <template #header>
        <div class="card-header">
          <h3>Service Responses ({{ responsesTotal }})</h3>
        </div>
      </template>

      <el-table
        v-loading="responsesLoading"
        :data="responsesList"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="response_id" label="Response ID" width="120" />
        <el-table-column prop="responder_name" label="Responder" width="150">
  <template #default="{ row }">
    <span>{{ row.responder_name || '-' }}</span>
  </template>
</el-table-column>
        <el-table-column prop="desc" label="Response Content" show-overflow-tooltip>
  <template #default="{ row }">
    <span>{{ row.desc || 'NO CONTENT' }}</span>
  </template>
</el-table-column>
        <el-table-column prop="responder_phone" label="Contact Phone" width="150">
  <template #default="{ row }">
    <span>{{ row.responder_phone || '-' }}</span>
  </template>
</el-table-column>
        <el-table-column prop="response_date" label="Response Time" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.response_date) }}
          </template>
        </el-table-column>
        <el-table-column prop="response_state" label="Status" width="100">
          <template #default="{ row }">
            <el-tag :type="getResponseStatusType(row.response_state)">
              {{ getResponseStatusText(row.response_state) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Actions" width="200" fixed="right">
          <template #default="{ row }">
            <!-- Debug information -->
            <div style="font-size: 12px; color: #999;">
              RS:{{ row.response_state }} | 
              MY:{{ isMyRequest ? 'Y' : 'N' }} |
              Show:{{ row.response_state === 0 && isMyRequest ? 'Y' : 'N' }}
            </div>
            <div v-if="row.response_state === 0 && isMyRequest">
              <el-button
                type="success"
                size="small"
                @click="handleAccept(row)"
                style="margin-right: 5px;"
              >
                Accept
              </el-button>
              <el-button
                type="danger"
                size="small"
                @click="handleReject(row)"
              >
                Reject
              </el-button>
            </div>
            <el-button
              type="primary"
              size="small"
              @click="viewResponseDetail(row)"
              plain
            >
              View Detail
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <Pagination
        v-model="responsesPagination"
        :total="responsesTotal"
        @change="loadResponses"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getNeedDetail, getNeedResponses, deleteNeed } from '@/api/serviceRequest'
import { acceptResponse, rejectResponse } from '@/api/match'
import { getServiceTypes } from '@/api/user'
import { useUserStore } from '@/stores/user'
import Pagination from '@/components/Pagination.vue'
import { RESPONSE_STATUS_TEXT, RESPONSE_STATUS_TYPE, CITIES } from '@/utils/constants'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const detail = ref(null)
const responsesLoading = ref(false)
const responsesList = ref([])
const responsesTotal = ref(0)
const responsesPagination = reactive({ page: 1, size: 10 })
const serviceTypes = ref([])

const isMyRequest = computed(() => {
  // 确保detail和userStore.userInfo都存在并且有正确的字段
  if (!detail.value || !userStore.userInfo || !userStore.userInfo.id) {
    return false
  }
  
  // 转换为数字进行比较，以防一个是字符串一个是数字
  const requestUserId = Number(detail.value.psr_userid)
  const currentUserId = Number(userStore.userInfo.id)
  
  console.log('Checking isMyRequest:')
  console.log('- detail.value:', detail.value)
  console.log('- psr_userid:', detail.value.psr_userid, '(type:', typeof detail.value.psr_userid, ')')
  console.log('- userStore.userInfo:', userStore.userInfo)
  console.log('- userStore.userInfo.id:', userStore.userInfo.id, '(type:', typeof userStore.userInfo.id, ')')
  console.log('- requestUserId:', requestUserId)
  console.log('- currentUserId:', currentUserId)
  console.log('- Comparison result:', requestUserId === currentUserId)
  
  return requestUserId === currentUserId
})

const hasResponses = computed(() => {
  return responsesTotal.value > 0
})

const formatDateTime = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('zh-CN')
}

const getResponseStatusText = (status) => {
  return RESPONSE_STATUS_TEXT[status] || 'Unknown'
}

const getResponseStatusType = (status) => {
  return RESPONSE_STATUS_TYPE[status] || 'info'
}

const getServiceTypeName = (typeId) => {
  const type = serviceTypes.value.find(t => t.id === typeId)
  return type ? type.name : 'Unknown'
}

const getCityName = (cityId) => {
  const city = CITIES.find(c => c.id === cityId)
  return city ? city.name : cityId
}

// Media file handling
const allFiles = computed(() => {
  return detail.value?.file_list ? detail.value.file_list.split(',') : []
})

const imageFiles = computed(() => {
  const imageExtensions = ['jpg', 'jpeg', 'png', 'gif']
  return allFiles.value.filter(file => {
    const ext = file.split('.').pop().toLowerCase()
    return imageExtensions.includes(ext)
  })
})

const videoFiles = computed(() => {
  const videoExtensions = ['mp4', 'avi', 'mov', 'wmv']
  return allFiles.value.filter(file => {
    const ext = file.split('.').pop().toLowerCase()
    return videoExtensions.includes(ext)
  })
})

const getFullImageUrl = (filename) => {
  return `${import.meta.env.VITE_API_BASE_URL}/api/v1/files/${filename}`
}

const getVideoType = (filename) => {
  const ext = filename.split('.').pop().toLowerCase()
  const typeMap = {
    'mp4': 'video/mp4',
    'avi': 'video/avi',
    'mov': 'video/quicktime',
    'wmv': 'video/x-ms-wmv'
  }
  return typeMap[ext] || 'video/mp4'
}

const loadDetail = async () => {
  loading.value = true
  console.log('Loading detail for request ID:', route.params.id)
  try {
    const res = await getNeedDetail(route.params.id)
    console.log('Response received:', res)
    console.log('Response data:', res.data)
    console.log('psr_userid in response:', res.data?.psr_userid)
    detail.value = res.data
    console.log('Detail value after assignment:', detail.value)
  } catch (error) {
    console.error('Error loading request details:', error)
    ElMessage.error('Failed to load request details')
  } finally {
    loading.value = false
  }
}

const handleEdit = () => {
  if (hasResponses.value) {
    ElMessageBox.confirm(
      'This request already has responses. Editing it may affect those who have responded. Do you want to continue?',
      'Editing Request with Responses',
      {
        confirmButtonText: 'Continue',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }
    ).then(() => {
      router.push(`/needs/edit/${route.params.id}`)
    }).catch(() => {
      // User cancelled
    })
  } else {
    router.push(`/needs/edit/${route.params.id}`)
  }
}

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm(
      'Are you sure you want to delete this service request? This action cannot be undone. Note: This will permanently delete the request and all associated responses.',
      'Confirm Delete',
      {
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }
    )
    
    const response = await deleteNeed(route.params.id)
    console.log('Delete response:', response)
    ElMessage.success('Service request deleted successfully')
    // 返回到列表页
    router.push('/needs')
  } catch (error) {
    console.error('Delete error:', error)
    if (error !== 'cancel') {
      ElMessage.error('Failed to delete service request: ' + (error.message || 'Unknown error'))
    }
  }
}

const loadResponses = async () => {
  responsesLoading.value = true
  try {
    const res = await getNeedResponses(route.params.id, {
      page: responsesPagination.page,
      size: responsesPagination.size
    })
    console.log('Responses loaded:', res)
    console.log('Response items:', res.data.items)
    responsesList.value = res.data.items || []
    responsesTotal.value = res.data.total || 0
  } catch (error) {
    ElMessage.error('Failed to load responses')
  } finally {
    responsesLoading.value = false
  }
}

const handleAccept = async (response) => {
  try {
    await ElMessageBox.confirm(
      `Are you sure you want to accept the response from ${response.responder_name}?`,
      'Confirm Accept',
      {
        confirmButtonText: 'Accept',
        cancelButtonText: 'Cancel',
        type: 'success'
      }
    )
    await acceptResponse(response.response_id)
    ElMessage.success('Response accepted successfully')
    loadResponses()
    loadDetail()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Failed to accept response')
    }
  }
}

const handleReject = async (response) => {
  try {
    await ElMessageBox.confirm(
      `Are you sure you want to reject the response from ${response.responder_name}?`,
      'Confirm Reject',
      {
        confirmButtonText: 'Reject',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }
    )
    await rejectResponse(response.response_id)
    ElMessage.success('Response rejected successfully')
    loadResponses()
    loadDetail()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Failed to reject response')
    }
  }
}

const viewResponseDetail = (response) => {
  // 在这里我们可以打开一个对话框显示响应的详细信息
  ElMessageBox.alert(
    `<div>
      <p><strong>Responder:</strong> ${response.responder_name || '-'}</p>
      <p><strong>Contact Phone:</strong> ${response.responder_phone || '-'}</p>
      <p><strong>Response Time:</strong> ${formatDateTime(response.response_date)}</p>
      <p><strong>Content:</strong> ${response.desc || 'NO CONTENT'}</p>
      ${response.file_list ? `
        <div style="margin-top: 15px;">
          <strong>Attached Files:</strong>
          <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
            ${response.file_list.split(',').map(file => {
              const fileName = file.trim();
              if (!fileName) return '';
              
              const ext = fileName.split('.').pop().toLowerCase();
              const imageExtensions = ['jpg', 'jpeg', 'png', 'gif'];
              const videoExtensions = ['mp4', 'avi', 'mov', 'wmv'];
              
              if (imageExtensions.includes(ext)) {
                return `<div style="width: 150px; height: 150px; overflow: hidden; border-radius: 4px;">
                  <img src="${getFullImageUrl(fileName)}" alt="${fileName}" style="width: 100%; height: 100%; object-fit: cover;" />
                </div>`;
              } else if (videoExtensions.includes(ext)) {
                return `<div style="width: 200px;">
                  <video controls style="width: 100%; height: 150px;">
                    <source src="${getFullImageUrl(fileName)}" type="${getVideoType(fileName)}">
                    Your browser does not support the video tag.
                  </video>
                </div>`;
              } else {
                return `<div><a href="${getFullImageUrl(fileName)}" target="_blank">${fileName}</a></div>`;
              }
            }).join('')}
          </div>
        </div>
      ` : ''}
    </div>`,
    'Response Detail',
    {
      dangerouslyUseHTMLString: true,
      customClass: 'response-detail-dialog'
    }
  );
}

const loadServiceTypes = async () => {
  try {
    const res = await getServiceTypes()
    serviceTypes.value = res.data || []
  } catch (error) {
    ElMessage.error('Failed to load service types')
  }
}

onMounted(async () => {
  await loadDetail()
  await loadResponses()
  await loadServiceTypes()
})
</script>

<style scoped>
.need-detail-page {
  padding: 20px;
}

.detail-card {
  margin-bottom: 20px;
}

.responses-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2,
.card-header h3 {
  margin: 0;
  font-size: 20px;
  color: #303133;
}

.card-header h3 {
  font-size: 18px;
}

/* Media Preview Styles */
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
</style>

<style>
.response-detail-dialog {
  width: 600px !important;
  max-width: 90vw;
}

.response-detail-dialog .el-message-box__content {
  max-height: 70vh;
  overflow-y: auto;
}
</style>
