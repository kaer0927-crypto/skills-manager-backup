# PC 表单页（v2 · 100vh 三段固定 + 三分组 + 14 个控件 + 完整校验）

此页由 `pc/form` 模板生成，作为 `pc` 端表单页示例展示。

## 模板能力一览

| 区域 | 实现要点 |
| --- | --- |
| 布局 | **三段式**：页头（固定）/ 表单区（`flex:1`，独立滚动）/ 底部操作栏（固定）。窗口再矮，「提交 / 保存草稿 / 取消」也不会被滚出屏幕 |
| 分组一 · 基本信息 | 输入框（含字数统计）/ 下拉单选 / 下拉多选（collapse-tags）/ 数字输入 / 日期 / 日期时间 |
| 分组二 · 业务信息 | **弹窗单选**（选择公司）/ **弹窗多选**（选择门店）/ 级联选择（省·市）/ 单选组 / 复选组 / 开关 |
| 分组三 · 其他设置 | 文本域（200 字上限 + 字数统计）/ 文件上传占位（不做真实上传）/ 说明 Alert |
| 校验 | 覆盖 **必填 / 长度上下限 / 数字范围 / 正则（手机号）/ 自定义校验函数** 五类；空表单点提交会同时亮出 8 条错误 |
| 栅格 | 主体两列；「备注 / 附件 / 说明」通过 `.span-2` 跨满两列 |
| 中文文案 | 日期面板、下拉、确认弹窗全中文，由 `assets/zh-cn-locale.js` 统一提供 |

## 布局实现

整页 `display: flex; flex-direction: column; height: 100vh`：

```
┌─ page-header  (flex-shrink:0)  表单页  带 * 为必填项          【重置】 ─┐
├─ form-body    (flex:1; min-height:0; overflow-y:auto)
│   ┌ form-card ▸ 基本信息   8 个字段 / 两列栅格                          │
│   ├ form-card ▸ 业务信息   6 个字段 / 含两个弹窗选择器                  │
│   └ form-card ▸ 其他设置   备注 / 附件 / 说明（均跨两列）               │
├─ form-footer  (flex-shrink:0)  最后保存：--  【取消】【保存草稿】【提交】 ─┤
└────────────────────────────────────────────────────────────────────────┘
```

- `#app { height: 100vh; display: flex; flex-direction: column; overflow: hidden }`
- `page-header` / `form-footer` 设 `flex-shrink:0`，只占自身高度；
- `form-body` 设 `flex:1; min-height:0; overflow-y:auto` —— **`min-height:0` 是关键**，
  没有它 flex 子项的默认 `min-height:auto` 会让内容把容器撑破，滚动条跑到 `<body>` 上，
  底部操作栏就跟着被顶出视口了；
- 两列栅格用 `display:grid; grid-template-columns: repeat(2,1fr)`，跨列项加 `.span-2`。

## 14 个控件分布

| # | 控件 | 字段 | 分组 | 校验 |
| --- | --- | --- | --- | --- |
| 1 | 输入框 | 名称 | 基本信息 | 必填 + 长度 2~40 |
| 2 | 输入框 | 编号 | 基本信息 | 自定义校验函数（字母 / 数字 / 短横线，4-20 位）|
| 3 | 下拉单选 | 类型 | 基本信息 | 必填 |
| 4 | 下拉多选 | 业务标签 | 基本信息 | 必填（数组非空）|
| 5 | 数字输入 | 数量 | 基本信息 | 数字范围 1~9999 |
| 6 | 输入框 | 联系电话 | 基本信息 | 必填 + 正则 `/^1[3-9]\d{9}$/` |
| 7 | 日期 | 生效日期 | 基本信息 | 必填 |
| 8 | 日期时间 | 截止时间 | 基本信息 | — |
| 9 | 弹窗单选 | 所属公司 | 业务信息 | 必填 |
| 10 | 弹窗多选 | 覆盖门店 | 业务信息 | — |
| 11 | 级联选择 | 所属区域 | 业务信息 | 必填 |
| 12 | 单选组 | 优先级 | 业务信息 | — |
| 13 | 复选组 / 开关 | 通知方式 / 立即启用 | 业务信息 | — |
| 14 | 文本域 / 上传 | 备注 / 附件 | 其他设置 | — |

## 弹窗选择器交互

与列表页 `pc-list` 完全一致的写法（`.picker-toolbar` / `.picker-list` / `.picker-row` 三个类名共用）：

1. 表单里放一个 `readonly` 输入框，`@click` 打开 Dialog；
2. Dialog 内带搜索框 + 列表，单选走 `is-checked` 高亮，多选走 `el-checkbox-group`；
3. 「确定」把选中项回填到 `form.companyName` / `form.storeNames`（多选逗号分隔）；
4. **回填后手动调 `validateField('companyId')`** —— 弹窗赋值不会触发 `change` 事件，
   不补这一步的话必填红字不会自动消掉。

## 数据模型用工厂函数

```js
const initialForm = () => ({ name: '', code: '', /* ... */ });
const form = reactive(initialForm());

// 重置 = 一行，不用逐字段手写
const onReset = () => {
  Object.assign(form, initialForm());
  formRef.value && formRef.value.clearValidate();
};
```

好处：新增字段只在 `initialForm()` 里加一处，重置逻辑自动跟随，杜绝「加了字段忘了在重置里清」这个经典 bug。

## 中文文案默认

所有用户可见的组件文案、标签、按钮、提示语均默认中文。日期面板、下拉空态、确认弹窗按钮由 `assets/zh-cn-locale.js` 提供的完整 zh-cn 语言包覆盖 —— `element-plus.full.min.js` 是**只打了英文**的构建（包内搜不到任何中文串），不配 locale 会显示 `Mon / Jan / OK / Cancel`。

## 使用方式

```bash
# 在已有项目里生成一个 pc-form 风格的表单页
python scripts/add_page.py . \
  --id order-form --title "新建订单" --template form --parent pc-templates
```

PM 拿到后可基于此页修改：

- `<title>` 与 `pageTitle`：页面标题；
- `initialForm()`：表单数据模型（增删字段只改这里）；
- `rules`：校验规则；
- `options`：各下拉 / 级联的候选项；
- `allCompanies` / `allStores`：弹窗选择器源数据；
- `onSubmit()`：提交逻辑（当前是 `setTimeout` + `ElMessage`，替换为真实接口调用）；
- `onCancel()` 里的 `gotoNode('xxx')`：改成真实的列表页节点 id。

> ⚠️ 不要在 `<div id="app">` 内部写 `{{XXX}}` 形式的占位符 —— 那是 Vue 的插值语法，会被当作表达式求值并抛 `XXX is not defined`（页面上表现为标题空白）。页面标题请改 `<title>` 与 `pageTitle`。

可删除此示例页另建：`python scripts/remove_page.py . --id pc-form`。
