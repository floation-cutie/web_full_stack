<template>
  <div class="statistics-container">
    <el-card class="query-card">
      <template #header>
        <div class="card-header">
          <span>Query Filters</span>
        </div>
      </template>

      <el-form :inline="true" :model="queryForm" class="query-form">
        <el-form-item label="Start Month">
          <el-date-picker
            v-model="queryForm.startMonth"
            type="month"
            placeholder="Select start month"
            format="YYYY-MM"
            value-format="YYYY-MM"
            style="width: 200px"
          />
        </el-form-item>

        <el-form-item label="End Month">
          <el-date-picker
            v-model="queryForm.endMonth"
            type="month"
            placeholder="Select end month"
            format="YYYY-MM"
            value-format="YYYY-MM"
            style="width: 200px"
          />
        </el-form-item>

        <el-form-item label="City">
          <el-select
            v-model="queryForm.cityId"
            placeholder="Select city"
            clearable
            style="width: 180px"
          >
            <el-option
              v-for="city in cities"
              :key="city.id"
              :label="city.name"
              :value="city.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="Service Type">
          <el-select
            v-model="queryForm.serviceTypeId"
            placeholder="Select service type"
            clearable
            style="width: 180px"
          >
            <el-option
              v-for="type in serviceTypes"
              :key="type.id"
              :label="type.name"
              :value="type.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            @click="handleQuery"
            :loading="loading"
            :icon="Search"
          >
            Query
          </el-button>
          <el-button @click="handleReset">Reset</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="chart-card">
      <template #header>
        <div class="card-header">
          <span>Service Statistics Trend</span>
        </div>
      </template>
      <div ref="chartRef" style="width: 100%; height: 400px;"></div>
    </el-card>

    <el-card class="table-card">
      <template #header>
        <div class="card-header">
          <span>Statistical Data Details</span>
        </div>
      </template>

      <el-table :data="tableData" stripe border v-loading="loading" style="width: 100%">
        <el-table-column prop="month" label="Month" width="120" />
        <el-table-column prop="serviceType" label="Service Type" width="150" />
        <el-table-column prop="city" label="City" width="120" />
        <el-table-column prop="publishedCount" label="Published Needs" width="140" sortable />
        <el-table-column prop="completedCount" label="Completed Services" width="160" sortable />
        <el-table-column prop="successRate" label="Success Rate" width="120">
          <template #default="{ row }">
            <el-progress
              :percentage="row.successRate"
              :color="getProgressColor(row.successRate)"
              :format="(percentage) => percentage + '%'"
            />
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @current-change="handlePageChange"
          @size-change="handleSizeChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import * as echarts from 'echarts'
import { Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getMonthlyStats } from '@/api/stats'
import { getCities, getServiceTypes } from '@/api/user'

const chartRef = ref(null)
const loading = ref(false)
const tableData = ref([])
const cities = ref([])
const serviceTypes = ref([])
const pagination = ref({ page: 1, size: 10, total: 0 })

let chartInstance = null

const queryForm = ref({
  startMonth: '',
  endMonth: '',
  cityId: null,
  serviceTypeId: null
})

onMounted(async () => {
  initChart()
  await loadFilterOptions()
  await initDefaultDates()
  await handleQuery()
})

const initChart = async () => {
  await nextTick()
  chartInstance = echarts.init(chartRef.value)
  window.addEventListener('resize', () => {
    chartInstance?.resize()
  })
}

const loadFilterOptions = async () => {
  try {
    const [citiesRes, typesRes] = await Promise.all([
      getCities(),
      getServiceTypes()
    ])
    cities.value = citiesRes.data || []
    serviceTypes.value = typesRes.data || []
  } catch (error) {
    ElMessage.error('Failed to load filter options')
  }
}

