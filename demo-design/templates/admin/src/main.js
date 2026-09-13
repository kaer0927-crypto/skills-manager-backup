import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import ElementPlus from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router, { buildRoutesFromMenu } from './router'
import { useMenuStore } from './stores/menu'
import { useTabsStore } from './stores/tabs'
import './styles/index.css'

async function bootstrap() {
  const app = createApp(App)
  const pinia = createPinia()
  pinia.use(piniaPluginPersistedstate)

  app.use(pinia)
  app.use(router)
  // ElementPlus 全局中文:分页 "Total/Go to"、日期选择器、上传按钮、空态等统一本地化
  app.use(ElementPlus, { locale: zhCn })

  // 1. 加载菜单（失败用 fallback）
  const menuStore = useMenuStore()
  await menuStore.loadMenu()

  // 2. 注入动态路由到 MainLayout
  const dynamicRoutes = buildRoutesFromMenu(menuStore.menuList)
  dynamicRoutes.forEach((r) => {
    router.addRoute('MainLayout', r)
  })

  // 3. 初始化 tab store
  const tabsStore = useTabsStore()
  tabsStore.init()

  // 4. 等路由 ready 后挂载
  await router.isReady()
  app.mount('#app')
}

bootstrap()
