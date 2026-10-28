# 组件规范总览（Components）

> 基于模板 `component-basic` / `component-extended` / `component-table-extended` / `component-list` / `component-chart` / `component-metric-card` / `component-rich-text` / `component-chart-palette` 八个演示页提炼。生产界面时，控件用法与状态以本文件 + 主题文档为准。

## 基础组件（component-basic）

### 按钮
- 五态：primary / secondary / outline / ghost / link-icon（见 ui-style-guide「按钮家族」）
- 尺寸族：默认 / sm / lg / pill；图标按钮 40×40；按钮组用 a-button-group（如富文本工具栏）
- 危险操作按钮一律 `status: danger`（红）

### 头像 / 头像组
- 头像：圆形或圆角，可带文字/图片；品牌头像用 `pro-avatar-brand`
- 头像组：多人并排（a-avatar-group），最多展示 N 个 + 溢出计数

### 标签 Tag / 徽标 Badge
- Tag：状态标签（成功/警告/危险/信息/中性），用于表格状态列、筛选区、卡片角标
- 状态色语义：成功绿 / 警告橙 / 危险红 / 信息蓝 / 中性灰，**点状使用不铺底**
- Badge：数字/红点徽标，挂图标/文字旁（消息数、待办数）

### 反馈类
- 提示条 Alert：主题静音底或浅色底，带图标 + 文案；强提示实底主色白字；用于页头说明、表单区提示
- Toast 消息：顶中、主题柔影、220ms 显隐，成功/错误/警告/信息四类
- 确认弹窗：见 crud-guide（删除确认）与 ui-style-guide「弹窗」
- 空状态 Empty：列表/图表无数据时显示，图标 + 引导文案（可带操作按钮）
- 加载 Spin：页面/区块加载态，局部加载用卡片内嵌

### 导航与信息类
- 面包屑 Breadcrumb：层级导航，页头使用
- Tabs：Tab 切换区块（详情页分区、设置页分组）
- 分页 Pagination：见 crud-guide「查询/分页」
- Tooltip / Popover：悬浮提示，Popover 带内容卡片
- Dropdown：下拉菜单（更多操作、批量动作收纳）

## 表格（component-table-extended）

- **表格基础**：`stripe`（默认 false）与 `bordered`（默认 true）二选一，不要同时开启；表头加粗；行高约 40–48px
- **列能力**：`fixed`、`ellipsis` + `tooltip`、`column-resizable`、`draggable`（2.16+）；列显隐开关需自建（Arco 无现成列设置器）
- **行选择**：`:row-selection="{ type: 'checkbox', onlyCurrent: true }"`，跨页保留用受控 `:selected-keys`，配合批量操作（见 crud-guide）
- **操作列**：编辑/删除文本按钮（见 crud-guide）
- **状态列**：用 Tag 渲染状态（启用/停用、成功/失败、进行中）
- **分页**：表格底部，共 X 条 / 当前第 N 页 / 每页条数可选（默认 10 条/页）
- **空/加载态**：空数据用 `#empty` 插槽（或全局 `ConfigProvider #empty`），首屏加载优先 `a-skeleton`，局部刷新用 `loading`
- **汇总行**：`summary` + `#summary-cell`（金额/数量合计列），首列文案用 `summary-text`
- **大数据量**：`:virtual-list-props="{ height: 520 }"` + 唯一 `row-key`；横向滚动用 `:scroll="{ x: 1400 }"`
- **分页位置**：`page-position="br"`（默认右下）；分页工具区用 `#pagination-left` / `#pagination-right`
- **表格卡片容器**：pro-table 外层 a-card，页头含标题 + 操作区

### 列设置与密度切换（官方实现，可直接照抄）

Arco 没有现成的「列设置」组件，官方 Arco Pro 是用 `a-popover` 自己拼的，这是唯一参考实现：

