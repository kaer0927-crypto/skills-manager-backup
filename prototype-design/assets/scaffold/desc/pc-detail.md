# PC 详情页（v2 · 100vh 两段固定 + 状态头 + 描述分组 + Tabs）

此页由 `pc/detail` 模板生成，作为 `pc` 端详情页示例展示。

## 模板能力一览

| 区域 | 实现要点 |
| --- | --- |
| 布局 | **两段式**：状态头（固定）/ 内容区（`flex:1`，独立滚动）。窗口再矮，顶部标题、状态、操作按钮也不会被滚出屏幕 |
| 状态头 | 返回 + 标题 + 编号 + 状态 Tag + 右侧操作组（**编辑 / 删除 / 更多下拉**，下拉含复制·打印·导出 PDF·停用）|
| 概要指标条 | 4 个关键数字横向排列（明细条数 / 总数量 / 总金额 / 已完成占比），带竖分隔线，供快速扫读 |
| 描述区 | 两组 `el-descriptions`（**基本信息 3 列 border / 业务信息 3 列 border**），支持 `span` 跨列与 Tag 着色 |
| Tabs | 三个页签：**明细列表**（8 行表格 + 合计行）/ **操作日志**（5 条时间线，按类型着色）/ **附件**（3 个文件 + 大小 + 下载）|
| 中文文案 | 表格空态、确认弹窗全中文，由 `assets/zh-cn-locale.js` 统一提供 |

## 布局实现

整页 `display: flex; flex-direction: column; height: 100vh`：

```
┌─ detail-header (flex-shrink:0)
│    返回 │ 示例名称  NO.202607280001  [已启用]    【编辑】【删除】【更多▾】
│    ─────────────────────────────────────────────────────────────────
│    明细条数 8 条 │ 总数量 156 件 │ 总金额 ¥23,470.00 │ 已完成占比 50.0%
├─ detail-body   (flex:1; min-height:0; overflow-y:auto)
│   ┌ detail-card ▸ 基本信息   el-descriptions 3 列 border
│   ├ detail-card ▸ 业务信息   el-descriptions 3 列 border
│   └ detail-card ▸ Tabs       明细列表 / 操作日志 / 附件
└──────────────────────────────────────────────────────────────────────
```

- `#app { height: 100vh; display: flex; flex-direction: column; overflow: hidden }`
- `detail-header` 设 `flex-shrink:0`，只占自身高度；
- `detail-body` 设 `flex:1; min-height:0; overflow-y:auto` —— `min-height:0` 不可省，
  否则内容会把容器撑破，滚动条跑到 `<body>` 上，固定头就失效了；
- 概要指标条用 `grid-template-columns: repeat(4,1fr)` + `border-right` 做竖分隔。

## 描述项数据驱动

两组描述区都是数组驱动，**改数据不用动模板**：

```js
const baseInfo = ref([
  { label: '名称', value: '示例名称' },
  { label: '状态', value: '已启用', tag: true, tagType: 'success' },  // tag:true → 渲染成 el-tag
  { label: '备注', value: '……', span: 3 },                            // span → 跨列
]);
```

| 字段 | 作用 |
| --- | --- |
| `label` / `value` | 描述项的标签与内容 |
| `tag` | 为 `true` 时渲染成 `el-tag` 而不是纯文本 |
| `tagType` | Tag 配色：`success` / `info` / `warning` / `danger` |
| `span` | 跨列数，默认 1；长文本用 3 铺满整行 |

## Tabs 三个页签

| 页签 | 组件 | 内容 |
| --- | --- | --- |
| 明细列表 | `el-table` + `show-summary` | 8 行示例数据；序号 / 明细名称 / 规格 / 数量 / 单价 / 小计 / 状态 Tag；底部**合计行**自动求和数量与金额 |
| 操作日志 | `el-timeline` | 5 条记录，`type` 控制节点着色（primary / success / warning / info），每条含操作人与备注 |
| 附件 | 自定义文件列表 | 3 个文件，含图标 / 文件名 / 大小 / 上传时间 / 下载按钮 |

金额格式由统一的 `money()` 函数产出（`¥ 23,470.00`），单价、小计、合计三处共用，保证格式一致。

> ⚠️ `el-table-column` 必须用显式 `</el-table-column>` 闭合。Element Plus 2.8.8 + Vue 3.5
> 在自闭合 `<el-table-column ... />` 写法下会把后续列错误地嵌套进前一列，表现为「每列变成一行」。

## 中文文案默认

所有用户可见的组件文案、表头、按钮、提示语均默认中文。表格空态、确认弹窗按钮由 `assets/zh-cn-locale.js` 提供的完整 zh-cn 语言包覆盖 —— `element-plus.full.min.js` 是**只打了英文**的构建，不配 locale 会显示 `No Data / OK / Cancel`。

## 使用方式

```bash
# 在已有项目里生成一个 pc-detail 风格的详情页
python scripts/add_page.py . \
  --id order-detail --title "订单详情" --template detail --parent pc-templates
```

PM 拿到后可基于此页修改：

- `<title>` 与 `detailHeader.title`：页面标题；
- `detailHeader`：状态头的标题 / 编号 / 状态文案与配色；
- `summaryItems`：概要指标条的 4 个数字；
- `baseInfo` / `bizInfo`：两组描述项（改数组即可）；
- `detailRows`：明细表格数据；
- `timeline`：操作日志；
- `attachments`：附件列表；
- `onBack()` / `onEdit()` 里的 `gotoNode('xxx')`：改成真实的列表页 / 表单页节点 id。

> ⚠️ 不要在 `<div id="app">` 内部写 `{{XXX}}` 形式的占位符 —— 那是 Vue 的插值语法，会被当作表达式求值并抛 `XXX is not defined`（页面上表现为标题空白）。

可删除此示例页另建：`python scripts/remove_page.py . --id pc-detail`。
