# 移动端 Demo 规范（mobile）

面向移动端 App 类场景的 H5 原型 Demo。通用约定见 `common.md`。

## 技术栈

| 维度 | 选型 |
|------|------|
| 框架 | Vue 3（`<script setup>`） |
| 构建 | Vite 5 |
| UI | **Vant 4**（Vue3 生态最流行的移动端组件库） |
| 路由 | Vue Router 4（`createWebHashHistory`） |
| Mock | **mockjs** |

对应 `templates/mobile/package.json`：`vue` / `vue-router` / `vant` / `mockjs` + `vite` / `@vitejs/plugin-vue`。

## 初始化内容（模板已含）

- 底部 Tabbar 三页骨架：首页 / 功能 / 我的（`src/views/Home.vue`、`Features.vue`、`Profile.vue`）。
- `src/App.vue`：`<van-nav-bar>`（fixed）+ `<router-view>` 套 `<keep-alive>` + `<van-tabbar route>`。
- `src/router/index.js`：hash 路由，3 条路由 + `meta.title` 同步 `document.title`。
- `src/mock/`：`index.js`（mockjs 拦截器风格）与 `api.js`（Promise 风格），演示两种用法。
- `src/main.js`：全量引入 Vant 样式与组件、启动 mock、挂载 app。

> 模板首版页面为「功能开发中」占位，实际状态以 `src/` 代码为准（见项目 `CLAUDE.md`）。

## 风格约定

- 移动端优先：视口 `<meta name="viewport">` 已在 `index.html` 配置。
- 组件优先用 Vant：列表、表单、弹窗、Toast、下拉刷新/上拉加载等直接用 Vant 组件。
- 演示期可全量注册 Vant；正式项目建议改 `unplugin-vue-components` 按需引入（仅作提示，不在 Demo 内强制）。

## 开发约定

- 新页面：在 `src/views/` 建组件 → `src/router/index.js` 注册路由（带 `meta.title`）→ 需要则在 Tabbar 或入口挂链接。
- 数据：一律走 `src/mock/`，新增接口在此扩展，不引真实请求库对接后端。
- 保持极简：不加 Pinia、持久化等，除非确有演示需要。

## 构建与发布

- `npm run build` → `dist/`（`vite.config.js` 已配 `manualChunks` 拆 vue / vant）。
- hash 路由天然适配静态托管；如需子路径部署可在 `vite.config.js` 设 `base: './'`。
