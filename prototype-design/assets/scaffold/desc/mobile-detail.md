# 移动端详情页（v3 · 标准化改造 · 订单详情场景）

此页由 `mobile/detail` 模板生成，作为 `mobile` 端详情页示例展示。
**v3 标准化改造**：顶部导航 N1'（返回+标题+更多）、底部 B3、ROUTES 集中跳转、状态头渐变映射、loading/error 态。

## 一句话用途

展示某个资源的详细信息，含状态头、关键指标、字段描述、商品明细、操作日志。

## 典型场景

订单详情（默认示例）/ 客户详情 / 审批详情 / 商品详情。

## 模板能力一览

| 区域 | 模式 | 实现要点 |
|---|---|---|
| 顶部导航 | **N1' 详情+更多** | 左返回 + 中标题 + 右 `van-icon ellipsis` 更多下拉 |
| 状态头 | — | 渐变色背景 + 标题 + 状态 Tag + 编号 + 快捷操作（复制/分享） |
| 概要指标 | — | 2×2 网格，4 项关键数字 |
| 基础信息 | — | `van-cell` × 6（基础信息） |
| 收货信息 | — | `van-cell` × 3（收货人/电话/地址） |
| 商品明细 | — | CSS 缩略图 + 名称 + 规格数量 + 价格 |
| 操作日志 | — | `van-cell` × N（时间 + 操作人 + 动作） |
| 操作栏 | **B3 action-bar** | 按状态动态按钮（取消/再来一单/支付/编辑） |
| 更多菜单 | — | `van-action-sheet`（复制/分享/导出/投诉） |
| loading | — | `van-skeleton` |
| error | — | `van-empty image="error"` + 重试 |

## 布局实现

```
┌─ van-nav-bar (固定, N1': 返回 | 标题 | ⋯)
├─ .page-scroll (flex:1; overflow-y:auto)
│   ▸ .header-card      渐变状态头 + 标题 + 状态 Tag
│   ▸ .card summary    2×2 概要指标条
│   ▸ .card 基础信息    van-cell × 6
│   ▸ .card 收货信息    van-cell × 3
│   ▸ .card 商品明细    goods-row × N（CSS 缩略图）
│   ▸ .card 操作日志    van-cell × N
├─ .action-bar (sticky bottom:0, B3: 次操作 + 主操作)
└─────────────────────────
```

## 状态头渐变映射

```js
const header = reactive({
  title: '订单 ORD-20260730001',
  code: 'NO.ORD-20260730001',
  statusText: '待付款',
  statusType: 'warning',
  gradient: 'var(--gradient-warning)',   // 状态 → 渐变 CSS 变量
});
```

| 业务状态 | statusType | gradient |
|---|---|---|
| 待付款 | `warning` | `--gradient-warning`（橙渐变） |
| 已付款 / 进行中 | `primary` | `--gradient-primary`（蓝渐变） |
| 已完成 | `success` | `--gradient-success`（绿渐变） |
| 退款中 / 异常 | `danger` | `--gradient-danger`（红渐变） |
| 已取消 | `default` | `--gradient-primary`（蓝渐变） |

## 按钮可见性（按状态动态）

```js
const canCancel  = computed(() => ['warning', 'primary'].includes(header.statusType));  // 待付款/进行中可取消
const canReorder = computed(() => ['success', 'danger'].includes(header.statusType));   // 已完成/退款可再来一单
```

底部 B3 操作栏根据状态显示不同按钮：
- `warning`（待付款）→ 取消订单 + 立即支付
- `primary`（进行中）→ 取消订单 + 编辑订单
- `success`（已完成）→ 再来一单 + 编辑订单
- `default`（已取消）→ 仅再来一单

## 数据模型

```js
header: { title, code, statusText, statusType, gradient }
summaryItems: [{ label, value, unit }]                // 4 项
baseInfo: [{ label, value }]                          // 6 项（基础信息）
shippingInfo: [{ label, value, color? }]              // 3 项（收货信息）
goodsList: [{ id, name, spec, qty, price, thumbText }]  // N 件商品
logList: [{ time, actor, action }]                    // N 条日志
```

## 跳转关系（ROUTES 集中配置）

```js
const ROUTES = {
  list:   'mobile-list',     // 删除 / 取消后回列表
  form:   'mobile-form',     // 编辑跳表单
  detail: 'mobile-detail',   // 当前详情
};
```

## 4 态约定

| 状态 | UI 表现 |
|---|---|
| loading | 2 块 `van-skeleton`（含 avatar） |
| error | `van-empty image="error"` + 重新加载按钮 |
| success | 完整渲染所有区块 |
| 空 | N/A（详情页通常不会空） |

## 使用方式

```bash
python scripts/add_page.py . \
  --id order-detail --title "订单详情" --template mobile-detail
```

## PM 改模板最小动作清单

1. 改 `pageTitle`
2. 填 `ROUTES`
3. 改 `header` / `summaryItems` / `baseInfo` / `shippingInfo` / `goodsList` / `logList`
4. 改 `onEdit` / `onCancel` / `onReorder` / `onPay` / `onMoreSelect` 逻辑

> ⚠️ **不要用 `<van-foo ... />` 自闭合写法**！
