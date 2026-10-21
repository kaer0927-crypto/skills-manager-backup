# 暗色低饱和黑灰 · 视觉规范

## 风格快照 / Style Snapshot
- **整体风格 / Overall style**：近纯黑低饱和画布（`#030303`–`#0F0F10`），近白文字与发丝级白边；几乎无彩色品牌色，主按钮用浅亮 `#FAFAFA`；标题 Rajdhani、正文 Manrope，圆角 10–18px，气质冷静、奢简、弱情绪。 完整反馈与 **`18px` 不透明柔影**弹窗。
- **语气关键词 / Tone keywords**：克制、低饱和、高对比文字、雾面黑、沉默高级感。
- **适配产品类型 / Suitable product types**：高端品牌站、暗色作品集、极简控制台、音乐/影像产品、夜间模式优先的内容站。

> 来源：本地预览页 `暗色低饱和黑灰-preview.html`。备份 DNA 已按当前预览补全弹窗 / 表单。

## 设计 Tokens / Design Tokens

### 颜色 / Colors
- `color.surface.base`：`#030303`；`canvas`：`#060606`；`elevated`：`#111113`；`card`：`#161618`
- `color.text.primary`：`#F4F4F5`；`secondary`：`#B4B4BC`；`tertiary`：`#8B8B96`
- `color.brand.light` / `brand.primary`：`#FAFAFA`（主 CTA / 共享组件强调色；需同步 `--text-on-primary: #050505`）
- `color.brand.soft`：`rgba(250, 250, 250, 0.12)`
- `color.border.default`：`rgba(255,255,255,0.11)`；`strong`：`rgba(255,255,255,0.18)`

### 字体 / Typography
- `font.family.display`：`Rajdhani`
- `font.family.body`：`Manrope`，中文回退 `PingFang SC, Microsoft YaHei`，亦可叠 `Inter`
- 标题偏宽字距或科技感紧缩按场景二选一，但需全站一致
- `motion.ease`：`cubic-bezier(0.16, 1, 0.3, 1)`

### 背景 / Backgrounds
- 页面：近黑纯色或极轻纵向明度差（`#030303`→`#060606`）
- 卡片：相对 elevated 的实心黑灰，不做高彩玻璃
- 可有极弱噪点/渐变雾，但不得引入彩色光斑作为主视觉

### 阴影 / Shadows
- `shadow.soft`：`0 24px 80px rgba(0,0,0,0.65)`
- `shadow.card-hover`：`0 14px 30px rgba(0,0,0,0.28)`
- 阴影为黑，不为彩色外发光

### 边框 / Borders
- `1px` 半透明白边区分层级；强边 `0.14` alpha 用于输入/选中

### 圆角 / Radii
- `radius.sm`：`10px`；`md`：`14px`；`lg`/`xl`：`18px`；`pill`：`999px`

### 滚动条 / Scrollbar
- **Token**：`--scrollbar-size` `8px`；`--scrollbar-track` `transparent`；`--scrollbar-thumb` `rgba(255, 255, 255, 0.14)`；悬停 `rgba(255, 255, 255, 0.26)`；按下 `rgba(255, 255, 255, 0.34)`。
- **Firefox**：`scrollbar-width: thin`；`scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track)`。
- **WebKit**：`*::-webkit-scrollbar` 宽/高 `8px`；滑块圆角 `var(--radius-pill)`，`border: 2px solid transparent`，`background-clip: padding-box`；轨道透明；转角透明。
- **状态**：默认 thumb → 悬停 `--scrollbar-thumb-hover` → 按下 `--scrollbar-thumb-active`。
- **主题倾向**：浅色半透明滑块（适暗底）；若派生亮色模式，需改用深色半透明滑块。


