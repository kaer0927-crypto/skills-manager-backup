# 电光玻璃 · 视觉规范

## 风格快照 / Style Snapshot
- **整体风格 / Overall style**：**电光玻璃（Electric Glass）**。浅色画布 `#F2F4F6`，深色 `#050505`。酸性主强调 **`#D4FF00`**（上用近黑字 `#111`），次强调电光紫 `#A855F7` / 霓虹粉 `#FF9FF3`。大圆角：控件 `16px`、卡 `24px`、面板可至 `40px`、胶囊 `100px`。磨砂顶栏/面板 + 紫绿彩色柔影。展示 **Plus Jakarta Sans**，正文 **Inter**。完整反馈：大圆角输入、酸绿焦环、错误红环、清空、提交行、顶中彩影 Toast，以及 **`24px` 圆角、不透明或高不透玻璃面、彩色柔影**弹窗（遮罩可 blur；面板勿过度透明吞字）。
- **语气关键词 / Tone keywords**：快、环保、社交、潮流、酸性图形、玻璃拟态、Z 世代。
- **适配产品类型 / Suitable product types**：年轻向社交 App、环保打卡、潮流工具 H5、活动落地、游戏化轻应用。

> 来源：本地预览页 `电光玻璃-preview.html`。备份「电光玻璃」理念已按当前 `:root` / 深浅主题规范化为 Tokens，并补全弹窗 / 表单。

## 设计 Tokens / Design Tokens
### 颜色 / Colors

**浅色（默认）**
- `color.canvas` → `#F2F4F6`
- `color.surface` → `#FFFFFF`；`surface1` → `#EEF1F5`；`n-50` → `#F3F4F6`
- `color.border` → `#E5E7EB`
- `color.text.primary` → `#111111`；`secondary` → `#6B7280`；`tertiary` → `#9CA3AF`
- `color.brand.acid` → `#D4FF00`；悬停 `#C5F000`；深 `#B0E000`
- `color.on_accent` → `#111111`（酸绿上深字，禁止白字）
- `color.accent.ink` → `#4A5600`（浅底上酸绿字）
- `color.brand.purple` → `#A855F7`；悬停 `#9333EA`；soft `rgba(168,85,247,0.16)`
- `color.brand.pink` → `#FF9FF3`
- `color.semantic.danger` → `#EF4444`；`success` → `#22C55E`
- `color.glass.header` → `rgba(255,255,255,0.72)`；`glass.border` → `rgba(255,255,255,0.55)`
- `color.overlay.scrim` → `rgba(15, 23, 42, 0.55)` + `blur(12px)`

**深色**
- `color.canvas` → `#050505`；`surface` → `#111111`；`surface1` → `#1A1A1A`
- `color.text.primary` → `#FFFFFF`；`secondary` → `#9CA3AF`
- `color.border` → `rgba(255,255,255,0.12)`
- 酸绿仍 `#D4FF00`，悬停可 `#E5FF4D`；`on_accent` 仍近黑
- 影改为深黑柔影 + 酸绿 CTA 彩影；scrim `rgba(0,0,0,0.62)`

### 字体 / Typography
- `font.display` → **Plus Jakarta Sans**（`500–800`）
- `font.sans` → **Inter** + 中文回退
- `font.size.body` → `14–16px`；标题紧字距约 `-0.02em`，字重 `700/800`
- `font.size.label` → `14px` / `600～700`
- `font.size.field-error` → `12px` / `500`
- `font.size.dialog.title` → `16px` / `700`

### 背景 / Backgrounds
- 页浅灰/深黑；可叠紫绿模糊 blob
- 顶栏磨砂；卡片可半透玻璃，但**弹窗正文面建议高不透明度**保证可读
- 禁止面板过度透明导致字溶入背景

### 阴影 / Shadows
- `shadow.1～3`：紫/绿彩色柔影叠层（见预览）
- `shadow.accent`：酸绿强晕给 CTA
- Toast / 弹窗：彩色柔影，非纯黑硬影

### 边框 / Borders
- 浅：`#E5E7EB`；玻璃：`rgba(255,255,255,0.55)`
- 聚焦：酸绿边；错误：红边 + 红环

### 圆角 / Radii
- `radius.el` → `16px`
- `radius.card` → **`24px`**（弹窗）
- `radius.panel` → **`40px`**（大面板/输入可偏大圆）
- `radius.pill` → `100px`

