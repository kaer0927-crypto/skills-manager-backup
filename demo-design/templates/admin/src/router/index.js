import { createRouter, createWebHashHistory } from 'vue-router'

const Home = () => import('@/views/Home.vue')
const NotFound = () => import('@/views/NotFound.vue')
const EmptyPage = () => import('@/components/EmptyPage.vue')
const MainLayout = () => import('@/layouts/MainLayout.vue')

// === 静态路由 ===
// 客户管理的 4 个路由直接注入 MainLayout children；不走 buildRoutesFromMenu
// （菜单叶子 id:411 仍带 path/name，给 MenuTree 渲染用；SKIP_NAMES 防止重复注入）
const CustomerList   = () => import('@/views/customer/CustomerList.vue')
const CustomerCreate = () => import('@/views/customer/CustomerCreate.vue')
const CustomerEdit   = () => import('@/views/customer/CustomerEdit.vue')
const CustomerDetail = () => import('@/views/customer/CustomerDetail.vue')

// === 案例管理（静态注入；同客户管理） ===
const CaseList   = () => import('@/views/case/CaseList.vue')
const CaseCreate = () => import('@/views/case/CaseCreate.vue')
const CaseEdit   = () => import('@/views/case/CaseEdit.vue')
const CaseDetail = () => import('@/views/case/CaseDetail.vue')

export const staticRoutes = [
  {
    path: '/',
    name: 'MainLayout',
    component: MainLayout,
    redirect: '/home',
    children: [
      { path: 'home', name: 'Home', component: Home, meta: { title: '首页', affix: true } },
      // === 客户管理（静态注入） ===
      { path: 'customer/list',        name: 'CustomerList',   component: CustomerList,   meta: { title: '客户列表' } },
      { path: 'customer/create',      name: 'CustomerCreate', component: CustomerCreate, meta: { title: '新增客户' } },
      { path: 'customer/edit/:id',    name: 'CustomerEdit',   component: CustomerEdit,   meta: { title: '编辑客户' } },
      { path: 'customer/detail/:id',  name: 'CustomerDetail', component: CustomerDetail, meta: { title: '客户详情' } },
      // === 案例管理（静态注入） ===
      { path: 'case/list',       name: 'CaseList',   component: CaseList,   meta: { title: '案例列表' } },
      { path: 'case/create',     name: 'CaseCreate', component: CaseCreate, meta: { title: '新增案例' } },
      { path: 'case/edit/:id',   name: 'CaseEdit',   component: CaseEdit,   meta: { title: '编辑案例' } },
      { path: 'case/detail/:id', name: 'CaseDetail', component: CaseDetail, meta: { title: '案例详情' } }
    ]
  },
  { path: '/404', name: 'NotFound', component: NotFound, meta: { title: '页面不存在' } },
  { path: '/:pathMatch(.*)*', redirect: '/404' }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes: staticRoutes
})

// 跳过已经被静态注入的路由名
const SKIP_NAMES = new Set([
  'CustomerList', 'CustomerCreate', 'CustomerEdit', 'CustomerDetail',
  'CaseList', 'CaseCreate', 'CaseEdit', 'CaseDetail'
])

/**
 * 从菜单生成动态路由（仅叶子节点）
 */
export function buildRoutesFromMenu(menuList) {
  const routes = []
  function walk(nodes) {
    for (const node of nodes || []) {
      if (SKIP_NAMES.has(node.name)) continue
      if (node.children && node.children.length) {
        walk(node.children)
      } else if (node.path) {
        routes.push({
          path: node.path.startsWith('/') ? node.path.slice(1) : node.path,
          name: node.name,
          component: EmptyPage,
          meta: { title: node.title }
        })
      }
    }
  }
  walk(menuList)
  return routes
}

/**
 * 重置路由（用于登出或重新登录场景；phase 1 暂不调用，保留扩展位）
 */
export function resetRouter() {
  // 简化：phase 1 不实现
}

export default router