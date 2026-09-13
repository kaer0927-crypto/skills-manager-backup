<template>
  <div class="app-wrapper">
    <!-- 顶部导航条 -->
    <van-nav-bar
      :title="pageTitle"
      fixed
      placeholder
      safe-area-inset-top
    />

    <!-- 路由出口 -->
    <main class="app-main">
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </main>

    <!-- 底部 Tabbar -->
    <van-tabbar v-model="activeTab" route safe-area-inset-bottom>
      <van-tabbar-item to="/home" icon="home-o">首页</van-tabbar-item>
      <van-tabbar-item to="/features" icon="apps-o">功能</van-tabbar-item>
      <van-tabbar-item to="/profile" icon="user-o">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeTab = ref(0)

// 根据路由显示对应标题
const pageTitle = computed(() => {
  const map = { '/home': '首页', '/features': '功能', '/profile': '我的' }
  return map[route.path] || '移动端 Demo'
})
</script>

<style scoped>
.app-wrapper {
  min-height: 100vh;
  background: #f7f8fa;
  display: flex;
  flex-direction: column;
}

.app-main {
  flex: 1;
  padding-bottom: 50px; /* 给底部 tabbar 留位置 */
}
</style>
