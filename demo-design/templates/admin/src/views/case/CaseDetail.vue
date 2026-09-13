<template>
  <el-card shadow="never" class="page-card">
    <template #header>
      <span class="page-title">案例详情</span>
    </template>
    <CaseForm v-if="!loading" mode="view" :initial-data="data" />
  </el-card>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import CaseForm from '@/components/case/CaseForm.vue'
import { fetchCaseDetail } from '@/api/case'

const route = useRoute()
const router = useRouter()
const id = route.params.id
const data = ref({})
const loading = ref(true)

onMounted(async () => {
  try {
    const detail = await fetchCaseDetail(id)
    data.value = detail
  } catch (err) {
    ElMessage.error('案例信息加载失败')
    router.replace('/case/list')
  } finally {
    loading.value = false
  }
})
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
