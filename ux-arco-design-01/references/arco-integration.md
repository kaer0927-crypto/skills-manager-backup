# Arco Design Vue 集成规范

> 本文所有 API、Token 名、断点、暗黑模式用法均对照 `arco-design/arco-design-vue` 源码与 npm 包 `@arco-design/web-vue@2.59.0` 核对，禁止凭印象改写。
> 核对来源：`packages/web-vue/components/grid/interface.ts`、`components/style/theme/global.less`、`components/style/theme/css-variables.less`、`packages/arco-vue-docs/docs/{start,theme,dark,i18n}.zh-CN.md`。
> 若要换版本，先复查 `theme/global.less` 与各组件 `README.zh-CN.md`，再更新本文。

---

## 一、版本与运行环境

| 项 | 要求 |
|---|---|
| 组件库版本 | `@arco-design/web-vue` 2.59.0（2026-10 最新稳定版） |
| Vue | `>= 3.2.0`（peer: `>=3.1.0`，官方文档要求 3.2+） |
| 浏览器 | Chrome ≥ 64 / Edge ≥ 79 / Firefox ≥ 78 / Safari ≥ 12 / Opera ≥ 53；**不支持 IE** |
| 类型 | 全量 TypeScript，自带 `.d.ts` |
| 依赖 | `dayjs`、`b-tween`、`b-validate`、`number-precision`、`resize-observer-polyfill` 等（随包安装，无需手动装） |

自 2.44.3 起包内启用 `exports` 字段，**统一从以下两个入口导入**：

```ts
import { Button, Table, Message } from '@arco-design/web-vue';
import { IconSearch } from '@arco-design/web-vue/es/icon';
```

---

## 二、安装与引入

### 完整引入

```ts
import { createApp } from 'vue';
import ArcoVue from '@arco-design/web-vue';
import ArcoVueIcon from '@arco-design/web-vue/es/icon';
import '@arco-design/web-vue/dist/arco.css';
import App from './App.vue';

createApp(App).use(ArcoVue).use(ArcoVueIcon).mount('#app');
```

`app.use(ArcoVue, { componentPrefix: 'arco' })` 可改组件前缀（默认 `a`）。

### 按需引入（推荐）

```ts
// vite.config.ts
import AutoImport from 'unplugin-auto-import/vite';
import Components from 'unplugin-vue-components/vite';
import { ArcoResolver } from 'unplugin-vue-components/resolvers';

export default defineConfig({
  plugins: [
    AutoImport({ resolvers: [ArcoResolver()] }),
    Components({ resolvers: [ArcoResolver({ sideEffect: true })] }),
  ],
});
```

两个坑：

- `script` 中手动导入的组件（`Message`、`Modal`、`Notification` 等函数式调用）**不会**被自动处理样式，需手动 `import '@arco-design/web-vue/es/message/style/css.js'`（或 `.../style/index.js` 走 less）。
- 走主题定制时必须导 less 样式：`import '@arco-design/web-vue/es/index.less'`（或 `dist/arco.less`），并在 `css.preprocessorOptions.less` 打开 `javascriptEnabled: true`。

### 使用 Arco 官方 Vite 插件

```ts
import { vitePluginForArco } from '@arco-plugins/vite-vue';

export default defineConfig({
  plugins: [vue(), vitePluginForArco({ style: 'css' })],
});
```

---

## 三、主题定制（三种方式，按场景选）

### 方式一：Less `modifyVars`（工程默认）

```ts
// vite.config.ts
css: {
  preprocessorOptions: {
    less: {
      modifyVars: {
        'arcoblue-6': '#0064FA', // SemiDesign 主色
        'border-radius-small': '3px',
        'border-radius-medium': '6px',
        // 不要写 border-radius-large：Arco 2.59.0 无组件消费，卡片/弹窗用组件级覆盖
        'font-family': `Inter, -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif`,
      },
      javascriptEnabled: true,
    },
  },
},
```

要点：

