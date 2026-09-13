<template>
  <el-card shadow="never" class="page-card">
    <template #header>
      <span class="page-title">新增客户</span>
    </template>
    <CustomerForm mode="create" />
  </el-card>
</template>

<script setup>
import CustomerForm from '@/components/customer/CustomerForm.vue'
</script>

<style scoped>
.page-card {
  --el-card-padding: 20px 24px;
}
.page-title {
  font-weight: 600;
  font-size: 15px;
  color: var(--color-text-primary);
}
</style>
