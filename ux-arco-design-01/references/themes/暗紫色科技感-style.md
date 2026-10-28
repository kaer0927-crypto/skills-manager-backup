# 暗紫色科技感 · 视觉规范

## 风格快照 / Style Snapshot
- **整体风格 / Overall style**：深空暗底上的半透明渐变卡片，品牌紫 `#6867F7` 作强调与外发光；Inter 无衬线；圆角 10–20px；阴影偏深 + 紫色按钮光晕，气质科技、沉浸、偏仪表盘/控制台。 完整反馈与 **`20px` 外发光**弹窗。
- **语气关键词 / Tone keywords**：沉浸、科技紫、玻璃薄雾、数据感、克制光效。
- **适配产品类型 / Suitable product types**：AI 控制台、数据看板、开发者后台、暗色 SaaS、智能硬件配套 Web。

> 来源：本地预览页 `暗紫色科技感-preview.html`。备份 DNA 已按当前预览补全弹窗 / 表单。

## 设计 Tokens / Design Tokens

### 颜色 / Colors
- `color.brand.primary`：`#6867F7`；`hover`：`#7B7AF9`；`glow`：`rgba(104,103,247,0.28)`
- `color.text.primary`：`#EDECEF`；`secondary`：`rgba(255,255,255,0.6)`
- `color.surface.card`：`linear-gradient(to bottom, rgba(255,255,255,0.055), rgba(255,255,255,0.018))`
- `color.surface.soft`：`rgba(255,255,255,0.06)`；`input-tint`：`rgba(104,103,247,0.12)`
- `color.border.default`：`rgba(255,255,255,0.06)`；`strong`：`rgba(255,255,255,0.12)`；`accent`：`rgba(104,103,247,0.34)`
- `color.semantic.success`：`#86EFAC`；`success-bg`：`rgba(110,231,183,0.14)`
- `color.semantic.error`：`#FDA4A4`；`error-bg`：`rgba(248,113,113,0.14)`

### 字体 / Typography
- `font.family.ui`：`Inter`，回退 `PingFang SC, Microsoft YaHei, system-ui, sans-serif`
- 字重 `400`/`500`/`600`/`700`；数据数字可略加字重
- `motion.ease`：`cubic-bezier(0.16, 1, 0.3, 1)`（expo）

### 背景 / Backgrounds
- 页面：深空近黑/深蓝紫黑（预览以暗底 + 透白卡片为主）
- 卡片：自上而下极低 alpha 白渐变，营造薄雾玻璃
- 输入：可叠紫色 soft tint

### 阴影 / Shadows
- `shadow.card`：`0 2px 20px rgba(0,0,0,0.4), 0 0 40px rgba(0,0,0,0.2)`
- `shadow.button`：`0 10px 20px rgba(104,103,247,0.28)`
- `shadow.button-hover`：`0 14px 28px rgba(104,103,247,0.34)`
- `shadow.focus-ring`：`0 0 0 1px rgba(104,103,247,0.35), 0 0 0 4px rgba(104,103,247,0.18)`

### 边框 / Borders
- 默认弱白边；强调/聚焦用紫色 `border.accent`
- 避免厚实实线框

### 圆角 / Radii
- `radius.sm`：`10px`；`md`：`12px`；`lg`：`16px`；`xl`：`20px`；`pill`：`999px`

### 滚动条 / Scrollbar
- **Token**：`--scrollbar-size` `8px`；`--scrollbar-track` `transparent`；`--scrollbar-thumb` `rgba(255, 255, 255, 0.14)`；悬停 `rgba(255, 255, 255, 0.26)`；按下 `rgba(255, 255, 255, 0.34)`。
- **Firefox**：`scrollbar-width: thin`；`scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track)`。
- **WebKit**：`*::-webkit-scrollbar` 宽/高 `8px`；滑块圆角 `999px`，`border: 2px solid transparent`，`background-clip: padding-box`；轨道透明；转角透明。
- **状态**：默认 thumb → 悬停 `--scrollbar-thumb-hover` → 按下 `--scrollbar-thumb-active`。
- **主题倾向**：浅色半透明滑块（适暗底）；若派生亮色模式，需改用深色半透明滑块。


