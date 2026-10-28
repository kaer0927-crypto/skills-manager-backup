# Arco Pro Vue 逐页实现比对

> 官方仓库：`arco-design/arco-design-pro-vue`（目录 `arco-design-pro-vite/`）。
> 本文基于**实际读取的源码**（`src/views/*/index.vue`、`src/layout/default-layout.vue`）逐页比对，不是按文件名猜。
> 用途：抄写法时知道哪些能直接学、哪些会和 vibepm 规则打架。

## 一、官方到底有哪些页（实测 19 个）

```
dashboard/workplace          dashboard/monitor
list/search-table            list/card
form/group                   form/step
profile/basic
result/success               result/error
exception/403 404 500        not-found
user/info                    user/setting
login
visualization/data-analysis  visualization/multi-dimension-data-analysis
```

覆盖度远低于本索引的 50 页：**没有**看板列视图、日历、文件管理、导入向导、行内编辑、左树右表、标签筛选、移动端壳。这些以 `component-catalog.md` 为准。

## 二、建议吸收的 7 个实现点

| # | 官方做法（源码位置） | 价值 | 落地到 |
|---|---|---|---|
| 1 | **序号列按分页算**：`#index` 插槽里 `rowIndex + 1 + (pagination.current - 1) * pagination.pageSize`（`list/search-table`） | 翻页后序号连续，不会每页都从 1 开始 | `crud-guide.md` 表格列 |
| 2 | **列设置**：`a-popover trigger="click" position="bl"` + `a-checkbox` 列表 + `sortablejs` 拖拽排序（`list/search-table`） | Arco 确实没有现成列设置器，这是官方参考实现 | `components-guide.md` 列能力 |
| 3 | **密度切换**：`a-dropdown` 里 `mini/small/medium/large` 写进表格 `:size` | 数据密集场景刚需，且是 Arco 原生支持的尺寸枚举 | `components-guide.md` 表格 |
| 4 | **长表单固定底栏**：`.actions { position: fixed; left/right/bottom: 0; height: 60px; background: var(--color-bg-2); text-align: right }`（`form/group`） | 分组表单很长时提交按钮始终可见 | `forms-guide.md` 提交行 |
| 5 | **分步表单用 `keep-alive` 包步骤内容** + 外层 `a-spin :loading`（`form/step`） | 回退上一步不丢已填数据 | `forms-guide.md` 分步表单 |
| 6 | **结果页补进度**：`a-result` 下方接 `a-steps type="dot"` 展示审批/处理链路（`result/success`） | 提交类结果页的“然后呢”有交代 | `pages-guide.md` 结果页 |
| 7 | **分类页签**：`a-tabs type="rounded"` + 右上角 `a-input-search`（`list/card`、`user/setting`） | 卡片列表 / 设置页的轻量分区 | `pages-guide.md` 列表、个人中心 |

## 三、不要照抄的 5 个地方（与 vibepm 规则冲突）

| 官方做法 | 冲突点 | vibepm 要求 |
|---|---|---|
| 搜索区 `a-col :span="8"` **一行 3 个字段**，右侧再用 `a-col :flex="'86px'"` 竖排「查询/重置」，中间加 `a-divider direction="vertical"` | 查询按钮独立成列、字段被压成 3 列 | 一行 6 个字段、按钮跟随字段流同行、字段不足 6 个仍同行（`ui-style-guide.md`） |
| 搜索表单 `label-align="left"`（显式覆盖了 Arco 默认的 right） | 标签左对齐会让标签宽度不齐 | 右对齐 + 固定标签宽（约 6em），见 `forms-guide.md` |
| 表格 `:bordered="false"` 为默认 | vibepm 模板是卡片内带边框表格 | 二选一，同一系统内保持一致；默认走 bordered |
| 状态列用 `<span class="circle">` 圆点 + 文案 | 纯圆点依赖颜色区分状态，色盲不可读 | 统一用 `a-tag` 语义色 + 文案；只在“在线/离线”这类二元且带文字的场合用圆点 |
| `visualization/*` 直接当后台页用 | 它是大屏/分析看板，不是 CRUD 页 | 大屏单独规范（`pages-guide.md`「大屏 / 多维分析」），不要混进 Admin 壳 |

> 补充：官方示例大量使用自定义 `Breadcrumb` 组件 + `$t()` 文案。可以沿用结构，但文案必须走 `ConfigProvider :locale` 或项目自身 i18n，不要照抄 `vue-i18n` 的 locale 文件组织。

## 四、官方布局的关键数值（`src/layout/default-layout.vue`）

| 项 | 值 | 说明 |
|---|---|---|
| 顶栏高度 | `60px`（`@nav-size-height`） | 与 `pages-guide.md` 一致 |
| 侧栏宽 | 默认 `menuWidth`，折叠 `48px` | `a-layout-sider` 组件默认 200 / 48 |
| 侧栏断点 | `breakpoint="xl"` | `<1200px` 自动折叠 |
| 侧栏定位 | `paddingTop: 60px`（navbar 固定时） | 避免内容被顶栏压住 |
| 布局最大宽 | `@layout-max-width: 1100px` | 部分内容居中场景使用 |