- 主色改的是**色板变量 `arcoblue-6`**（官方示例即如此），`--primary-6` 由 `--arcoblue-6` 派生；改完 hover/active 的 5/7 阶会随色板自动生成。
- 可覆盖的粒子变量在 `@arco-design/web-vue/es/style/theme/global.less`；组件级变量在各组件 `style/token.less`。
- **阴影只有 Less 变量**（`@shadow1-down`…`@shadow3-*`），没有 CSS 变量，无法运行时切换。

### 方式二：风格配置平台（Design Lab）主题包

访问 https://arco.design/themes 生成主题包，Vue 已支持。按官方 Design Lab 指引引入生成的主题 CSS/主题包，不得自行拼装 Token。

### 方式三：运行时改 CSS 变量（换肤 / 预览）

```ts
const root = document.body; // 变量定义在 body 上
root.style.setProperty('--primary-6', '76, 117, 242'); // 注意：值是 R,G,B，不带 rgb()
```

- Arco 的 `--primary-*` 存的是 **RGB 三元组**（`--arcoblue-6: 22, 93, 255`），`rgb(var(--arcoblue-6))` 再消费。
- 只改 `--primary-6` 会导致 hover/active 仍是旧色，必须同时给 1–10 阶。
- 阴影、字体族不在 CSS 变量里，运行时换肤只能改颜色与圆角。

### 主题产物路径

| 用途 | 路径 |
|---|---|
| 编译后全量 CSS | `@arco-design/web-vue/dist/arco.css` |
| 全量 Less（定制入口） | `@arco-design/web-vue/dist/arco.less`、`es/index.less` |
| 全局粒子变量 | `es/style/theme/global.less` |
| 全局 CSS 变量声明 | `es/style/theme/css-variables.less` |
| 编译产物（组件级主题） | `es/style/theme/index.css` |

---

## 四、Token 体系

Arco 是**双层**结构：Less 粒子变量（编译期）→ CSS 变量（运行期，挂在 `body`）。

- 语义色：`--primary-1..10`、`--success-1..10`、`--warning-*`、`--danger-*`、`--link-*`
- 文字：`--color-text-1..4`（1 最重）
- 背景：`--color-bg-1..5`（1 页面 → 5 浮层）
- 填充：`--color-fill-1..4`
- 边框：`--color-border`、`--color-border-1..4`
- 圆角：`--border-radius-small|medium|large|circle`（2 / 4 / 8px / 50%）

完整取值与 vibepm 主题映射见 [`arco-tokens.md`](./arco-tokens.md)。

---

## 五、暗黑模式

**官方唯一方式：改 `body` 的 `arco-theme` 属性**（没有 `setTheme` API，`ConfigProvider` 也没有 `theme` prop）。

```ts
document.body.setAttribute('arco-theme', 'dark'); // 开
document.body.removeAttribute('arco-theme');      // 关
```

- 选择器是 `body[arco-theme='dark']`，所以**只能整页切换**，不能只让某个卡片变暗。
- 切换后所有 `--color-*` 变量自动反转，组件无需改代码。
- 自定义组件必须消费 `var(--color-*)` 才能跟着变；写死 `#fff` 的样式在暗色下必然错。
- 各主题的暗黑配色映射见 [`dark-mode-tokens.md`](./dark-mode-tokens.md)。

```ts
// 推荐封装：跟随系统 + 手动覆盖
const applyTheme = (pref: 'light' | 'dark' | 'auto') => {
  const dark = pref === 'dark' ||
    (pref === 'auto' && matchMedia('(prefers-color-scheme: dark)').matches);
  document.body.removeAttribute('arco-theme');
  if (dark) document.body.setAttribute('arco-theme', 'dark');
};
```

---

## 六、图标

```vue
<template>
  <a-button type="primary">
    <template #icon><icon-search /></template>
    查询
  </a-button>
</template>
```

- 图标从 `@arco-design/web-vue/es/icon` 导入，或 `app.use(ArcoVueIcon)` 后直接用全局 `<icon-xxx />`。
- 图标全集与命名查 https://arco.design/vue/icon ；**不得**混入第三方图标库（会破坏描边粗细与视觉重心）。
- 图标按钮：`<a-button shape="circle"><template #icon><icon-more /></template></a-button>`。

---

## 七、国际化