### 按钮 / Buttons
- **基础 `.btn`**：高 `2.75rem`，`padding` `0.58rem 1.18rem`，圆角 `var(--radius-pill)`，边框 `1px solid transparent`，字号 `0.875rem`，字重 `600`，过渡 `background 0.2s var(--ease), border-color 0.2s var(--ease), transform 0.2s var(--ease), opacity 0.2s var(--ease)`。
- **尺寸 / 形态**：`.btn-sm` 高 `2rem` / `0 12px` / `0.8125rem`；`.btn-lg` 高 `3rem` / `0 1.35rem` / `0.92rem`；`.btn-pill` 圆角 `var(--radius-pill)`。
- **主按钮 `.btn-primary`**：背景 `--brand-light` → `#fafafa`，文字 `#050505`，边色 `#e4e4e7`。
- **主按钮悬停**：位移 `translateY(-1px)`。
- **主按钮按下**：`translateY(1px)`。
- **次按钮 `.btn-secondary`**：背景 `rgba(255, 255, 255, 0.06)`，边色 `--border-strong` → `rgba(255, 255, 255, 0.18)`，文字 `--text-primary` → `#f4f4f5`。
- **次按钮悬停**：背景 `--brand-soft` → `rgba(250, 250, 250, 0.12)`，边色 `rgba(255, 255, 255, 0.28)`，文字 `--brand-primary` → `#fafafa`，位移 `translateY(-1px)`，投影 `0 8px 20px rgba(0, 0, 0, 0.35)`。
- **描边 `.btn-outline`**：透明底，边色 `--border-strong` → `rgba(255, 255, 255, 0.18)`，文字 `--text-primary` → `#f4f4f5`。
- **描边悬停**：背景 `rgba(255, 255, 255, 0.06)`，边色 `rgba(255, 255, 255, 0.32)`，文字 `--brand-light` → `#fafafa`，位移 `translateY(-1px)`，投影 `0 8px 20px rgba(0, 0, 0, 0.32)`。
- **幽灵 `.btn-ghost`**：透明底，边框 `1px solid var(--border-default)`，文字 `--text-secondary` → `#b4b4bc`，字重 `500`。
- **幽灵悬停**：背景 `--brand-soft` → `rgba(250, 250, 250, 0.12)`，文字 `--brand-primary` → `#fafafa`，`transform` `none`。
- **链接 `.btn-link`**：无边无底，色 `--brand-light` → `#fafafa`，字号 `14px`，`gap` `6px`。
- **图标 `.btn-icon`**：`40px×40px`，圆角 `var(--radius-sm)`；悬停浅强调填充。
- **禁用 `.btn-disabled`**：`not-allowed`，透明度 `0.55`。
- **交互通则**：主钮悬停微抬并强化投影；次/描边悬停强调色浅染；幽灵悬停不抬升；按下 `translateY(1px)`。


### 表单与反馈 / Forms & Feedback
- **标签**：`14px` / `600`，主文色，下距约 `6～10px`
- **输入**：圆角 **`14px`**，表面底 + 细边；占位弱文色
- **聚焦**：边转强调 `#fafafa`；`0 0 0 3～4px` 透明环
- **错误**：`.is-error` 边 `#EF4444` + 红透明环；`.field-error` `12px/500` 短句，`role="alert"`
- **清空**：约 `28px` 圆/方圆钮；有值且聚焦/悬停出现
- **提交行**：上距 `20px`，`gap 12`，`min-width 120px`
- **提示条 `.alert`**：圆角 `14px`，浅强调底或软面 + 细边
- **Toast**：顶中，实面 + 双层柔影，`220ms` 显隐

### 弹窗 / Dialog
- **遮罩**：半透明 + `blur(12px)`；打开锁滚动
- **面板**：宽 `440px`（内容型 `560px`），圆角 **`18px`**，不透明表面，柔影；禁止面板玻璃半透明
- **结构**：顶栏（弱面 + 标题 + 关闭）/ 正文 / 脚部右对齐按钮；头脚 `1px` 分割
- **关闭**：`28×28`，圆角 `10px`；悬停浅底
- **消息型**：左圆图标——警告/信息语义，带柔影
- **内容型**：内嵌面板、列表、芯片、表单
- **动效**：遮罩 `200ms`；面板 `translateY(10px) scale(0.98)` → 归位 `220ms`

### 布局 / Layout
- 大留白、少卡片；桌面宽容器但内容列宜窄以利阅读
- 区块间距偏大（`32–72px`）；避免仪表盘式多色指标墙
- 首屏以品牌字形与一句文案为主，弱化彩色插图依赖

## 风格原则 / Style Principles
1. **无彩色主品牌**：情绪靠黑白灰阶，不作第二高饱和色。
2. **表面阶梯细微**：base/canvas/elevated/card 四级递进。
3. **发丝白边**：边界靠半透明白，不靠厚描边。
4. **双字体**：Rajdhani 标题、Manrope 正文。
5. **投影深但干净**：大范围黑影，无色相。
6. **圆角中等**：10–18px，既不锋利街头也不气泡化。
7. **沉默交互**：悬停只改明度/边，不闪彩。
8. **文字对比优先**：主文近白，辅文锌灰，保证可读。
9. **表单与弹窗圆角/柔影与卡片 DNA 同构，面板保持不透明。**

