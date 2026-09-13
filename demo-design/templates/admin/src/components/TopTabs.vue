<template>
  <div class="top-tabs">
    <el-dropdown
      v-for="tab in tabsStore.tabs"
      :key="tab.path"
      trigger="contextmenu"
      @command="(cmd) => handleCommand(cmd, tab)"
      @visible-change="(v) => onContextVisible(v, tab)"
    >
      <div
        class="tab-item"
        :class="{ active: tabsStore.activeTab === tab.path }"
        @click="onClickTab(tab)"
      >
        <span class="tab-title">{{ tab.title }}</span>
        <el-icon
          v-if="tab.closable"
          class="tab-close"
          @click.stop="onClose(tab)"
        >
          <Close />
        </el-icon>
      </div>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item command="close" :disabled="tab.affix">
            关闭当前
          </el-dropdown-item>
          <el-dropdown-item command="others">关闭其他</el-dropdown-item>
          <el-dropdown-item command="left">关闭左侧</el-dropdown-item>
          <el-dropdown-item command="right">关闭右侧</el-dropdown-item>
          <el-dropdown-item command="all">关闭全部</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useTabsStore } from '@/stores/tabs'
import { Close } from '@element-plus/icons-vue'

const router = useRouter()
const tabsStore = useTabsStore()

function onClickTab(tab) {
  tabsStore.setActive(tab.path)
  if (router.currentRoute.value.path !== tab.path) {
    router.push(tab.path)
  }
}

function onClose(tab) {
  tabsStore.removeTab(tab.path)
  // 跳到当前激活的 tab
  if (tabsStore.activeTab !== router.currentRoute.value.path) {
    router.push(tabsStore.activeTab)
  }
}

function handleCommand(cmd, tab) {
  switch (cmd) {
    case 'close':
      tabsStore.removeTab(tab.path)
      break
    case 'others':
      tabsStore.removeOthers(tab.path)
      break
    case 'left':
      tabsStore.removeLeft(tab.path)
      break
    case 'right':
      tabsStore.removeRight(tab.path)
      break
    case 'all':
      tabsStore.removeAll()
      break
  }
  // 兜底：如果当前路由已被关闭，跳到激活 tab
  if (!tabsStore.tabs.some((t) => t.path === router.currentRoute.value.path)) {
    router.push(tabsStore.activeTab)
  }
}

// 占位：可见性切换（后续可加坐标定位）
function onContextVisible(_v, _tab) {}
</script>

<style scoped>
.top-tabs {
  display: flex;
  align-items: center;
  height: var(--layout-tabs-height);
  background: #fff;
  border-bottom: 1px solid var(--color-border);
  padding: 0 8px;
  overflow-x: auto;
  white-space: nowrap;
}
.tab-item {
  display: inline-flex;
  align-items: center;
  height: 28px;
  padding: 0 10px;
  margin-right: 4px;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  color: var(--color-text-regular);
  position: relative;
  user-select: none;
}
.tab-item:hover {
  color: var(--color-primary);
}
.tab-item.active {
  color: var(--color-primary);
  border-color: var(--color-primary);
}
.tab-item.active::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: -1px;
  height: var(--tab-active-line-height);
  background: var(--color-primary);
}
.tab-close {
  margin-left: 6px;
  font-size: 12px;
  border-radius: 50%;
  padding: 2px;
}
.tab-close:hover {
  background: var(--color-danger);
  color: #fff;
}
</style>
