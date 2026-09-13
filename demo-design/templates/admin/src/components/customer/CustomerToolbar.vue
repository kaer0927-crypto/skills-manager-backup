<template>
  <div class="customer-toolbar">
    <el-button type="primary" :icon="Plus" @click="$emit('create')">新增客户</el-button>
    <el-button :icon="Download" @click="$emit('export')">导出</el-button>
    <el-button :icon="Setting" @click="$emit('columns')">列设置</el-button>
  </div>
</template>

<script setup>
import { Plus, Download, Setting } from '@element-plus/icons-vue'

defineEmits(['create', 'export', 'columns'])
</script>

<style scoped>
.customer-toolbar {
  display: flex;
  gap: 8px;
  padding: 8px 0;
}
</style>
