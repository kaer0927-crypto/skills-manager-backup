# PC 仪表盘（v2 · KPI + 三图表 + Top10 排行榜 + 自适应重绘）

此页由 `pc/dashboard` 模板生成，作为 `pc` 端仪表盘示例展示。

## 模板能力一览

| 区域 | 实现要点 |
| --- | --- |
| 布局 | **整页自然滚动**（区别于 list / form / detail 的 100vh 固定框架）。图表多时向下浏览更自然，不做内部滚动区嵌套 |
| 页头 | 标题 + 数据更新时间 + 时间范围快捷切换（今日 / 近 7 天 / 近 30 天，静默切换不弹 toast）+ 自定义日期区间（与列表页日期范围组件一致）+ 刷新按钮 |
| KPI × 4 | 数值 + 单位 + **环比**（涨绿跌红，带 ▲▼ 箭头）+ 说明 Tooltip |
| 折线图 | 全宽，双 Y 轴（订单量 / 成交额），带渐变面积 |
| 柱状图 | 半宽，本期 vs 上期分组对比 |
| 饼图 | 半宽，环形，右侧竖排图例，鼠标悬浮显示占比 |
| 排行榜 | Top 10 `el-table`：前三名彩色名次徽标 + 进度条占比 + 环比着色，数量 / 金额列可排序 |
| 自适应 | 每个图表实例注册 **ResizeObserver + window.resize**，卸载时统一 `dispose()` 并 `disconnect()` |
| 中文文案 | 日期选择器、表格空态全中文，由 `assets/zh-cn-locale.js` 统一提供 |

## 布局实现

```
┌─ page-header    仪表盘  数据更新于 …    [今日|近7天|近30天] [日期区间] (刷新) ─┐
├─ kpi-grid       今日订单 │ 活跃用户 │ 转化率 │ 异常数        (4 列等宽)      ─┤
├─ chart-row.one  ▸ 趋势分析     折线图（全宽，340px 高）                      ─┤
├─ chart-row.two  ▸ 分布对比 │ ▸ 构成占比   柱状图 + 饼图（各半宽，300px 高）  ─┤
├─ rank-card      ▸ Top 10 排行榜   el-table（10 行）                          ─┤
└──────────────────────────── ↓ 页面整体向下滚动 ───────────────────────────────┘
```

- `#app { padding: 12px }`，**不设 `height:100vh`**，让内容自然撑高、整页滚动；
- 图表容器 `.chart-box` 必须给确定高度（300px / 340px）—— `echarts.init` 拿到 0 高度容器不会渲染；
- `onMounted` 里先 `await nextTick()` 再 init，确保 DOM 布局稳定后再取容器尺寸。

## 图表自适应重绘（关键实现）

viewer 支持拖拽改栏宽、收起左右栏，此时 **iframe 容器尺寸变了但 `window.resize` 不一定触发**。
只挂 `window.resize` 的话，图表会保持旧尺寸变形。所以每个实例双保险：

```js
const mountChart = (el, option) => {
  const inst = echarts.init(el);
  inst.setOption(option);
  let ro = null;
  if (typeof ResizeObserver !== 'undefined') {
    ro = new ResizeObserver(() => inst.resize());   // 容器级：拖栏宽也能感知
    ro.observe(el);
  }
  charts.push({ inst, ro });
};
window.addEventListener('resize', onWindowResize);  // 窗口级

onBeforeUnmount(() => {                              // 统一清理，避免内存泄漏
  window.removeEventListener('resize', onWindowResize);
  charts.forEach(({ inst, ro }) => { if (ro) ro.disconnect(); inst.dispose(); });
});
```

## 三个图表的配置要点

| 图表 | 类型 | 要点 |
| --- | --- | --- |
| 趋势分析 | `line` × 2 | 双 Y 轴（`yAxisIndex: 1` 挂第二轴）；订单量带 `LinearGradient` 渐变面积；**`grid.top: 64` + `nameGap: 20`** 让轴名与图例错开，否则右轴名「成交额」会和图例项叠在一起 |
| 分布对比 | `bar` × 2 | 本期实色 / 上期浅色，`barMaxWidth: 28` 防止分类少时柱子过粗 |
| 构成占比 | `pie` | `radius: ['45%','68%']` 环形；`center: ['38%','52%']` 给右侧竖排图例让位；`label: {show:false}` 靠 tooltip 显示 `{b}: {c} ({d}%)` |

所有配置集中在 `buildOptions()` 一个函数里返回 `{ trend, bar, pie }`，改图表类型 / 配色 / 轴只需动这一处。

## 数据与刷新

- `mockData` 集中存放三个图表与排行榜的数据源，替换为真实接口返回即可；
- 切换时间范围 / 自定义区间 → 调 `applyOptions()` 重新 `setOption(opt, true)`，**不销毁实例**（`true` 表示不合并，完全替换配置）；
- **静默刷新**：今日 / 近 7 天 / 近 30 天 / 自定义区间切换成功不弹 toast，只更新 `updatedAt` 时间戳；
- 点刷新按钮仍弹 `ElMessage.success('已刷新')`，给用户明确反馈；
- `updatedAt` 时间戳同步刷新，页头实时显示。

> ⚠️ `el-table-column` 必须用显式 `</el-table-column>` 闭合。Element Plus 2.8.8 + Vue 3.5
> 在自闭合写法下会把后续列错误地嵌套进前一列。

## 中文文案默认

所有用户可见的组件文案、表头、按钮均默认中文。日期选择器面板、表格空态由 `assets/zh-cn-locale.js` 提供的完整 zh-cn 语言包覆盖 —— `element-plus.full.min.js` 是**只打了英文**的构建，不配 locale 日期面板会显示 `Mon / Jan`。

## 使用方式

```bash
# 在已有项目里生成一个 pc-dashboard 风格的看板页
python scripts/add_page.py . \
  --id order-overview --title "订单概览" --template dashboard --parent pc-templates
```

PM 拿到后可基于此页修改：

- `<title>` 与 `pageTitle`：页面标题；
- `kpiItems`：4 个 KPI 卡片（`delta` 正负自动决定涨绿跌红）；
- `mockData`：三个图表 + 排行榜的数据源；
- `buildOptions()`：ECharts 配置（改图表类型 / 配色 / 轴在这里）；
- 想加图表：复制一个 `.chart-card` + `ref`，在 `onMounted` 里多调一次 `mountChart()` 即可，
  resize 与 dispose 会自动纳入统一管理。

> ⚠️ 不要在 `<div id="app">` 内部写 `{{XXX}}` 形式的占位符 —— 那是 Vue 的插值语法，会被当作表达式求值并抛 `XXX is not defined`（页面上表现为标题空白）。

可删除此示例页另建：`python scripts/remove_page.py . --id pc-dashboard`。
