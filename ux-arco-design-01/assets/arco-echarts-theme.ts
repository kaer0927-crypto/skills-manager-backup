/**
 * Arco Design Vue ↔ ECharts 主题桥接
 *
 * 用法：
 *   import { createArcoChartTheme, watchArcoTheme } from '@skill/assets/arco-echarts-theme';
 *   const chart = echarts.init(el);
 *   chart.setOption(buildOption(createArcoChartTheme()));
 *   watchArcoTheme(chart, () => buildOption(createArcoChartTheme()));
 *
 * 前提：文档以 @arco-design/web-vue/dist/arco.css 为基础样式，
 * 且已 import '<skill>/assets/frame-presets.css'（提供 --frame-* 与滚动条）。
 */

type EChartsLike = {
  setOption: (option: unknown, notMerge?: boolean) => void;
};

export interface ArcoChartTheme {
  color: string[];
  textStyle: Record<string, unknown>;
  axis: Record<string, unknown>;
  tooltip: Record<string, unknown>;
  legend: Record<string, unknown>;
  grid: Record<string, unknown>;
}

/** Arco 变量有两种形态：`R, G, B` 三元组 与完整颜色，取值时必须归一化。 */
export function readArcoVar(name: string, fallback: string): string {
  if (typeof window === 'undefined') return fallback;
  const raw = getComputedStyle(document.body).getPropertyValue(name).trim();
  if (!raw) return fallback;
  if (/^\d+\s*,\s*\d+\s*,\s*\d+$/.test(raw)) return `rgb(${raw})`;
  return raw;
}

export function createArcoChartTheme(): ArcoChartTheme {
  const primary = readArcoVar('--primary-6', '#165DFF');
  const cyan = readArcoVar('--cyan-6', '#14C9C9');
  const purple = readArcoVar('--purple-6', '#722ED1');
  const gold = readArcoVar('--gold-6', '#F7BA1E');
  const blue = readArcoVar('--blue-6', '#3491FA');

  const text1 = readArcoVar('--color-text-1', '#1d2129');
  const text2 = readArcoVar('--color-text-2', '#4e5969');
  const text3 = readArcoVar('--color-text-3', '#86909c');
  const border2 = readArcoVar('--color-border-2', '#e5e6eb');
  const bg5 = readArcoVar('--color-bg-5', '#ffffff');

  return {
    // 主色打头；语义红绿不进入普通分类序列
    color: [primary, cyan, purple, gold, blue],
    // 字体族只存在于 Less，不在 CSS 变量里，直接读 body
    textStyle: {
      color: text2,
      fontFamily: getComputedStyle(document.body).fontFamily,
    },
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

/**
 * 监听 `body[arco-theme]` 变化并重绘。
 * 用 setOption(option, true) 覆盖，不 dispose 重建（避免动画闪断与实例泄漏）。
 * @returns 取消监听函数
 */
export function watchArcoTheme(
  chart: EChartsLike,
  buildOption: () => unknown,
): () => void {
  if (typeof MutationObserver === 'undefined') return () => {};

  const observer = new MutationObserver(() => {
    chart.setOption(buildOption(), true);
  });

  observer.observe(document.body, {
    attributes: true,
    attributeFilter: ['arco-theme'],
  });

  return () => observer.disconnect();
}