```vue
<template>
  <a-config-provider :locale="zhCN">
    <app />
  </a-config-provider>
</template>

<script setup lang="ts">
import zhCN from '@arco-design/web-vue/es/locale/lang/zh-cn';
</script>
```

- 内置 18 种语言：`zh-CN`、`zh-TW`、`en-US`、`ja-JP`、`ko-KR`、`fr-FR`、`de-DE`、`es-ES`、`pt-PT`、`it-IT`、`id-ID`、`ms-MY`、`th-TH`、`vi-VN`、`km-KH`、`ar-EG`、`ru-RU`、`nl-NL`。
- 组件内置文案（分页“共 X 条”、空状态、Modal 按钮等）自动跟随 `locale`。
- **函数式组件（`Message` / `Modal` / `Notification`）拿不到 Vue Context**：要么 `Message._context = app._context`，要么给 `ConfigProvider` 加 `global` 属性，否则 i18n 不生效。
- RTL：`<a-config-provider rtl>`。

---

## 八、尺寸与密度（必须显式对齐 vibepm）

Arco 默认是**紧凑密度**，与 vibepm 的 40px 触控目标 / 600 字重不一致，落地时必须显式设置：

| 项 | Arco 默认 | vibepm 要求 | 处理方式 |
|---|---|---|---|
| 按钮高度 | mini 24 / small 28 / **default 32** / large 36 | 主操作 ≥36，图标按钮 40×40 | 表单/列表主按钮用 `size="large"`；图标按钮 40×40 用自定义样式或 `size="large"` + padding |
| 按钮字重 | 400 | 主按钮 600 观感 | CSS 覆盖 `.arco-btn-primary { font-weight: 600 }` |
| 按钮圆角 | `border-radius-small` = 2px | 主题圆角档（3/6/12） | `modifyVars` 覆盖 `border-radius-small` |
| 正文 | 14px / 1.5715 | 14–16 / 1.5–1.6 | 主题已匹配，无需改 |
| 输入框 | 32px 高 | 表单控件 32–36 | 默认可用，密集表单保持 32 |
| 弹窗圆角 | `border-radius-medium`（4px） | 12px | 改 `--border-radius-medium`，或 `:modal-style="{ borderRadius }"`；**`border-radius-large` 无人消费，改了没用** |

结论：**先跑 `modifyVars` 对齐圆角与主色，再用组件级 `*-style` 补差异**，不要在业务页面里到处写死像素。

---

## 九、响应式断点（Arco 真实断点）

来自 `grid/interface.ts`，与 Ant Design 系一致，**不是** 768/992/1200/1600/1920：

| 断点 | 宽度 | 含义 |
|---|---|---|
| `xs` | `< 576px` | 手机 |
| `sm` | `≥ 576px` | 大手机 / 小平板竖屏 |
| `md` | `≥ 768px` | 平板 |
| `lg` | `≥ 992px` | 小桌面 |
| `xl` | `≥ 1200px` | 标准桌面 |
| `xxl` | `≥ 1600px` | 大屏 |

```vue
<a-row :gutter="[16, 16]">
  <a-col :xs="24" :sm="12" :md="8" :lg="6" :xl="6" :xxl="4">…</a-col>
</a-row>
```

`a-row` 的 `gutter`、`a-grid` 的 `cols/rowGap/colGap` 都支持传响应式对象：

```vue
<a-row :gutter="{ xs: 8, md: 16, xl: 24 }">…</a-row>
```

业务侧固定规则（与断点配合，不要混用）：

- 筛选区标签列：`≤ 980px` 隐藏标签，控件占满整行。
- 表单栅格：`≤ 900px` 降为单列。
- 侧边栏：用 `a-layout-sider breakpoint="xl"`，`<1200px` 折叠；移动端改用 `a-drawer` 承载菜单。

---

## 十、性能与工程约定

- 大表格（> 200 行）开 `:virtual-list-props="{ height: 520 }"`，并保持 `row-key` 唯一。
- `a-table` 自带 `scrollbar`（2.38+），不要在外层再套自定义滚动条，避免双滚动条。
- 页面缓存用 `<keep-alive :include="cacheList">`（Arco Pro 同款做法），配合多页签。
- 按需加载时，函数式组件样式要单独引入（见第二节坑点）。
- 不要在 `v-for` 里用 `:key="index"` 做可排序/可删除列表。

