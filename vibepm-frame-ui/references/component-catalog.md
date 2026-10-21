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
