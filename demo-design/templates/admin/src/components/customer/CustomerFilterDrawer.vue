<template>
  <el-drawer
    :model-value="visible"
    title="更多筛选"
    direction="rtl"
    size="380px"
    @update:model-value="$emit('update:visible', $event)"
  >
    <el-form :model="local" label-width="80px" class="drawer-form">
      <el-form-item label="城市">
        <el-select v-model="local.city" placeholder="全部" clearable style="width: 100%">
          <el-option v-for="c in cityOptions" :key="c.code" :label="c.name" :value="c.code" />
        </el-select>
      </el-form-item>
      <el-form-item label="区/县">
        <el-select v-model="local.region" placeholder="全部" clearable :disabled="!local.city" style="width: 100%">
          <el-option v-for="r in regionOptions" :key="r.code" :label="r.name" :value="r.code" />
        </el-select>
      </el-form-item>
      <el-form-item label="跟进人">
        <el-select v-model="local.assignedTo" placeholder="全部" clearable style="width: 100%">
          <el-option v-for="a in options.assignees || []" :key="a" :label="a" :value="a" />
        </el-select>
      </el-form-item>
      <el-form-item label="创建时间">
        <el-date-picker
          v-model="local.createdAtRange"
          type="datetimerange"
          range-separator="至"
          start-placeholder="开始"
          end-placeholder="结束"
          value-format="YYYY-MM-DD HH:mm:ss"
          style="width: 100%"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="drawer-footer">
        <el-button @click="onReset">重置</el-button>
        <el-button type="primary" @click="onApply">应用</el-button>
      </div>
    </template>
  </el-drawer>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { fetchAreaDict } from '@/api/options'

const props = defineProps({
  visible: { type: Boolean, default: false },
  filters: { type: Object, required: true },
  options: { type: Object, default: () => ({}) }
})
const emit = defineEmits(['update:visible', 'update:filters', 'apply', 'reset'])

const areaData = ref([])
const local = reactive({ city: '', region: '', assignedTo: '', createdAtRange: [] })

watch(() => props.filters, (v) => { Object.assign(local, v) }, { immediate: true, deep: true })
watch(local, (v) => { emit('update:filters', { ...v }) }, { deep: true })

// 拉平所有省下的市（去重）
const cityOptions = computed(() => {
  const seen = new Map()
  for (const p of areaData.value) {
    for (const c of p.children || []) {
      if (!seen.has(c.code)) seen.set(c.code, c)
    }
  }
  return Array.from(seen.values())
})
const regionOptions = computed(() => {
  if (!local.city) return []
  for (const p of areaData.value) {
    for (const c of p.children || []) {
      if (c.code === local.city) return c.children || []
    }
  }
  return []
})

watch(() => local.city, () => { local.region = '' })
watch(() => props.visible, async (v) => {
  if (v && areaData.value.length === 0) {
    try { areaData.value = await fetchAreaDict() } catch { /* 抽屉里静默失败即可 */ }
  }
})

function onApply() { emit('apply'); emit('update:visible', false) }
function onReset() {
  Object.assign(local, { city: '', region: '', assignedTo: '', createdAtRange: [] })
  emit('reset')
}
</script>

<style scoped>
.drawer-form {
  padding: 0 8px;
}
.drawer-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
</style>
