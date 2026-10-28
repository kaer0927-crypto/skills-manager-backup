# SemiDesign · 视觉规范

## 风格快照 / Style Snapshot
- **整体风格 / Overall style**：Semi Design 官方亮色默认主题落地页。画布 `#F9F9F9` / 白卡 `#FFFFFF`，品牌蓝 **`#0064FA`**（悬停 `#0062D6`、按下 `#004FB3`），选中浅蓝底 **`#EAF5FF`**。Inter 全栈；圆角克制——按钮 **`3px`**、输入/面板 **`6px`**、卡片/弹窗 **`12px`**。层次靠 `8%` 墨色描边 + 浅填充，轻投影抬升而非重阴影。完整反馈：字段 `.is-error` 红环 + `.field-error`、清空钮、提交行、顶部 Toast、浅蓝提示条，以及 **`12px` 圆角、不透明、柔影**弹窗。
- **语气关键词 / Tone keywords**：专业、清晰、中性、工程感、字节系 B 端、克制圆角。
- **适配产品类型 / Suitable product types**：管理后台、设计系统文档站、中台控制台、表格与表单密集型产品。

> 来源：本地预览页 `SemiDesign-preview.html`。备份 DNA（semi.design / `@douyinfe/semi-ui`）已按当前预览补全弹窗 / 表单 / 提示规则。

## 设计 Tokens / Design Tokens
### 颜色 / Colors

**浅色（默认）**
- `color.canvas` → `#F9F9F9`（`--bg`）
- `color.surface.card` → `#FFFFFF`（`--surface` / `--surface-panel`）
- `color.surface.fill0` → `rgba(46, 50, 56, 0.05)`（`--surface1` / `--n-50`）
- `color.border.default` → `rgba(28, 31, 35, 0.08)`（`--n-200`）
- `color.text.primary` → `#1C1F23`
- `color.text.secondary` → `rgba(28, 31, 35, 0.8)`
- `color.text.tertiary` → `rgba(28, 31, 35, 0.62)`
- `color.brand.primary` → `#0064FA`
- `color.brand.hover` → `#0062D6`；`active` → `#004FB3`
- `color.brand.subtle` → `rgba(0, 100, 250, 0.18)`
- `color.brand.selected` → `#EAF5FF`（`--b-50`，导航/选中底）
- `color.semantic.success` → `#10b981`（备份 Semi 绿 `#3BB346` 可互换）
- `color.semantic.warning` → `#FC8800` / 预览 `#f5a623`
- `color.semantic.danger` → `#EF4444`（备份 Semi 红 `#F93920`）
- `color.overlay.scrim` → `rgba(15, 23, 42, 0.55)` + `blur(12px)`

**深色**
- `color.canvas` → `#16161A`
- `color.surface.card` → `#232429`；弹窗实底可用 `#161616`，顶栏/内嵌面 `#1C1C1C`
- `color.border.default` → `rgba(255, 255, 255, 0.12)`
- `color.text.primary` → `#F9F9F9`；`secondary` → `0.8`；`tertiary` → `0.6`
- `color.brand.primary` → `#3C8CFF`；悬停 `#5A9EFF`；按下回 `#0064FA`
- `color.brand.selected` → `rgba(0, 100, 250, 0.18)`
- `color.overlay.scrim` → `rgba(0, 0, 0, 0.62)` + `blur(12px)`

**选区 / 焦点**：`focus-visible` 用 `2px solid rgba(0, 100, 250, 0.35)`，`outline-offset: 2px`。

### 字体 / Typography
- `font.family.ui` → **Inter**, `-apple-system`, `BlinkMacSystemFont`, `"PingFang SC"`, `"Hiragino Sans GB"`, `"Microsoft YaHei"`, …sans-serif
- `font.size.body` → `14px`，`line-height: 1.5`
- `font.size.caption` → `12px`–`13px`
- `font.size.label` → `14px` / `600`
- `font.size.field-error` → `12px` / `500`
- `font.size.hero` → `clamp(28px, 4vw, 40px)` / `600` / `1.2`
- `font.size.section` → `18px` / `700`（演示舞台标题）
- `font.size.dialog.title` → `16px` / `700`，`letter-spacing: -0.02em`
- `font.weight.heading` → `600`；强调 `700`

