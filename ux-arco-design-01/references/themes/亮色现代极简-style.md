# 亮色现代极简 · 视觉规范

## 风格快照 / Style Snapshot
- **整体风格 / Overall style**：浅灰白画布（页底 `#F9FAFB` / 渐变近白）、近黑主按钮 `#000000`、锌灰辅文与发丝描边；标题 **Manrope**、正文 **Inter**。圆角中柔（`0.65rem`～`16px`），卡片靠三层弱投影浮起。完整反馈：字段 `.is-error` 红环 + `.field-error`、清空钮、提交行、顶中 Toast、静音提示条，以及 **`16px` 圆角、不透明、柔影**弹窗。
- **语气关键词 / Tone keywords**：冷静、留白充足、低彩度、清晰层级、轻浮起、无装饰噪音。
- **适配产品类型 / Suitable product types**：现代 SaaS 落地页、设置页、空状态引导、定价表、表单与组件展示、B2B 产品站。

> 来源：本地预览页 `亮色现代极简-preview.html`。备份 DNA 已按当前预览补全弹窗 / 表单 / 提示规则。

## 设计 Tokens / Design Tokens
### 颜色 / Colors

**浅色（默认）**
- `color.brand.primary` → `#000000`
- `color.brand.hover` → `#27272A`
- `color.brand.on_primary` → `#FFFFFF`
- `color.text.primary` → `#101112`；`strong` → `#18181B`
- `color.text.secondary` → `#71717A`
- `color.surface.page` → `#F9FAFB`
- `color.surface.card` → `#FFFFFF`
- `color.surface.muted` → `#F4F4F5`
- `color.border.subtle` → `rgba(0, 0, 0, 0.06)`
- `color.border.default` → `#E4E4E7`
- `color.border.form` → `#D4D4D8`
- `color.focus.ring` → `#A1A1AA`
- `color.semantic.danger` → `#C84F3D`（字段错误环；可与 `#EF4444` 互换）
- `color.overlay.scrim` → `rgba(15, 23, 42, 0.55)` + `blur(12px)`

**氛围（预览装饰，勿作第二品牌色）**
- 页底：`linear-gradient(180deg, #FFFFFF 0%, #FAFAFA 100%)`
- 极淡径向洗色：靛/紫/玫红低透明度椭圆（仅氛围）
- 点阵：`18px` 网格点 `rgba(0,0,0,0.06)`，透明度约 `0.42`

**深色反相（可选）**
- 页近黑、卡深锌、主钮改为白底黑字；圆角与间距体系不变；scrim `rgba(0,0,0,0.62)`

### 字体 / Typography
- `font.family.heading` → **Manrope**（`600–800`），回退 Inter
- `font.family.body` → **Inter** + PingFang / 微软雅黑
- `font.size.body` → `14–16px`，`line-height: 1.6`，`letter-spacing: -0.015em`
- `font.size.label` → `14px` / `600`
- `font.size.field-error` → `12px` / `500`
- `font.size.dialog.title` → `16px` / `700`（用 Inter/Manrope UI，勿用展示级超大字抢戏）
- `motion.ease` → `cubic-bezier(0.16, 1, 0.3, 1)`

### 背景 / Backgrounds
- 页面浅灰/近白渐变 + 极淡色晕与点阵；卡片纯白实心
- 弹窗面板不透明白；禁止面板玻璃半透明

### 阴影 / Shadows
- `shadow.card` → `0 0 0 1px rgba(0,0,0,0.03), 0 2px 4px rgba(0,0,0,0.05), 0 12px 24px rgba(0,0,0,0.05)`
- `shadow.button` → `0 20px 60px -30px rgba(0, 0, 0, 0.12)`
- Toast / 弹窗：`0 10px 28px rgba(15,23,42,0.12), 0 2px 8px …06`

### 边框 / Borders
- `1px`；默认 `#E4E4E7`；表单 `#D4D4D8`；分割 `rgba(0,0,0,0.06)`
- 聚焦：灰环 `#A1A1AA` 或 `2px` outline
- 错误：红边 + `3px`/`4px` 红透明环