## 提示词包

### 基础提示词

**审美方向**  
生成**暗色低饱和黑灰**界面：近黑画布、近白文字、主 CTA 用浅亮 `#FAFAFA`。标题 **Rajdhani**，正文 **Manrope**。整体奢简、冷静、低饱和，禁止霓虹与彩色渐变主题。

**Token 约束**  
- 表面 `#030303` / `#060606` / `#0C0C0C` / `#0F0F10`。  
- 文字 `#F4F4F5` / `#A1A1AA` / `#71717A`。  
- 边 `rgba(255,255,255,0.08–0.14)`；主强调 `#FAFAFA` 与 soft `rgba(250,250,250,0.12)`。  
- 圆角 10–18；阴影仅黑色深影。
- 滚动条：宽 `8px`，轨道透明，滑块 `rgba(255, 255, 255, 0.14)`（悬停/按下加深）；胶囊滑块 + Firefox `thin`。


**布局约束**  
疏朗留白；少而精的分区；首屏单焦点；卡片轻量，勿彩色图标矩阵。

**交互约束**  
主/次/描边/幽灵按钮态齐全：主钮悬停微抬并强化投影，次与描边用强调色浅染，幽灵不抬升；主钮按下 `translateY(1px)`；触控高度建议 ≥ `44px`（或沿用主题默认 `.btn` 高度）；聚焦环与品牌色协调。


**避免项**  
- 禁止紫/蓝/绿霓虹主色与外发光。  
- 禁止浅色模式默认（本风格以暗色为 DNA）。  
- 禁止大面积高饱和插画抢层级。  
- 禁止把主按钮做成彩色实心。  
- 禁止玻璃拟态过重导致发雾发灰、对比崩溃。

### 组件提示词
**主按钮 `.btn-primary`**：`--brand-light` → `#fafafa` 底，`#050505` 字，投影 —；悬停微抬；按下 `translateY(1px)`。
**次按钮 `.btn-secondary`**：软面/细边；悬停强调色浅底与边，微抬。
**描边 `.btn-outline`**：透明底 + 主题边；悬停强调色浅染。
**幽灵 `.btn-ghost`**：透明底，`--text-secondary` → `#b4b4bc` 字；悬停浅强调底，不抬升。
**尺寸族**：默认 / `.btn-sm` / `.btn-lg` / `.btn-pill`；另含 `.btn-link`、`.btn-icon`、`.btn-disabled`。

**卡片**：`#0F0F10` + 弱白边 + 深影；悬停 `shadow.card-hover`。  
**输入**：深面、强白边聚焦。  
**导航**：透明底，选中近白字加重。  
**分割线**：`border.default` 发丝线。


### 变体提示词

- **更亮（仍暗色）**：卡面提到 `#141414`，文字层级不变。  
- **更密**：间距降档，保留对比。  
- **微冷/微暖**：仅允许极轻微蓝/褐偏移（几乎不可辨），禁止可命名彩色品牌。  
- **反相浅色**：若必须日间模式，反相灰白并保持无彩色主色与字体栈。

## 复用说明
- **必须保持不变**：低饱和黑灰阶、浅亮 CTA、Rajdhani+Manrope、无彩色霓虹、发丝白边。  
- **可弹性调整**：留白量、卡片数量、是否轻噪点、容器宽度。  
- **风格跑偏风险**：加入品牌蓝/紫、外发光、过度玻璃、圆角过大变软萌。

---

## 质量评分 / Quality Score
- **总分**：90/100
- **结论**：通过（可直接用于迭代与批量出稿）

## 分项得分 / Dimension Scores
- 风格一致性：19/20
- Token 可执行性：14/15
- 色彩与对比：13/15
- 排版层级：9/10
- 组件完整度：8/10
- 布局与间距：9/10
- 防跑偏约束：9/10
- 变体控制力：9/10

## 扣分说明 / Deductions
- 语义色几乎缺失（风格使然），组件完整度与色彩维度略扣；需在业务中单独定义成功/错误色且保持低饱和。

## 关键风险 / Key Risks
- 纯黑灰界面易导致状态不可辨，必须另设低饱和语义色规范。

## 优先修订（三项）
1. 增补低饱和成功/警告/错误色（建议灰绿/灰琥珀/灰红）。  
2. 明确主按钮字色（近黑）对比达标。  
3. 补充表格与空状态样式，避免「有色插画」破坏 DNA。
