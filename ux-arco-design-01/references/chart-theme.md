# 图表主题规范（ECharts ↔ Arco 变量）

> Arco Vue 不含图表组件，vibepm 用 ECharts。图表必须读取 Arco 的 CSS 变量，否则暗黑模式会出现白底、黑字、亮网格。
> 本文给出可直接使用的主题工厂与硬规则。

---

## 一、变量读取（关键：两种格式）

Arco 的变量有两种形态，取值时必须归一化：

| 变量 | 形态 | 示例 |
|---|---|---|
| `--primary-6` 等语义色 | `R, G, B` 三元组 | `22, 93, 255` |
| `--color-text-1` 等 | 完整颜色 | `#1d2129` / `rgba(255,255,255,.9)` |

```ts
const readVar = (name: string, fallback: string) => {
  const v = getComputedStyle(document.body).getPropertyValue(name).trim();
  if (!v) return fallback;
  // R,G,B 三元组 → rgb()
  if (/^\d+\s*,\s*\d+\s*,\s*\d+$/.test(v)) return `rgb(${v})`;
  return v;
};
```

---

## 二、主题工厂

```ts
// chart/arco-theme.ts
import type { EChartsOption } from 'echarts';

export interface ArcoChartTheme {
  color: string[];
  textStyle: Record<string, unknown>;
  axis: Record<string, unknown>;
  tooltip: Record<string, unknown>;
  legend: Record<string, unknown>;
  grid: Record<string, unknown>;
}

const readVar = (name: string, fallback: string) => {
  const v = getComputedStyle(document.body).getPropertyValue(name).trim();
  if (!v) return fallback;
  if (/^\d+\s*,\s*\d+\s*,\s*\d+$/.test(v)) return `rgb(${v})`;
  return v;
};

export function createArcoChartTheme(): ArcoChartTheme {
  const primary = readVar('--primary-6', '#165DFF');
  const cyan = readVar('--cyan-6', '#14C9C9');
  const purple = readVar('--purple-6', '#722ED1');
  const gold = readVar('--gold-6', '#F7BA1E');
  const blue = readVar('--blue-6', '#3491FA');

  const text1 = readVar('--color-text-1', '#1d2129');
  const text2 = readVar('--color-text-2', '#4e5969');
  const text3 = readVar('--color-text-3', '#86909c');
  const border2 = readVar('--color-border-2', '#e5e6eb');
  const bg2 = readVar('--color-bg-2', '#fff');
  const bg5 = readVar('--color-bg-5', '#fff');

  return {
    // 分类色：主色打头，其余为低冲突辅助色；语义红绿不进入分类序列
    color: [primary, cyan, purple, gold, blue],
    // 字体族不是 CSS 变量（只存在于 Less），直接从 body 取
    textStyle: { color: text2, fontFamily: getComputedStyle(document.body).fontFamily },
    axis: {
      axisLine: { lineStyle: { color: border2 } },
      axisTick: { lineStyle: { color: border2 } },
      axisLabel: { color: text3, fontSize: 12 },
      splitLine: { lineStyle: { color: border2, type: 'dashed' } },
      nameTextStyle: { color: text3, fontSize: 12 },
    },
    tooltip: {
      backgroundColor: bg5,
      borderColor: border2,
      borderWidth: 1,
      textStyle: { color: text1, fontSize: 12 },
      extraCssText: 'box-shadow: 0 4px 16px rgba(0,0,0,.12); border-radius: 8px;',
    },
    legend: {
      textStyle: { color: text2, fontSize: 12 },
      icon: 'circle',
      itemWidth: 8,
      itemHeight: 8,
      itemGap: 16,
    },
    grid: { left: 16, right: 16, top: 40, bottom: 8, containLabel: true },
  };
}
```

### 应用到实例