```vue
<a-popover trigger="click" position="bl" @popup-visible-change="syncColumns">
  <a-button type="text"><template #icon><icon-settings /></template></a-button>
  <template #content>
    <div class="column-setting">
      <div v-for="(col, i) in showColumns" :key="col.dataIndex" class="row">
        <icon-drag-arrow class="drag" />
        <a-checkbox v-model="col.checked" @change="toggleColumn($event, i)" />
        <span>{{ col.title }}</span>
      </div>
    </div>
  </template>
</a-popover>
```

- 列显隐用 `checked` 过滤 `cloneColumns` 后传给 `:columns`；顺序调整需要 `sortablejs`（官方引入），不想加依赖就只做显隐。
- 首次打开要**同步当前列状态**（`@popup-visible-change` 里做深拷贝），否则用户改到一半关掉会残留未提交状态。
- 至少要保留 1 列（通常是名称/编号），全不选时要兜底。

**密度切换**：Arco 表格原生 `size` 只有 `mini | small | medium | large`，用 `a-dropdown` 收口即可：

```vue
<a-dropdown @select="(v) => (tableSize = v)">
  <a-button type="text"><template #icon><icon-line-height /></template></a-button>
  <template #content>
    <a-doption v-for="d in densities" :key="d.value" :value="d.value">{{ d.name }}</a-doption>
  </template>
</a-dropdown>
```

- 默认 `medium`；密度只影响行高与内边距，不改变字号与列宽，所以列宽不要写死到依赖行高的值。
- 主题若指定了行高（40–48px），密度切换应被视为“可选能力”，不要默认开在 `mini`。

## 列表与卡片（component-list）

- **标准列表** a-list：列表项 + 图标/头像 + 标题/描述 + 时间 + 操作；适合动态、通知、日志
- **卡片网格**：a-card + a-row/a-col 栅格（2–4 列），适合资源/内容浏览；卡片含封面/标题/摘要/标签/操作
- **描述列表** a-descriptions：只读键值展示（详情页基础信息），带标题分区

## 图表（component-chart / metric-card / palette）

- **图表类型**：折线 line / 柱状 bar / 面积 area / 雷达 radar / 仪表盘 gauge / 漏斗 funnel / 环形 radial（ECharts 实现）
- **扩展图表（component-chart-extended）**：对比图（双指标对比）、交互柱状（chart-bar-interactive 点击/悬浮联动）、图例内联（chart-legend--inline 图例并入卡片）、动效图表（chart-motion）
- **图表容器**：a-card 内嵌 chart-host，卡片带标题 + 描述（chart-card-desc）
- **图例**：chart-legend（圆点 + 文案），与图表同卡片内
- **指标卡 metric-card**：a-card 栅格排布（一行 2–4 个），模板内置多种变体，按数据形态选用：
  - **基础数字**：指标名（metric-stat-title）+ 大号数值（metric-value）
  - **图标横条 icon-bar**：左侧图标块 + 指标名 + 数值（workplace-kpi 同族：icon-box + title + main + delta）
  - **趋势箭头 trend**：数值 + 环比箭头（trending-up/down 绿涨红跌）+ 环比标签
  - **迷你趋势图 spark**：数值 + 迷你折线/面积小图（spark-line / spark-area）
  - **spark-kpi**：迷你趋势图 + KPI 数值组合
  - **进度条 progress**：数值 + 进度条（进度/达成率/使用率）
  - **圆环 ring**：数值 + 环形进度（spark-ring-progress）
  - **状态 status**：状态色块/标签 + 数值（告警、预警类）
  - **翻牌数字 flip**：数字滚动翻牌效果（大屏/活动指标）
  - **类型化 type**：数值 + 单位（元/笔/人）+ 说明（type-value / type-unit）
  - **色块 color-fill**：色块底 + 数字（浅色/深色色块）
  - 所有变体支持 Tooltip 说明与点击跳转（可选）