### 背景 / Backgrounds
- 页级洗色：`linear-gradient(160deg, #EAF5FF 0%, #F9F9F9 42%, #FFFFFF 100%)`（`.page-painterly`）
- 深色：极轻蓝径向 + `#16161A` 纵深，禁止大面积海军蓝空洞
- 顶栏：`rgba(255,255,255,0.92)` + `blur(12px)`；深色对应 `rgba(22,22,26,0.92)`
- 弹窗：面板/正文/脚部不透明白或深面；**禁止**面板 `backdrop-filter`

### 阴影 / Shadows
- `shadow.1` → `0 1px 2px rgba(28, 31, 35, 0.04)`
- `shadow.2` → `0 4px 14px rgba(28, 31, 35, 0.08)`
- `shadow.3` → `0 8px 24px rgba(28, 31, 35, 0.1)`
- `shadow.card` → `0 1px 2px …04, 0 4px 12px …06`
- `shadow.accent` → `0 2px 8px rgba(0, 100, 250, 0.22)`
- Toast / 弹窗：`0 10px 28px rgba(15,23,42,0.12), 0 2px 8px …06`（深色加黑影）
- 默认卡片靠描边；悬停可抬至 `shadow.2`

### 边框 / Borders
- `border.width` → `1px`
- `border.color` → `rgba(28, 31, 35, 0.08)`（深色白 12%）
- 输入聚焦：边转品牌蓝
- 错误：红边 + `3px`/`4px` 红透明环
- 弹窗头脚：`1px` 分割（浅 `rgba(15,23,42,0.08)` / 深白 10%）

### 圆角 / Radii
- `radius.el` / 按钮 → **`3px`**（`--r-el`）
- `radius.panel` / 输入 → **`6px`**（`--r-panel`）
- `radius.card` / 弹窗 → **`12px`**（`--r-card`）
- 清空钮圆形 `50%`；消息图标可 `9999px`；Logo 方块约 `8px`

### 滚动条 / Scrollbar
- **Token**：`--scrollbar-size` `8px`；`--scrollbar-track` `transparent`；`--scrollbar-thumb` `rgba(0, 0, 0, 0.18)`；悬停 `rgba(0, 0, 0, 0.28)`；按下 `rgba(0, 0, 0, 0.36)`。
- **Firefox**：`scrollbar-width: thin`；`scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track)`。
- **WebKit**：`*::-webkit-scrollbar` 宽/高 `8px`；滑块圆角 `999px`，`border: 2px solid transparent`，`background-clip: padding-box`；轨道透明；转角透明。
- **状态**：默认 thumb → 悬停 `--scrollbar-thumb-hover` → 按下 `--scrollbar-thumb-active`。
- **暗色覆盖**：thumb `rgba(255, 255, 255, 0.14)`；悬停 `rgba(255, 255, 255, 0.26)`；按下 `rgba(255, 255, 255, 0.34)`。


