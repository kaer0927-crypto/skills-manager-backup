# 绯雾轻写 · 视觉规范

﻿## 风格快照 / Style Snapshot
- **整体风格 / Overall style**：**绯雾轻写** — 亮白 / 暖浅灰纸面 + 单一绯雾红 `#e74c3c`；Inter 超黑英雄标题（关键词点绯）+ Plus Jakarta Sans 辅助；中圆角卡与胶囊筛选；主 CTA 柔绯光晕。完整反馈层：`.is-error` 红环 + `.field-error`、清空钮、提交行、顶部 Toast、绯雾浅底提示条，以及约 `16px` 圆角不透明弹窗（遮罩可 `blur`）。
- **语气关键词 / Tone keywords**：绯雾、轻纸、超黑 Inter、柔绯光晕、胶囊筛选、写作工具、克制反馈、不透明弹层。
- **适配产品类型 / Suitable product types**：写作 / 排版工具、内容创作落地页、侧栏工作台、含校验与确认的生产力 SaaS。

> 来源：本地预览页 `绯雾轻写-preview.html`。与「翠绿轻写 / 紫雾轻写」同构，仅品牌强调色不同。已按当前预览刷新弹窗 / 表单 / 提示。

## 设计 Tokens / Design Tokens
### 颜色 / Colors
- `color.brand.primary` → `#e74c3c`；`strong` → `#c0392b`；`muted` → `rgba(231,76,60,0.15)`
- `color.surface.page` → `#FFFFFF`；深色 `#0d0d0d`
- `color.surface.base` → `rgba(255,255,255,0.42)`；深色 `rgba(26,26,26,0.78)`
- `color.surface.soft` → `rgba(246,245,244,0.36)`；深色 `rgba(36,36,36,0.72)`
- `color.ink.primary` → `rgba(0,0,0,0.95)`；深色 `rgba(255,255,255,0.92)`
- `color.ink.body` → `#1a1a1a`；深色 `#e5e5e5`
- `color.ink.secondary` → `#615d59`；深色 `#b0aaa4`
- `color.ink.muted` → `#7a756f`；深色 `#6e6a65`
- `color.ink.on-primary` → `#FFFFFF`
- `color.line.default` → `rgba(0,0,0,0.10)`；深色 `rgba(255,255,255,0.10)`
- `color.semantic.danger` → `#ef4444`（字段错误；与品牌绯接近但语义独立）
- `color.semantic.success` → `#10b981`；`warning` → `#f5a623`
- `color.overlay.scrim` → `rgba(15,23,42,0.55)` + `blur(12px)`；深色 `rgba(0,0,0,0.62)`

### 字体 / Typography
- `font.family.display` → `"Plus Jakarta Sans", "Inter", system-ui, sans-serif`
- `font.family.sans` → `"Inter", "PingFang SC", "Microsoft YaHei", sans-serif`
- 英雄 `800`～`900` + 紧字距；关键词可用 `#e74c3c`
- 正文 `16px` / `1.5`；错误 `12px` / `500`；弹窗标题 `16px` / `700`

### 背景 / Backgrounds
- 页底白纸；可叠低 alpha 绯雾粒子，勿满屏红底
- 提示条：`rgba(231,76,60,0.15)`；强提示实底绯 + 白字
- 弹窗不透明面 + 顶栏弱表面；遮罩可模糊

### 阴影 / Shadows
- `shadow.card` → `0 4px 12px rgba(0,0,0,0.03), 0 14px 36px rgba(0,0,0,0.07)`
- `shadow.cta` → `0 0 20px 2px rgba(231,76,60,0.15)`；`shadow.button` → `0 10px 25px rgba(231,76,60,0.3)`
- `shadow.toast` / `shadow.dialog` → 双层中性柔影
- **禁止**：硬偏移贴纸影

### 边框 / Borders
- 浅黑透明边；选中 / 聚焦转绯雾；错误红环 `3px`/`4px`

### 圆角 / Radii
- `6 / 12 / 14 / 16`（控件 / CTA / 功能卡 / 卡与弹窗）；筛选约 `20`；`pill 999`；dock `40`