### 按钮 / Buttons
- **基础 `.btn`**：高 `42px`，`padding` `0 22px`，圆角 `var(--radius-sm)`，边框 `1px solid transparent`，字号 `14px`，字重 `600`，过渡 `background-color 0.22s var(--ease-expo), border-color 0.22s var(--ease-expo), box-shadow 0.22s var(--ease-expo), transform 0.22s var(--ease-expo)`。
- **尺寸 / 形态**：`.btn-sm` 高 `34px` / `0 14px` / `12px`；`.btn-lg` 高 `44px` / `0 26px` / `15px`；`.btn-pill` 圆角 `var(--radius-pill)`。
- **主按钮 `.btn-primary`**：背景 `--brand-primary` → `#6867f7`，文字 `#fff`，边色 `rgba(104, 103, 247, 0.85)`，投影 `--shadow-button` → `0 10px 20px rgba(104, 103, 247, 0.28)`。
- **主按钮悬停**：背景 `--brand-primary-hover` → `#7b7af9`，边色 `--brand-primary-hover` → `#7b7af9`，投影 `--shadow-button-hover` → `0 14px 28px rgba(104, 103, 247, 0.34)`，位移 `translateY(-1px)`。
- **次按钮 `.btn-secondary`**：背景 `rgba(255, 255, 255, 0.06)`，边色 `--border-strong` → `rgba(255, 255, 255, 0.12)`，文字 `--text-primary` → `#edecef`。
- **次按钮悬停**：强调色边/字 + 浅强调底（`color-mix` ≈18%）+ `translateY(-1px)` + 轻投影。
- **描边 `.btn-outline`**：透明底，边色 `--border-accent` → `rgba(104, 103, 247, 0.34)`，文字 `--text-primary` → `#edecef`。
- **描边悬停**：强调色边/字 + 浅强调底（`color-mix` ≈14%）+ `translateY(-1px)` + 轻投影。
- **幽灵 `.btn-ghost`**：透明底，边框 `1px solid var(--border-strong)`，文字 `--text-secondary` → `rgba(255, 255, 255, 0.6)`，字重 `500`。
- **幽灵悬停**：背景 `rgba(104, 103, 247, 0.12)`，文字 `--brand-primary-hover` → `#7b7af9`，`transform` `none`。
- **链接 `.btn-link`**：无边无底，色 `--brand-primary-hover` → `#7b7af9`，字号 `14px`，`gap` `6px`。
- **图标 `.btn-icon`**：`40px×40px`，圆角 `var(--radius-sm)`；悬停浅强调填充。
- **禁用 `.btn-disabled`**：`not-allowed`。
- **交互通则**：主钮悬停微抬并强化投影；次/描边悬停强调色浅染；幽灵悬停不抬升；按下可微缩放或下沉。


### 表单与反馈 / Forms & Feedback
- **标签**：`14px` / `600`，主文色，下距约 `6～10px`
- **输入**：圆角 **`12px`**，深/玻璃面 + 细发光边；占位弱文色
- **聚焦**：边转强调 `#6867f7` + 外发光环（`0 0 0 3～4px` 透明强调或柔光）
- **错误**：`.is-error` 边 `#ef4444` + 红/警告透明环；`.field-error` 短句，`role="alert"`
- **清空**：约 `28px`；悬停转强调色
- **提交行**：上距 `20px`，`gap 12`，`min-width 120px`
- **提示条**：圆角 `12px`，强调浅底 + 可带微光边
- **Toast**：顶中，实面 + **外发光/霓虹晕**（发光风保留），`220ms`

### 弹窗 / Dialog
- **遮罩**：深 scrim + `blur(12px)`；锁滚动
- **面板**：`440px` / `560px`，圆角 **`20px`**，不透明深面，**保留外发光**（发光风签名）；禁止去光变普通白卡
- **结构**：顶栏弱面 / 正文 / 脚部右对齐；头脚细分割
- **关闭**：`28×28`，圆角 `10px`；悬停发光或浅透底
- **消息型**：左圆/方图标带 glow
- **动效**：遮罩 `200ms`；面板归位 `220ms`

### 布局 / Layout
- 控制台常见：侧栏 + 主画布；卡片网格 `gap 16–24px`
- 内边距中等；数据区可更密，营销区更疏
- 强调色面积受控，留大量暗底呼吸

## 风格原则 / Style Principles
1. **紫是唯一高彩锚点**：主 CTA、聚焦、关键高亮回 `#6867F7`。
2. **薄雾卡片**：用极低 alpha 白渐变，而非厚重实色块。
3. **紫影服务按钮**：内容卡用深黑影，按钮才用紫色光晕。
4. **语义色柔和**：成功/错误用浅彩字 + 透明底，不放大色块。
5. **圆角中等偏柔**：10–20px，科技但不锐。
6. **文字降噪**：主文浅灰白，次文 60% 白。
7. **聚焦清晰**：双层紫环保证键盘可达性。
8. **动效沉稳**：expo 曲线，禁止闪烁霓虹。
9. **表单与弹窗必须保留发光外晕，禁止去光变成普通灰卡模态。**

