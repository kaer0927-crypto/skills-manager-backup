<template>
  <el-table
    v-loading="loading"
    :data="data"
    :empty-text="emptyText"
    stripe
    style="width: 100%"
    class="customer-table"
  >
    <!-- 序号列（首列，硬编码，不进列设置） -->
    <el-table-column label="序号" width="64" align="center">
      <template #default="{ $index }">{{ indexFn($index) }}</template>
    </el-table-column>

    <el-table-column
      v-for="col in visibleColumns"
      :key="col.prop"
      :prop="col.prop"
      :label="col.label"
      :width="col.width"
      :min-width="col.width"
      :fixed="col.fixed ? 'left' : false"
    >
      <template #default="{ row }">
        <!-- 来源 -->
        <span v-if="col.prop === 'source'">{{ options.sourceMap[row.source] || row.source }}</span>
        <!-- 状态（带 el-tag） -->
        <el-tag
          v-else-if="col.prop === 'status'"
          :type="options.statusTagType[row.status]"
          size="small"
        >
          {{ options.statusMap[row.status] || row.status }}
        </el-tag>
        <!-- 城市 -->
        <span v-else-if="col.prop === 'city'">{{ cityNameMap[row.city] || row.city }}</span>
        <!-- 跟进人 -->
        <span v-else-if="col.prop === 'assignedTo'">{{ row.assignedTo || '未分配' }}</span>
        <!-- 最后跟进 -->
        <span v-else-if="col.prop === 'lastFollowedAt'">{{ row.lastFollowedAt || '—' }}</span>
        <!-- 默认 -->
        <span v-else>{{ row[col.prop] }}</span>
      </template>
    </el-table-column>

    <!-- 操作列：固定右侧 -->
    <el-table-column label="操作" width="180" fixed="right">
      <template #default="{ row }">
        <el-button link type="primary" @click="$emit('view', row)">查看</el-button>
        <el-button link type="primary" @click="$emit('edit', row)">编辑</el-button>
        <el-button link type="danger" @click="$emit('delete', row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup>
import { computed } from 'vue'
import { CITY_NAME_MAP } from '@/mock/customerOptions'
import { makeIndex } from '@/utils/listIndex'

const props = defineProps({
  data: { type: Array, default: () => [] },
  columns: { type: Array, default: () => [] },
  options: { type: Object, default: () => ({}) },
  loading: { type: Boolean, default: false },
  emptyText: { type: String, default: '暂无客户数据' },
  page: { type: Number, default: 1 },
  pageSize: { type: Number, default: 20 }
})
defineEmits(['view', 'edit', 'delete'])

const visibleColumns = computed(() => props.columns.filter(c => c.visible))
const cityNameMap = CITY_NAME_MAP
const indexFn = computed(() => makeIndex(props.page, props.pageSize))
</script>

<style scoped>
.customer-table {
  flex: 1;
  min-height: 0;
}
</style>
