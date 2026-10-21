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

- **表格基础**：斑马纹或细边框二选一（跟主题）；表头加粗；行高约 40–48px
- **列设置**：支持列显示开关（onColumnCheckChange）、列拖拽排序（onColDragStart/Drop）、列固定
- **行选择**：勾选列（checkbox），配合批量操作（见 crud-guide）
- **操作列**：编辑/删除文本按钮（见 crud-guide）
- **状态列**：用 Tag 渲染状态（启用/停用、成功/失败、进行中）
- **分页**：表格底部，共 X 条 / 当前第 N 页 / 每页条数可选（默认 10 条/页）
- **空/加载态**：空数据 Empty，加载中 Spin
- **表格卡片容器**：pro-table 外层 a-card，页头含标题 + 操作区

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

## 自查清单

1. 按钮五态齐全、危险操作红色、图标按钮尺寸正确？
2. 表格有列设置/行选择/状态 Tag/分页，操作列规范？
3. 图表与指标卡用主题色板，指标卡栅格 2–4 列？
4. 反馈类（Alert/Toast/Empty/Spin）齐全，语义色不铺底？
5. 列表/卡片栅格布局、描述列表用于只读展示？
