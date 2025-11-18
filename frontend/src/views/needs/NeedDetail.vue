<template>
  <div class="need-detail-page">
    <el-card v-loading="loading" class="detail-card">
      <template #header>
        <div class="card-header">
          <h2>Service Request Details</h2>
          <el-button @click="router.back()">Back</el-button>
        </div>
      </template>

      <el-descriptions v-if="detail" :column="2" border>
        <el-descriptions-item label="Request ID">
          {{ detail.srid }}
        </el-descriptions-item>
        <el-descriptions-item label="Service Type">
          {{ detail.service_type_name }}
        </el-descriptions-item>
        <el-descriptions-item label="Status">
          <el-tag :type="detail.ps_state === 0 ? 'success' : 'info'">
            {{ detail.ps_state === 0 ? 'Published' : 'Cancelled' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="Publish Time">
          {{ formatDateTime(detail.ps_time) }}
        </el-descriptions-item>
        <el-descriptions-item label="Publisher">
          {{ detail.publisher_name }}
        </el-descriptions-item>
        <el-descriptions-item label="Contact Phone">
          {{ detail.ps_phone }}
        </el-descriptions-item>
        <el-descriptions-item label="Service Address" :span="2">
          {{ detail.ps_address }}
        </el-descriptions-item>
        <el-descriptions-item label="Description" :span="2">
          {{ detail.ps_content }}
        </el-descriptions-item>
        <el-descriptions-item v-if="detail.ps_remark" label="Remarks" :span="2">
          {{ detail.ps_remark }}
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
        <el-table-column prop="responder_name" label="Responder" width="150" />
        <el-table-column prop="response_content" label="Response Content" show-overflow-tooltip />
        <el-table-column prop="response_phone" label="Contact Phone" width="150" />
        <el-table-column prop="response_time" label="Response Time" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.response_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="response_state" label="Status" width="100">
          <template #default="{ row }">
            <el-tag :type="getResponseStatusType(row.response_state)">
              {{ getResponseStatusText(row.response_state) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Actions" width="120" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="row.response_state === 0 && isMyRequest"
              type="success"
              size="small"
              @click="handleAccept(row)"
            >
              Accept
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
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getNeedDetail, getNeedResponses } from '@/api/serviceRequest'
import { acceptResponse } from '@/api/match'
import { useUserStore } from '@/stores/user'
import Pagination from '@/components/Pagination.vue'
import { RESPONSE_STATUS_TEXT, RESPONSE_STATUS_TYPE } from '@/utils/constants'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const detail = ref(null)
const responsesLoading = ref(false)
const responsesList = ref([])
const responsesTotal = ref(0)
const responsesPagination = reactive({ page: 1, size: 10 })

const isMyRequest = computed(() => {
  return detail.value?.psr_userid === userStore.userInfo.buid
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

const loadDetail = async () => {
  loading.value = true
  try {
    const res = await getNeedDetail(route.params.id)
    detail.value = res.data
  } catch (error) {
    ElMessage.error('Failed to load request details')
  } finally {
    loading.value = false
  }
}

const loadResponses = async () => {
  responsesLoading.value = true
  try {
    const res = await getNeedResponses(route.params.id, {
      page: responsesPagination.page,
      size: responsesPagination.size
    })
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
    await acceptResponse({
      sr_id: route.params.id,
      response_id: response.response_id
    })
    ElMessage.success('Response accepted successfully')
    loadResponses()
    loadDetail()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Failed to accept response')
    }
  }
}

onMounted(() => {
  loadDetail()
  loadResponses()
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
</style>
