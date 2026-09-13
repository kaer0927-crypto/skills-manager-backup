<template>
  <el-card shadow="never" class="page-card">
    <template #header><span class="page-title">新增案例</span></template>
    <CaseForm mode="create" />
  </el-card>
</template>

<script setup>
import CaseForm from '@/components/case/CaseForm.vue'
</script>

<style scoped>
.page-card {
  --el-card-padding: 20px 24px;
}
.page-title {
  font-weight: 600;
  font-size: 15px;
  color: var(--color-text-primary, #303133);
}
</style>