```ts
import * as echarts from 'echarts';

const chart = echarts.init(el, undefined, { renderer: 'canvas' });
chart.setOption({
  color: theme.color,
  textStyle: theme.textStyle,
  tooltip: { ...theme.tooltip, trigger: 'axis' },
  legend: { ...theme.legend, top: 0, right: 0 },
  grid: theme.grid,
  xAxis: { type: 'category', ...theme.axis },
  yAxis: { type: 'value', ...theme.axis, axisLine: { show: false } },
  series: [{ type: 'line', smooth: true, areaStyle: { opacity: .08 } }],
});
```

### 暗黑切换后重绘

```ts
const observer = new MutationObserver(() => {
  chart.setOption(buildOption(createArcoChartTheme()), true); // notMerge
});
observer.observe(document.body, { attributes: true, attributeFilter: ['arco-theme'] });
```

> 不要 `dispose()` 后重建；用 `setOption(option, true)` 覆盖即可，避免动画闪断与内存泄漏。

---

## 三、配色规则

| 规则 | 说明 |
|---|---|
| 分类色 ≤ 6 | 超过 6 个系列先合并“其他”，不要靠加色区分 |
| 主色打头 | 第一个系列用 `--primary-6`，保证与界面主色一致 |
| 语义色专用 | 成功/警告/危险只用于状态语义，不进入普通分类序列 |
| 暗色不换色相 | 暗色下只调透明度与文字色，不改主色相，保持品牌一致 |
| 面积图透明 | `areaStyle.opacity ≤ .12`，否则暗色下过亮 |
| 网格线弱化 | `type: 'dashed'` + `--color-border-2`，不要用实线黑 |
| 单系列不用图例 | 只有一个系列时隐藏图例，减少噪音 |

---

## 四、图表结构硬规则

1. **卡片容器**：标题（14/600）+ 可选说明 + 右上角操作（时间范围/更多），图表区独立 `ResizeObserver` 自适应。
2. **轴与单位**：Y 轴单位写在轴名或首屏说明里（`万元` / `%`），不要每条数据带单位。
3. **数值格式**：千分位；百分比 1 位小数；金额与列表保持一致（见 components-guide「数据展示规范」）。
4. **空态**：`series.data` 全空时显示 `a-empty` 覆盖层，不显示空坐标轴。
5. **加载态**：切换筛选时给图表区 `v-loading`/骨架，避免旧数据停留。
6. **交互**：tooltip `trigger: 'axis'` + `axisPointer: { type: 'line' }`；点击联动时高亮同步，不做无意义的 3D/旋转。
7. **无障碍**：颜色之外提供图例与数值标签；不要仅用红/绿区分正负，配 `+/-` 号。
8. **性能**：> 2000 点开启 `sampling: 'lttb'`；实时数据用 `appendData` 或节流，禁止每秒全量 `setOption`。

---

## 五、图表类型选择

| 场景 | 类型 | 备注 |
|---|---|---|
| 趋势 | 折线 / 面积 | 面积仅单系列或强调总量 |
| 对比 | 柱状 / 分组柱 | 系列 ≤ 4，多了改横向条形 |
| 占比 | 环形 | 分类 ≤ 6，中心放总量 |
| 分布 | 直方图 / 箱线 | 不要用饼图表达分布 |
| 进度 | 进度条 / 仪表盘 | 仪表盘只用于单一达成率 |
| 相关 | 散点 | 需说明气泡大小含义 |
| 漏斗 | 漏斗 | 阶段 ≤ 6，标注转化率 |

---

## 六、自查

- [ ] 图表颜色来自 `--primary-*` / 主题色板，而非硬编码十六进制？
- [ ] 暗黑切换后坐标轴、网格、tooltip 都跟着变？
- [ ] 分类色 ≤ 6，语义色没有混进普通系列？
- [ ] 有标题、单位、空态、加载态？
- [ ] 金额/百分比格式与表格一致？
- [ ] 大数据量是否开启采样或虚拟化？
