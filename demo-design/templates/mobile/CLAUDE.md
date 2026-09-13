# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> 本项目以简体中文为主；代码、文件路径、命令、技术专有名词保留英文。

---

## 项目概览

移动端 H5 Demo — Vue 3 + Vite + Vant 4，**仅前端骨架**，无真实后端，数据由 `mockjs` 生成。

**当前状态**：底部三 Tab 骨架（首页 / 功能 / 我的），**三个页面均为「功能开发中」占位**（参见 `src/views/Home.vue`、`Features.vue`、`Profile.vue`，仅渲染 `<van-empty description="功能开发中" />`）。`src/mock/` 下的接口文件暂未被调用。

> README.md 中描述的 Banner / 表单 / 用户卡片等内容属于首版交付物，**不代表当前代码**。开发新模块前先读 `src/App.vue` + `src/views/` 三个空壳确认实际状态。

---

## 常用命令

```bash
npm install        # 首次安装依赖
npm run dev        # 启动 dev server（默认 http://localhost:8080）
npm run build      # 生产构建 → dist/
npm run preview    # 预览构建产物
```

**关于测试 / Lint**：本项目无 `npm test` / `npm run lint` / Prettier — 验证靠 `npm run dev` + 浏览器人工对照。

---

## 启动顺序（`src/main.js`）

1. `import 'vant/lib/index.css'` 全量引入样式
2. 解构导入 Vant 组件（`Button / Cell / Tabbar / Toast / Swipe` 等共 24 个）→ `app.use()` 全量注册
3. `import './mock'` → 启动 mockjs 拦截器（`src/mock/index.js`）
4. `app.use(router).use(Lazyload).mount('#app')`

> 全量 Vant 注册是 demo 简便做法；正式项目建议切到 `unplugin-vue-components` 按需引入。

---

## 高层架构

### 路由（`src/router/index.js`）

- `createWebHashHistory()` — H5 必须用 hash，避免服务端路由配置
- 3 个路由：`/home` `/features` `/profile`，`/` redirect `/home`
- `meta.title` 通过 `router.afterEach` 同步 `document.title`
- 都加了 `<keep-alive>`（见 `App.vue` 内 `<router-view>` 的 `keep-alive` 包裹）

### 根组件（`src/App.vue`）

- `<van-nav-bar>` (`fixed` + `placeholder`)：标题来自 `pageTitle` computed，按 `route.path` 映射
- `<router-view>` 套 `<keep-alive>`
- `<van-tabbar route>` + 3 个 `<van-tabbar-item to="...">` — **使用 `route` 属性而非 v-model**，激活态由 router 自动同步

### Mock 数据（`src/mock/`）

两个文件演示两种风格，**当前均未被页面调用**：

- `index.js` — `Mock.mock(/\/api\/xxx/, 'get', ...)` 拦截 XHR，配合 axios 用
- `api.js` — `fetchXxx()` 返回 `Promise`，内置 `setTimeout` 模拟延迟，**真正对接 axios 见 mock 注释，暂无消费者**

> 真正按 mock 切换到真实接口：删 `import './mock'`，把 `api.js` 内函数体替换成 `axios.get('/api/xxx')` 即可。

### 响应式适配

`index.html` 已配 `viewport-fit=cover` + `user-scalable=no`；App.vue 与 Tabbar 用 `safe-area-inset-top/bottom` 处理刘海/底栏。

---

## 开发过程约束（硬约束）

- **`npm run build` 不要在 Claude 自动化里跑**，验证靠 `npm run dev` 浏览器对照即可。
- **`git add` / `git commit` / `git push` 只能由人发起**。完成任务后**只**保留 working tree 改动 + 给「建议 commit 信息」。
- 例外：用户**明确**说「帮我 commit」/「提交」/「push」时才走 commit 流程。