const initDefaultDates = () => {
  const now = new Date()
  const endMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`

  const startDate = new Date(now.getFullYear(), now.getMonth() - 5, 1)
  const startMonth = `${startDate.getFullYear()}-${String(startDate.getMonth() + 1).padStart(2, '0')}`

  queryForm.value.startMonth = startMonth
  queryForm.value.endMonth = endMonth
}

const handleQuery = async () => {
  if (!queryForm.value.startMonth || !queryForm.value.endMonth) {
    ElMessage.warning('Please select month range')
    return
  }

  if (queryForm.value.startMonth > queryForm.value.endMonth) {
    ElMessage.warning('Start month cannot be later than end month')
    return
  }

  loading.value = true
  try {
    const res = await getMonthlyStats({
      startMonth: queryForm.value.startMonth,
      endMonth: queryForm.value.endMonth,
      cityId: queryForm.value.cityId,
      serviceTypeId: queryForm.value.serviceTypeId,
      page: pagination.value.page,
      size: pagination.value.size
    })

    const data = res.data || res

    tableData.value = (data.items || []).map(item => ({
      month: item.month,
      serviceType: item.service_type_name,
      city: item.city_name,
      publishedCount: item.published_count || 0,
      completedCount: item.completed_count || 0,
      successRate: calculateSuccessRate(item.completed_count, item.published_count)
    }))

    pagination.value.total = data.total || 0

    updateChart(data.chart_data)
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || 'Failed to load statistics')
  } finally {
    loading.value = false
  }
}

const updateChart = (chartData) => {
  if (!chartData) return

  const months = chartData.months || []
  const published = chartData.published_counts || []
  const completed = chartData.completed_counts || []

  const option = {
    title: {
      text: 'Service Statistics Trend',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      textStyle: {
        color: '#fff'
      }
    },
    legend: {
      data: ['Published Needs', 'Completed Services'],
      top: 40,
      left: 'center'
    },
    grid: {
      left: '10%',
      right: '10%',
      top: '15%',
      bottom: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: months,
      boundaryGap: false
    },
    yAxis: {
      type: 'value',
      name: 'Count',
      nameTextStyle: {
        color: '#666'
      }
    },
    series: [
      {
        name: 'Published Needs',
        type: 'line',
        data: published,
        smooth: true,
        itemStyle: {
          color: '#409EFF'
        },
        areaStyle: {
          color: 'rgba(64, 158, 255, 0.2)'
        },
        emphasis: {
          focus: 'series'
        }
      },
      {
        name: 'Completed Services',
        type: 'line',
        data: completed,
        smooth: true,
        itemStyle: {
          color: '#67C23A'
        },
        areaStyle: {
          color: 'rgba(103, 194, 58, 0.2)'
        },
        emphasis: {
          focus: 'series'
        }
      }
    ]
  }

  chartInstance.setOption(option)
}

const calculateSuccessRate = (completed, published) => {
  if (published === 0) return 0
  return Math.round((completed / published) * 100)
}

const getProgressColor = (percentage) => {
  if (percentage >= 80) return '#67C23A'
  if (percentage >= 50) return '#E6A23C'
  return '#F56C6C'
}

const handlePageChange = (page) => {
  pagination.value.page = page
  handleQuery()
}

const handleSizeChange = (size) => {
  pagination.value.size = size
  pagination.value.page = 1
  handleQuery()
}

const handleReset = () => {
  initDefaultDates()
  queryForm.value.cityId = null
  queryForm.value.serviceTypeId = null
  pagination.value.page = 1
  handleQuery()
}
</script>

<style scoped>
.statistics-container {
  padding: 20px;
}

.query-card {
  margin-bottom: 20px;
}

.query-form {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: flex-end;
}

.card-header {
  font-weight: bold;
  font-size: 16px;
  color: #303133;
}

.chart-card {
  margin-bottom: 20px;
}

.table-card {
  margin-bottom: 20px;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

:deep(.el-form-item) {
  margin-bottom: 0;
}

@media (max-width: 768px) {
  .statistics-container {
    padding: 10px;
  }

  .query-form {
    flex-direction: column;
  }

  :deep(.el-select),
  :deep(.el-date-picker) {
    width: 100% !important;
  }
}
</style>
