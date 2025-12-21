<template>
  <div class="browse-needs-page">
    <el-card class="header-card">
      <div class="header-content">
        <h2>All Service Requests</h2>
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
        <el-table-column prop="sr_id" label="ID" width="80" />
        <el-table-column prop="sr_title" label="Title" show-overflow-tooltip min-width="150" />
        <el-table-column prop="stype_id" label="Service Type" width="120">
          <template #default="{ row }">
            {{ getServiceTypeName(row.stype_id) }}
          </template>
        </el-table-column>
        <el-table-column prop="desc" label="Description" show-overflow-tooltip />
        <el-table-column prop="city_name" label="City" width="100" />
        <el-table-column prop="ps_begindate" label="Start Date" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.ps_begindate) }}
          </template>
        </el-table-column>
        <el-table-column prop="psr_userid" label="Publisher" width="120">
          <template #default="{ row }">
            {{ row.publisher_name || 'Unknown' }}
          </template>
        </el-table-column>
        <el-table-column label="Actions" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewDetail(row.sr_id)">
              View
            </el-button>
            <el-button 
              type="success" 
              size="small" 
              @click="respondToRequest(row.sr_id)"
              :disabled="row.psr_userid === currentUser.id"
            >
              Respond
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
import { ElMessage } from 'element-plus'
import { getAllNeeds } from '@/api/serviceRequest'
import { useUserStore } from '@/stores/user'
import Pagination from '@/components/Pagination.vue'
import { getServiceTypes } from '@/api/user'
import { CITIES } from '@/utils/constants'

const router = useRouter()
const userStore = useUserStore()
const currentUser = userStore.userInfo

const loading = ref(false)
const tableData = ref([])
const total = ref(0)
const pagination = reactive({ page: 1, size: 10 })
const serviceTypes = ref([])
const cities = ref(CITIES)

const filterForm = reactive({
  serviceTypeId: null,
  cityId: null
})

const formatDateTime = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('zh-CN')
}

const getServiceTypeName = (typeId) => {
  const type = serviceTypes.value.find(t => t.id === typeId)
  return type ? type.name : typeId
}

const loadData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      size: pagination.size,
      ps_state: 0, // Only show published requests
      ...filterForm
    }
    
    // Map serviceTypeId to stype_id for API
    if (params.serviceTypeId) {
      params.stype_id = params.serviceTypeId
      delete params.serviceTypeId
    }
    
    // Map cityId to city_id for API
    if (params.cityId) {
      params.city_id = params.cityId
      delete params.cityId
    }
    
    console.log('Sending request with params:', params)
    
    const res = await getAllNeeds(params)
    console.log('Received response:', res)
    
    const data = res.data || res
    
    tableData.value = data.items || []
    total.value = data.total || 0
  } catch (error) {
    console.error('Error loading data:', error)
    ElMessage.error(error.response?.data?.detail || 'Failed to load data')
  } finally {
    loading.value = false
  }
}

const loadServiceTypes = async () => {
  try {
    const res = await getServiceTypes()
    serviceTypes.value = res.data || []
  } catch (error) {
    ElMessage.error('Failed to load service types')
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadData()
}

const handleReset = () => {
  filterForm.serviceTypeId = null
  filterForm.cityId = null
  pagination.page = 1
  loadData()
}

const viewDetail = (id) => {
  router.push(`/needs/${id}`)
}

const respondToRequest = (id) => {
  router.push(`/responses/create/${id}`)
}

onMounted(() => {
  loadData()
  loadServiceTypes()
})
</script>

<style scoped>
.browse-needs-page {
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