### 圆角 / Radii
- `radius.sm` → `0.65rem`（~10px）——提示条、小控件
- `radius.md` → `0.85rem`——输入 / `--ix-radius`
- `radius.lg` → `1rem`
- `radius.xl` → **`16px`**——卡片 / 弹窗
- `radius.pill` → `9999px`

### 滚动条 / Scrollbar
- **Token**：`--scrollbar-size` `8px`；`--scrollbar-track` `transparent`；`--scrollbar-thumb` `rgba(0, 0, 0, 0.18)`；悬停 `rgba(0, 0, 0, 0.28)`；按下 `rgba(0, 0, 0, 0.36)`。
- **Firefox**：`scrollbar-width: thin`；`scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track)`。
- **WebKit**：`*::-webkit-scrollbar` 宽/高 `8px`；滑块圆角 `999px`，`border: 2px solid transparent`，`background-clip: padding-box`；轨道透明；转角透明。
- **状态**：默认 thumb → 悬停 `--scrollbar-thumb-hover` → 按下 `--scrollbar-thumb-active`。
- **暗色覆盖**：thumb `rgba(255, 255, 255, 0.14)`；悬停 `rgba(255, 255, 255, 0.26)`；按下 `rgba(255, 255, 255, 0.34)`。


### 按钮 / Buttons
- **基础 `.btn`**：高 `2.8rem`，`padding` `0 1.25rem`，圆角 `var(--radius-pill)`，边框 `1px solid transparent`，字号 `14px`，字重 `600`，过渡 `background-color 0.2s var(--ease), border-color 0.2s var(--ease), box-shadow 0.2s var(--ease), transform 0.2s var(--ease)`。
- **尺寸 / 形态**：`.btn-sm` 高 `2.5rem` / `0 14px` / `12px`；`.btn-lg` 高 `3rem` / `0 1.5rem` / `15px`；`.btn-pill` 圆角 `var(--radius-pill)`。
- **主按钮 `.btn-primary`**：背景 `--brand-primary` → `#000000`，文字 `--brand-on-primary` → `#ffffff`，边色 `--brand-primary` → `#000000`，投影 `--shadow-button` → `0 20px 60px -30px rgba(0, 0, 0, 0.12)`。
- **主按钮悬停**：背景 `--brand-primary-hover` → `#27272a`，边色 `--brand-primary-hover` → `#27272a`，投影 `0 20px 50px -28px rgba(0, 0, 0, 0.18)`，位移 `translateY(-1px)`。
- **主按钮按下**：`translateY(1px)`。
- **次按钮 `.btn-secondary`**：背景 `--surface-muted` → `#f4f4f5`，边色 `--border-default` → `#e4e4e7`，文字 `--text-strong` → `#18181b`。
- **次按钮悬停**：背景 `#ffffff`，边色 `--brand-primary` → `#000000`，文字 `--brand-primary` → `#000000`，位移 `translateY(-1px)`，投影 `0 8px 20px rgba(0, 0, 0, 0.06)`。
- **描边 `.btn-outline`**：透明底，边色 `--border-form` → `#d4d4d8`，文字 `--text-strong` → `#18181b`。
- **描边悬停**：背景 `rgba(0, 0, 0, 0.03)`，边色 `#a1a1aa`，文字 `--text-strong` → `#18181b`，位移 `translateY(-1px)`，投影 `0 8px 20px rgba(0, 0, 0, 0.05)`。
- **幽灵 `.btn-ghost`**：透明底，边框 `1px solid var(--border-default)`，文字 `--text-secondary` → `#71717a`，字重 `500`。
- **幽灵悬停**：强调色边/字 + 浅强调底；`transform` `none`，通常无抬升投影。
- **链接 `.btn-link`**：无边无底，色 `--brand-primary` → `#000000`，字号 `14px`，`gap` `6px`。
- **图标 `.btn-icon`**：`40px×40px`，圆角 `var(--radius-sm)`；悬停浅强调填充。
- **禁用 `.btn-disabled`**：`not-allowed`。
- **交互通则**：主钮悬停微抬并强化投影；次/描边悬停强调色浅染；幽灵悬停不抬升；按下 `translateY(1px)`。


