# 亮色电光蓝 · 视觉规范

## 风格快照 / Style Snapshot
- **整体风格 / Overall style**：近白画布 `#FAFAFA` + 电光蓝 **`#0052FF`**（辅 `#4D7CFF`）。白卡中性影分层；展示标题可 **Calistoga**，正文 **Inter**。圆角 `10 / 14 / 18px`。页底可有淡蓝径向晕与极淡噪点、`64px` 浅格。完整反馈：字段错误红环、清空、提交行、顶中 Toast、浅蓝提示条，以及 **`18px` 圆角、不透明、柔影**弹窗。
- **语气关键词 / Tone keywords**：清晰、可信、电光感、中高对比、行动导向。
- **适配产品类型 / Suitable product types**：金融科技落地页、开发者工具官网、B2B SaaS、活动报名、强 CTA 产品站。

> 来源：本地预览页 `亮色电光蓝-preview.html`。备份 DNA 已按当前预览补全弹窗 / 表单 / 提示规则。

## 设计 Tokens / Design Tokens
### 颜色 / Colors

**浅色（默认）**
- `color.brand.primary` → `#0052FF`（`--accent` / `--ring`）
- `color.brand.secondary` → `#4D7CFF`
- `color.brand.on_primary` → `#FFFFFF`
- `color.text.foreground` → `#0F172A`
- `color.text.muted` → `#64748B`
- `color.surface.background` → `#FAFAFA`
- `color.surface.muted` → `#F1F5F9`
- `color.surface.card` → `#FFFFFF`
- `color.border.default` → `#E2E8F0`
- `color.semantic.success` → `#10B981`
- `color.semantic.warning` → `#F5A623`
- `color.semantic.danger` → `#EF4444`
- `color.semantic.premium` → `#8B5CF6`（点缀，非主色）
- `color.overlay.scrim` → `rgba(15, 23, 42, 0.55)` + `blur(12px)`

**氛围**
- 淡蓝径向：`rgba(0,82,255,0.09)` / `rgba(77,124,255,0.08)` + 大模糊
- 极淡噪点层；`64px` slate 浅格（顶部 mask 渐隐）

### 字体 / Typography
- `font.family.display` → **Calistoga**（仅展示标题）
- `font.family.body` → **Inter** + PingFang / 微软雅黑 / system-ui
- `font.size.body` → `14–16px`，`line-height: 1.65`
- `font.size.label` → `14px` / `600`
- `font.size.field-error` → `12px` / `500`
- `font.size.dialog.title` → `16px` / `700` **Inter**（不用 Calistoga 抢戏）
- `motion.ease` → `cubic-bezier(0.16, 1, 0.3, 1)`

### 背景 / Backgrounds
- 页 `#FAFAFA`；分区可用 `#F1F5F9`；Hero 勿整屏灌蓝
- 弹窗不透明白；禁止面板玻璃

### 阴影 / Shadows
- `shadow.sm`→`xl`：中性黑灰阶梯（见预览）
- `shadow.accent` → `0 4px 14px rgba(0, 82, 255, 0.25)`
- `shadow.accent-lg` → `0 8px 24px rgba(0, 82, 255, 0.35)`
- Toast / 弹窗：双层柔影 `0 10px 28px …`

### 边框 / Borders
- `1px` `#E2E8F0`；聚焦环品牌蓝；错误红边 + `3px`/`4px` 红环

### 圆角 / Radii
- `radius.sm` → `10px`（提示条等）
- `radius.md` → `14px`（输入 / `--ix-radius`）
- `radius.lg` / `xl` → **`18px`**（卡片 / 弹窗）
- `radius.pill` → `999px`

### 滚动条 / Scrollbar
- **Token**：`--scrollbar-size` `8px`；`--scrollbar-track` `transparent`；`--scrollbar-thumb` `rgba(0, 0, 0, 0.18)`；悬停 `rgba(0, 0, 0, 0.28)`；按下 `rgba(0, 0, 0, 0.36)`。
- **Firefox**：`scrollbar-width: thin`；`scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track)`。
- **WebKit**：`*::-webkit-scrollbar` 宽/高 `8px`；滑块圆角 `999px`，`border: 2px solid transparent`，`background-clip: padding-box`；轨道透明；转角透明。
- **状态**：默认 thumb → 悬停 `--scrollbar-thumb-hover` → 按下 `--scrollbar-thumb-active`。
- **暗色覆盖**：thumb `rgba(255, 255, 255, 0.14)`；悬停 `rgba(255, 255, 255, 0.26)`；按下 `rgba(255, 255, 255, 0.34)`。


