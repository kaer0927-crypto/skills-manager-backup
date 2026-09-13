<template>
  <div class="customer-filter">
    <el-form :inline="true" :model="local" @submit.prevent>
      <el-form-item label="客户姓名">
        <el-input
          v-model="local.name"
          placeholder="姓名"
          clearable
          style="width: 140px"
          @keyup.enter="emitSearch"
        />
      </el-form-item>
      <el-form-item label="手机号">
        <el-input
          v-model="local.phone"
          placeholder="手机号"
          clearable
          style="width: 160px"
          @keyup.enter="emitSearch"
        />
      </el-form-item>
      <el-form-item label="来源">
        <el-select v-model="local.source" placeholder="全部" clearable style="width: 130px">
          <el-option v-for="s in options.sources || []" :key="s" :label="options.sourceMap[s]" :value="s" />
        </el-select>
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="local.status" placeholder="全部" clearable style="width: 130px">
          <el-option v-for="s in options.statuses || []" :key="s" :label="options.statusMap[s]" :value="s" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" :icon="Search" @click="emitSearch">查询</el-button>
        <el-button :icon="RefreshLeft" @click="emitReset">重置</el-button>
        <el-button text :icon="ArrowDown" @click="$emit('more')">
          更多筛选
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'
import { Search, RefreshLeft, ArrowDown } from '@element-plus/icons-vue'

const props = defineProps({
  modelValue: { type: Object, required: true },
  options: { type: Object, default: () => ({}) }
})
const emit = defineEmits(['update:modelValue', 'search', 'reset', 'more'])

const local = reactive({ name: '', phone: '', source: '', status: '' })
watch(
  () => props.modelValue,
  (v) => { Object.assign(local, v) },
  { immediate: true, deep: true }
)
watch(local, (v) => { emit('update:modelValue', { ...v }) }, { deep: true })

function emitSearch() { emit('search') }
function emitReset() {
  Object.assign(local, { name: '', phone: '', source: '', status: '' })
  emit('reset')
}
</script>

<style scoped>
.customer-filter {
  padding: 4px 0;
}
</style>
