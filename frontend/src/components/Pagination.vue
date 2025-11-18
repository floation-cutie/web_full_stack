<template>
  <div class="pagination-wrapper">
    <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :total="total"
      :page-sizes="[10, 20, 50, 100]"
      layout="total, sizes, prev, pager, next, jumper"
      @current-change="handlePageChange"
      @size-change="handleSizeChange"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  total: { type: Number, required: true },
  modelValue: { type: Object, required: true }
})

const emit = defineEmits(['update:modelValue', 'change'])

const currentPage = computed({
  get: () => props.modelValue.page,
  set: (val) => emit('update:modelValue', { ...props.modelValue, page: val })
})

const pageSize = computed({
  get: () => props.modelValue.size,
  set: (val) => emit('update:modelValue', { ...props.modelValue, size: val })
})

const handlePageChange = (page) => {
  emit('change', { page, size: pageSize.value })
}

const handleSizeChange = (size) => {
  emit('change', { page: 1, size })
}
</script>

<style scoped>
.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>
