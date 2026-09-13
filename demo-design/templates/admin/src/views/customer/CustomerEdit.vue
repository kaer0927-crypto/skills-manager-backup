<template>
  <el-card shadow="never" class="page-card">
    <template #header>
      <span class="page-title">编辑客户</span>
    </template>
    <div v-if="loading" v-loading="true" class="loading-placeholder" />
    <CustomerForm v-else-if="data" mode="edit" :initial-data="data" />
  </el-card>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import CustomerForm from '@/components/customer/CustomerForm.vue'
import { fetchCustomerDetail } from '@/api/customer'

const route = useRoute()
const router = useRouter()
const data = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const id = Number(route.params.id)
    const detail = await fetchCustomerDetail(id)
    if (detail.isDeleted) {
      ElMessage.warning('该客户已被删除，无法编辑')
      router.replace('/customer/list')
      return
    }
    data.value = detail
  } catch (err) {
    ElMessage.error('客户信息加载失败')
    router.replace('/customer/list')
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
  color: var(--color-text-primary);
}
.loading-placeholder {
  height: 200px;
}
</style>
