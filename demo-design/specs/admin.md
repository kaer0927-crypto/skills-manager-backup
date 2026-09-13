# PC 管理后台 Demo 规范（admin）

面向 PC 端管理后台场景的原型 Demo。通用约定见 `common.md`。

## 技术栈

| 维度 | 选型 |
|------|------|
| 框架 | Vue 3（`<script setup>`） |
| 构建 | Vite 5 |
| UI | **Element Plus**（含 `@element-plus/icons-vue`，中文 locale `zh-cn`） |
| 路由 | Vue Router 4（`createWebHashHistory`） |
| 状态 | **Pinia**（+ `pinia-plugin-persistedstate`） |
| Mock | `vite-plugin-mock`（dev） + 内联 mock 适配器（prod） |

对应 `templates/admin/package.json`。模板还内置了富文本（`@wangeditor`）、表格导出（`xlsx`）、拖拽（`vuedraggable`）等演示能力，按需使用。

## 架构要点（模板已实现）

- **入口 `src/main.js`**：异步 `bootstrap()` —— 装 Pinia/持久化 → 装 Element Plus（`zhCn`）→ 加载菜单（失败走 fallback）→ 由菜单生成动态路由注入 `MainLayout` → 初始化 tabs → `router.isReady()` 后挂载。
- **路由 `src/router/index.js`**：hash 模式。核心业务（客户/案例）为**静态路由**直接注入 `MainLayout.children`；其余菜单叶子由 `buildRoutesFromMenu` 动态生成（`SKIP_NAMES` 防重复），`/:pathMatch(.*)*` → `/404`。
- **布局 `src/layouts/MainLayout.vue`**：侧边菜单树 + 顶部多标签页（tabs）+ 内容区。
- **Mock 单一数据源 `src/mock/index.js`**：`mockEndpoints` 数组同时供 dev（`viteMockServe` default export）与 prod（`inlineMockAdapter` named export）使用，数据零分叉。
- **Vite `vite.config.js`**：`base: './'`（支持子路径/`file://`）、`@` 别名指向 `src`、`viteMockServe({ prefix:'/api', mockPath:'src/mock' })`。

## 风格约定

- 组件优先用 Element Plus：表格、表单、分页、对话框、消息提示等。
- 图标用 `@element-plus/icons-vue`。
- 页面放 `src/views/<module>/`，可复用组件放 `src/components/<module>/`，接口封装放 `src/api/`。
- 全局中文 locale 已启用，分页/日期选择器等无需再单独汉化。

## 开发约定

- **新增业务模块**（以「客户/案例」为范例）：
  1. `src/mock/<module>.js` 定义接口与假数据，注册进 `src/mock/index.js` 的 `mockEndpoints`。
  2. `src/api/<module>.js` 封装请求（走 `request.js` → `/api/*`）。
  3. `src/views/<module>/` 建 List/Create/Edit/Detail 页面。
  4. `src/router/index.js` 注册路由（静态注入或经菜单动态生成，注意 `SKIP_NAMES`）。
  5. 需持久化的 UI 状态放 `src/stores/`（Pinia）。
- 数据一律走 mock，**不对接真实后端**。
- 保持克制：不因单个演示点引入重型依赖，能用 Element Plus 现成组件就不自造。

## 构建与发布

- `npm run build` → `dist/`；`base: './'` + hash 路由 → 可部署到任意静态子路径。
- 另有 `npm run lint` / `npm run format`（eslint + prettier），非必需，供整理代码用。
- prod 期由内联 mock 适配器提供数据，构建产物为纯静态、无需后端。
