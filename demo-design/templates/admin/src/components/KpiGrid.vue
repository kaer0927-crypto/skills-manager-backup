<template>
  <div class="kpi-grid">
    <!-- 加载骨架 -->
    <el-row v-if="loading" :gutter="16">
      <el-col v-for="i in 3" :key="i" :span="8">
        <el-card class="kpi-card" shadow="never">
          <el-skeleton :rows="2" animated />
        </el-card>
      </el-col>
    </el-row>

    <!-- 空数据 -->
    <el-empty v-else-if="kpis.length === 0" description="暂无数据" />

    <!-- 实际数据 -->
    <el-row v-else :gutter="16">
      <el-col v-for="kpi in kpis" :key="kpi.key" :span="8">
        <el-card class="kpi-card" shadow="hover">
          <div class="kpi-head">
            <el-icon class="kpi-icon" :class="`accent-${kpi.accent}`">
              <component :is="resolveIcon(kpi.icon)" />
            </el-icon>
            <span class="kpi-label">{{ kpi.label }}</span>
          </div>
          <div class="kpi-value">{{ kpi.value }}</div>
          <div v-if="kpi.sub" class="kpi-sub">{{ kpi.sub }}</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import * as ElIcons from '@element-plus/icons-vue'

defineProps({
  kpis: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false }
})

function resolveIcon(name) {
  if (!name) return null
  return ElIcons[name] || null
}
</script>

<style scoped>
.kpi-grid {
  width: 100%;
}
.kpi-card {
  --el-card-padding: 16px 20px;
}
.kpi-head {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}
.kpi-icon {
  font-size: 18px;
}
.kpi-icon.accent-primary { color: var(--color-primary); }
.kpi-icon.accent-success { color: #67c23a; }
.kpi-icon.accent-warning { color: #e6a23c; }
.kpi-icon.accent-danger  { color: var(--color-danger); }
.kpi-label {
  color: var(--color-text-regular);
  font-size: 13px;
}
.kpi-value {
  font-size: 26px;
  font-weight: 600;
  color: var(--color-text-primary);
  line-height: 1.2;
}
.kpi-sub {
  margin-top: 4px;
  font-size: 12px;
  color: var(--color-text-secondary);
}
</style>