### 滚动条 / Scrollbar
- **Token**：`--scrollbar-size` `8px`；`--scrollbar-track` `transparent`；`--scrollbar-thumb` `rgba(0, 0, 0, 0.18)`；悬停 `rgba(0, 0, 0, 0.28)`；按下 `rgba(0, 0, 0, 0.36)`。
- **Firefox**：`scrollbar-width: thin`；`scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track)`。
- **WebKit**：`*::-webkit-scrollbar` 宽/高 `8px`；滑块圆角 `999px`，`border: 2px solid transparent`，`background-clip: padding-box`；轨道透明；转角透明。
- **状态**：默认 thumb → 悬停 `--scrollbar-thumb-hover` → 按下 `--scrollbar-thumb-active`。
- **暗色覆盖**：thumb `rgba(255, 255, 255, 0.14)`；悬停 `rgba(255, 255, 255, 0.26)`；按下 `rgba(255, 255, 255, 0.34)`。


### 按钮 / Buttons
- **基础 `.btn`**：高 `46px`，`padding` `12px 24px`，圆角 `var(--r-panel)`，边框 `1px solid transparent`，字号 `16px`，字重 `500`，过渡 `all 250ms ease-in-out`。
- **尺寸 / 形态**：`.btn-sm` 高 `36px` / `10px 20px` / `14px`；`.btn-lg` 高 `52px` / `16px 32px` / `18px`；`.btn-pill` 圆角 `var(--r-pill)`。
- **主按钮 `.btn-primary`**：背景 `#111111`，文字 `#FFFFFF`，边色 `#111111`，字重 `800`。
- **主按钮悬停**：背景 `--accent` → `#D4FF00`，边色 `--accent` → `#D4FF00`，投影 `--shadow-accent` → `0px 10px 28px rgba(212, 255, 0, 0.45), 0px 4px 14px rgba(212, 255, 0, 0.25)`，位移 `translateY(-1px) scale(1.02)`。
- **主按钮按下**：`scale(0.97)`。
- **次按钮 `.btn-secondary`**：背景 `--surface1` → `#EEF1F5`，边色 `--n-200` → `#E5E7EB`，文字 `--text1` → `#111111`。
- **次按钮悬停**：强调色边/字 + 浅强调底（`color-mix` ≈18%）+ `translateY(-1px)` + 轻投影。
- **描边 `.btn-outline`**：透明底，边色 `--n-200` → `#E5E7EB`，文字 `--text1` → `#111111`。
- **描边悬停**：背景 `--purple-soft` → `rgba(168, 85, 247, 0.16)`，边色 `--electric-purple` → `#A855F7`，文字 `--electric-purple` → `#A855F7`，位移 `translateY(-1px)`，投影 `0 6px 16px rgba(168, 85, 247, 0.22)`。
- **幽灵 `.btn-ghost`**：透明底，边框 `1px solid var(--n-200)`，文字 `--text2` → `#6B7280`，字重 `500`。
- **幽灵悬停**：背景 `--b-50` → `rgba(212, 255, 0, 0.14)`，文字 `--accent` → `#D4FF00`，`transform` `none`。
- **链接 `.btn-link`**：无边无底，色 `--electric-purple` → `#A855F7`，字号 `14px`，`gap` `6px`。
- **图标 `.btn-icon`**：`40px×40px`，圆角 `var(--r-el)`；悬停浅强调填充。
- **禁用 `.btn-disabled`**：`not-allowed`，透明度 `0.75`。
- **暗色覆盖**：主按钮 `--accent` → `#D4FF00` / `#111111`；主悬停 `#FFFFFF`。
- **交互通则**：主钮悬停微抬并强化投影；次/描边悬停强调色浅染；幽灵悬停不抬升；按下 `scale(0.97)`。


### 表单与反馈 / Forms & Feedback
- **标签**：Jakarta/Inter `14/600+`，下距 `6～10px`
- **标签体系**：中性 = 白底/浅边、全大写加重、胶囊；强调 `.chip-accent` = 酸绿 `#D4FF00` 实底近黑字；信息 `.chip-marked` = 紫浅底、柔边 `rgba(168,85,247,0.45)`（深 `0.5`）、电光紫字 `#A855F7`；选项组**不切酸绿**，统一紫色系：默认=信息紫，选中=实心电光紫 + 白字 + 紫柔影
- **输入**：大圆角（`16～40px` 档按控件），浅灰/玻璃底；聚焦酸绿边 + 浅绿环
- **错误**：红边 + `3px`/`4px` 红环；`.field-error` 短句
- **清空**：`28px`；悬停酸绿/紫
- **提交行**：上距 `20px`，`gap 12`
- **提示条**：浅绿软底或紫 soft；强提示酸绿底深字
- **Toast**：顶中、大圆角、彩色柔影，`220ms`

### 弹窗 / Dialog
- **遮罩**：半透明 + `blur(12px)`；锁滚动
- **面板**：`440/560`，圆角 **`24px`**，高不透白/深面（可极轻玻璃边），**紫绿彩影**；禁止低透明毛玻璃吞字
- **结构**：顶栏弱面 / 正文 / 脚部右对齐酸绿主钮
- **关闭**：`28×28`、圆角 `16px`
- **消息型**：左圆图标——警告/信息；信息可用酸绿或紫
- **动效**：`200/220ms`；可轻微 scale

