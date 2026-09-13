<template>
  <div class="empty-page">
    <el-card class="empty-card">
      <div class="empty-title">功能开发中</div>
      <div v-if="title" class="empty-subtitle">{{ title }}</div>
    </el-card>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, default: '' }
})
</script>

<style scoped>
.empty-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 40px - 32px);
}
.empty-card {
  width: 480px;
  text-align: center;
  padding: 40px 20px;
}
.empty-title {
  font-size: 28px;
  color: var(--color-primary);
  font-weight: 500;
  margin-bottom: 12px;
}
.empty-subtitle {
  font-size: 14px;
  color: var(--color-text-secondary);
}
</style>