### 按钮 / Buttons
- **基础 `.btn`**：高 `44px`，`padding` `0 22px`，圆角 `var(--radius-sm)`，边框 `1px solid transparent`，字号 `0.9rem`，字重 `600`，过渡 `transform 0.2s ease-out, box-shadow 0.2s ease-out, filter 0.2s ease-out, border-color 0.2s ease-out, background 0.2s ease-out`。
- **尺寸 / 形态**：`.btn-sm` 高 `36px` / `0 14px` / `0.82rem`；`.btn-lg` 高 `42px` / `0 40px` / `0.95rem`；`.btn-pill` 圆角 `var(--radius-pill)`。
- **主按钮 `.btn-primary`**：背景 `linear-gradient(135deg, var(--accent), var(--accent-secondary))`，文字 `--accent-foreground` → `#ffffff`，边色 `rgba(0, 82, 255, 0.35)`，投影 `--shadow-accent` → `0 4px 14px rgba(0, 82, 255, 0.25)`。
- **主按钮悬停**：投影 `--shadow-accent-lg` → `0 8px 24px rgba(0, 82, 255, 0.35)`，位移 `translateY(-2px)`，滤镜 `brightness(1.08)`。
- **主按钮按下**：`scale(0.98)`。
- **次按钮 `.btn-secondary`**：背景 `--muted` → `#f1f5f9`，边色 `--border` → `#e2e8f0`，文字 `--foreground` → `#0f172a`。
- **次按钮悬停**：强调色边/字 + 浅强调底（`color-mix` ≈18%）+ `translateY(-1px)` + 轻投影。
- **描边 `.btn-outline`**：透明底，边色 `--border` → `#e2e8f0`，文字 `--foreground` → `#0f172a`。
- **描边悬停**：强调色边/字 + 浅强调底（`color-mix` ≈14%）+ `translateY(-1px)` + 轻投影。
- **幽灵 `.btn-ghost`**：透明底，边框 `1px solid var(--border)`，文字 `--muted-foreground` → `#64748b`，字重 `500`。
- **幽灵悬停**：强调色边/字 + 浅强调底；`transform` `none`，通常无抬升投影。
- **链接 `.btn-link`**：无边无底，色 `--accent` → `#0052ff`，字号 `14px`，`gap` `6px`。
- **图标 `.btn-icon`**：`40px×40px`，圆角 `var(--radius-sm)`；悬停浅强调填充。
- **禁用 `.btn-disabled`**：`not-allowed`，透明度 `0.75`。
- **交互通则**：主钮悬停微抬并强化投影；次/描边悬停强调色浅染；幽灵悬停不抬升；按下 `scale(0.98)`。


### 表单与反馈 / Forms & Feedback
- **标签**：`14px` / `600`，下距 `6～10px`
- **输入**：圆角 **`14px`**，白底 + `#E2E8F0`；聚焦蓝环
- **错误**：`.is-error` 红边 + 红透明环；`.field-error` 短句，`role="alert"`
- **清空**：圆钮 `28px`；**提交行** 上距 `20px`，`gap 12`，`min-width 120px`
- **提示条**：圆角 `10px`，浅蓝软底（`rgba(0,82,255,0.08)` 级）或 muted；强提示蓝实底白字
- **Toast**：顶中、圆角 `14px`、柔影，`220ms`

### 弹窗 / Dialog
- **遮罩**：半透明 + `blur(12px)`；锁滚动
- **面板**：`440px` / 内容 `560px`，圆角 **`18px`**，不透明白，柔影
- **结构**：顶栏 muted / 正文 / 脚部右对齐；头脚分割线
- **关闭**：`28×28`；消息型左圆图标（警告橙 / 信息蓝）
- **动效**：遮罩 `200ms`；面板归位 `220ms`

### 布局 / Layout
- 容器约 `1100–1200px`；水平 `16–24px`；区块 `32–64px`
- 首屏：品牌 + 标题 + 一句 + 主/次 CTA
- 弹窗演示双列；`≤900px` 单列