### 按钮 / Buttons
- **基础 `.btn`**：高 `32px`，`padding` `6px 16px`，圆角 `var(--r-el)`，边框 `1px solid transparent`，字号 `14px`，字重 `600`，过渡 `background 180ms ease, border-color 180ms ease, box-shadow 180ms ease, color 180ms ease, transform 180ms ease`。
- **尺寸 / 形态**：`.btn-sm` 高 `28px` / `4px 12px` / `12px`；`.btn-lg` 高 `40px` / `8px 20px` / `16px`；`.btn-pill` 圆角 `var(--r-pill)`。
- **主按钮 `.btn-primary`**：背景 `--accent` → `#0064FA`，文字 `#fff`，边色 `--accent` → `#0064FA`。
- **主按钮悬停**：背景 `--accent-hover` → `#0062D6`，边色 `--accent-hover` → `#0062D6`，投影 `--shadow-accent` → `0 2px 8px rgba(0, 100, 250, 0.22)`，位移 `translateY(-1px)`。
- **次按钮 `.btn-secondary`**：背景 `--surface1` → `rgba(46, 50, 56, 0.05)`，边色 `--n-200` → `rgba(28, 31, 35, 0.08)`，文字 `--text1` → `#1C1F23`。
- **次按钮悬停**：背景 `--b-50` → `#EAF5FF`，边色 `--accent` → `#0064FA`，文字 `--accent` → `#0064FA`，位移 `translateY(-1px)`，投影 `--shadow-2` → `0 4px 14px rgba(28, 31, 35, 0.08)`。
- **描边 `.btn-outline`**：透明底，边色 `--n-200` → `rgba(28, 31, 35, 0.08)`，文字 `--text1` → `#1C1F23`。
- **描边悬停**：背景 `--b-50` → `#EAF5FF`，边色 `--accent` → `#0064FA`，文字 `--accent` → `#0064FA`，位移 `translateY(-1px)`，投影 `--shadow-2` → `0 4px 14px rgba(28, 31, 35, 0.08)`。
- **幽灵 `.btn-ghost`**：透明底，边框 `1px solid var(--n-200)`，文字 `--text2` → `rgba(28, 31, 35, 0.8)`，字重 `500`。
- **幽灵悬停**：背景 `--b-50` → `#EAF5FF`，文字 `--accent` → `#0064FA`，`transform` `none`。
- **链接 `.btn-link`**：无边无底，色 `--accent` → `#0064FA`，字号 `14px`，`gap` `6px`。
- **图标 `.btn-icon`**：`40px×40px`，圆角 `var(--r-el)`；悬停浅强调填充。
- **禁用 `.btn-disabled`**：`not-allowed`，透明度 `0.75`。
- **暗色覆盖**：暗色主色 `--accent` → #3C8CFF（浅色为 #0064FA）。
- **交互通则**：主钮悬停微抬并强化投影；次/描边悬停强调色浅染；幽灵悬停不抬升；按下可微缩放或下沉。


### 表单与反馈 / Forms & Feedback
- **标签**：`14px` / `600`，下距 `6px`，无大写强迫
- **标签体系**：中性 = 浅底 + `n-200` 边 + 次文色；强调 `.chip-accent` = 品牌蓝 `#0064FA` 实底白字；信息 `.chip-marked` = `b-50` 底、柔边 `rgba(0,100,250,0.28)`、蓝字；选项组统一信息色系，选中 = 蓝实底白字 + 轻蓝影
- **输入**：高 `32px`（sm `28px`），圆角 **`6px`**，白底 + `1px` `n-200`；字 `14px`
- **悬停**：边混主墨约 `16%`
- **聚焦**：边转品牌蓝；页级 `focus-visible` 蓝环
- **错误**：`.is-error` 红边 + `0 0 0 3px`（聚焦 `4px`）红透明环；`.field-error` `12px/500` 短句，`role="alert"`
- **清空**：`.input-wrap` 内圆钮 `20px`，有值且聚焦/悬停出现
- **表单辅助图标（统一偏小、偏淡）**：下拉 `.combo-chevron` 约 `9px`；步进器按钮约 `22×22` / 图标 `10px`；清空 `.input-clear` 约 `20×20` / `11px`；均用 muted + 透明度约 `0.72`
- **提交行**：上距 `20px`，`gap 12`，钮 `min-width 120px`
- **提示条 `.alert`**：圆角 `6px`，`--b-50` 底 + 蓝混边；强提示实底品牌蓝白字
- **Toast**：顶中、`max-width min(92vw, 360px)`，圆角随面板档，双层柔影，`220ms` 显隐

