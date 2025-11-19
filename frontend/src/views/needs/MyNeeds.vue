<template>
  <div class="need-list-page">
    <el-card class="header-card">
      <div class="header-content">
        <h2>My Service Requests</h2>
        <el-button type="primary" @click="router.push('/needs/create')">
          <el-icon><Plus /></el-icon>
          Publish New Request
        </el-button>
      </div>
    </el-card>

    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="Service Type">
          <el-select v-model="filterForm.serviceTypeId" placeholder="All" clearable style="width: 200px">
            <el-option
              v-for="type in serviceTypes"
              :key="type.id"
              :label="type.name"
              :value="type.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Status">
          <el-select v-model="filterForm.status" placeholder="All" clearable style="width: 150px">
            <el-option label="Published" :value="0" />
            <el-option label="Cancelled" :value="-1" />
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
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="stype_id" label="Service Type" width="120" />
        <el-table-column prop="ps_desc" label="Description" show-overflow-tooltip />
        <el-table-column prop="cityID" label="City" width="100" />
        <el-table-column prop="ps_begindate" label="Start Date" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.ps_begindate) }}
          </template>
        </el-table-column>
        <el-table-column prop="ps_state" label="Status" width="100">
          <template #default="{ row }">
            <el-tag :type="row.ps_state === 0 ? 'success' : 'info'">
              {{ row.ps_state === 0 ? 'Published' : 'Cancelled' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Actions" width="250" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewDetail(row.id)">
              View
            </el-button>
            <el-button
              v-if="row.ps_state === 0"
              type="warning"
              size="small"
              @click="handleCancel(row.id)"
            >
              Cancel
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click="handleDelete(row.id)"
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
import { Plus } from '@element-plus/icons-vue'
import { getMyNeeds, cancelNeed, deleteNeed } from '@/api/serviceRequest'
import { getServiceTypes } from '@/api/user'
import Pagination from '@/components/Pagination.vue'
import { SERVICE_TYPES } from '@/utils/constants'

const router = useRouter()

const loading = ref(false)
const tableData = ref([])
const total = ref(0)
const pagination = reactive({ page: 1, size: 10 })
const serviceTypes = ref(SERVICE_TYPES)

const filterForm = reactive({
  serviceTypeId: null,
  status: null
})

const formatDateTime = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('zh-CN')
}

const loadData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      size: pagination.size,
      ...filterForm
    }
    const res = await getMyNeeds(params)
    tableData.value = res.data.items || []
    total.value = res.data.total || 0
  } catch (error) {
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
  filterForm.serviceTypeId = null
  filterForm.status = null
  pagination.page = 1
  loadData()
}

const viewDetail = (id) => {
  router.push(`/needs/${id}`)
}

const handleCancel = async (id) => {
  try {
    await ElMessageBox.confirm(
      'Are you sure you want to cancel this request?',
      'Confirm Cancel',
      {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }
    )
    await cancelNeed(id)
    ElMessage.success('Request cancelled successfully')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Failed to cancel request')
    }
  }
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm(
      'Are you sure you want to delete this request? This action cannot be undone.',
      'Confirm Delete',
      {
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        type: 'error'
      }
    )
    await deleteNeed(id)
    ElMessage.success('Request deleted successfully')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Failed to delete request')
    }
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.need-list-page {
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

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