- **图表配色**：按主题色板（component-chart-palette 提供方案 A/B/C）；同一界面图表色系与主题主色一致，语义色不抢主色
- **响应式**：图表容器自适应宽度，窄屏图例换行
- **接入方式**：ECharts 主题必须读取 Arco CSS 变量（`--primary-6`、`--color-text-*`、`--color-border-*`），实现见 [`chart-theme.md`](./chart-theme.md)；禁止硬编码色值与白底

## 富文本（component-rich-text）

- 结构：顶部工具栏（a-button-group：加粗/斜体/列表/链接/清除等）+ 可编辑内容区（contenteditable）
- 工具栏按钮：图标 + 激活态（加粗/斜体等 toggle 状态高亮）
- 内容区：主题字体栈、行高 1.6、段落间距

## 扩展组件（component-extended）

- 折叠面板 a-collapse：分组收纳（帮助文档、高级设置、FAQ）
- 时间线 a-timeline：流程/进度/变更记录展示
- 步骤条 a-steps：分步流程指示（表单分步、审批进度）
- 树 a-tree：分类树（左树右表列表页的左侧、组织架构、权限树）
- 穿梭框 a-transfer / 级联 a-cascader：见 forms-guide 控件表

## Arco 原生但模板未覆盖的组件（可直接用，勿重造）

| 组件 | 用途 | 关键点 |
|---|---|---|
| `a-result` | 结果页 / 异常页 | `status`: `success/warning/info/error/403/404/500`；`title` + `subtitle` + `#extra` |
| `a-empty` | 空状态 | 全局统一文案用 `<config-provider><template #empty>` |
| `a-skeleton` | 首屏骨架 | 列表用 `:animation`，详情用 `shape="circle"` |
| `a-drawer` | 侧滑详情 / 移动端菜单 | `placement`、`width`、`unmount-on-close`；面板必须实色 |
| `a-statistic` | 数值展示 | `precision`、`separator`、`animation`、`value-from`；KPI 卡片的数字部分可直接复用 |
| `a-typography` | 文本排版 | `ellipsis`（可展开）、`copyable`、`editable` |
| `a-link` | 文字链接 | 自带主色与 hover，比 `type="text"` 更语义化 |
| `a-page-header` | 详情页页头 | `title` + `subtitle` + `show-back` + `#breadcrumb` |
| `a-overflow-list` | 标签/头像溢出折叠 | 比手写 “+N” 更稳 |
| `a-resize-box` | 可拖拽面板 | 编辑器三栏、可调宽度侧栏 |
| `a-split` | 左右/上下分割 | 主从布局、对比视图 |
| `a-scrollbar` | 自定义滚动条容器 | 与全局滚动条规范保持一致 |
| `a-image` | 图片预览 | 内置预览/旋转/缩放 |
| `a-watermark` | 水印 | 后台导出/截图溯源场景 |
| `a-verification-code` | 验证码输入 | 登录/二次验证 |
| `a-comment` / `a-carousel` / `a-anchor` / `a-affix` / `a-back-top` | 评论、轮播、锚点、吸顶、回到顶部 | 按需启用，勿为“丰富”而加 |

> Arco 公开组件约 76 个（含图标、布局、数据录入、反馈、导航、其他六类）。上表只列模板尚未覆盖、且中后台真实会用到的部分；其余组件用法直接查官方文档，不再重复定义。

### 易漏但常用的信息与反馈组件