### 滚动条 / Scrollbar
- **Token**：`--scrollbar-size` `8px`；`--scrollbar-track` `transparent`；`--scrollbar-thumb` `rgba(0, 0, 0, 0.18)`；悬停 `rgba(0, 0, 0, 0.28)`；按下 `rgba(0, 0, 0, 0.36)`。
- **Firefox**：`scrollbar-width: thin`；`scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track)`。
- **WebKit**：`*::-webkit-scrollbar` 宽/高 `8px`；滑块圆角 `999px`，`border: 2px solid transparent`，`background-clip: padding-box`；轨道透明；转角透明。
- **状态**：默认 thumb → 悬停 `--scrollbar-thumb-hover` → 按下 `--scrollbar-thumb-active`。
- **暗色覆盖**：thumb `rgba(255, 255, 255, 0.14)`；悬停 `rgba(255, 255, 255, 0.26)`；按下 `rgba(255, 255, 255, 0.34)`。


### 按钮 / Buttons
- **基础 `.btn`**：高 `46px`，`padding` `0 22px`，圆角 `var(--radius-xl)`，边框 `1px solid transparent`，字号 `14px`，字重 `600`，过渡 `background-color .15s ease, border-color .15s ease, transform .15s ease`。
- **尺寸 / 形态**：`.btn-sm` 高 `36px` / `0 14px` / `12px`；主色小钮字号 `13px`、字重 `800`；`.btn-lg` 高 `52px` / `0 26px` / `15px`；`.btn-pill` 圆角 `var(--radius-pill)`。
- **主按钮 `.btn-primary`**：背景 `--brand-primary` → `#e74c3c`，文字 `--text-on-primary` → `#FFFFFF`，边色 `--brand-primary` → `#e74c3c`，字重 `600`，字号 `16px`，圆角 `--radius-lg` → `12px`，投影 `--shadow-cta` → `0 0 20px 2px rgba(231, 76, 60, 0.15)`。
- **主按钮悬停**：背景 `--brand-primary-strong` → `#c0392b`，边色 `--brand-primary-strong` → `#c0392b`，投影 强调色浅底（约 32% → #e74c3c），位移 `translateY(-1px)`。
- **主按钮按下**：`scale(0.95)`。
- **次按钮 `.btn-secondary`**：背景 `--brand-primary-muted` → `rgba(231, 76, 60, 0.15)`，边色 `transparent`，文字 `--brand-primary` → `#e74c3c`。
- **次按钮悬停**：强调色边/字 + 浅强调底（`color-mix` ≈18%）+ `translateY(-1px)` + 轻投影。
- **描边 `.btn-outline`**：透明底，边色 `--border-default` → `rgba(0, 0, 0, 0.10)`，文字 `--text-primary` → `rgba(0, 0, 0, 0.95)`。
- **描边悬停**：强调色边/字 + 浅强调底（`color-mix` ≈14%）+ `translateY(-1px)` + 轻投影。
- **幽灵 `.btn-ghost`**：透明底，边框 `1px solid var(--border-default)`，文字 `--text-secondary` → `#615d59`，字重 `500`。
- **幽灵悬停**：强调色边/字 + 浅强调底；`transform` `none`，通常无抬升投影。
- **链接 `.btn-link`**：无边无底，色 `--brand-primary` → `#e74c3c`，字号 `14px`，`gap` `6px`。
- **图标 `.btn-icon`**：`40px×40px`，圆角 `50%`；悬停浅强调填充。
- **禁用 `.btn-disabled`**：`not-allowed`，透明度 `0.65`。
- **交互通则**：主钮悬停微抬并强化投影；次/描边悬停强调色浅染；幽灵悬停不抬升；按下 `scale(0.95)`。


### 表单与反馈 / Forms & Feedback
- 输入圆角约 `6px`；聚焦绯边 / 浅绯环
- `.is-error` + `.field-error` 短文；清空钮 `20px`；提交行上距 `20px`
- **表单辅助图标（统一偏小、偏淡）**：下拉 `.combo-chevron` 约 `9px`；步进器按钮约 `22×22` / 图标 `10px`；清空 `.input-clear` 约 `20×20` / `11px`；均用 muted + 透明度约 `0.72`
- `.alert` 约 `6px` 圆角浅绯底；Toast 顶中 `220ms`

### 弹窗 / Dialog
- 遮罩半透明 + `blur(12px)`；面板宽 `440～560px`，圆角 **`16px`**，不透明
- 消息型：警告黄 / 信息绯圆图标；内容型可嵌表单
- 动效：遮罩 `200ms`，面板缩放归位 `220ms`

### 布局 / Layout
- 营销约 `1020～1100px`；编辑器满宽双栏；间距 `6～32` 八倍数节奏

