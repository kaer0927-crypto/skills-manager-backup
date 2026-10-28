<!--
  大屏 / 多维分析骨架（1920×1080 等比缩放）

  设计依据：references/pages-guide.md「大屏 / 多维分析」
  取值来源：references/themes/暗紫色科技感-style.md（brand #6867F7 / 卡片薄雾渐变 / 弱白边）
  图表接入：内置与 assets/arco-echarts-theme.ts 同源的变量读取逻辑（本文件自包含，复制即用；
           若项目里已引入 arco-echarts-theme.ts，可删掉下方同源实现改为 import）

  硬规则：
  1. 只读，不放大屏内表单；下钻通过 adminBase 新开后台页。
  2. 动画只用于数据更新（≤600ms）与榜单轮播（可 hover 暂停）。
  3. 画布固定 1920×1080，外层 scale 等比缩放，1366×768 不出横向滚动条。
  4. 所有数据走 props，`demo*` 只是占位，接真实接口时整体替换。
-->
<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, shallowRef, watch } from 'vue';
import { Message } from '@arco-design/web-vue';
import * as echarts from 'echarts';

/* ---------- 与 arco-echarts-theme.ts 同源：读 Arco CSS 变量 ---------- */
interface ArcoChartTheme {
  color: string[];
  textStyle: Record<string, unknown>;
  axis: Record<string, unknown>;
  tooltip: Record<string, unknown>;
  legend: Record<string, unknown>;
  grid: Record<string, unknown>;
}

function readArcoVar(name: string, fallback: string): string {
  const raw = getComputedStyle(document.body).getPropertyValue(name).trim();
  if (!raw) return fallback;
  return /^\d+\s*,\s*\d+\s*,\s*\d+$/.test(raw) ? `rgb(${raw})` : raw;
}

function createArcoChartTheme(): ArcoChartTheme {
  const text2 = readArcoVar('--color-text-2', '#4e5969');
  const text3 = readArcoVar('--color-text-3', '#86909c');
  const border2 = readArcoVar('--color-border-2', '#e5e6eb');
  return {
    color: [
      readArcoVar('--primary-6', '#165DFF'),
      readArcoVar('--cyan-6', '#14C9C9'),
      readArcoVar('--purple-6', '#722ED1'),
      readArcoVar('--gold-6', '#F7BA1E'),
      readArcoVar('--blue-6', '#3491FA'),
    ],
    textStyle: { color: text2, fontFamily: getComputedStyle(document.body).fontFamily },
    axis: {
      axisLine: { lineStyle: { color: border2 } },
      axisTick: { lineStyle: { color: border2 } },
      axisLabel: { color: text3, fontSize: 11 },
      splitLine: { lineStyle: { color: border2, type: 'dashed' } },
      nameTextStyle: { color: text3, fontSize: 11 },
    },
    tooltip: {
      backgroundColor: readArcoVar('--color-bg-5', '#fff'),
      borderColor: border2,
      borderWidth: 1,
      textStyle: { color: readArcoVar('--color-text-1', '#1d2129'), fontSize: 12 },
      extraCssText: 'box-shadow: 0 4px 16px rgba(0,0,0,.28); border-radius: 8px;',
    },
    legend: {
      textStyle: { color: text2, fontSize: 11 },
      icon: 'circle',
      itemWidth: 8,
      itemHeight: 8,
      itemGap: 14,
    },
    grid: { left: 16, right: 16, top: 40, bottom: 8, containLabel: true },
  };
}

function watchArcoTheme(chart: echarts.ECharts, rebuild: () => void): () => void {
  const observer = new MutationObserver(rebuild);
  observer.observe(document.body, { attributes: true, attributeFilter: ['arco-theme'] });
  return () => observer.disconnect();
}

export interface KpiItem {
  key: string;
  label: string;
  value: string;
  unit?: string;
  delta?: number;
  hint?: string;
  spark?: number[];
  /** 指标的“变好”方向：默认上升为好；响应时长/告警数等下降为好 */
  good?: 'up' | 'down';
}

export interface EventItem {
  time: string;
  system: string;
  content: string;
  level: 'info' | 'warning' | 'error';
}

