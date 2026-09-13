<template>
  <div class="not-found">
    <el-result icon="warning" title="404" sub-title="页面不存在">
      <template #extra>
        <el-button type="primary" @click="$router.push('/')">返回首页</el-button>
      </template>
    </el-result>
  </div>
</template>

<script setup>
// phase 1 简单占位
</script>

<style scoped>
.not-found {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 40px - 32px);
}
</style>