## 提示词包

### 基础提示词

**审美方向**  
生成**暗色紫色科技感**界面：深空暗底、半透明薄雾卡片、品牌紫 `#6867F7`。使用 **Inter**，圆角 10–20px，按钮带紫色柔光投影，适合 AI/数据控制台。

**Token 约束**  
- 主色 `#6867F7` / 悬停 `#7B7AF9` / glow `rgba(104,103,247,0.28)`。  
- 主文 `#EDECEF`，次文白 60%。  
- 卡片白渐变表面；边弱白；聚焦双层紫环。  
- 按钮影 `0 10px 20px rgba(104,103,247,0.28)`；卡影深黑双层。
- 滚动条：宽 `8px`，轨道透明，滑块 `rgba(255, 255, 255, 0.14)`（悬停/按下加深）；胶囊滑块 + Firefox `thin`。


**布局约束**  
暗底呼吸充足；卡片网格整齐；侧栏与内容区分层级；首屏/概览避免多主色图表墙。

**交互约束**  
主/次/描边/幽灵按钮态齐全：主钮悬停微抬并强化投影，次与描边用强调色浅染，幽灵不抬升；主钮按下可微缩放；触控高度建议 ≥ `44px`（或沿用主题默认 `.btn` 高度）；聚焦环与品牌色协调。


**避免项**  
- 禁止改用青绿/粉红作为主品牌色。  
- 禁止高饱和满屏渐变背景。  
- 禁止去掉聚焦环。  
- 禁止浅色白天模式作为默认 DNA（变体可另述）。  
- 禁止卡片使用厚实纯白不透明块破坏薄雾感（除非对比特殊需要）。

### 组件提示词
**主按钮 `.btn-primary`**：`--brand-primary` → `#6867f7` 底，`#fff` 字，投影 `--shadow-button` → `0 10px 20px rgba(104, 103, 247, 0.28)`；悬停微抬；按下 `scale(0.95)`。
**次按钮 `.btn-secondary`**：软面/细边；悬停强调色浅底与边，微抬。
**描边 `.btn-outline`**：透明底 + 主题边；悬停强调色浅染。
**幽灵 `.btn-ghost`**：透明底，`--text-secondary` → `rgba(255, 255, 255, 0.6)` 字；悬停浅强调底，不抬升。
**尺寸族**：默认 / `.btn-sm` / `.btn-lg` / `.btn-pill`；另含 `.btn-link`、`.btn-icon`、`.btn-disabled`。

**卡片**：白 alpha 渐变 + 弱白边 + 深影。  
**输入**：soft 面 + 紫 tint 可选；聚焦紫环。  
**标签成功/错误**：对应浅彩字与透明底。  
**图表**：轴线弱白，高亮序列用品牌紫，其余降饱和。


### 变体提示词

- **更亮（仍暗色）**：soft 面 alpha +2%–4%，紫不变。  
- **更密**：看板间距降档，字号底线 `12px`。  
- **更冷**：底略偏蓝黑，紫相保持。  
- **弱光**：按钮影 alpha 降低，保留色相。

## 复用说明
- **必须保持不变**：品牌紫、薄雾卡片语言、Inter、紫聚焦环、深底、按钮紫影。  
- **可弹性调整**：侧栏有无、网格列数、语义色具体 hex（保持低刺激）、圆角在 10–20 内微调。  
- **风格跑偏风险**：霓虹粉绿混入、厚白实卡、无紫聚焦、亮色默认主题。

---

## 质量评分 / Quality Score
- **总分**：91/100
- **结论**：通过（可直接用于迭代与批量出稿）

## 分项得分 / Dimension Scores
- 风格一致性：18/20
- Token 可执行性：14/15
- 色彩与对比：14/15
- 排版层级：9/10
- 组件完整度：9/10
- 布局与间距：9/10
- 防跑偏约束：9/10
- 变体控制力：9/10

## 扣分说明 / Deductions
- 页面级精确底色在变量中偏「卡片驱动」，需实现时固定画布底色 Token。

## 关键风险 / Key Risks
- 紫光晕过强会发「游戏化」；需限制在按钮/聚焦，不扩到整卡描边发光。

## 优先修订（三项）
1. 明确 `color.surface.page` 实色值（建议近 `#0B0B12` 级）。  
2. 补齐表格行悬停与禁用态。  
3. 规定图表配色序列（紫 + 灰阶）。
