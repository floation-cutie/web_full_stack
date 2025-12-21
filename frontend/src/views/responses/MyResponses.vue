<template>
  <div class="response-list-page">
    <el-card class="header-card">
      <div class="header-content">
        <h2>My Service Responses</h2>
      </div>
    </el-card>

    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="City">
          <el-select v-model="filterForm.cityId" placeholder="Select city" clearable style="width: 150px">
            <el-option
              v-for="city in cities"
              :key="city.id"
              :label="city.name"
              :value="city.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSearch">Search</el-button>
          <el-button @click="handleReset">Reset</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card">
      <el-table
        v-loading="loading"
        :data="tableData"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="response_id" label="Response ID" width="120" />
        <el-table-column prop="sr_id" label="Request ID" width="120" />
        <el-table-column prop="desc" label="My Response" show-overflow-tooltip>
  <template #default="{ row }">
    <span>{{ row.desc || 'NO CONTENT' }}</span>
  </template>
</el-table-column>
        <el-table-column prop="responder_name" label="Responder Name" width="150">
          <template #default="{ row }">
            <span>{{ row.responder_name || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="responder_phone" label="Responder Phone" width="150">
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
            <el-tag :type="getStatusType(row.response_state)">
              {{ getStatusText(row.response_state) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Actions" width="250" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewRequest(row.sr_id)">
              View Request
            </el-button>
            <el-button
              v-if="row.response_state === 0"
              type="success"
              size="small"
              @click="editResponse(row.response_id)"
            >
              Edit
            </el-button>
            <el-button
              v-if="row.response_state === 0"
              type="warning"
              size="small"
              @click="handleCancel(row.response_id)"
            >
              Cancel
            </el-button>
            <el-button
              v-if="row.response_state === 0"
              type="danger"
              size="small"
              @click="handleDelete(row.response_id)"
            >
              Delete
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <Pagination
        v-model="pagination"
        :total="total"
        @change="loadData"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getMyResponses, cancelResponse, deleteResponse } from '@/api/serviceResponse'
import Pagination from '@/components/Pagination.vue'
import { RESPONSE_STATUS_TEXT, RESPONSE_STATUS_TYPE, CITIES } from '@/utils/constants'

const router = useRouter()

const loading = ref(false)
const tableData = ref([])
const total = ref(0)
const pagination = reactive({ page: 1, size: 10 })

const filterForm = reactive({
  cityId: null
})

const cities = ref(CITIES)

const formatDateTime = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('zh-CN')
}

const getStatusText = (status) => {
  return RESPONSE_STATUS_TEXT[status] || 'Unknown'
}

const getStatusType = (status) => {
  return RESPONSE_STATUS_TYPE[status] || 'info'
}

const loadData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      size: pagination.size,
      // Map cityId to city_id for API
      city_id: filterForm.cityId
    }
    const res = await getMyResponses(params)
    console.log('API Response:', res)
    console.log('Items:', res.data.items)
    tableData.value = res.data.items || []
    total.value = res.data.total || 0
    console.log('Table Data:', tableData.value)
  } catch (error) {
    console.error('Load data error:', error)
    ElMessage.error('Failed to load data')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadData()
}

const handleReset = () => {
  filterForm.cityId = null
  pagination.page = 1
  loadData()
}

const viewRequest = (srId) => {
  router.push(`/needs/${srId}`)
}

const handleCancel = async (id) => {
  try {
    await ElMessageBox.confirm(
      'Are you sure you want to cancel this response?',
      'Confirm Cancel',
      {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }
    )
    await cancelResponse(id)
    ElMessage.success('Response cancelled successfully')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Failed to cancel response')
    }
  }
}

const editResponse = (id) => {
  router.push(`/responses/edit/${id}`)
}

const handleDelete = async (id) => {
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
    await deleteResponse(id)
    ElMessage.success('Response deleted successfully')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Failed to delete response')
    }
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.response-list-page {
  padding: 20px;
}

.header-card {
  margin-bottom: 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h2 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.filter-card {
  margin-bottom: 20px;
}

.table-card {
  margin-bottom: 20px;
}
</style>