---

## 十一、常见坑

| 现象 | 原因 | 处理 |
|---|---|---|
| 暗色不生效 | 没有给 `body` 设 `arco-theme`，或只给某个 div 设 | 改成 `document.body.setAttribute('arco-theme','dark')` |
| 换主色后 hover 还是旧色 | 只改了 `--primary-6` | 给 1–10 阶，或用 `modifyVars` 改 `arcoblue-6` |
| `Message` 没样式 | 按需加载未引 `es/message/style/css.js` | 手动引入，或用 Arco Vite 插件 |
| Modal 面板半透明“玻璃态” | 自定义了 `background: rgba(...)` / `backdrop-filter` | 面板实色，仅遮罩可 blur（vibepm 硬规则） |
| 表格分页双份 | `a-table` 内建分页 + 外层又放 `a-pagination` | 二选一，vibepm 统一用表格内建分页 |
| 删除确认无 loading | 用了 `onOk` 同步回调 | 用 `onBeforeOk: (done) => { … done(true) }` |
| 深色下图表仍是白底 | 图表写死颜色 | 图表配色从 CSS 变量读 `--color-bg-*`、`--color-text-*` |
| 行选中跨页丢失 | 分页后 `data` 被替换 | 用受控 `:selected-keys` 维护跨页选择 |

---

## 十二、自查清单

- [ ] 从 `@arco-design/web-vue` / `/es/icon` 导入，未走深路径？
- [ ] 主题通过 `modifyVars` 或 Design Lab 主题包，未在业务页散落写死颜色？
- [ ] 主色、圆角、字体、阴影四项已按所选主题对齐？
- [ ] 暗黑模式用 `body[arco-theme]`，自定义样式全部走 `var(--color-*)`？
- [ ] 函数式 `Message`/`Modal` 语言与样式都生效（`_context` 或 `global`）？
- [ ] 按钮尺寸、字重、圆角按第八节显式对齐，未沿用 Arco 默认 32px/400/2px？
- [ ] 响应式用 576/768/992/1200/1600 断点，未写 1920 断点？
- [ ] 大表格开虚拟滚动，`row-key` 唯一？

---

## 十三、验证记录（本 Skill 的结论是怎么来的）

所有硬结论都做过两种核对，不接受“凭印象”：

| 手段 | 范围 | 结果 |
|---|---|---|
| 源码 / 类型定义阅读 | `@arco-design/web-vue@2.59.0` 的 `es/*/*.d.ts`、`dist/arco.css` | 组件 Props、枚举、Token 声明位置 |
| 静态统计 | `dist/arco.css` 全量 | `--border-radius-*` 的引用次数（large = 0） |
| 真实构建 | Vite 8 + Vue 3.5 + Arco 2.59 最小工程，引入 `assets/frame-presets.css` + `assets/arco-echarts-theme.ts`，含侧栏/筛选区/表格/弹窗/图表 | 构建通过，产物 CSS 中 Preset 位于 Arco 基础样式之后 |
| 浏览器实测 | Chrome headless，`getComputedStyle` 读取亮/暗两套计算值并截图 | 卡片 12px、主按钮 36px/600/`rgba(22,93,255,.22)`、表格外框 12px、筛选区 1440px 下 6 列、暗色 `bg-1 #17171a` 等 |
| 主题实测 | 逐个给 `body` 设 `data-frame-theme`，读取控件/卡片/弹窗圆角与主按钮投影 | 12 套主题全部按 `frame-themes.css` 表值生效（如 `tech-blue` 3 档 16/20/24、`neon-pink` 2/4/6） |

实测发现、已回写文档的三个问题：

1. 暗色下 `--color-border-1..4` 是重映射后的实色灰阶（`#2e2e30`…`#929293`），不是白色透明度梯度。
2. 暗色下 `--primary-6` 会变成 `60,126,255`；整套色板（含 `--arcoblue-*`）都被重映射，不能假设“主色稳定”。
3. 页面根容器缺 `background: var(--color-bg-1)` 时，暗色会出现“黑卡片 + 白页面”的露白（已写进 `assets/frame-presets.css`）。
