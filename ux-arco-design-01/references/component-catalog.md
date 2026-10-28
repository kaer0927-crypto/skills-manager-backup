# Frame 组件索引（VibePM / 中后台原型及前端交付解决方案）

> 来源：vibepm.top/frame 全量离线镜像（2026-09-10 抓取）。页面名 = `admin/` 下 HTML 文件名；
> 组件渲染依赖共享的 `admin/css/*` 与 `admin/js/pages/*`（Vue SPA 结构）。
> 生产前端界面时按此索引选页面骨架，再按主题规范（见 `ui-style-guide.md` 与 `themes/`）改造。

## 选型速查

| 要做的界面 | 首选组件 type | 源文件（admin/） |
|---|---|---|
| 登录页 | `login` / `login-banner` / `login-split` | login-cover.html（默认）/ login-banner.html / login-split.html |
| 业务首页/看板 | `dashboard` | dashboard.html（默认首页，指标+图表区） |
| 电商/CRM/教务/财务/银行等业态看板 | `dashboard-ecommerce` / `dashboard-crm` / `dashboard-academy` / `dashboard-finance` / `dashboard-analytics` / `dashboard-customer` / `dashboard-productivity` / `dashboard-banking` | 同名 HTML |
| 数据列表（CRUD 主范式） | `list` | list-search-table.html（筛选+表格+分页，最常用） |
| 卡片/看板/树表/筛选/标签列表 | `list-card` / `list-kanban` / `list-tree-table` / `list-filter-table` / `list-tag-filter` | 同名 HTML |
| 行内编辑 / 日历 / 文件管理 / 导入向导 | `list-editable` / `list-calendar` / `list-media` / `list-import` | 同名 HTML |
| 基础/分组/分步/纵向表单 | `form-basic` / `form` / `form-step` / `form-step-vertical` | form-basic.html / form-group.html / form-step.html / form-step-vertical.html |
| 详情页 | `detail` / `detail-advanced` / `list-master-detail` | profile-basic.html / profile-advanced.html / list-master-detail.html |
| 结果页 | `result-success` / `result-waiting` / `result-warning` / `result-error` | 同名 HTML |
| 异常页 | `exception-403` / `exception-404` / `exception-500` | 同名 HTML |
| 个人中心 | `user-home` / `user-setting` / `user-message` | user-home.html / user-setting.html / message-list.html |
| 移动端 iOS 壳 | `ios-nav`（完整）/ `ios-content` / `ios-header` / `ios-tabs` | app/ios_frame_nav.html 等 |
| 移动端微信小程序壳 | `wechat-nav`（完整）/ `wechat-content` / `wechat-header` / `wechat-tabs` | app/wechat-frame-nav.html 等 |
| 组件/控件参考 | `component-basic` / `component-form` / `component-table-extended` / `component-list` / `component-chart` / `component-metric-card` / `component-rich-text` 等 | admin/component-*.html（演示页） |

## Admin 后台页面全量清单（50 个）

### 登录页（3）
| type | 源文件 | 说明 |
|---|---|---|
| `login` | login-cover.html | 全屏封面背景 + 居中登录卡；默认鉴权入口 |
| `login-banner` | login-banner.html | 左侧 Banner + 右侧表单 |
| `login-split` | login-split.html | 居中双栏卡片登录 |

### 数据看板（9）
`dashboard`（默认首页）、`dashboard-ecommerce`、`dashboard-crm`、`dashboard-academy`、`dashboard-finance`、`dashboard-analytics`、`dashboard-customer`、`dashboard-productivity`、`dashboard-banking`。均为 KPI 指标区 + 图表/表格区结构，业务语义不同。

### 列表页（11）
| type | 源文件 | 说明 |
|---|---|---|
| `list` | list-search-table.html | 筛选面板 + 表格 + 分页，CRUD 主范式（常用） |
| `list-card` | list-card.html | 卡片网格列表 |
| `list-kanban` | list-kanban.html | 列式看板 |
| `list-tree-table` | list-tree-table.html | 左树右表 |
| `list-filter-table` | list-filter-table.html | 左筛右表 |
| `list-tag-filter` | list-tag-filter.html | 顶部平铺标签筛选 + 表格 |
| `list-master-detail` | list-master-detail.html | 左列表右详情（工单/会话） |
| `list-editable` | list-editable.html | 行内编辑 + 批量保存 |
| `list-calendar` | list-calendar.html | 日历排期 |
| `list-media` | list-media.html | 目录树 + 宫格素材 |
| `list-import` | list-import.html | 上传→校验→结果三步导入 |

### 表单页（4）
`form-basic`（form-basic.html）、`form`（form-group.html 分组）、`form-step`（form-step.html 横向分步）、`form-step-vertical`（form-step-vertical.html 侧向步骤）。

### 详情页（3）
`detail`（profile-basic.html）、`detail-advanced`（profile-advanced.html）、`list-master-detail`（同列表类，左列表右详情）。

### 结果页（4）
`result-success`、`result-waiting`、`result-warning`、`result-error`。

### 异常页（3）
`exception-403`、`exception-404`、`exception-500`。

### 个人中心（3）
`user-home`（user-home.html）、`user-setting`（user-setting.html）、`user-message`（message-list.html）。

### 组件演示页（11，供抄控件写法）
`component-basic`（按钮/标签/反馈）、`component-extended`、`component-form`、`component-form-extended`、`component-table-extended`、`component-list`、`component-rich-text`、`component-chart`、`component-chart-extended`、`component-metric-card`、`component-chart-palette`（图表配色方案 A/B/C）。