## 风格原则 / Style Principles
1. **绯雾唯一品牌强调**：选中、关键词、主 CTA 回到 `#e74c3c`。
2. **亮纸优先**：绯不作大面积底；绯底必须白字。
3. **与语义红分工**：品牌绯管行动；字段错误用 `#ef4444` 环，避免整页「报警感」。
4. **Inter 超黑 + 中圆角** 为指纹。
5. **柔绯光晕克制**：仅 CTA / FAB。
6. **弹窗不透明 `16px`**；遮罩可模糊。
7. **深色只反转表面**，强调不变。
8. **反馈层级**：Alert → Toast → 模态。
9. **暖灰辅文**：`#615d59` / `#a39e98`。
10. **动效短促** `150～200ms`。

## 提示词包
### 基础提示词

**审美方向**  
生成「绯雾轻写」{页面类型}：亮白暖浅灰纸 + 单一绯雾 `#e74c3c`。Inter 超黑标题关键词点绯，主钮绯底白字 + 柔绯光晕。含表单错误环、清空、提交行、提示条、Toast、`16px` 不透明弹窗。气质：干净写作生产力——不是霓虹潮牌，也不是蓝紫科技壳。

**Token 约束**  
`#e74c3c` / `#c0392b` / `rgba(231,76,60,0.15)`；面白；主文近黑；次文 `#615d59`；圆角 `6/12/14/16/20`；弹窗不透明；错误环 `#ef4444`。
- 滚动条：宽 `8px`，轨道透明，滑块 `rgba(0, 0, 0, 0.18)`（悬停/按下加深）；胶囊滑块 + Firefox `thin`。


**布局约束**  
居中英雄 + 单 CTA；或双栏编辑器；弹窗脚钮右对齐。

**交互约束**  
主/次/描边/幽灵按钮态齐全：主钮悬停微抬并强化投影，次与描边用强调色浅染，幽灵不抬升；主钮按下 `scale(0.95)`；触控高度建议 ≥ `44px`（或沿用主题默认 `.btn` 高度）；聚焦环与品牌色协调。


**避免项**  
避免多强调并存、满屏红底、酸性暗黑、大玻璃壳、硬边刊风、弹窗毛玻璃、用大红底块替代字段错误环、把品牌绯与语义红混成一片报警 UI。

### 组件提示词
**主按钮 `.btn-primary`**：`--brand-primary` → `#e74c3c` 底，`--text-on-primary` → `#FFFFFF` 字，投影 `--shadow-cta` → `0 0 20px 2px rgba(231, 76, 60, 0.15)`；悬停微抬；按下 `scale(0.95)`。
**次按钮 `.btn-secondary`**：软面/细边；悬停强调色浅底与边，微抬。
**描边 `.btn-outline`**：透明底 + 主题边；悬停强调色浅染。
**幽灵 `.btn-ghost`**：透明底，`--text-secondary` → `#615d59` 字；悬停浅强调底，不抬升。
**尺寸族**：默认 / `.btn-sm` / `.btn-lg` / `.btn-pill`；另含 `.btn-link`、`.btn-icon`、`.btn-disabled`。

英雄点绯词；输入 `6px`；主 CTA 绯晕；提示条浅绯；Toast 顶中；弹窗 `16px` 不透明；筛选选中绯底白字。


### 变体提示词
更深色反相；更工具双栏；更营销粒子；表单确认流——圆角与单强调不变。

## 复用说明
- **必须保持不变**：亮纸 + 单绯雾、Inter 超黑、中圆角、柔绯 CTA、错误红环、弹窗不透明 `16px`、Toast 顶中。
- **可弹性调整**：粒子、编辑器默认、深色开关、容器宽。
- **风格跑偏风险**：滑向「全红报警」；换成绿 / 紫轻写主色却自称本皮；弹窗玻璃拟态。

---

## 质量评分 / Quality Score
- **总分**：88/100
- **结论**：通过（可直接用于同构轻写系生成）

## 分项得分 / Dimension Scores
- 风格一致性：18/20
- Token 可执行性：13/15
- 色彩与对比：13/15
- 排版层级：9/10
- 组件完整度：10/10
- 布局与间距：8/10
- 防跑偏约束：9/10
- 变体控制力：8/10

## 扣分说明 / Deductions
- 品牌绯与语义红接近，需在文案中强制分工。
- 与翠绿 / 紫雾同构，变体区分主要靠色相。

## 关键风险 / Key Risks
- 易把整页做成「错误态红色 UI」。
- 易忽略单强调约束引入第二品牌色。

## 优先修订（三项）
1. 写明品牌绯 ≠ 字段错误红的用法边界。
2. 弹窗固定不透明 + `16px`。
3. 禁止大面积绯雾铺底。
