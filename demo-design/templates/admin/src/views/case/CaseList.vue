<template>
  <div class="case-list">
    <el-card shadow="never" class="filter-card">
      <el-form :inline="true" :model="filters" class="filter-form" @submit.prevent>
        <el-form-item label="名称">
          <el-input v-model="filters.name" placeholder="请输入名称" clearable style="width: 200px" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="filters.enabled" placeholder="全部" clearable style="width: 140px">
            <el-option label="启用" value="true" />
            <el-option label="禁用" value="false" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :icon="Search" @click="reload">查询</el-button>
          <el-button :icon="RefreshLeft" @click="onReset">重置</el-button>
        </el-form-item>
      </el-form>
      <div class="toolbar">
        <el-button type="primary" :icon="Plus" @click="goCreate">+新增</el-button>
      </div>
    </el-card>

    <el-card shadow="never" class="table-card">
      <el-table v-loading="loading" :data="records" stripe style="width: 100%">
        <!-- 序号（首列，硬编码） -->
        <el-table-column label="序号" width="64" align="center">
          <template #default="{ $index }">{{ indexFn($index) }}</template>
        </el-table-column>

        <!-- 主图 -->
        <el-table-column label="主图" width="80" align="center">
          <template #default="{ row }">
            <el-image
              v-if="row.cover"
              :src="row.cover"
              :fit="'cover'"
              style="width: 60px; height: 40px; border-radius: 4px"
              class="cover-img"
            >
              <template #error>
                <div class="cover-placeholder">×</div>
              </template>
            </el-image>
            <div v-else class="cover-placeholder cover-empty">无</div>
          </template>
        </el-table-column>

        <!-- 名称 -->
        <el-table-column prop="name" label="名称" min-width="200" show-overflow-tooltip />

        <!-- 标签 -->
        <el-table-column label="标签" min-width="200">
          <template #default="{ row }">
            <el-tag
              v-for="t in row.tags"
              :key="t"
              type="primary"
              size="small"
              effect="light"
              class="tag-chip"
            >{{ t }}</el-tag>
            <span v-if="!row.tags?.length" class="tag-empty">—</span>
          </template>
        </el-table-column>

        <!-- 排序 -->
        <el-table-column prop="sort" label="排序" width="80" align="center" />

        <!-- 状态 -->
        <el-table-column label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.enabled ? 'success' : 'info'" size="small">
              {{ row.enabled ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>

        <!-- 创建时间 -->
        <el-table-column prop="createdAt" label="创建时间" width="170" />

        <!-- 操作列:固定右侧 -->
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="goDetail(row)">查看</el-button>
            <el-button link type="primary" @click="goEdit(row)">编辑</el-button>
            <el-button link type="danger" @click="onDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        class="pager"
        :current-page="page"
        :page-size="pageSize"
        :total="total"
        :page-sizes="[20, 50, 100]"
        :pager-count="5"
        layout="total, sizes, prev, pager, next, jumper"
        prev-text="上一页"
        next-text="下一页"
        background
        @current-change="(p) => { page = p; loadList() }"
        @size-change="(s) => { pageSize = s; page = 1; loadList() }"
      />
    </el-card>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, RefreshLeft, Plus } from '@element-plus/icons-vue'
import { fetchCaseList, deleteCase } from '@/api/case'
import { makeIndex } from '@/utils/listIndex'

const router = useRouter()

const loading = ref(true)
const records = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)

const filters = ref({ name: '', enabled: '' })
const indexFn = computed(() => makeIndex(page.value, pageSize.value))
// enabled: '' = 全部;'true' = 启用;'false' = 禁用

function buildListQuery() {
  return {
    name: filters.value.name || undefined,
    enabled: filters.value.enabled === '' ? undefined : filters.value.enabled
  }
}

async function loadList() {
  loading.value = true
  try {
    const res = await fetchCaseList({ page: page.value, pageSize: pageSize.value, ...buildListQuery() })
    records.value = res.list
    total.value = res.total
  } catch (err) {
    console.warn('[CaseList] load failed:', err)
    records.value = []
    total.value = 0
    ElMessage.warning('案例列表加载失败')
  } finally {
    loading.value = false
  }
}

function reload() { page.value = 1; loadList() }

function onReset() {
  filters.value = { name: '', enabled: '' }
  reload()
}

function goCreate() { router.push('/case/create') }
function goEdit(row) { router.push(`/case/edit/${row.id}`) }
function goDetail(row) { router.push(`/case/detail/${row.id}`) }

async function onDelete(row) {
  try {
    await ElMessageBox.confirm(`确定要删除「${row.name}」吗?此操作可由 IT 恢复。`, '删除确认', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
  } catch { return /* 用户取消 */ }
  try {
    await deleteCase(row.id)
    ElMessage.success('已删除')
    await loadList()
  } catch (err) {
    ElMessage.error('删除失败')
  }
}

onMounted(loadList)
</script>

<style scoped>
.case-list { display: flex; flex-direction: column; gap: 12px; height: 100%; }
.filter-card { --el-card-padding: 12px 20px; flex-shrink: 0; }
.filter-card :deep(.filter-form) { margin-bottom: 0; }
.filter-card .toolbar { border-top: 1px solid var(--color-border); padding-top: 12px; margin-top: 4px; }

.table-card {
  --el-card-padding: 0;
  flex: 1; min-height: 0;
  display: flex; flex-direction: column;
}
.table-card :deep(.el-card__body) { display: flex; flex-direction: column; flex: 1; min-height: 0; padding: 0; }
.pager { padding: 12px 16px; border-top: 1px solid var(--color-border); flex-shrink: 0; justify-content: flex-end; }

.tag-chip { margin-right: 4px; margin-bottom: 4px; }
.tag-empty { color: var(--color-text-secondary, #909399); font-size: 12px; }

.cover-placeholder {
  width: 60px; height: 40px; border-radius: 4px;
  background: var(--color-bg-disabled, #f5f7fa);
  color: var(--color-text-secondary, #909399);
  display: inline-flex; align-items: center; justify-content: center;
  font-size: 12px;
}
</style>
