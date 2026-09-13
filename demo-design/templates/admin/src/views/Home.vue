<template>
  <div class="home">
    <KpiGrid :kpis="kpis" :loading="loading" />
    <div class="home-spacer" />
    <QuickActions :actions="actions" :loading="loading" />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import KpiGrid from '@/components/KpiGrid.vue'
import QuickActions from '@/components/QuickActions.vue'
import { fetchDashboard, fetchQuickActions } from '@/api/dashboard'

// 降级数据：mock 失败时使用
const FALLBACK_KPIS = [
  { key: 'customerTotal', label: '客户总数', value: '--', sub: '暂不可用', icon: 'UserFilled', accent: 'primary' },
  { key: 'caseTotal', label: '案例数', value: '--', sub: '暂不可用', icon: 'Document', accent: 'warning' },
  { key: 'todoApproval', label: '待办审批', value: '--', sub: '暂不可用', icon: 'Bell', accent: 'danger' }
]

const FALLBACK_ACTIONS = [
  { id: 1, title: '案例管理', path: '/case/list' },
  { id: 2, title: '客户列表', path: '/customer/list' }
]

const loading = ref(true)
const kpis = ref([])
const actions = ref([])

onMounted(async () => {
  const [dRes, aRes] = await Promise.allSettled([
    fetchDashboard(),
    fetchQuickActions()
  ])

  let failedCount = 0
  if (dRes.status === 'fulfilled') {
    kpis.value = dRes.value?.kpis || []
  } else {
    console.warn('[Home] dashboard failed:', dRes.reason)
    kpis.value = FALLBACK_KPIS
    failedCount++
  }

  if (aRes.status === 'fulfilled') {
    actions.value = aRes.value || []
  } else {
    console.warn('[Home] quick-actions failed:', aRes.reason)
    actions.value = FALLBACK_ACTIONS
    failedCount++
  }

  if (failedCount > 0) {
    ElMessage.warning(
      failedCount === 2 ? '数据加载失败，已显示降级数据' : '部分数据加载失败，已显示降级数据'
    )
  }

  loading.value = false
})
</script>

<style scoped>
.home {
  max-width: 960px;
  margin: 0 auto;
}
.home-spacer {
  height: 16px;
}
</style>