export interface HealthItem {
  name: string;
  value: number;
  status: 'ok' | 'warning' | 'error';
}

const props = withDefaults(
  defineProps<{
    title?: string;
    subtitle?: string;
    kpis?: KpiItem[];
    trend?: { hours: string[]; inbound: number[]; outbound: number[] };
    categories?: { name: string; value: number }[];
    regions?: { name: string; value: number }[];
    events?: EventItem[];
    health?: HealthItem[];
    adminBase?: string;
    rotateInterval?: number;
  }>(),
  {
    title: '智慧运营数据驾驶舱',
    subtitle: '全域业务实时监控 · 数据每 5 分钟刷新',
    adminBase: '',
    rotateInterval: 4000,
  },
);

/* ---------- demo 占位数据（接入真实接口时整体替换） ---------- */
const demoTrend = {
  hours: ['00', '02', '04', '06', '08', '10', '12', '14', '16', '18', '20', '22'],
  inbound: [320, 268, 210, 386, 742, 1180, 1320, 1246, 1108, 986, 812, 534],
  outbound: [286, 240, 188, 342, 660, 1024, 1188, 1092, 968, 872, 706, 468],
};

const demoKpis: KpiItem[] = [
  { key: 'flow', label: '今日处理量', value: '128,460', unit: '件', delta: 12.4, spark: [38, 42, 40, 48, 52, 49, 58, 61] },
  { key: 'online', label: '在线终端', value: '8,726', unit: '台', delta: 3.1, spark: [60, 62, 61, 64, 66, 65, 68, 70] },
  { key: 'latency', label: '平均响应', value: '186', unit: 'ms', delta: -8.6, good: 'down', spark: [72, 68, 70, 64, 61, 58, 55, 52] },
  { key: 'rate', label: '任务达成率', value: '96.8', unit: '%', delta: 1.7, spark: [80, 82, 81, 85, 86, 88, 90, 92] },
  { key: 'alarm', label: '待处理告警', value: '23', unit: '条', delta: -4.2, good: 'down', spark: [48, 44, 46, 40, 38, 34, 30, 27] },
];

const demoEvents: EventItem[] = [
  { time: '14:32:08', system: '订单中心', content: '批量导入任务 #A2318 完成，成功 1,204 条', level: 'info' },
  { time: '14:31:52', system: '支付网关', content: '渠道响应超时率 1.8%，已自动切换备用通道', level: 'warning' },
  { time: '14:30:41', system: '用户中心', content: '实名认证队列积压回落至 120 条', level: 'info' },
  { time: '14:29:16', system: '风控引擎', content: '规则 R-107 命中 3 次，已进入人工复核', level: 'warning' },
  { time: '14:27:33', system: '数据同步', content: '主从延迟 320ms，超过阈值 200ms', level: 'error' },
  { time: '14:26:02', system: '消息服务', content: '短信通道切换完成，送达率恢复至 99.2%', level: 'info' },
  { time: '14:24:47', system: '报表服务', content: '日报生成任务已排入队列，预计 6 分钟', level: 'info' },
  { time: '14:23:19', system: '权限中心', content: '角色变更审批通过，影响 12 个账号', level: 'warning' },
];

const demoCategories = [
  { name: '在线办理', value: 486 },
  { name: '自助终端', value: 312 },
  { name: '人工窗口', value: 208 },
  { name: '移动端', value: 164 },
];

const demoRegions = [
  { name: '城东片区', value: 986 },
  { name: '城南片区', value: 842 },
  { name: '中心城区', value: 768 },
  { name: '城北片区', value: 604 },
  { name: '城西片区', value: 512 },
];

const demoHealth: HealthItem[] = [
  { name: '统一认证', value: 99.98, status: 'ok' },
  { name: '文件服务', value: 99.72, status: 'ok' },
  { name: '数据同步', value: 97.4, status: 'warning' },
  { name: '短信通道', value: 92.1, status: 'error' },
];

