<template>
  <el-container class="main-layout">
    <el-aside :width="asideWidth" class="aside">
      <!-- Logo 区 -->
      <div class="logo" @click="$router.push('/')">
        <el-icon class="logo-icon"><Box /></el-icon>
        <span v-show="!collapsed" class="logo-text">admin</span>
      </div>

      <!-- 折叠按钮 -->
      <div class="collapse-btn" @click="toggleCollapsed">
        <el-icon>
          <Fold v-if="!collapsed" />
          <Expand v-else />
        </el-icon>
      </div>

      <!-- 菜单区 -->
      <el-scrollbar class="menu-scroll">
        <el-menu
          :default-active="route.path"
          :collapse="collapsed"
          :collapse-transition="false"
          background-color="#001529"
          text-color="#bfcbd9"
          active-text-color="#fff"
        >
          <MenuTree
            v-for="item in menuStore.menuList"
            :key="item.id"
            :node="item"
            @click-leaf="onMenuClick"
          />
        </el-menu>
      </el-scrollbar>

      <!-- 个人中心入口 -->
      <div class="personal-center" @click="onPersonalClick">
        <el-avatar :size="32" class="avatar">A</el-avatar>
        <div v-show="!collapsed" class="user-info">
          <div class="user-name">admin</div>
          <div class="user-role">超级管理员</div>
        </div>
      </div>
    </el-aside>

    <el-container>
      <el-header class="header" :height="`var(--layout-tabs-height)`">
        <TopTabs />
      </el-header>
      <el-main class="main">
        <router-view v-slot="{ Component, route: r }">
          <component :is="Component" :key="r.fullPath" />
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Box, Fold, Expand } from '@element-plus/icons-vue'
import MenuTree from '@/components/MenuTree.vue'
import TopTabs from '@/components/TopTabs.vue'
import { useMenuStore } from '@/stores/menu'
import { useTabsStore } from '@/stores/tabs'

const route = useRoute()
const router = useRouter()
const menuStore = useMenuStore()
const tabsStore = useTabsStore()

const collapsed = ref(false)
const asideWidth = computed(() =>
  collapsed.value ? 'var(--layout-aside-collapsed-width)' : 'var(--layout-aside-width)'
)

function toggleCollapsed() {
  collapsed.value = !collapsed.value
  localStorage.setItem('jzerp_aside_collapsed', collapsed.value ? '1' : '0')
}

// 恢复折叠状态
const saved = localStorage.getItem('jzerp_aside_collapsed')
if (saved === '1') collapsed.value = true

// 菜单点击：切换 tab + 路由
function onMenuClick(node) {
  if (!node.path) return
  tabsStore.addTab({
    path: node.path,
    name: node.name,
    title: node.title,
    closable: true
  })
  router.push(node.path)
}

// 个人中心 dropdown 模拟
function onPersonalClick(event) {
  // phase 1 不做 dropdown 组件，简单用 message 提示
  // 简化处理：直接给两个提示
  const choice = event.shiftKey ? '退出登录' : '个人中心'
  ElMessage.info(`${choice} - 功能开发中`)
}

// 路由变化时同步 tab
watch(
  () => route.path,
  (path) => {
    // 首页特殊处理：避免 addTab 重复添加（已由 init() 注入）
    if (path === '/home') {
      tabsStore.setActive('/home')
      return
    }
    const meta = route.meta || {}
    tabsStore.addTab({
      path,
      name: route.name,
      title: meta.title || path,
      affix: !!meta.affix,
      closable: !meta.affix
    })
  },
  { immediate: true }
)
</script>

<style scoped>
.main-layout {
  height: 100vh;
}
.aside {
  background: #001529;
  position: relative;
  display: flex;
  flex-direction: column;
  transition: width 0.2s;
}
.logo {
  height: var(--layout-aside-logo-height);
  display: flex;
  align-items: center;
  padding: 0 16px;
  color: #fff;
  cursor: pointer;
  border-bottom: 1px solid #1f2d3d;
}
.logo-icon {
  font-size: 24px;
  margin-right: 8px;
  color: var(--color-primary);
}
.logo-text {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 1px;
}
.collapse-btn {
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 12px;
  color: #bfcbd9;
  cursor: pointer;
  border-bottom: 1px solid #1f2d3d;
}
.collapse-btn:hover {
  color: #fff;
}
.menu-scroll {
  flex: 1;
  min-height: 0;
}
.personal-center {
  height: var(--aside-personal-center-height);
  display: flex;
  align-items: center;
  padding: 0 16px;
  background: #001529;
  border-top: 1px solid #1f2d3d;
  color: #fff;
  cursor: pointer;
}
.personal-center:hover {
  background: #1f2d3d;
}
.avatar {
  background: var(--color-primary);
  color: #fff;
  flex-shrink: 0;
}
.user-info {
  margin-left: 10px;
  overflow: hidden;
}
.user-name {
  font-size: 13px;
  line-height: 1.2;
}
.user-role {
  font-size: 11px;
  color: #bfcbd9;
}
.header {
  padding: 0;
  --el-header-padding: 0;
}
.main {
  padding: var(--layout-main-padding);
  background: var(--layout-main-bg);
}
</style>
