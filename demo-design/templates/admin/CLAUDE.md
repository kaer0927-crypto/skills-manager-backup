# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> 本项目以简体中文为主；代码、文件路径、命令、技术专有名词保留英文。

---

## 项目概览

PC 管理后台 Demo — Vue 3 + Vite + **Element Plus** + Pinia，**仅前端**，无真实后端，数据由 mock 提供（dev 用 `vite-plugin-mock`，prod 用内联 mock 适配器）。内置「客户管理 / 案例管理 / 首页看板」示例模块。

**开发前先读实际代码**：`src/router/index.js`（有哪些路由）、`src/mock/index.js`（有哪些接口与数据）、`src/views/`（页面现状）。README/文档可能滞后于代码。

---

## 常用命令

```bash
npm install        # 首次安装依赖
npm run dev        # dev server（默认 http://localhost:5173，自动开浏览器）
npm run build      # 生产构建 → dist/
npm run preview    # 预览构建产物
npm run lint       # eslint --fix（非必需）
npm run format     # prettier 格式化（非必需）
```

无 `npm test`；验证靠 `npm run dev` + 浏览器人工对照，以及 `npm run build` 能否通过。

---

## 启动顺序（`src/main.js` 的 `bootstrap()`）

1. 创建 app + Pinia（`pinia-plugin-persistedstate`）
2. `app.use(router)`
3. `app.use(ElementPlus, { locale: zhCn })` —— 全局中文
4. `menuStore.loadMenu()` —— 拉菜单（失败走 `src/mock/menuFallback.js`）
5. `buildRoutesFromMenu()` 生成动态路由并 `router.addRoute('MainLayout', ...)`
6. `tabsStore.init()` 初始化多标签页
7. `await router.isReady()` → `app.mount('#app')`

---

## 高层架构

### 路由（`src/router/index.js`）
- `createWebHashHistory()` —— hash 模式，适配静态托管。
- **静态路由**：`home` + 客户管理（list/create/edit/detail）+ 案例管理（list/create/edit/detail）直接注入 `MainLayout.children`。
- **动态路由**：其余菜单叶子由 `buildRoutesFromMenu(menuList)` 生成，指向 `EmptyPage` 占位；`SKIP_NAMES` 防止与静态路由重复注入。
- `/:pathMatch(.*)*` → `/404`。

### 布局（`src/layouts/MainLayout.vue`）
- 侧边 `MenuTree` + 顶部 `TopTabs`（多标签页）+ 内容区 `<router-view>`。

### 状态（`src/stores/`）
- `menu.js`：菜单数据；`tabs.js`：打开的标签页（持久化）。

### Mock（`src/mock/`）
- `index.js` 导出 **单一数据源** `mockEndpoints`：dev 由 `viteMockServe`（default）消费，prod 由 `src/utils/inlineMockAdapter.js`（named）消费，数据零分叉。
- 各业务 mock：`customer.js` / `case.js` / `menu.js` / `dashboard.js` + `*Seed.js` 假数据。
- 接口前缀 `/api`，请求封装在 `src/api/*` → `src/api/request.js`。

### 构建配置（`vite.config.js`）
- `base: './'`（子路径/`file://` 均可）、`@` → `src`、`viteMockServe({ prefix:'/api', mockPath:'src/mock' })`。

---

## 开发约定

- UI 一律优先 Element Plus 组件 + `@element-plus/icons-vue`。
- 新模块流程：`mock/<m>.js`（注册进 `mockEndpoints`）→ `api/<m>.js` → `views/<m>/` → `router` 注册（注意 `SKIP_NAMES`）→ 需要则加 `stores/`。
- 数据全部走 mock，**不对接真实后端**。保持极简，勿因单点演示引入重型依赖。
- 有实质进度变化时更新本文件下方「当前进度」。
