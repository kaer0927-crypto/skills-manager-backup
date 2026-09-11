# 移动端表单页（v3 · 标准化改造 · 订单场景）

此页由 `mobile/form` 模板生成，作为 `mobile` 端表单页示例展示。
**v3 标准化改造**：顶部导航 N2、底部 B2、ROUTES 集中跳转、dirty 检测、提交 loading、9 字段覆盖。

## 一句话用途

新建 / 编辑某资源的表单页，支持输入、电话、选择器、数字、单选、开关、文本域等 7 类字段。

## 典型场景

新建订单（默认示例）/ 客户资料 / 审批申请 / 反馈建议。

## 模板能力一览

| 区域 | 模式 | 实现要点 |
|---|---|---|
| 顶部导航 | **N2 编辑页** | 左「取消」+ 中标题 + 右「保存」 |
| 表单字段 | — | 9 个 `van-field`：输入/电话/地址/选择器/金额/数量/单选组/开关/文本域 |
| 校验 | — | 必填 + 手机号正则 + 数字范围（在 `validate()` 里手写） |
| 选择器 | — | `van-action-sheet`（点击「订单类型」字段弹出） |
| 提交栏 | **B2 submit-bar** | 主操作按钮（block），loading 态 |
| dirty 检测 | — | 表单被改才弹二次确认；未改直接返回 |
| 提交 loading | — | 按钮 loading + 防重复点击 |

## 布局实现

```
┌─ van-nav-bar (固定, N2: 取消 | 标题 | 保存)
├─ .page-scroll (flex:1; overflow-y:auto)
│   ▸ van-field × 9
├─ .submit-bar (sticky bottom:0, B2: 提交)
└─────────────────────────
```

## 字段类型覆盖

| # | 控件 | 字段 | 类型 | 校验 |
|---|---|---|---|---|
| 1 | `van-field text required` | 客户名称 | 文本 | 必填 |
| 2 | `van-field type="tel" required` | 联系电话 | 电话 | 必填 + 手机号正则 |
| 3 | `van-field text` | 收货地址 | 文本 | 选填 ≤100 |
| 4 | `van-field readonly is-link` | 订单类型 | 选择器 | 必填（action-sheet） |
| 5 | `van-field type="digit" required` | 订单金额 | 数字 | 必填 |
| 6 | `van-field type="digit" required` | 商品数量 | 数字 | 必填 ≥1 |
| 7 | `van-field + #input slot` | 支付方式 | 单选组 | 默认微信 |
| 8 | `van-field + #input slot` | 加急处理 | 开关 | 默认 false |
| 9 | `van-field textarea` | 备注 | 文本域 | 选填 ≤200 |

## 数据模型（工厂函数）

```js
const initialForm = () => ({
  customer: '', phone: '', address: '',
  type: '', typeLabel: '',
  amount: '', quantity: 1,
  pay: 'wechat', urgent: false,
  remark: '',
});
const form = reactive(initialForm());
```

PM 新增字段：改 `initialForm()` 一处即可，`dirty` 检测无需改。

## dirty 检测

```js
const isDirty = computed(() => JSON.stringify(form) !== JSON.stringify(initialForm()));

const onCancel = () => {
  if (!isDirty.value) return goBack();           // 未改 → 直接返回
  showConfirmDialog({ title: '提示', message: '放弃当前编辑？' })
    .then(goBack).catch(() => {});
};
```

## 校验策略

模板用 `validate()` 手动校验（PM 接入 `van-form :rules` 可改为字段级实时校验）：

```js
const validate = () => {
  if (!form.customer) { toast.err('请填写客户名称'); return false; }
  if (!/^1\d{10}$/.test(form.phone)) { toast.err('手机号格式不正确'); return false; }
  if (!form.type) { toast.err('请选择订单类型'); return false; }
  // ...
  return true;
};
```

## 跳转关系（ROUTES 集中配置）

```js
const ROUTES = {
  list: 'mobile-list',     // 提交成功后跳列表
  back: 'mobile-list',     // 取消 / 返回
};
```

## 反馈封装

```js
const toast = {
  ok:  (m) => showToast && showToast({ message: m, type: 'success' }),
  err: (m) => showToast && showToast({ message: m, type: 'fail' }),
};
```

## 使用方式

```bash
python scripts/add_page.py . \
  --id order-form --title "新建订单" --template mobile-form
```

## PM 改模板最小动作清单

1. 改 `pageTitle`
2. 填 `ROUTES`
3. 改 `initialForm()` / `typeOptions`
4. 改 `validate()` / `onSubmit()` 提交逻辑

> ⚠️ **不要用 `<van-foo ... />` 自闭合写法**！