### 布局 / Layout
- 移动单列大圆角卡；底栏悬浮玻璃
- 桌面可侧栏玻璃 + 多列
- 容器约 `1200px`；弹窗双列演示

## 风格原则 / Style Principles
1. **酸绿唯一主 CTA**：`#D4FF00` + 近黑字，禁止白字酸绿。
2. **紫/粉只点缀**：渐变与游戏化，不替代主钮。
3. **大圆角宣言**：`16/24/40/100`，忌尖角工具风。
4. **彩色柔影**：紫绿光晕，忌纯黑 Material 重影。
5. **玻璃有边界**：顶栏可磨砂；关键表单/弹窗保可读不透明。
6. **Jakarta 几何标题 + Inter 正文**。
7. **深浅双主题**：酸绿不变，表面换肤。
8. **表单大圆 + 酸绿焦**：错误红环短句。
9. **弹窗彩影同构**：`24px` + 紫绿影。
10. **快社交语气**：微文案活泼，但避免贴纸墙抢 CTA。

## 提示词包
### 基础提示词

**审美方向**  
生成电光玻璃界面：浅 `#F2F4F6` 或深 `#050505`，酸绿 `#D4FF00` 主 CTA（近黑字），紫/粉点缀，大圆角玻璃与彩色柔影。Jakarta + Inter。含表单、Toast、`24px` 彩影弹窗。

**Token 约束**  
色板见 Tokens；圆角 16/24/40/pill；酸绿影 CTA；危险 `#EF4444`；弹窗高不透明。
- 滚动条：宽 `8px`，轨道透明，滑块 `rgba(0, 0, 0, 0.18)`（悬停/按下加深）；胶囊滑块 + Firefox `thin`。


**布局约束**  
移动单列；底栏悬浮；弹窗脚右对齐。

**交互约束**  
主/次/描边/幽灵按钮态齐全：主钮悬停微抬并强化投影，次与描边用强调色浅染，幽灵不抬升；主钮按下 `scale(0.97)`；触控高度建议 ≥ `44px`（或沿用主题默认 `.btn` 高度）；聚焦环与品牌色协调。


**避免项**  
禁止酸绿白字；禁止尖角 Semi 风；禁止弹窗全透明玻璃；禁止紫替主 CTA；禁止丢掉彩色影改纯黑影。

### 组件提示词
**主按钮 `.btn-primary`**：`#111111` 底，`#FFFFFF` 字，投影 —；悬停微抬；按下 `scale(0.97)`。
**次按钮 `.btn-secondary`**：软面/细边；悬停强调色浅底与边，微抬。
**描边 `.btn-outline`**：透明底 + 主题边；悬停强调色浅染。
**幽灵 `.btn-ghost`**：透明底，`--text2` → `#6B7280` 字；悬停浅强调底，不抬升。
**尺寸族**：默认 / `.btn-sm` / `.btn-lg` / `.btn-pill`；另含 `.btn-link`、`.btn-icon`、`.btn-disabled`。

主钮酸绿深字；玻璃顶栏；输入大圆角酸绿焦；弹窗 `24px` 彩影。  
**标签 / Chip**：中性白底大写胶囊；强调酸绿近黑字；信息与选项组走电光紫（柔边紫字 / 选中实心紫白字），勿把选项组选中切成酸绿。


### 变体提示词
更深聚焦模式；更玻璃（须保对比）；去紫仅酸绿单强调；表单确认流。

## 复用说明
- **必须保持不变**：`#D4FF00`+近黑字、紫粉点缀、大圆角、彩色柔影、Jakarta/Inter、字段红环、弹窗 `24px` 高不透彩影。
- **可弹性调整**：blob 多少、默认深浅、是否底栏。
- **风格跑偏风险**：酸绿变黄且白字；弹窗透明难读；圆角过小。

---

## 质量评分 / Quality Score
- **总分**：90/100
- **结论**：通过（可直接用于社交/潮流 H5 与确认流）

## 分项得分 / Dimension Scores
- 风格一致性：18/20
- Token 可执行性：15/15
- 色彩与对比：14/15
- 排版层级：9/10
- 组件完整度：10/10
- 布局与间距：8/10
- 防跑偏约束：10/10
- 变体控制力：8/10

## 扣分说明 / Deductions
- 备份原为角色提示书，桌面栅格细节仍可再补。
- 输入圆角 `16` vs `40` 需按控件类型写死映射。

## 关键风险 / Key Risks
- 生成器给酸绿配白字导致对比崩溃。
- 弹窗做成低透明玻璃不可读。
- 圆角被收成 8px SaaS。

## 优先修订（三项）
1. 写死「酸绿上必须 `#111`」。
2. 区分卡片玻璃 alpha 与弹窗实面 alpha。
3. 补底栏 dock 高度与安全区。