### 弹窗 / Dialog
- **遮罩**：`rgba(15,23,42,0.55)` + `blur(12px)`；打开锁滚动
- **面板**：宽 `440px`（内容型 `560px`），圆角 **`12px`**，不透明白/深面，柔影双层；禁止玻璃半透明
- **结构**：顶栏（浅灰 `#f3f3f3` / 深 `#1c1c1c` + 标题 + 关闭）/ 正文 `24×20` / 脚部右对齐
- **关闭**：`28×28`、圆角 `3px`；悬停浅墨底
- **消息型**：左圆图标 `36px`——警告橙、信息品牌蓝实底白字，带色影
- **内容型**：内嵌面圆角 `6px`、列表、蓝芯片、表单（字段可压缩）
- **动效**：遮罩 `200ms`；面板 `translateY(10px) scale(0.98)` → 归位 `220ms`

### 布局 / Layout
- 容器 `max-width: 1200px`，水平 `32px`；内容区上下 `24px` / `64px`
- 顶栏 sticky 高 `60px`（与 shell 骨架统一）
- 备份 DNA：侧栏文档宽 `280px`、内容 gutter `16px`、`.page-body` 圆角 `12px`
- 弹窗演示双列 `gap 20`；`≤900px` 单列
- 间距阶梯：`4/6/8/12/14/16/20/24/26/32`

## 风格原则 / Style Principles
1. **品牌蓝唯一主色**：交互强调统一 `#0064FA`，勿混 Ant Design 蓝或紫系渐变。
2. **选中态浅蓝底**：导航/列表用 `#EAF5FF` + 主色字，非深底白字。
3. **圆角三档纪律**：`3 / 6 / 12`，弹窗跟卡片 `12px`，勿滑向消费级大圆角。
4. **层次靠填充与描边**：`fill-0` 灰底 + 白卡 + `8%` 边，投影仅轻抬升。
5. **Inter 中性栈**：中文回退 PingFang / 微软雅黑，无衬线装饰字体。
6. **语义色点状使用**：成功/警告/危险用于 Tag、状态、错误环，不大面积铺底。
7. **表单密度偏 Semi**：输入高 `32px`、标签 `14/600`，错误红环短句。
8. **弹窗工程感**：`12px` 圆角、不透明、柔影；顶栏浅灰分区。
9. **深色提亮蓝**：主色改 `#3C8CFF`，仍保留浅蓝选中逻辑。
10. **组件优先 Semi DNA**：覆盖走 CSS 变量，避免手写与 Semi 冲突的皮肤。

## 提示词包
### 基础提示词

**审美方向**  
生成 Semi Design 官方亮色主题风格的管理/文档静态页。专业、克制、工程感。画布 `#F9F9F9`，白卡细描边，品牌蓝 `#0064FA`，选中浅蓝 `#EAF5FF`。Inter 全栈。圆角按钮 `3px`、输入 `6px`、卡片与弹窗 `12px`。含完整表单（错误红环、清空、提交行）、浅蓝提示条、顶部柔影 Toast，以及 `12px` 圆角不透明柔影弹窗。

**Token 约束**  
主色 `#0064FA` / 悬停 `#0062D6` / 浅底 `#EAF5FF`；文本 `#1C1F23` 与 80%/62% 阶；描边 `rgba(28,31,35,0.08)`；页底 `#F9F9F9`；圆角 `3/6/12`；阴影轻量 `shadow.1–2`；弹窗遮罩可 blur，面板必须不透明。
- 滚动条：宽 `8px`，轨道透明，滑块 `rgba(0, 0, 0, 0.18)`（悬停/按下加深）；胶囊滑块 + Firefox `thin`。


**布局约束**  
主宽 `1200px`、左右 `32px`；顶栏 `60px`；弹窗 `440～560px` 脚钮右对齐；可选侧栏 `280px`。

