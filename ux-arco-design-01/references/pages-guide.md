# 页面模板规范（Pages）

> 基于模板 admin/ 50 页 + app/ 8 壳提炼。生产页面时：先按本文件选页面类型骨架，再叠加组件规范（components-guide）、表单规范（forms-guide）、CRUD 规范（crud-guide）、筛选区规范（ui-style-guide）与主题 Token。

## 布局类型（layout）

| layout | 含义 | 适用页面 |
|---|---|---|
| shell | 完整后台壳：顶栏 + 侧栏 + 内容区 | 看板、列表、表单页、详情、组件页 |
| center | 居中卡片 | 登录、结果页、异常页 |
| split | 左右分栏 | 树表/筛表、主从详情、纵向分步 |
| phone | 设备壳内页面 | app/ 移动端 8 壳 |

### shell 骨架结构（对齐 Arco Pro 官方布局）

```
a-layout
├─ NavBar            固定顶栏，高 60px（Logo / 面包屑 / 搜索 / 通知 / 用户）
└─ a-layout
   ├─ a-layout-sider 宽 200–240px（Arco 默认 200），折叠后 48px（默认），breakpoint="xl"
   │   └─ a-menu
   ├─ a-layout（移动端：a-drawer 承载同一份 Menu）
   └─ a-layout-content
      ├─ TabBar（可选，多页签）
      └─ 页面容器（padding 16–20px，内容卡片化）
```

- 侧栏用 `a-layout-sider breakpoint="xl" :collapsed-width="48"`，`<1200px` 自动折叠；小屏改为 `a-drawer`。
- 侧栏默认宽 200px、折叠 48px（组件默认值，源码 `sider.vue` 核对）。需要用户自调宽度时加 `:resize-directions="['right']"`（内部用 `a-resize-box`），并把宽度存进 state 持久化；不需要折叠箭头时用 `hide-trigger`。
- 顶栏 60px 与侧栏 48px 折叠宽是 Arco Pro 的实测值，直接沿用，不要自定成 52/56。
- 多页签（TabBar）为可选能力：开启时必须支持关闭当前/关闭其他/刷新，并与 `keep-alive :include` 的缓存列表联动。
- 页面内容统一走 `PageLayout` 容器，业务页不再自己写 `padding` 与背景色。
- 长列表页底部用 `a-back-top`；帮助文档类页面用 `a-anchor`。

## 登录页（3 种）

- **封面 login-cover**（默认）：全屏品牌封面背景 + 居中登录卡；品牌区 + 表单区（账号/密码/验证码/记住我/登录按钮/忘记密码）；背景用主题氛围色，禁止把氛围色当品牌色
- **Banner login-banner**：左侧品牌 Banner + 右侧表单卡
- **分栏 login-split**：居中双栏卡片（品牌简介栏 + 表单栏）
- 登录卡：白底/主题卡面、主题圆角、柔影；表单校验、提交 loading、错误 Toast；演示账号 admin / 123456

## 数据看板（9 种，结构同构）

- 结构：页头（标题 + 说明/时间）→ **KPI 指标卡行**（一行 2–4 个，见 metric-card）→ **图表区**（折线/柱状/面积/雷达/环形等，见 component-chart）→ **数据表/明细区**（最近列表、排行榜、订单表）
- 业态差异只在业务语义：电商（销售概览+订单）、CRM（管道+商机）、教务（课表+作业）、财务（收支+账户）、银行（账户+现金流）、效率（任务/项目/日历）等
- 通用规范：卡片栅格留白、指标卡数值大字号加粗、图表带图例与描述

## 大屏 / 多维分析（Arco Pro 有、本模板无，需自建）

> 这一页型不在 50 页骨架内。Arco Pro 的 `visualization/*` 只能作布局参考，**不要把它当 Admin 页面套用**。
>
> 现成骨架：[assets/skeletons/visualization-screen.vue](../assets/skeletons/visualization-screen.vue)（1920×1080 / 1366×768 实测，四段分区 + 环形图 + TOP5 + 事件流轮播 + 健康度），用法见 [README](../assets/skeletons/README.md)。

- **设计基准 1920×1080**，外层用 `transform: scale()` 等比缩放并 `transform-origin: left top`；不要用 `vw/vh` 硬凑，否则图表文字在不同屏幕上大小不一致。
- **分区**：顶部标题条（含时间与刷新）→ KPI 卡带（4–6 个）→ 主图区（1 大 + 2 小，或左右 1:1）→ 底部明细条（滚动榜单/告警流）。
- **主题**：只允许「暗紫色科技感 / 暗黑亮青发光 / 暗色低饱和黑灰」三类；亮色主题不做大屏。改暗色仍走 `body[arco-theme='dark']`，不要另写一套色板。
- **图表**：全部走 [`chart-theme.md`](chart-theme.md) 的变量桥接；发光只用于关键数值与描边，禁止整卡外发光。
- **动效**：只在数据更新时做 1 次 300–600ms 过渡；禁止无限循环的装饰动画（影响可读性也耗 GPU）。
- **滚动**：榜单超过 8 行自动轮播，轮播必须可暂停（hover 暂停），否则关键信息会被跳过。
- **交互**：大屏默认只读；需要下钻时提供明确的入口（点击卡片 → 新开 Admin 页），不要在大屏里塞表单。
- **降级**：在 1366×768 笔记本上按比例缩放到可用，不出现横向滚动条。

## 列表页（11 种）