## APP 设备壳（8 个）

| type | 源文件 | 说明 |
|---|---|---|
| `ios-content` | app/ios_frame.html | iOS 纯内容（沉浸页） |
| `ios-header` | app/ios_frame_header.html | iOS 仅顶栏标题 |
| `ios-tabs` | app/ios_frame_tabs.html | iOS 仅底部 Tab |
| `ios-nav` | app/ios_frame_nav.html | iOS 标题栏 + 底部 Tab（常用） |
| `wechat-content` | app/wechat-frame.html | 微信纯内容（胶囊+隐藏标题栏） |
| `wechat-header` | app/wechat-frame_header.html | 微信仅顶栏 + 胶囊 |
| `wechat-tabs` | app/wechat-frame-tabs.html | 微信仅底部 Tab + 胶囊 |
| `wechat-nav` | app/wechat-frame-nav.html | 微信完整导航（常用） |

## 规范扩展模式（`references/extensions/`）

索引里没有、但业务确实需要的结构，先在 `extensions/` 登记再实现，禁止私自立一套 Token 或组件。
登记要求与模板见 [extensions/README.md](extensions/README.md)。

| 场景 | 归属文档 | 说明 |
|---|---|---|
| 页面内多页签 / 面包屑换页签 | `pages-guide.md`「shell 骨架结构」TabBar + `extensions/page-tabs.md`（待登记） | 已有基础规则（可关闭/关闭其他/刷新 + keep-alive 联动）；路由级多页签的固定、右键批量关闭、最多 8 条再登记 |
| 复杂审批流 / 流程编排 | `extensions/approval-flow.md`（待登记） | 状态机 + 节点权限 + 会签/或签，需要 `state-machine.md` 与 `permission-guide.md` 同时落地 |
| 多维交叉分析 / 透视表 | `extensions/pivot-table.md`（待登记） | 列动态生成，需要单独的列宽、冻结与合计规则 |
| 大屏 / 指挥中心 | `pages-guide.md`「大屏 / 多维分析」+ `assets/skeletons/visualization-screen.vue` | 已实装，不必另行登记 |
| 富文本 / 文档编辑 | `components-guide.md`「富文本」 | 已有规范，扩展能力（协同、版本）再登记 |

> 判定口径：现有 50 页骨架 + 8 个移动壳 + 本文规范能覆盖 80% 以上结构 → 直接复用；只有「结构层面新增」才登记。

## 布局类型（layout 字段）
- `shell`：完整后台壳（顶栏 + 侧栏 + 内容区）
- `center`：居中卡片（登录/结果/异常页）
- `split`：左右分栏（树表/筛选表/主从详情）
- `phone`：设备壳内页面（app/）

## 页面打开方式
- 母版库总览：打开 `gallery.html`（左侧分类、右侧页面卡片，点预览查看）
- 直接打开：`admin/<文件名>.html` 或 `app/<文件名>.html`
- 带鉴权的页面（dashboard 系列等）：URL 后加 `?galleryPreview=1` 跳过登录，或先开 login-cover.html 用演示账号 admin / 123456 登录
- 全部资源已本地化，file:// 双击即可离线使用

## Arco Pro 官方示例页对照（实现参考，非骨架来源）

> `arco-design/arco-design-pro-vue` 只有 19 个页面，覆盖度低于本索引的 50 页；它的价值是**官方 API 写法参考**，不是骨架来源。
> 骨架仍以本索引 + `pages-guide.md` 为准；需要看真实 Arco 写法时对照下表。
> 逐页实现级比对（可吸收的 7 点、不要照抄的 5 点）见 [arco-pro-pages.md](arco-pro-pages.md)。

| Arco Pro 页面 | 对应 vibepm 骨架 | 可借鉴点 |
|---|---|---|
| `dashboard/workplace` | `dashboard` | 欢迎区 + 快捷入口 + 最近访问 + 公告卡 |
| `dashboard/monitor` | `dashboard-analytics` | 实时指标卡 + 数据面板 + 状态卡 |
| `list/search-table` | `list` | 筛选 + 表格 + 分页的标准组合（官方实现） |
| `list/card` | `list-card` | 卡片网格与分页配合 |
| `form/group` | `form` | 分组卡片表单 + 底部提交行 |
| `form/step` | `form-step` | 分步表单 + 完成页 |
| `result/success`、`result/error` | `result-success`、`result-error` | `a-result` 的标题/副标题/操作区写法 |
| `exception/403`、`404`、`500` | `exception-403/404/500` | `a-result status="403/404/500"` 直接复用 |
| `user/info` | `user-home` | 个人信息 + 最近动态 + 通知 |
| `user/setting` | `user-setting` | 设置项分组与保存 |
| `profile/basic` | `detail` | 描述列表 + 操作日志 |
| `login` | `login` | 登录卡、Banner 区、表单校验 |
| `visualization/*` | 无（需自建大屏骨架） | 多维分析布局可参考，但需另做深色大屏规范 |

### 差异说明

- Pro 没有：看板列视图、日历、文件管理、导入向导、行内编辑、左树右表、标签筛选、移动端壳——这些以本索引为准。
- Pro 有而本索引缺：`visualization` 大屏/多维分析页 —— 已在 `pages-guide.md`「大屏 / 多维分析」补出规则，并实装骨架 `assets/skeletons/visualization-screen.vue`（可直接引入）。
- 抄写法时优先看 Pro 的 `src/layout/default-layout.vue`（顶栏 60 / 侧栏 200·48 / breakpoint xl / 多页签 / keep-alive），页面细节再看 `src/views/*`。
