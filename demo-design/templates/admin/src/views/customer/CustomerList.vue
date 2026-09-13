<template>
  <div class="customer-list">
    <!-- 筛选 + 工具栏：固定顶部 -->
    <el-card shadow="never" class="filter-card">
      <CustomerFilter
        v-model="inlineFilters"
        :options="options"
        @search="reload"
        @reset="onInlineReset"
        @more="drawerVisible = true"
      />
      <CustomerToolbar
        @create="goCreate"
        @export="onExport"
        @columns="columnSettingVisible = true"
      />
    </el-card>

    <!-- 表格 + 分页：表格区，垂直/横向滚动时表头/操作列固定 -->
    <el-card shadow="never" class="table-card">
      <CustomerTable
        :data="customers"
        :columns="columns"
        :options="options"
        :loading="loading"
        :page="page"
        :page-size="pageSize"
        @view="goDetail"
        @edit="goEdit"
        @delete="onDelete"
      />
      <el-pagination
        class="pager"
        :current-page="page"
        :page-size="pageSize"
        :total="total"
        :page-sizes="[20, 50, 100]"
        :pager-count="5"
        layout="total, sizes, prev, pager, next, jumper"
        background
        @current-change="(p) => { page = p; loadList() }"
        @size-change="(s) => { pageSize = s; page = 1; loadList() }"
      />
    </el-card>

    <!-- 抽屉 -->
    <CustomerFilterDrawer
      v-model:visible="drawerVisible"
      v-model:filters="drawerFilters"
      :options="options"
      @apply="reload"
      @reset="onDrawerReset"
    />

    <!-- 列设置 -->
    <CustomerColumnSetting
      v-model:visible="columnSettingVisible"
      v-model:columns="columns"
      @reset-default="resetDefaultColumns"
    />
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import * as XLSX from 'xlsx'
import CustomerFilter from '@/components/customer/CustomerFilter.vue'
import CustomerFilterDrawer from '@/components/customer/CustomerFilterDrawer.vue'
import CustomerToolbar from '@/components/customer/CustomerToolbar.vue'
import CustomerColumnSetting from '@/components/customer/CustomerColumnSetting.vue'
import CustomerTable from '@/components/customer/CustomerTable.vue'
import { fetchCustomerList, deleteCustomer } from '@/api/customer'
import { fetchCustomerOptions } from '@/api/options'
import { DEFAULT_COLUMNS, CITY_NAME_MAP, REGION_NAME_MAP } from '@/mock/customerOptions'

const STORAGE_KEY = 'jzerp_customer_columns_v1'
const router = useRouter()

const loading = ref(true)
const customers = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)

const inlineFilters = ref({ name: '', phone: '', source: '', status: '' })
const drawerFilters = ref({ city: '', region: '', assignedTo: '', createdAtRange: [] })

const columns = ref([])
const drawerVisible = ref(false)
const columnSettingVisible = ref(false)

const options = ref({ sources: [], statuses: [], assignees: [], sourceMap: {}, statusMap: {}, statusTagType: {} })

// 把 UI filters 映射为 API query
function buildListQuery() {
  const f = { ...inlineFilters.value, ...drawerFilters.value }
  const [start, end] = f.createdAtRange || []
  return {
    name: f.name || undefined,
    phone: f.phone || undefined,
    source: f.source || undefined,
    status: f.status || undefined,
    city: f.city || undefined,
    region: f.region || undefined,
    assignedTo: f.assignedTo || undefined,
    createdAtStart: start || undefined,
    createdAtEnd: end || undefined
  }
}

async function loadList() {
  loading.value = true
  try {
    const res = await fetchCustomerList({ page: page.value, pageSize: pageSize.value, ...buildListQuery() })
    customers.value = res.list
    total.value = res.total
  } catch (err) {
    console.warn('[CustomerList] load failed:', err)
    customers.value = []
    total.value = 0
    ElMessage.warning('客户列表加载失败')
  } finally {
    loading.value = false
  }
}