**交互约束**  
主/次/描边/幽灵按钮态齐全：主钮悬停微抬并强化投影，次与描边用强调色浅染，幽灵不抬升；主钮按下可微缩放；触控高度建议 ≥ `44px`（或沿用主题默认 `.btn` 高度）；聚焦环与品牌色协调。


**避免项**  
禁止 Ant Design `#4C75F2` 或紫蓝渐变 Logo；禁止主按钮圆角 >`6px`；禁止深色 Ant Pro 侧栏冒充 Semi 默认；禁止去掉细边框导致卡面融底；禁止弹窗毛玻璃半透明；禁止大红底块代替字段错误环。

### 组件提示词
**主按钮 `.btn-primary`**：`--accent` → `#0064FA` 底，`#fff` 字，投影 —；悬停微抬；按下 `scale(0.95)`。
**次按钮 `.btn-secondary`**：软面/细边；悬停强调色浅底与边，微抬。
**描边 `.btn-outline`**：透明底 + 主题边；悬停强调色浅染。
**幽灵 `.btn-ghost`**：透明底，`--text2` → `rgba(28, 31, 35, 0.8)` 字；悬停浅强调底，不抬升。
**尺寸族**：默认 / `.btn-sm` / `.btn-lg` / `.btn-pill`；另含 `.btn-link`、`.btn-icon`、`.btn-disabled`。

**顶栏**：半透明白 + blur，高 `60px`，底 `1px` 边；滚动轻影。  
**选中项**：`#EAF5FF` 底 + 品牌蓝字。  
**卡片**：白底、`12px` 圆角、`1px` 边、轻双层影。  
**输入**：`6px` 圆角、高 `32px`；错误红环；圆清空钮。  
**提示条 / Toast**：浅蓝底或蓝实底；Toast 顶中柔影。  
**弹窗**：`12px` 圆角、不透明、柔影；顶栏浅灰；脚部主钮蓝。


### 变体提示词

- **更紧凑**：内容 padding `16px`，表格 denser，圆角档位不变。  
- **更文档化**：页底改纯白，弱化卡影，贴近 semi.design 阅读。  
- **Semi Dark**：画布 `#16161A`，面 `#232429`，蓝 `#3C8CFF`。  
- **表单确认流**：保留 B 端密度，加入校验表单 + `12px` 确认弹窗。

## 复用说明
- **必须保持不变**：主色 `#0064FA`、选中浅蓝底、Inter 栈、圆角 `3/6/12`、细描边层次、字段错误红环、弹窗不透明柔影 `12px`。
- **可弹性调整**：登录渐变角度、统计卡数量、业务文案、是否本地化 Inter。
- **风格跑偏风险**：混用 Ant/Element 色板；过大圆角与重阴影；侧栏改深色 Pro；弹窗做成玻璃模态。

---

## 质量评分 / Quality Score
- **总分**：90/100
- **结论**：通过（可直接用于 Semi 亮色主题落地与表单确认流）

## 分项得分 / Dimension Scores
- 风格一致性：18/20
- Token 可执行性：15/15
- 色彩与对比：14/15
- 排版层级：9/10
- 组件完整度：10/10
- 布局与间距：9/10
- 防跑偏约束：9/10
- 变体控制力：8/10

## 扣分说明 / Deductions
- 预览语义红/绿与备份 Semi 官方色略有偏差，落地时需统一写死一套。
- 变体未展开完整组件矩阵（表格分页等）。

## 关键风险 / Key Risks
- 生成器易把按钮圆角做成 `8～16px` 消费级，偏离 Semi `3px`。
- 易用 Ant 蓝替换 `#0064FA`。
- 弹窗易被加成毛玻璃，破坏不透明工程面。

## 优先修订（三项）
1. 统一语义色：落地选定预览 `#EF4444` 或 Semi `#F93920` 并写死。
2. 为输入聚焦与 `focus-visible` 蓝环写清优先级，避免双环冲突。
3. 补充表格/筛选条密度 token，与表单 `32px` 对齐。
