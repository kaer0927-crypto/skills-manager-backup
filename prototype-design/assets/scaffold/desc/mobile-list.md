# 移动端列表页（v3 · 标准化改造 · 电商订单场景）

此页由 `mobile/list` 模板生成，作为 `mobile` 端列表页示例展示。
**v3 标准化改造**：顶部导航 N1、底部 B1、ROUTES 集中跳转表、4 态（loading/empty/error/success）、design tokens。

## 一句话用途

展示某资源的列表，支持搜索过滤、状态分类、下拉/底部 tab 导航切换。

## 典型场景

电商订单列表（默认示例）/ 客户管理 / 待办审批 / 商品列表。

## 模板能力一览

| 区域 | 模式 | 实现要点 |
|---|---|---|
| 顶部导航 | **N1 浏览页** | `van-nav-bar` 左返回 + 中标题 + 右搜索图标 |
| 搜索栏 | — | `van-search shape="round"` 实时过滤（computed） |
| 列表 | — | `van-cell v-for`，每行：状态点 + 标题 + 副标题 + 金额 + Tag |
| loading | — | `van-skeleton × 4` 骨架屏 |
| empty | — | `van-empty`（无关键字时显示「新建订单」按钮） |
| error | — | `van-empty image="error"` + 重新加载按钮 |
| 底部 tabbar | **B1 tabbar 导航** | `van-tabbar` sticky 黏底，3 个 tab |

## 布局实现

```
┌─ van-nav-bar (固定, N1)
├─ .page-scroll (flex:1; overflow-y:auto)
│   ▸ van-search
│   ▸ van-skeleton × 4   (loading)
│   ▸ van-empty + 重试   (error)
│   ▸ van-empty + 新建   (empty)
│   ▸ van-cell × N       (success)
├─ .tabbar-wrap (sticky bottom:0, B1)
└─────────────────────────
```

## 数据模型

```js
items: Array<{
  id: string,            // 'ORD-20260730001'
  title: string,         // 标题（订单号）
  subtitle: string,      // 副标题（客户 · 时间）
  statusText: string,    // 状态文案（待付款）
  statusType: string,    // 状态类型（primary/success/warning/danger/default）
  amount: string,        // 金额（含 ¥ 符号）
  time: string,          // 时间
}>
```

## 状态映射

| 业务状态 | statusType | 渐变色 | Tag 颜色 |
|---|---|---|---|
| 待付款 | `warning` | `--gradient-warning` | 橙 |
| 待发货 / 已发货 / 进行中 | `primary` | `--gradient-primary` | 蓝 |
| 已完成 | `success` | `--gradient-success` | 绿 |
| 退款中 / 异常 | `danger` | `--gradient-danger` | 红 |
| 已取消 | `default` | — | 灰 |

## 跳转关系（ROUTES 集中配置）

```js
const ROUTES = {
  detail:  'mobile-detail',     // 列表 → 详情
  newForm: 'mobile-form',       // 列表 → 新建表单
  back:    'mobile-list',       // 默认返回
};
```

PM 只需改 ROUTES 一处即可。

## 4 态约定

| 状态 | 触发条件 | UI 表现 |
|---|---|---|
| loading | 数据加载中 | 4 条 `van-skeleton` 骨架屏 |
| error | 接口异常 | `van-empty image="error"` + 重新加载按钮 |
| empty | 过滤无结果 / 列表为空 | `van-empty`；无关键字时显示「新建订单」按钮 |
| success | 默认 | `van-cell` 列表 + 底部「已加载 N 条」 |

## 标准变体

- 可去掉 `.tabbar-wrap`，改用 B0（无底部），适用于二级页面
- 可加 `<van-tabs>` 在搜索栏下做横向分类筛选
- 可用 `<van-pull-refresh>` + `<van-list>` 实现下拉刷新 + 触底加载

## 使用方式

```bash
python scripts/add_page.py . \
  --id order-list --title "订单列表" --template mobile-list
```

## PM 改模板最小动作清单

1. 改 `pageTitle`（顶部 nav 标题）
2. 填 `ROUTES` 跳转路由表
3. 改 `items` 业务数据
4. 改 `tabbarItems`（业务 tab）
5. 在 `desc/order-list.md` 写字段说明 + 跳转关系图
6. 跑 `python scripts/sync_nav.py <项目名>` 同步

> ⚠️ 不要在 `<div id="app">` 内写 `{{XXX}}` 占位符（Vue 插值语法）。
>
> ⚠️ **不要用 `<van-foo ... />` 自闭合写法**！file:// HTML parser 会吞后续内容。
