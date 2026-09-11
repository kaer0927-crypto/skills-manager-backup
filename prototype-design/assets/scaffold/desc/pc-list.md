# PC 列表页（v2 · 12 筛选项 + 固定表头/分页 + 左右固定列）

此页由 `pc/list` 模板生成，作为 `pc` 端列表页示例展示。

## 模板能力一览

| 区域 | 实现要点 |
| --- | --- |
| 筛选区 | 共 12 个筛选项，覆盖 **输入框搜索 / 下拉单选 / 下拉多选 / 日期范围 / 弹窗单选 / 弹窗多选** 6 种类型；前 4 个直接展示在主表单，剩余 8 个收起在右侧「更多筛选」抽屉内（**抽屉内一行一个，单列网格**），按钮带已选数量 badge |
| 弹窗单选 | 以「选择公司」为例，点击输入框 → 弹出 Dialog → 列表内单选一个公司 → 确定后回填输入框 |
| 弹窗多选 | 以「选择门店」为例，点击输入框 → 弹出 Dialog → 复选框组多选 → 确定后回填（逗号分隔展示） |
| 操作区 | **新增 / 导入 / 导出** 三个按钮横向一次摆放，右侧带刷新按钮 |
| 列表区 | 列：选择 / **序号** / 字段1..字段10 / 创建时间 / 创建人 / 操作（共 15 列；序号列的表头文案为中文「序号」）；**表头背景 #f0f2f5 + 文字 #333333 / 600 加粗**，与白色数据行拉开视觉层级 |
| 模拟数据 | 默认 **100 条**，每页 **20 条**，分页 `page-sizes=[10,20,50,100]`；创建时间格式 `YYYY-MM-DD HH:mm:ss`（精确到秒） |
| 滚动行为 | **上下滚动只滚动数据区**（表头 + 分页组件固定）；**左右滚动**时「选择 + 序号 + 字段1」共 3 列固定在左，「操作」固定在右 |

## 布局实现

整页 `display: flex; flex-direction: column; height: 100vh`：

```
┌─ filter-card  (flex-shrink:0)  主筛选（前 4 项）+ 更多筛选按钮 ─┐
├─ toolbar      (flex-shrink:0)  新增 / 导入 / 导出 / 刷新         ─┤
├─ table-card   (flex:1; min-height:0)
│   ├─ el-table height="100%"   ← 数据区纵向滚动；左右固定列吸边  ─┤
│   └─ pagination-bar           (flex-shrink:0)                    ─┤
└──────────────────────────────────────────────────────────────────┘
```

- `#app { height: 100vh; display: flex; flex-direction: column; overflow: hidden }`
- `filter-card` / `toolbar` / `pagination-bar` 都设 `flex-shrink:0`，只占自身高度；
- `table-card` 设为 `flex: 1; min-height: 0; display: flex; flex-direction: column`，
  内部 el-table 再 `flex: 1; height: 100%`，让 Element Plus 接管表头固定 + 数据区滚动；
- 选择 + 序号两列 `fixed="left"`，操作列 `fixed="right"`，自然实现左右固定列；
- 列总宽（约 1758px）远大于容器宽度，左右滚动条自动出现。

## 12 个筛选项分布

| # | 类型 | 字段 | 位置 |
| --- | --- | --- | --- |
| 1 | 输入框搜索 | 关键字 | 主表单 |
| 2 | 下拉单选 | 订单状态 | 主表单 |
| 3 | 下拉多选 | 支付方式 | 主表单 |
| 4 | 日期范围 | 下单日期 | 主表单 |
| 5 | 弹窗单选 | 所属公司 | 抽屉 |
| 6 | 弹窗多选 | 所属门店 | 抽屉 |
| 7 | 输入框搜索 | 订单编号 | 抽屉 |
| 8 | 下拉单选 | 渠道来源 | 抽屉 |
| 9 | 下拉多选 | 业务标签 | 抽屉 |
| 10 | 日期范围 | 创建日期 | 抽屉 |
| 11 | 下拉单选 | 会员等级 | 抽屉 |
| 12 | 下拉单选 | 配送方式 | 抽屉 |

抽屉内每个字段填值后，主表单的「更多筛选」按钮右上角会显示数字 badge（`moreFilterCount`）。

## 中文文案默认

所有用户可见的组件文案、表头、按钮、提示语均默认为中文（必要的英文图标 / 代码字段除外）。

本地化统一由 `assets/zh-cn-locale.js` + `<el-config-provider :locale="zhCnLocale">` 提供，**四个 PC 模板共用同一份语言包**：

```html
<script src="../assets/zh-cn-locale.js"></script>
...
<el-config-provider :locale="zhCnLocale">
```

```js
const zhCnLocale = window.ZH_CN_LOCALE;
```

原因：scaffold 自带的 `element-plus.full.min.js` 是**只打了英文**的构建（包内搜不到任何中文串，也没有 `zhCn` 导出）。不配 locale 的话，分页器显示 `Total 100 / Go to`、日期面板显示 `Mon Jan`、确认弹窗按钮是 `OK / Cancel`。

抽成共享文件而不是每页内联，是因为这份对象有 20 个组件命名空间、100+ 个 key，且 key 名并不直觉（月份是 `month1..month12` 而非 `months.jan`；表格清空筛选是 `clearFilter` 而非 `resetFilter`）。四份副本意味着漏一个 key 就漏一句英文，且修正要改四处。

## 使用方式

```bash
# 新建业务项目，自动包含此示例页
python .claude/skills/prototype-design/scripts/init_project.py my-project --name "我的项目"

# 在已有的项目里再生成一个 pc-list 风格的列表页
python scripts/add_page.py . \
  --id order-list --title "订单列表" --template list --parent pc-templates
```

PM 拿到后可基于此页修改：

- `options`：每个下拉 / 多选的候选项（可替换为接口返回）；
- `columns`：表格 10 个数据列的 `prop / label / width`；
- `allCompanies` / `allStores`：弹窗单选 / 多选的源数据；
- `initMock()`：将构造 100 条模拟数据改为真实接口调用。

可删除此示例页另建：`python scripts/remove_page.py . --id pc-list`。