### 表单与反馈 / Forms & Feedback
- **标签**：`14px` / `600`，下距约 `6～10px`
- **标签体系**：中性 = 静音底 + 细边 + 次文灰；强调 `.chip-accent` = 近黑实底白字；信息 `.chip-marked` = 浅底、边 `--border-default`、次文色；选项组统一信息色系，选中 = 近黑 `--text-strong` 实底白字 + 中性柔影
- **输入**：圆角 **`0.85rem`（md）**，白底 + `#D4D4D8` 边；占位次文灰
- **悬停**：边略加深；**聚焦**：灰环 `#A1A1AA` / 近黑描边
- **错误**：`.is-error` 红边 + `3px`/`4px` 红透明环；`.field-error` 短句，`role="alert"`
- **清空**：圆钮 `28px`，有值且聚焦/悬停出现
- **提交行**：上距 `20px`，`gap 12`，钮 `min-width 120px`
- **提示条 `.alert`**：圆角 `sm`，静音底 `#F4F4F5` 或浅边；强提示可用近黑实底白字
- **Toast**：顶中、圆角 md、白底双层柔影，`220ms` 显隐

### 弹窗 / Dialog
- **遮罩**：半透明 + `blur(12px)`；打开锁滚动
- **面板**：宽 `440px`（内容型 `560px`），圆角 **`16px`**，不透明白，柔影；禁止玻璃面板
- **结构**：顶栏（muted 底 + 标题 + 关闭）/ 正文 / 脚部右对齐；头脚 `1px` 分割
- **关闭**：`28×28`、圆角 sm；悬停浅墨底
- **消息型**：左圆图标——警告/信息语义色，带柔影
- **内容型**：内嵌面圆角 md、列表、芯片、表单
- **动效**：遮罩 `200ms`；面板 `translateY(10px) scale(0.98)` → 归位 `220ms`

### 布局 / Layout
- 容器约 `1120–1200px`，水平 `16–24px`
- 区块间距 `24–48px`；卡片内边距 `16–24px`；8pt 节奏
- 首屏单焦点：品牌/标题/一句说明/CTA，勿堆 KPI
- 弹窗演示双列；`≤900px` 单列

## 风格原则 / Style Principles
1. **近黑即品牌**：主交互回到黑/锌灰，不引入第二高饱和主色。
2. **灰白分层**：页浅灰、卡纯白、静音 `#F4F4F5`，用表面差建层级。
3. **投影代替厚边**：卡片三层弱影浮起，边框发丝级。
4. **双字体分工**：Manrope 标题，Inter 正文与表单。
5. **圆角中柔**：约 10–16px，弹窗跟 `16px`，忌超大气泡圆角。
6. **动效平滑不花**：统一 expo 缓动，禁弹跳与霓虹。
7. **留白即气质**：区块要有呼吸，勿塞统计条与徽章墙。
8. **表单克制反馈**：错误用红环短句，提示条用静音面。
9. **弹窗同构**：`16px`、不透明、柔影；遮罩可模糊。
10. **氛围色不可品牌化**：页底淡靛/紫晕仅装饰，CTA 仍近黑。

## 提示词包
### 基础提示词

**审美方向**  
生成亮色现代极简界面：浅灰页底 `#F9FAFB`、白卡、近黑主按钮。标题 Manrope，正文 Inter。冷静留白、低彩度。含表单（错误红环、清空、提交行）、静音提示条、顶中柔影 Toast，以及 `16px` 圆角不透明柔影弹窗。

**Token 约束**  
主色 `#000` / 悬停 `#27272A`；文 `#101112` / `#71717A`；面 `#F9FAFB` / `#FFF` / `#F4F4F5`；边 `#E4E4E7` / 表单 `#D4D4D8`；聚焦 `#A1A1AA`；圆角 `0.65rem`～`16px`；卡片三层弱影；缓动 `cubic-bezier(0.16,1,0.3,1)`。
- 滚动条：宽 `8px`，轨道透明，滑块 `rgba(0, 0, 0, 0.18)`（悬停/按下加深）；胶囊滑块 + Firefox `thin`。


