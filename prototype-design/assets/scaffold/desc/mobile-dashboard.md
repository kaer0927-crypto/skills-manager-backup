# 移动端仪表盘（v3 · 标准化改造 · 电商运营首页）

此页由 `mobile/dashboard` 模板生成，作为 `mobile` 端仪表盘示例展示。
**v3 标准化改造**：顶部导航 N3（位置+标题+铃铛+badge）、底部 B1、ROUTES 集中跳转、KPI 渐变卡、loading/error 态。

## 一句话用途

主页 / 工作台：聚合关键指标、快捷入口、近期活动，一屏掌握业务全貌。

## 典型场景

电商运营首页（默认示例）/ 后台工作台 / 销售个人看板 / 数据总览。

## 模板能力一览

| 区域 | 模式 | 实现要点 |
|---|---|---|
| 顶部导航 | **N3 主页** | 左位置 + 中标题 + 右铃铛（带 `van-badge` 通知数） |
| KPI 卡 | — | 2 个渐变卡：标签 + 数值 + 单位 + 环比（涨/跌着色） |
| 快捷入口 | — | `van-grid :column-num="4"` 4 个最常用入口 |
| 近期活动 | — | `van-cell` + CSS 缩略图占位 |
| loading | — | KPI 卡 value 显示「—」 |
| error | — | 整页 `van-empty image="error"` + 重试 |
| empty | — | 近期活动为空显示 `van-empty` |
| 底部 tabbar | **B1 tabbar** | `van-tabbar` sticky 黏底，3 个 tab |

## 布局实现

```
┌─ van-nav-bar (固定, N3: 北京 | 仪表盘 | 🔔[badge])
├─ .page-scroll (flex:1; overflow-y:auto)
│   ▸ .kpi-row        2 列渐变 KPI 卡
│   ▸ .section-title  快捷入口
│   ▸ .card quick     van-grid 4 列
│   ▸ .section-title  近期订单
│   ▸ .card recent    van-cell × N
├─ .tabbar-wrap (sticky bottom:0, B1)
└─────────────────────────
```

## KPI 卡数据结构

```js
const kpiItems = ref([
  {
    label: '今日订单', value: '1,286', unit: '单',
    delta: 12.4, deltaLabel: '较昨日',
    gradient: 'var(--gradient-primary)',
  },
  {
    label: '今日金额', value: '¥ 58,420', unit: '',
    delta: 8.6, deltaLabel: '较昨日',
    gradient: 'var(--gradient-warning)',
  },
]);
```

| 字段 | 作用 |
|---|---|
| `label` | 卡片标签 |
| `value` | 主数值（loading 时显示 `—`） |
| `unit` | 灰色后缀 |
| `delta` | 环比百分比（≥0 涨；<0 跌） |
| `deltaLabel` | 环比文字（较昨日/同比上月） |
| `gradient` | 渐变 CSS 变量 |

## 快捷入口

```js
const quickEntries = ref([
  { name: 'order-new',  label: '新建订单', icon: 'add-o' },
  { name: 'order-list', label: '订单列表', icon: 'orders-o' },
  { name: 'goods',      label: '商品管理', icon: 'goods-collect-o' },
  { name: 'stats',      label: '数据看板', icon: 'chart-trending-o' },
]);
```

## 近期活动

```js
const recentList = ref([
  { id, title, subtitle, amount, amountColor?, thumbText, thumbClass },
]);
```

`thumbClass` 配色：
- `''`（默认）→ 蓝渐变
- `'alt'` → 橙渐变
- `'success'` → 绿渐变
- `'danger'` → 红渐变

## 跳转关系（ROUTES 集中配置）

```js
const ROUTES = {
  list:   'mobile-list',     // 订单列表
  form:   'mobile-form',     // 新建订单
  detail: 'mobile-detail',   // 订单详情
  home:   'mobile-list',     // tab: 首页
  me:     'mobile-list',     // tab: 我的
};
```

`onQuick` 按 `name` 分发到 ROUTES：
- `order-new` → form
- `order-list` → list
- 其他 → toast 提示

## Bug D 修复

CSS 缩略图占位（替代外网图）：

```css
.thumb-placeholder { background: var(--gradient-primary); }
.thumb-placeholder.alt     { background: var(--gradient-warning); }
.thumb-placeholder.success { background: var(--gradient-success); }
.thumb-placeholder.danger  { background: var(--gradient-danger); }
```

完全离线，零外网请求（playwright 测试强制校验）。

## 4 态约定

| 状态 | UI 表现 |
|---|---|
| loading | KPI 卡 value 显示 `—` + spinner 不显示 |
| error | 整页 `van-empty image="error"` + 重新加载按钮 |
| empty（recentList） | 「暂无近期订单」empty |
| success | 完整渲染 |

## 使用方式

```bash
python scripts/add_page.py . \
  --id order-overview --title "订单概览" --template mobile-dashboard
```

## PM 改模板最小动作清单

1. 改 `pageTitle`
2. 填 `ROUTES`
3. 改 `kpiItems` / `quickEntries` / `recentList` / `tabbarItems`
4. 改 `onQuick` 分发逻辑（按 name 路由）

> ⚠️ **不要用 `<van-foo ... />` 自闭合写法**！
>
> ⚠️ **不要引外网图片**（file:// 必须完全离线）。