- **标准 CRUD 列表 list**（最常用）：筛选区（见 ui-style-guide「筛选区布局」）→ 工具栏（新增 + 批量操作）→ 表格（见 crud-guide + components-guide「表格」）→ 分页；行按钮由 [state-machine.md](state-machine.md) 的「状态 → 动作」矩阵推导
- **卡片列表 list-card**：筛选区 → 工具栏 → 卡片网格（2–4 列）→ 分页；适合内容/资源。分类切换用 `a-tabs type="rounded"`（官方 `list/card` 写法），页签 2–5 个；超过 5 个改用左侧分类树或标签筛选，不要做成横向滚动页签。
- **任务看板 list-kanban**：列式看板（列 = 状态，卡片 = 任务，列头计数）
- **左树右表 list-tree-table**：左侧分类树 + 右侧筛选表格（split）
- **左筛右表 list-filter-table**：侧栏筛选 + 主表（split）
- **标签筛选 list-tag-filter**：顶部平铺标签（可多选）+ 表格
- **分栏详情 list-master-detail**：左列表右详情（工单/会话），点行右侧更新
- **行内编辑 list-editable**：行内直接编辑（字段变输入控件）+ 行保存/保存全部 + 未保存修改警告（见 crud-guide「行内编辑模式」）
- **日历页面 list-calendar**：日历 + 事件/排期
- **文件管理 list-media**：目录树 + 宫格/列表素材
- **导入向导 list-import**：三步——① 上传（拖拽/点击，含格式与大小提示 uploadTip）→ ② 校验（逐行校验，无效行标红、checkbox 勾选处理）→ ③ 结果（成功条数 + 失败原因 + 重新上传入口）

## 表单页（4 种）

见 forms-guide「表单页结构」：基础（title+desc+表单+提交行）/ 分组（多卡片分组）/ 横向分步（顶部步骤条+成功页）/ 纵向分步（左侧步骤+右侧内容，split）。

## 详情页（3 种）

- **基础详情 detail**：页头（标题+操作按钮）→ 描述列表（a-descriptions）分区展示基础信息；页头按钮同样由状态矩阵推导，无权动作按 [permission-guide.md](permission-guide.md) 降级
- **高级详情 detail-advanced**：多分区（卡片）或 Tab 分区 → 每区描述列表/表格/图表组合
- **分栏详情 list-master-detail**：左列表 + 右侧详情抽屉/面板（点行切换），含编辑/删除联动（见 crud-guide）

## 结果页（4 种，center 布局）

- 优先用 `a-result`：`status` 取 `success / warning / info / error`，配 `title`、`subtitle`、`#extra` 放操作按钮。
- 需要品牌插画时再自绘居中卡片（result-page-card）：大图标 → 主标题 → 说明 → 主次按钮。
- 成功：告知完成 + 下一步引导；失败：原因 + 重试；等待：进度/预计时间。文案按 [content-guide.md](content-guide.md) 的错误三段式（发生什么 + 为什么 + 怎么办）书写。
- 403/404/500 异常页同样可用 `a-result status="403|404|500"`，无需自造状态码插画。
- **提交类结果页补进度链路**：`a-result` 下方接 `a-steps type="dot" :current="n"`，把「提交 → 审核 → 制证 → 完成」这类流程和时间点交代清楚（官方 `result/success` 的做法）。纯粹“操作成功”的轻量结果页不需要步骤条。

## 加载与空态（所有页面通用）

- 首屏数据未回：`a-skeleton`（列表 5–8 行 / 详情 3–4 块），不要直接白屏或只放一个 Spin。
- 局部刷新：表格 `loading`、按钮 `loading`。
- 空数据：`a-empty` + 一句可执行的引导（新建 / 调整筛选），不要只写“暂无数据”；四类空态（首次/无结果/无权限/出错）的判定与文案见 [feedback-patterns.md](feedback-patterns.md)。
- 错误：`a-result status="error"` 或页内 `a-alert` + 重试按钮；禁止静默失败。
- 长任务（导入、批量导出、批量改状态）：超过 3 秒不要靠页面转圈，按 [feedback-patterns.md](feedback-patterns.md)「长任务」分档处理。

## 异常页（3 种，center 布局）

- 403 / 404 / 500：居中插画图（illust-img）+ 状态码 + 文案（无权限/页面不存在/服务异常）→ 返回首页按钮（back）
- 插画用主题色系大插画（非文字堆砌）；文案克制，不放业务噪音

## 个人中心（3 种）

- **个人主页 user-home**：封面/头像区（含更换头像）→ 项目/动态/团队分区
- **用户设置 user-setting**：Tabs 或分组设置项（资料/偏好/安全），表单提交行
- **消息管理 message-list**：消息/通知/待办列表，已读未读状态（Tag/Badge）、批量已读

## 移动端壳（8 种，app/）

| 壳 | 适用 |
|---|---|
| ios-nav（常用） | iOS 标题栏 + 底部 Tab，常规 App 主结构 |
| ios-content / ios-header / ios-tabs | 沉浸内容 / 二级页 / 主 Tab 首页 |
| wechat-nav（常用） | 微信标题栏 + 底部 Tab + 胶囊，小程序主结构 |
| wechat-content / wechat-header / wechat-tabs | 沉浸 / 二级 / Tab 首页 |
- 壳内页面遵守移动端规范：触控目标 ≥44px、单列、卡片式内容

## 生产流程速查

1. 选布局类型与页面骨架（本文件）→ 2. 叠加组件（components-guide）→ 3. 表单/CRUD/筛选区规范（forms/crud/ui-style-guide）→ 4. 套主题 Token → 5. 自查清单逐条过。
