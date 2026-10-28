# 大屏骨架 · visualization-screen.vue

`visualization-screen.vue` 是按 `references/pages-guide.md`「大屏 / 多维分析」做出来的可直接运行骨架，已在 1920×1080 与 1366×768 两档实测（等比缩放、无横向滚动条）。

## 依赖

- Vue 3.5+、`@arco-design/web-vue@2.59.x`、`echarts@5`
- 样式顺序（不能反）：

```ts
import '@arco-design/web-vue/dist/arco.css';
import '<skill>/assets/frame-presets.css';
import '<skill>/assets/frame-themes.css';
```

- 主题：大屏只允许暗色，挂载前设定，避免首屏闪白：

```ts
document.body.setAttribute('arco-theme', 'dark');
document.body.dataset.frameTheme = 'violet'; // 也支持 cyan-glow / graphite
```

## 用法

```vue
<script setup lang="ts">
import VisualizationScreen from '@/components/visualization-screen.vue';
import { useOverview } from '@/api/overview';

const { kpis, trend, categories, regions, events, health } = useOverview();
</script>

<template>
  <VisualizationScreen
    title="智慧运营数据驾驶舱"
    subtitle="全域业务实时监控 · 数据每 5 分钟刷新"
    :kpis="kpis"
    :trend="trend"
    :categories="categories"
    :regions="regions"
    :events="events"
    :health="health"
    admin-base="/admin"
  />
</template>
```

路由要独立于 Admin 壳（不要塞进有侧栏的 `layout`），因为它自带整屏定位与缩放。

## Props

| Prop | 类型 | 默认 | 说明 |
|---|---|---|---|
| `title` | `string` | `智慧运营数据驾驶舱` | 顶部主标题 |
| `subtitle` | `string` | 全域业务实时监控… | 标题下说明，建议写清刷新频率 |
| `kpis` | `KpiItem[]` | demo 5 项 | 指标卡，建议 4–6 个；超过 6 个会挤压数值 |
| `trend` | `{ hours, inbound, outbound }` | demo 24h | 主趋势图，两组序列 |
| `categories` | `{ name, value }[]` | demo 4 项 | 环形图，分类 ≤ 6 |
| `regions` | `{ name, value }[]` | demo 5 项 | 横向条形 TOP5，按值降序传入 |
| `events` | `EventItem[]` | demo 8 条 | 事件流，> 8 条自动轮播 |
| `health` | `HealthItem[]` | demo 4 项 | 服务健康度，`value` 为百分比 |
| `adminBase` | `string` | `''` | 下钻地址前缀；为空时点击只弹提示 |
| `rotateInterval` | `number` | `4000` | 事件流轮播间隔（ms） |

`KpiItem.good` 用来声明“哪个方向算好”：默认 `'up'`（上升为绿），响应时长、告警数这类指标传 `'down'`，否则会出现“响应变快反而标红”的语义错误。

## 已内置的规范

- 1920×1080 画布 + `transform: scale()` 等比缩放，`1366×768` 下自动缩到 0.71，不出现滚动条。
- 四段分区：标题条 72 / KPI 132 / 图表 470 / 底部自适应；间距统一 16。
- 图表配色读 Arco CSS 变量（`--primary-6`、`--color-text-*`、`--color-border-*`），`body[arco-theme]` 变化自动重绘。
- 事件流 `> 8` 条自动轮播，**hover 暂停**；卡片没有无限装饰动画。
- 下钻统一走 `adminBase` 新开后台页，大屏内不放表单。
- `prefers-reduced-motion` 下关闭过渡。

## 需要替换的部分

- 文件内 `demoKpis / demoTrend / demoEvents / demoCategories / demoRegions / demoHealth` 全是占位数据，接真实接口时**全部删掉或改为 props 默认值**，不要留着冒充真实数据。
- 品牌名「智慧运营中心」、生产环境标签、下钻路径按项目改。
- 若要接实时推送（WebSocket），只更新 props，不要每秒重建图表实例：`setOption(option, true)` 即可。