const kpis = computed(() => props.kpis ?? demoKpis);
const trend = computed(() => props.trend ?? demoTrend);
const events = computed(() => props.events ?? demoEvents);
const categories = computed(() => props.categories ?? demoCategories);
const regions = computed(() => props.regions ?? demoRegions);
const health = computed(() => props.health ?? demoHealth);

/* ---------- 时钟 ---------- */
const now = ref(new Date());
let clockTimer: number | undefined;

const clockText = computed(() => {
  const d = now.value;
  const p = (n: number) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}`;
});

const weekday = computed(
  () => ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][now.value.getDay()],
);

/* ---------- 1920×1080 等比缩放 ---------- */
const stageRef = ref<HTMLElement>();
const scale = ref(1);

function fitStage() {
  const w = window.innerWidth;
  const h = window.innerHeight;
  scale.value = Math.min(w / 1920, h / 1080);
  stageRef.value?.style.setProperty('--bs-scale', String(scale.value));
  charts.forEach((c) => c?.resize());
}

/* ---------- 图表 ---------- */
const trendEl = ref<HTMLElement>();
const categoryEl = ref<HTMLElement>();
const regionEl = ref<HTMLElement>();
const charts: (echarts.ECharts | undefined)[] = [];
let stopTheme: (() => void) | undefined;

function trendOption() {
  const theme = createArcoChartTheme();
  return {
    color: [theme.color[0], theme.color[1]],
    textStyle: theme.textStyle,
    tooltip: { ...theme.tooltip, trigger: 'axis' },
    legend: { ...theme.legend, top: 0, right: 0 },
    grid: { ...theme.grid, top: 44, left: 12, right: 16, bottom: 4 },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: trend.value.hours.map((h) => `${h}:00`),
      ...theme.axis,
    },
    yAxis: { type: 'value', ...theme.axis, axisLine: { show: false } },
    series: [
      {
        name: '受理量',
        type: 'line',
        smooth: true,
        showSymbol: false,
        lineStyle: { width: 2 },
        areaStyle: { opacity: 0.1 },
        data: trend.value.inbound,
      },
      {
        name: '办结量',
        type: 'line',
        smooth: true,
        showSymbol: false,
        lineStyle: { width: 2 },
        data: trend.value.outbound,
      },
    ],
  };
}

function categoryOption() {
  const theme = createArcoChartTheme();
  return {
    color: theme.color,
    textStyle: theme.textStyle,
    tooltip: { ...theme.tooltip, trigger: 'item' },
    legend: {
      ...theme.legend,
      orient: 'vertical',
      right: 8,
      top: 'center',
    },
    series: [
      {
        type: 'pie',
        radius: ['52%', '76%'],
        center: ['32%', '50%'],
        avoidLabelOverlap: true,
        itemStyle: { borderWidth: 2, borderColor: 'transparent' },
        label: { show: false },
        data: categories.value,
      },
    ],
  };
}

function regionOption() {
  const theme = createArcoChartTheme();
  return {
    color: [theme.color[0]],
    textStyle: theme.textStyle,
    tooltip: { ...theme.tooltip, trigger: 'axis' },
    grid: { left: 8, right: 20, top: 8, bottom: 0, containLabel: true },
    xAxis: { type: 'value', ...theme.axis, axisLine: { show: false }, splitLine: { show: false } },
    yAxis: {
      type: 'category',
      inverse: true,
      data: regions.value.map((r) => r.name),
      ...theme.axis,
      splitLine: { show: false },
    },
    series: [
      {
        type: 'bar',
        barWidth: 10,
        itemStyle: { borderRadius: 5 },
        label: { show: true, position: 'right', color: theme.textStyle.color as string, fontSize: 11 },
        data: regions.value.map((r) => r.value),
      },
    ],
  };
}

function renderCharts() {
  charts[0]?.setOption(trendOption(), true);
  charts[1]?.setOption(categoryOption(), true);
  charts[2]?.setOption(regionOption(), true);
}

/* ---------- 榜单轮播（hover 暂停） ---------- */
const rotateOffset = ref(0);
const paused = ref(false);
let rotateTimer: number | undefined;

const visibleEvents = computed(() => {
  const list = events.value;
  if (!list.length) return [];
  const n = Math.min(8, list.length);
  return Array.from({ length: n }, (_, i) => list[(i + rotateOffset.value) % list.length]);
});

function startRotate() {
  if (events.value.length <= 8) return;
  rotateTimer = window.setInterval(() => {
    if (!paused.value) rotateOffset.value = (rotateOffset.value + 1) % events.value.length;
  }, props.rotateInterval);
}

/* ---------- 下钻 ---------- */
function drill(label: string) {
  if (props.adminBase) {
    window.open(`${props.adminBase}?focus=${encodeURIComponent(label)}`, '_blank', 'noopener');
    return;
  }
  Message.info({ content: `下钻：${label}（配置 adminBase 后新开后台页）`, position: 'top' });
}

function deltaTone(k: KpiItem) {
  const positive = (k.delta ?? 0) >= 0;
  const wantUp = (k.good ?? 'up') === 'up';
  return positive === wantUp ? 'is-good' : 'is-bad';
}

function levelText(level: EventItem['level']) {
  return { info: '正常', warning: '关注', error: '异常' }[level];
}

const levelColor = (level: EventItem['level']) =>
  ({ info: 'arcoblue', warning: 'orange', error: 'red' } as const)[level];

/* ---------- sparkline ---------- */
function spark(values: number[], w = 96, h = 28) {
  const max = Math.max(...values);
  const min = Math.min(...values);
  const span = max - min || 1;
  return values
    .map((v, i) => {
      const x = (i / (values.length - 1)) * w;
      const y = h - ((v - min) / span) * (h - 4) - 2;
      return `${i === 0 ? 'M' : 'L'}${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(' ');
}

onMounted(() => {
  clockTimer = window.setInterval(() => (now.value = new Date()), 1000);
  fitStage();
  window.addEventListener('resize', fitStage);

  if (trendEl.value && categoryEl.value && regionEl.value) {
    charts[0] = echarts.init(trendEl.value);
    charts[1] = echarts.init(categoryEl.value);
    charts[2] = echarts.init(regionEl.value);
    renderCharts();
    stopTheme = watchArcoTheme(charts[0]!, renderCharts);
  }
  startRotate();
});

onBeforeUnmount(() => {
  window.clearInterval(clockTimer);
  window.clearInterval(rotateTimer);
  window.removeEventListener('resize', fitStage);
  stopTheme?.();
  charts.forEach((c) => c?.dispose());
});

watch([trend, categories, regions], renderCharts, { deep: true });
watch(() => events.value.length, startRotate);
</script>

<template>
  <div class="bs-viewport">
    <section ref="stageRef" class="bs-stage" aria-label="运营数据大屏">
      <!-- 顶部标题条 -->
      <header class="bs-header">
        <div class="bs-brand">
          <span class="bs-logo" aria-hidden="true">◈</span>
          <span class="bs-brand-name">智慧运营中心</span>
          <span class="bs-env">生产环境</span>
        </div>

        <div class="bs-title-wrap">
          <h1 class="bs-title">{{ title }}</h1>
          <p class="bs-subtitle">{{ subtitle }}</p>
        </div>

        <div class="bs-header-right">
          <div class="bs-clock">
            <span class="bs-clock-time">{{ clockText }}</span>
            <span class="bs-clock-week">{{ weekday }}</span>
          </div>
          <a-button type="text" class="bs-icon-btn" aria-label="刷新数据" @click="renderCharts">
            <template #icon><icon-refresh /></template>
          </a-button>
          <a-button v-if="adminBase" type="text" class="bs-link-btn" @click="drill('后台管理')">
            进入后台
          </a-button>
        </div>
      </header>

      <!-- KPI 指标带 -->
      <section class="bs-kpis" aria-label="核心指标">
        <article
          v-for="k in kpis"
          :key="k.key"
          class="bs-kpi"
          tabindex="0"
          role="button"
          @click="drill(k.label)"
          @keydown.enter="drill(k.label)"
        >
          <div class="bs-kpi-head">
            <span class="bs-kpi-label">{{ k.label }}</span>
            <span
              v-if="typeof k.delta === 'number'"
              class="bs-delta"
              :class="deltaTone(k)"
            >
              {{ k.delta >= 0 ? '▲' : '▼' }} {{ Math.abs(k.delta).toFixed(1) }}%
            </span>
          </div>
          <div class="bs-kpi-value">
            {{ k.value }}<span v-if="k.unit" class="bs-kpi-unit">{{ k.unit }}</span>
          </div>
          <svg v-if="k.spark" class="bs-spark" viewBox="0 0 96 28" preserveAspectRatio="none">
            <path :d="spark(k.spark)" fill="none" stroke="currentColor" stroke-width="1.6" />
          </svg>
        </article>
      </section>

      <!-- 主图区 -->
      <section class="bs-charts">
        <article class="bs-card bs-card-lg">
          <header class="bs-card-head">
            <h2>24 小时受理 / 办结趋势</h2>
            <span class="bs-card-hint">单位：件</span>
          </header>
          <div ref="trendEl" class="bs-chart bs-chart-lg"></div>
        </article>

        <div class="bs-side">
          <article class="bs-card">
            <header class="bs-card-head">
              <h2>业务渠道占比</h2>
            </header>
            <div ref="categoryEl" class="bs-chart bs-chart-sm"></div>
          </article>

          <article class="bs-card">
            <header class="bs-card-head">
              <h2>区域办理量 TOP5</h2>
            </header>
            <div ref="regionEl" class="bs-chart bs-chart-sm"></div>
          </article>
        </div>
      </section>

      <!-- 底部事件流 + 服务健康度 -->
      <section class="bs-bottom">
        <article
          class="bs-card bs-events"
          @mouseenter="paused = true"
          @mouseleave="paused = false"
        >
          <header class="bs-card-head">
            <h2>实时事件流</h2>
            <span class="bs-card-hint">悬停暂停轮播</span>
          </header>

          <div v-if="visibleEvents.length" class="bs-event-list">
            <div class="bs-event-row is-head">
              <span>时间</span><span>系统</span><span>事件内容</span><span>状态</span>
            </div>
            <TransitionGroup name="bs-row">
              <div v-for="e in visibleEvents" :key="e.time + e.content" class="bs-event-row">
                <span class="bs-mono">{{ e.time }}</span>
                <span class="bs-ellipsis">{{ e.system }}</span>
                <span class="bs-ellipsis bs-event-content">{{ e.content }}</span>
                <span class="bs-event-status">
                  <a-tag :color="levelColor(e.level)" size="small">{{ levelText(e.level) }}</a-tag>
                </span>
              </div>
            </TransitionGroup>
          </div>
          <a-empty v-else description="暂无事件" />
        </article>

        <article class="bs-card bs-health">
          <header class="bs-card-head">
            <h2>服务健康度</h2>
            <span class="bs-card-hint">近 5 分钟</span>
          </header>
          <ul class="bs-health-list">
            <li v-for="h in health" :key="h.name">
              <div class="bs-health-top">
                <span>{{ h.name }}</span>
                <span class="bs-mono" :class="`is-${h.status}`">{{ h.value.toFixed(2) }}%</span>
              </div>
              <div class="bs-bar">
                <i :class="`is-${h.status}`" :style="{ width: `${Math.max(0, Math.min(100, h.value))}%` }"></i>
              </div>
            </li>
          </ul>
        </article>
      </section>
    </section>
  </div>
</template>

<style scoped>
/* 深空底 + 薄雾卡片，取值见 themes/暗紫色科技感-style.md */
.bs-viewport {
  position: fixed;
  inset: 0;
  overflow: hidden;
  background: radial-gradient(120% 90% at 50% -10%, #1a1834 0%, #0e0d18 46%, #08070d 100%);
}

.bs-stage {
  --bs-scale: 1;
  --bs-brand: #6867f7;
  --bs-brand-soft: rgba(104, 103, 247, 0.14);
  --bs-text: #edecef;
  --bs-text-2: rgba(255, 255, 255, 0.6);
  --bs-text-3: rgba(255, 255, 255, 0.42);
  --bs-border: rgba(255, 255, 255, 0.06);
  --bs-border-strong: rgba(255, 255, 255, 0.12);
  --bs-card: linear-gradient(to bottom, rgba(255, 255, 255, 0.055), rgba(255, 255, 255, 0.018));
  --bs-shadow: 0 2px 20px rgba(0, 0, 0, 0.4), 0 0 40px rgba(0, 0, 0, 0.2);
  --bs-ease: cubic-bezier(0.16, 1, 0.3, 1);

  position: absolute;
  top: 0;
  left: 50%;
  width: 1920px;
  height: 1080px;
  padding: 20px 24px 24px;
  display: grid;
  grid-template-rows: 72px 132px 470px minmax(0, 1fr);
  gap: 16px;
  color: var(--bs-text);
  font-family: Inter, 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif;
  transform: translateX(-50%) scale(var(--bs-scale));
  transform-origin: top center;
  box-sizing: border-box;
}

.bs-stage *,
.bs-stage *::before,
.bs-stage *::after {
  box-sizing: border-box;
}

/* ---------- 顶部 ---------- */
.bs-header {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  padding: 0 20px;
  border: 1px solid var(--bs-border);
  border-radius: 16px;
  background: var(--bs-card);
}

.bs-brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.bs-logo {
  display: grid;
  place-items: center;
  width: 30px;
  height: 30px;
  border-radius: 10px;
  font-size: 15px;
  color: #fff;
  background: linear-gradient(140deg, #6867f7, #4b45c9);
  box-shadow: 0 8px 18px rgba(104, 103, 247, 0.32);
}

.bs-brand-name {
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.bs-env {
  padding: 1px 8px;
  border: 1px solid rgba(104, 103, 247, 0.34);
  border-radius: 999px;
  font-size: 11px;
  color: #b9b8ff;
}

.bs-title-wrap {
  text-align: center;
}

.bs-title {
  margin: 0;
  font-size: 26px;
  font-weight: 700;
  letter-spacing: 2px;
  background: linear-gradient(180deg, #ffffff 20%, #b9b7ff 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.bs-subtitle {
  margin: 2px 0 0;
  font-size: 12px;
  color: var(--bs-text-3);
  letter-spacing: 1px;
}

.bs-header-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
}

.bs-clock {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  margin-right: 6px;
  line-height: 1.25;
}

.bs-clock-time {
  font-size: 15px;
  font-variant-numeric: tabular-nums;
}

.bs-clock-week {
  font-size: 11px;
  color: var(--bs-text-3);
}

.bs-icon-btn,
.bs-link-btn {
  color: var(--bs-text-2) !important;
}

.bs-icon-btn:hover,
.bs-link-btn:hover {
  color: #b9b8ff !important;
  background: var(--bs-brand-soft) !important;
}

/* ---------- KPI ---------- */
.bs-kpis {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 16px;
}

.bs-kpi {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 6px;
  padding: 16px 20px;
  border: 1px solid var(--bs-border);
  border-radius: 16px;
  background: var(--bs-card);
  box-shadow: var(--bs-shadow);
  cursor: pointer;
  transition: border-color 0.32s var(--bs-ease), transform 0.32s var(--bs-ease);
}

.bs-kpi:hover,
.bs-kpi:focus-visible {
  border-color: rgba(104, 103, 247, 0.34);
  transform: translateY(-2px);
  outline: none;
}

.bs-kpi-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.bs-kpi-label {
  font-size: 13px;
  color: var(--bs-text-2);
}

.bs-delta {
  font-size: 12px;
  font-variant-numeric: tabular-nums;
}

.bs-delta.is-good {
  color: #86efac;
}

.bs-delta.is-bad {
  color: #fda4a4;
}

.bs-kpi-value {
  font-size: 34px;
  font-weight: 700;
  line-height: 1.05;
  font-variant-numeric: tabular-nums;
  letter-spacing: 0.5px;
}

.bs-kpi-unit {
  margin-left: 4px;
  font-size: 13px;
  font-weight: 500;
  color: var(--bs-text-3);
}

.bs-spark {
  position: absolute;
  right: 18px;
  bottom: 18px;
  width: 124px;
  height: 34px;
  color: rgba(134, 133, 255, 0.85);
  opacity: 0.9;
}

/* ---------- 卡片通用 ---------- */
.bs-card {
  position: relative;
  display: flex;
  flex-direction: column;
  min-height: 0;
  padding: 14px 18px 12px;
  border: 1px solid var(--bs-border);
  border-radius: 16px;
  background: var(--bs-card);
  box-shadow: var(--bs-shadow);
}

.bs-card-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
  padding-bottom: 8px;
}

.bs-card-head h2 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.4px;
}

.bs-card-head h2::before {
  content: '';
  display: inline-block;
  width: 3px;
  height: 12px;
  margin-right: 8px;
  border-radius: 2px;
  background: var(--bs-brand);
  vertical-align: -1px;
}

.bs-card-hint {
  font-size: 11px;
  color: var(--bs-text-3);
}

/* ---------- 图表区 ---------- */
.bs-charts {
  display: grid;
  grid-template-columns: 1.55fr 1fr;
  gap: 16px;
  min-height: 0;
}

.bs-side {
  display: grid;
  grid-template-rows: 1fr 1fr;
  gap: 16px;
  min-height: 0;
}

.bs-chart {
  flex: 1;
  min-height: 0;
}

.bs-chart-lg {
  min-height: 340px;
}

.bs-chart-sm {
  min-height: 130px;
}

/* ---------- 底部 ---------- */
.bs-bottom {
  display: grid;
  grid-template-columns: 1.9fr 1fr;
  gap: 16px;
  min-height: 0;
}

.bs-event-list {
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.bs-event-row {
  display: grid;
  grid-template-columns: 88px 120px minmax(0, 1fr) 84px;
  align-items: center;
  gap: 12px;
  height: 30px;
  padding: 0 4px;
  font-size: 12.5px;
  color: var(--bs-text-2);
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}

.bs-event-row.is-head {
  height: 26px;
  font-size: 11px;
  color: var(--bs-text-3);
  letter-spacing: 0.5px;
  border-bottom-color: var(--bs-border);
}

.bs-event-content {
  color: var(--bs-text);
}

.bs-event-status {
  justify-self: start;
}

.bs-mono {
  font-variant-numeric: tabular-nums;
  font-feature-settings: 'tnum';
  color: var(--bs-text-3);
}

.bs-ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.bs-row-enter-active,
.bs-row-leave-active,
.bs-row-move {
  transition: all 0.4s var(--bs-ease);
}

.bs-row-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.bs-row-leave-to {
  opacity: 0;
}

/* ---------- 健康度 ---------- */
.bs-health-list {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  gap: 10px;
  margin: 0;
  padding: 0;
  list-style: none;
  flex: 1;
}

.bs-health-top {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  font-size: 12.5px;
  color: var(--bs-text-2);
  margin-bottom: 6px;
}

.bs-bar {
  height: 6px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.06);
  overflow: hidden;
}

.bs-bar i {
  display: block;
  height: 100%;
  border-radius: 999px;
  transition: width 0.5s var(--bs-ease);
}

.bs-bar i.is-ok {
  background: linear-gradient(90deg, #4ade80, #86efac);
}

.bs-bar i.is-warning {
  background: linear-gradient(90deg, #f59e0b, #fbbf24);
}

.bs-bar i.is-error {
  background: linear-gradient(90deg, #ef4444, #fda4a4);
}

.bs-mono.is-ok {
  color: #86efac;
}

.bs-mono.is-warning {
  color: #fbbf24;
}

.bs-mono.is-error {
  color: #fda4a4;
}

/* Arco 组件在深底上的适配 */
.bs-stage :deep(.arco-empty-description) {
  color: var(--bs-text-3);
}

.bs-stage :deep(.arco-tag) {
  border-radius: 999px;
}

@media (prefers-reduced-motion: reduce) {
  .bs-row-enter-active,
  .bs-row-leave-active,
  .bs-row-move,
  .bs-kpi,
  .bs-bar i {
    transition: none;
  }
}
</style>
