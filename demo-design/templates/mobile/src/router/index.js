import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { title: '首页', keepAlive: true }
  },
  {
    path: '/features',
    name: 'Features',
    component: () => import('../views/Features.vue'),
    meta: { title: '功能', keepAlive: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: { title: '我的', keepAlive: true }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.afterEach((to) => {
  if (to.meta?.title) {
    document.title = `${to.meta.title} - 移动端 Demo`
  }
})

export default router