## 风格原则 / Style Principles
1. **电光蓝唯一强色**：交互与聚焦统一 `#0052FF`。
2. **中性卡影 + 彩色 CTA 影**：内容卡黑灰影，主钮蓝影。
3. **衬线只作点睛**：Calistoga 限展示标题。
4. **圆角 10–18**：弹窗跟 `18px`。
5. **浅 slate 辅面**：`#F1F5F9` 弱分区，禁整屏蓝底。
6. **对比清晰**：`#0F172A` 对近白，辅文 `#64748B`。
7. **动效果断**：expo，无弹跳霓虹。
8. **表单克制**：错误红环短句；提示浅蓝软底。
9. **弹窗同构**：`18px`、不透明、柔影。
10. **语义色点状**：成功/警告/危险/premium 不抢主蓝。

## 提示词包
### 基础提示词

**审美方向**  
生成亮色电光蓝界面：`#FAFAFA` 近白、白卡、主强调 `#0052FF`。标题可 Calistoga，正文 Inter。理性行动导向。含表单校验、浅蓝提示条、顶中 Toast、`18px` 不透明柔影弹窗。

**Token 约束**  
蓝 `#0052FF` / `#4D7CFF`；文 `#0F172A` / `#64748B`；边 `#E2E8F0`；静音 `#F1F5F9`；圆角 10/14/18；主钮蓝影；语义色见 Tokens。
- 滚动条：宽 `8px`，轨道透明，滑块 `rgba(0, 0, 0, 0.18)`（悬停/按下加深）；胶囊滑块 + Firefox `thin`。


**布局约束**  
宽容器居中；首屏单焦点；弹窗 `440～560px` 脚钮右对齐。

**交互约束**  
主/次/描边/幽灵按钮态齐全：主钮悬停微抬并强化投影，次与描边用强调色浅染，幽灵不抬升；主钮按下 `scale(0.98)`；触控高度建议 ≥ `44px`（或沿用主题默认 `.btn` 高度）；聚焦环与品牌色协调。


**避免项**  
禁止紫/靛替主色；禁止暗黑霓虹铺底；禁止全文衬线；禁止去掉主钮蓝影；禁止同视口多实心主 CTA；禁止弹窗玻璃半透明。

### 组件提示词
**主按钮 `.btn-primary`**：`linear-gradient(135deg, var(--accent), var(--accent-secondary))` 底，`--accent-foreground` → `#ffffff` 字，投影 `--shadow-accent` → `0 4px 14px rgba(0, 82, 255, 0.25)`；悬停微抬；按下 `scale(0.98)`。
**次按钮 `.btn-secondary`**：软面/细边；悬停强调色浅底与边，微抬。
**描边 `.btn-outline`**：透明底 + 主题边；悬停强调色浅染。
**幽灵 `.btn-ghost`**：透明底，`--muted-foreground` → `#64748b` 字；悬停浅强调底，不抬升。
**尺寸族**：默认 / `.btn-sm` / `.btn-lg` / `.btn-pill`；另含 `.btn-link`、`.btn-icon`、`.btn-disabled`。

**卡片**：白底细边或 `shadow.md`，圆角 `14–18px`。  
**输入**：`14px` 圆角，聚焦蓝环；错误红环。  
**徽章**：浅蓝软底 + 蓝字。  
**弹窗**：`18px`、不透明、柔影；脚部蓝主钮。


### 变体提示词

- **更亮**：页 `#FFFFFF`，静音保留。  
- **更暗（浅色内）**：页 `#F1F5F9`，卡仍白。  
- **更密**：间距降档，正文 ≥`14px`。  
- **表单确认流**：校验 + `18px` 确认弹窗。  
- **更暖**：禁止改 Token；暖色仅插图。

## 复用说明
- **必须保持不变**：`#0052FF`、近白面、Inter 正文、蓝影 CTA、中等圆角、字段红环、弹窗 `18px` 不透明柔影。
- **可弹性调整**：是否 Calistoga、列数、投影档、容器宽。
- **风格跑偏风险**：蓝面积过大、第二品牌色、卡用彩色投影。

---

## 质量评分 / Quality Score
- **总分**：92/100
- **结论**：通过（可直接用于科技/金融落地与表单流）

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
- 主按钮悬停「提亮 vs 加深」仍需产品写死单一规则。
- 移动端底栏规范可再补。

## 关键风险 / Key Risks
- Calistoga 滥用削弱理性科技感。
- 生成器易把页底改成大面积蓝渐变。
- 弹窗圆角被做成过大软卡。

## 优先修订（三项）
1. 写死主按钮悬停色为单一值（建议向 `#4D7CFF` 提亮）。
2. 明确 premium 紫仅 Tag，不进 CTA。
3. 补移动端触控间距与粘性底栏规范。