**布局约束**  
容器约 `1200px`；首屏单焦点；弹窗 `440～560px` 脚钮右对齐。

**交互约束**  
主/次/描边/幽灵按钮态齐全：主钮悬停微抬并强化投影，次与描边用强调色浅染，幽灵不抬升；主钮按下 `translateY(1px)`；触控高度建议 ≥ `44px`（或沿用主题默认 `.btn` 高度）；聚焦环与品牌色协调。


**避免项**  
禁止紫靛蓝品牌主题、霓虹发光、大面积玻璃；禁止高饱和色块底；禁止主 CTA 做成幽灵描边；禁止首屏 KPI 墙；禁止丢掉 Manrope。

### 组件提示词
**主按钮 `.btn-primary`**：`--brand-primary` → `#000000` 底，`--brand-on-primary` → `#ffffff` 字，投影 `--shadow-button` → `0 20px 60px -30px rgba(0, 0, 0, 0.12)`；悬停微抬；按下 `translateY(1px)`。
**次按钮 `.btn-secondary`**：软面/细边；悬停强调色浅底与边，微抬。
**描边 `.btn-outline`**：透明底 + 主题边；悬停强调色浅染。
**幽灵 `.btn-ghost`**：透明底，`--text-secondary` → `#71717a` 字；悬停浅强调底，不抬升。
**尺寸族**：默认 / `.btn-sm` / `.btn-lg` / `.btn-pill`；另含 `.btn-link`、`.btn-icon`、`.btn-disabled`。

**卡片**：白底 + `shadow.card`，圆角 `16px`。  
**标签 / Chip**：静音底或细边；强调近黑实底；信息浅底细边；选项组选中近黑实底白字。  
**输入**：圆角 md、边 `#D4D4D8`；错误红环；圆清空。  
**提示条 / Toast**：sm/md 圆角，柔影 Toast 顶中。  
**弹窗**：`16px`、不透明、柔影；脚部黑主钮。


### 变体提示词

- **更亮**：页趋近纯白，主黑不变。  
- **更密**：内边距降一档，正文 ≥`13px`。  
- **更暖**：仅米白微调表面，禁止棕色主色。  
- **深色反相**：近黑页、白主钮；圆角体系不变。  
- **表单确认流**：校验表单 + `16px` 确认弹窗。

## 复用说明
- **必须保持不变**：近黑主色、灰白分层、Manrope+Inter、弱多层投影、中等圆角、字段红环、弹窗 `16px` 不透明柔影。
- **可弹性调整**：文案、栏数、是否胶囊钮、容器最大宽。
- **风格跑偏风险**：第二品牌色、彩色光晕影、过大圆角、首屏指标墙。

---

## 质量评分 / Quality Score
- **总分**：91/100
- **结论**：通过（可直接用于 SaaS 落地与表单确认流）

## 分项得分 / Dimension Scores
- 风格一致性：19/20
- Token 可执行性：15/15
- 色彩与对比：14/15
- 排版层级：9/10
- 组件完整度：10/10
- 布局与间距：9/10
- 防跑偏约束：10/10
- 变体控制力：8/10

## 扣分说明 / Deductions
- 预览页底含淡彩径向，需在落地时标明「非品牌色」。
- 深色反相变体未给完整 token 表。

## 关键风险 / Key Risks
- 生成器易把近黑 CTA 换成蓝紫渐变按钮。
- 易把弹窗圆角做成 `24px+` 软萌卡。
- 氛围靛紫晕被误当成主色延伸。

## 优先修订（三项）
1. 写死危险色为单一 hex（`#C84F3D` 或 `#EF4444`）。
2. 明确氛围径向「装饰 only」与品牌黑的边界。
3. 补充深色反相完整色板若产品需要暗模式。