function reload() {
  page.value = 1
  loadList()
}

function onInlineReset() {
  inlineFilters.value = { name: '', phone: '', source: '', status: '' }
  reload()
}

function onDrawerReset() {
  drawerFilters.value = { city: '', region: '', assignedTo: '', createdAtRange: [] }
  reload()
}

function goCreate() { router.push('/customer/create') }
function goEdit(row) { router.push(`/customer/edit/${row.id}`) }
function goDetail(row) { router.push(`/customer/detail/${row.id}`) }

async function onDelete(row) {
  try {
    await ElMessageBox.confirm(`确定要删除客户「${row.name}」吗？此操作可由 IT 恢复。`, '删除确认', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
  } catch {
    return // 用户取消
  }
  try {
    await deleteCustomer(row.id)
    ElMessage.success('已删除')
    await loadList()
  } catch (err) {
    ElMessage.error('删除失败')
  }
}

function resetDefaultColumns() {
  localStorage.removeItem(STORAGE_KEY)
  columns.value = JSON.parse(JSON.stringify(DEFAULT_COLUMNS))
  ElMessage.success('已恢复默认列设置')
}

// === xlsx 导出 ===
function pad(n) { return String(n).padStart(2, '0') }
function timestamp() {
  const d = new Date()
  return `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}_${pad(d.getHours())}${pad(d.getMinutes())}${pad(d.getSeconds())}`
}

function onExport() {
  if (customers.value.length === 0) {
    ElMessage.info('当前页暂无数据可导出')
    return
  }
  if (customers.value.length > 100) {
    ElMessage.warning('当前页数据超过 100 条，请缩小筛选范围或翻页后导出')
    return
  }
  const rows = customers.value.map(c => {
    const o = options.value
    return {
      '客户姓名': c.name,
      '手机号': c.phone,
      '来源': o.sourceMap[c.source] || c.source,
      '城市': CITY_NAME_MAP[c.city] || c.city,
      '区/县': REGION_NAME_MAP[c.region] || c.region,
      '状态': o.statusMap[c.status] || c.status,
      '跟进人': c.assignedTo || '未分配',
      '最后跟进': c.lastFollowedAt || '',
      '备注': c.remark || '',
      '创建时间': c.createdAt
    }
  })
  const ws = XLSX.utils.json_to_sheet(rows)
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, '客户档案')
  XLSX.writeFile(wb, `客户档案_${timestamp()}.xlsx`)
  ElMessage.success('已导出')
}

// 初始化：options + columns
async function loadOptions() {
  try {
    const opts = await fetchCustomerOptions()
    options.value = opts
  } catch (err) {
    console.warn('[CustomerList] options load failed:', err)
  }
}

function loadColumns() {
  const cached = localStorage.getItem(STORAGE_KEY)
  if (cached) {
    try {
      columns.value = JSON.parse(cached)
      return
    } catch { /* 损坏的缓存 */ }
  }
  columns.value = JSON.parse(JSON.stringify(DEFAULT_COLUMNS))
}

watch(columns, (v) => {
  if (v && v.length) localStorage.setItem(STORAGE_KEY, JSON.stringify(v))
}, { deep: true })

// 翻页/每页大小由 el-pagination 的 @current-change / @size-change 直接触发；筛选/重置由子组件 emit 触发 reload()
// 不在 page/pageSize 上加 watcher，避免 reload() 内 page=1 引发回环

onMounted(async () => {
  loadColumns()
  await loadOptions()
  await loadList()
})
</script>

<style scoped>
.customer-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  height: 100%;
}
.filter-card {
  --el-card-padding: 12px 20px;
  flex-shrink: 0;
}
.table-card {
  --el-card-padding: 0;
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
}
.table-card :deep(.el-card__body) {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  padding: 0;
}
.pager {
  padding: 12px 16px;
  border-top: 1px solid var(--color-border);
  flex-shrink: 0;
  justify-content: flex-end;
}
</style>
