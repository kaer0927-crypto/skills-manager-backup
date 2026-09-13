<template>
  <el-card v-if="loading || actions.length > 0" class="quick-actions" shadow="never">
    <template #header>
      <span class="header-title">常用功能</span>
    </template>

    <!-- 加载骨架 -->
    <div v-if="loading" class="grid">
      <div v-for="i in 6" :key="i" class="tile tile-skeleton">
        <el-skeleton-item variant="circle" style="width: 28px; height: 28px" />
        <el-skeleton-item variant="text" style="width: 60%; margin-top: 8px" />
      </div>
    </div>

    <!-- 实际数据 -->
    <div v-else class="grid">
      <div
        v-for="action in actions"
        :key="action.id"
        class="tile"
        role="button"
        :title="action.title"
        @click="go(action)"
      >
        <el-icon class="tile-icon">
          <component :is="resolveIcon(action.title)" />
        </el-icon>
        <span class="tile-title">{{ action.title }}</span>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { useRouter } from 'vue-router'
import * as ElIcons from '@element-plus/icons-vue'

defineProps({
  actions: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false }
})

const router = useRouter()

// 静态映射：title 关键字 → Element Plus icon 组件
const ICON_MAP = {
  '销售订单': ElIcons.Document,
  '采购订单': ElIcons.ShoppingCart,
  '入库单': ElIcons.Upload,
  '出库单': ElIcons.Download,
  '实时库存': ElIcons.DataLine,
  '库存预警': ElIcons.Warning,
  '用户管理': ElIcons.User,
  '角色管理': ElIcons.UserFilled,
  '商品档案': ElIcons.Goods,
  '客户档案': ElIcons.OfficeBuilding
}

function resolveIcon(title) {
  for (const key of Object.keys(ICON_MAP)) {
    if (title && title.includes(key)) {
      return ICON_MAP[key]
    }
  }
  return ElIcons.Menu
}

function go(action) {
  if (action?.path) {
    router.push(action.path)
  }
}
</script>

<style scoped>
.quick-actions {
  --el-card-padding: 16px 20px;
}
.header-title {
  font-weight: 600;
  font-size: 15px;
  color: var(--color-text-primary);
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 12px;
}
.tile {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 92px;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  cursor: pointer;
  background: #fff;
  transition: box-shadow 0.15s, transform 0.15s, border-color 0.15s;
}
.tile:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-1px);
  border-color: var(--color-primary);
}
.tile-skeleton {
  cursor: default;
}
.tile-skeleton:hover {
  transform: none;
  border-color: var(--color-border);
  box-shadow: none;
}
.tile-icon {
  font-size: 28px;
  color: var(--color-primary);
  margin-bottom: 8px;
}
.tile-title {
  font-size: 13px;
  color: var(--color-text-regular);
  max-width: 96%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
