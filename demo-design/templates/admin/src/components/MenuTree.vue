<template>
  <!-- 叶子节点（带 path） -->
  <el-menu-item v-if="isLeaf(node)" :index="node.path" @click="handleClick">
    <el-icon v-if="iconName"><component :is="iconName" /></el-icon>
    <template #title>{{ node.title }}</template>
  </el-menu-item>

  <!-- 父节点：递归 -->
  <el-sub-menu v-else :index="String(node.id)">
    <template #title>
      <el-icon v-if="iconName"><component :is="iconName" /></el-icon>
      <span>{{ node.title }}</span>
    </template>
    <MenuTree
      v-for="child in node.children"
      :key="child.id"
      :node="child"
      @click-leaf="(n) => $emit('click-leaf', n)"
    />
  </el-sub-menu>
</template>

<script setup>
import { computed } from 'vue'
import * as ElIcons from '@element-plus/icons-vue'

const props = defineProps({
  node: { type: Object, required: true }
})
const emit = defineEmits(['click-leaf'])

const isLeaf = (n) => !n.children || n.children.length === 0

const iconName = computed(() => {
  if (!props.node.icon) return null
  return ElIcons[props.node.icon] || null
})

function handleClick() {
  emit('click-leaf', props.node)
}
</script>