| 组件 | 场景 | 关键写法 / 坑（按 2.59.0 类型定义核对） |
|---|---|---|
| `a-notification` | 系统级异步通知（右上角浮出） | `position` 只有 `topLeft / topRight / bottomLeft / bottomRight`，**没有 `topCenter`**；默认 `topRight` |
| `a-message` | 操作即时反馈（顶部居中条） | `position` 只有 `'top' \| 'bottom'`，默认 `top` |
| `a-popconfirm` | 轻量二次确认（气泡内） | `position` 是 Trigger 的 12 向（`top/tl/tr/bottom/bl/br/left/lt/lb/right/rt/rb`），**不是** `top-center`；异步确认用 `on-before-ok`（不是 `onOk`） |
| `a-tree-select` | 组织架构 / 多级分类选择 | 带搜索与层级，优先于 Cascader（后者偏“路径选择”） |
| `a-input-tag` | 标签批量录入（关键词、白名单） | `:max-tag-count`、`allow-clear`；提交前做去重与长度校验 |
| `a-auto-complete` | 输入即建议（单位名、制度名） | 与 `a-input-search` 区别：前者可自由输入，后者只做提交 |
| `a-mention` | @人 / 引用对象 | `:data` + `prefix`；需要人员数据源，无数据不要硬编码 |
| `a-color-picker` | 主题色 / 标签色配置 | `show-preset`、`:history-colors`；结果存 hex，不要存 RGB 三元组 |
| `a-slider` + `a-input-number` | 阈值、比例类输入 | 同一 v-model 双向绑定，滑块快速调、数字框精确填 |
| `a-progress` | 达成率 / 使用率 | 卡片内 `type="circle"` 必须固定 `:size`，否则跟随容器抖动 |
| `a-spin` | 区块级加载 | 包裹内容容器，不要整页白屏 |
| `a-calendar` | 排班 / 值班 / 日程 | 组件较重，只有真存在“日历语义”时才用 |
| `a-badge` | 数字/红点计数 | `:max-count`、`dot`；计数不要用 Tag 冒充 |
| `a-trigger` | 自定义浮层基座 | 业务优先用 Tooltip / Dropdown / Popconfirm，不要直接拼 Trigger |

### 类型系统的两个坑

- **枚举型 props 才有编译期保护**：`a-button` 的 `type` 是字面量联合 `'primary' | 'secondary' | 'outline' | 'dashed' | 'text'`，写 `"link"` 会直接报错。
- **部分 props 只声明成 `StringConstructor`**（如 Popconfirm 的 `okText`），属性名写错不会报错，只会在运行时静默失效。这类属性必须回到本规范 / 官方文档逐项核对，别指望 TS。

## 自查清单

1. 按钮五态齐全、危险操作红色、图标按钮尺寸正确？
2. 表格有列设置/行选择/状态 Tag/分页，操作列规范？
3. 图表与指标卡用主题色板，指标卡栅格 2–4 列？
4. 反馈类（Alert/Toast/Empty/Spin）齐全，语义色不铺底？
5. 列表/卡片栅格布局、描述列表用于只读展示？
6. 大数据表格是否开启虚拟滚动并保证 `row-key` 唯一？
7. 空状态是否走 `#empty` 插槽、首屏是否优先骨架屏？

## 数据展示规范（所有列表/详情/看板通用）

| 类型 | 规则 | 示例 |
|---|---|---|
| 空值 | 统一 `--`，不写 `null`/`undefined`/`无` 混用 | `--` |
| 金额 | 千分位 + 两位小数，单位在列头或后缀，不在每个单元格重复 | `1,234.50` / 列头 `金额（元）` |
| 整数数量 | 千分位，不加小数 | `12,340` |
| 百分比 | 保留 1 位小数，带 `%`；环比用 `+3.2%` / `-1.8%` | `98.5%` |
| 日期 | `YYYY-MM-DD` | `2026-10-28` |
| 日期时间 | `YYYY-MM-DD HH:mm`，秒仅在排障场景显示 | `2026-10-28 14:30` |
| 状态 | 用 Tag 语义色 + 文案，不只用颜色（色盲可读） | 成功绿/警告橙/危险红/中性灰 |
| 长文本 | 列表 `ellipsis` + `tooltip`，详情完整展示 | — |
| 数值对齐 | 数字右对齐，文本左对齐，状态居中 | — |
| 单位 | 同一列单位统一，混合单位拆列 | — |

金额/数量列如需合计，用表格 `summary` 行，不要让用户自己加总。
