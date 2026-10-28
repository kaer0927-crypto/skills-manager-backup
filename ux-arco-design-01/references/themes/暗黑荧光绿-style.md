# 暗黑荧光绿 · 视觉规范

## 风格快照 / Style Snapshot
- **整体风格 / Overall style**：纯黑近空 `#0A0A0A`，酸性荧光绿 `#D9FF00` 作主强调；深灰表面 `#121212`/`#1A1A1A`；Inter；大圆角卡 24px、底栏 40px；主 CTA/FAB 带绿黄柔光，气质酸性、高能、暗黑潮。 完整反馈与 **`18px` 不透明柔影**弹窗。
- **语气关键词 / Tone keywords**：酸性、高对比、夜店感克制版、行动发光、移动端。
- **适配产品类型 / Suitable product types**：潮牌/活动 App、电竞周边 H5、夜间工具、创意社区、带强 CTA 的暗色移动原型。

> 来源：本地预览页 `暗黑荧光绿-preview.html`。备份 DNA 已按当前预览补全弹窗 / 表单。

## 设计 Tokens / Design Tokens

### 颜色 / Colors
- `color.brand.primary`：`#D9FF00`；`muted`：`rgba(217,255,0,0.1)`；`strong`：`#C5EA00`
- `color.text.primary`：`#FFFFFF`；`body`：`#F0F0F0`；`secondary`：`#6B7280`；`muted`：`#9CA3AF`
- `color.text.tab-inactive`：`#4B5563`；`on-primary`：`#000000`（荧光绿上的黑字）
- `color.surface.base`：`#1A1A1A`；`soft`：`#121212`；`page`：`#0A0A0A`
- `color.border.subtle`：`rgba(255,255,255,0.05)`；`default`：`rgba(255,255,255,0.10)`
- `color.divider`：`rgba(255,255,255,0.05)`

### 字体 / Typography
- `font.family.ui`：`Inter`，回退 `system-ui, PingFang SC, Microsoft YaHei, Helvetica Neue, Arial, sans-serif`
- 辅文可低至 `11px`；标题加粗；CTA `600`/`700`

### 背景 / Backgrounds
- 页面 `#0A0A0A` 实色
- 卡片/面板深灰实色（可轻边），强调靠荧光绿行动色而非彩色渐变底
- 可选极弱暗角，禁止粉紫光斑抢主色

### 阴影 / Shadows
- `shadow.card`：`0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)`
- `shadow.dock`：`0 25px 50px -12px rgb(0 0 0 / 0.25)`
- `shadow.control`：`0 1px 2px rgb(0 0 0 / 0.05)`
- `shadow.cta`：`0 8px 30px rgba(217,255,0,0.2)`
- `shadow.fab`：`0 12px 24px rgba(217,255,0,0.3)`
- `shadow.input`：`0 8px 24px rgba(0,0,0,0.35)`
- `shadow.dropdown`：`0 18px 34px rgba(0,0,0,0.45)`

### 边框 / Borders
- 弱白边分层；选中可用 primary muted 边

### 圆角 / Radii
- `radius.sm`/`md`：`6px`；`lg`：`16px`；`xl`：`18px`；`card`：`24px`；`dock`：`40px`；`pill`：`999px`

### 滚动条 / Scrollbar
- **Token**：`--scrollbar-size` `8px`；`--scrollbar-track` `transparent`；`--scrollbar-thumb` `rgba(255, 255, 255, 0.14)`；悬停 `rgba(255, 255, 255, 0.26)`；按下 `rgba(255, 255, 255, 0.34)`。
- **Firefox**：`scrollbar-width: thin`；`scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track)`。
- **WebKit**：`*::-webkit-scrollbar` 宽/高 `8px`；滑块圆角 `999px`，`border: 2px solid transparent`，`background-clip: padding-box`；轨道透明；转角透明。
- **状态**：默认 thumb → 悬停 `--scrollbar-thumb-hover` → 按下 `--scrollbar-thumb-active`。
- **主题倾向**：浅色半透明滑块（适暗底）；若派生亮色模式，需改用深色半透明滑块。


### 按钮 / Buttons
- **基础 `.btn`**：高 `46px`，`padding` `0 22px`，圆角 `var(--radius-xl)`，边框 `1px solid transparent`，字号 `14px`，字重 `600`，过渡 `background-color .15s ease, border-color .15s ease, transform .15s ease`。
- **尺寸 / 形态**：`.btn-sm` 高 `36px` / `0 14px` / `12px`；主色小钮字号 `13px`、字重 `800`；`.btn-lg` 高 `52px` / `0 26px` / `15px`；`.btn-pill` 圆角 `var(--radius-pill)`。
- **主按钮 `.btn-primary`**：背景 `--brand-primary` → `#D9FF00`，文字 `--text-on-primary` → `#000000`，边色 `--brand-primary` → `#D9FF00`，字重 `900`，字号 `16px`，圆角 `--radius-xl` → `18px`，投影 `--shadow-cta` → `0 8px 30px rgba(217, 255, 0, 0.2)`。
- **主按钮悬停**：背景 `--brand-primary-strong` → `#c5ea00`，边色 `--brand-primary-strong` → `#c5ea00`，投影 强调色浅底（约 32% → #D9FF00），位移 `translateY(-1px)`。
- **主按钮按下**：`scale(0.95)`。
- **次按钮 `.btn-secondary`**：背景 `--surface-soft` → `#121212`，边色 `--border-default` → `rgba(255, 255, 255, 0.10)`，文字 `--text-primary` → `#FFFFFF`。
- **次按钮悬停**：强调色边/字 + 浅强调底（`color-mix` ≈18%）+ `translateY(-1px)` + 轻投影。
- **描边 `.btn-outline`**：透明底，边色 `--border-default` → `rgba(255, 255, 255, 0.10)`，文字 `--text-primary` → `#FFFFFF`。
- **描边悬停**：强调色边/字 + 浅强调底（`color-mix` ≈14%）+ `translateY(-1px)` + 轻投影。
- **幽灵 `.btn-ghost`**：透明底，边框 `1px solid var(--border-default)`，文字 `--text-secondary` → `#6B7280`，字重 `500`。
- **幽灵悬停**：强调色边/字 + 浅强调底；`transform` `none`，通常无抬升投影。
- **链接 `.btn-link`**：无边无底，色 `--brand-primary` → `#D9FF00`，字号 `14px`，`gap` `6px`。
- **图标 `.btn-icon`**：`40px×40px`，圆角 `50%`；悬停浅强调填充。
- **禁用 `.btn-disabled`**：`not-allowed`，透明度 `0.65`。
- **交互通则**：主钮悬停微抬并强化投影；次/描边悬停强调色浅染；幽灵悬停不抬升；按下 `scale(0.95)`。


### 表单与反馈 / Forms & Feedback
- **标签**：`14px` / `600`，浅字，下距约 `6～10px`
- **标签体系**：中性 = 深面 + 浅边 + 次文色；强调 `.chip-accent` = 荧光绿 `#D9FF00` 实底黑字；信息 `.chip-marked` = 酸浅底 `rgba(217,255,0,0.1)`、柔边 `rgba(217,255,0,0.45)`、酸字；选项组选中可走强调酸实底；徽章 = muted 酸底或酸描边 + 黑/白字按对比
- **输入**：圆角约 `6～16px`，深面 + 细浅边；聚焦 **#D9FF00** 边 + 外发光环
- **错误**：红边 + 红透明环；`.field-error` 短句
- **清空**：`28px`；提交行上距 `20px`
- **提示条**：强调浅底 + 微光边
- **Toast**：顶中，深面 + **强调色外发光**，`220ms`

### 弹窗 / Dialog
- **遮罩**：深 scrim + `blur(12px)`
- **面板**：`440/560`，圆角约 **18px～24px**，不透明深面，**保留 CTA 色外发光**（发光风签名）；禁止去光普通灰模态
- **结构**：顶栏软面 / 正文 / 脚部右对齐发光主钮
- **关闭**：`28×28`；消息图标带 glow
- **动效**：`200/220ms`

### 布局 / Layout
- 移动优先；底栏/FAB 预留；单列卡片堆叠
- 荧光绿面积严格受限：按钮、徽章、选中指示

## 风格原则 / Style Principles
1. **荧光绿即品牌**：行动与选中回到 `#D9FF00`。
2. **黑底深灰面**：页面更黑、卡略抬升。
3. **黑字贴荧光绿**：保证酸性色上的可读对比。
4. **彩影只给 CTA/FAB**：卡片用中性黑影。
5. **大圆角移动壳**：卡 24 / dock 40。
6. **灰阶辅文**：`#6B7280`/`#9CA3AF`，未选 Tab 更深。
7. **高能但克制**：不做满屏扫描线与闪烁。
8. **与亮青风格区分**：主色是黄绿酸色，不是青色。
9. **表单与弹窗圆角/柔影与卡片 DNA 同构，面板保持不透明。**

## 提示词包

### 基础提示词

**审美方向**  
生成**暗黑荧光绿**移动界面：纯黑底 `#0A0A0A`、深灰卡、酸性主色 `#D9FF00`。Inter 字体，主按钮黑字贴荧光绿并带绿黄柔光，气质高能暗黑潮，但装饰克制。

**Token 约束**  
- 主色 `#D9FF00` / `#C5EA00`，on-primary `#000000`。  
- 面 `#1A1A1A`/`#121212`；边弱白。  
- CTA 影 `0 8px 30px rgba(217,255,0,0.2)`；FAB 更强。  
- 圆角控件 6、卡 24、dock 40。
- 滚动条：宽 `8px`，轨道透明，滑块 `rgba(255, 255, 255, 0.14)`（悬停/按下加深）；胶囊滑块 + Firefox `thin`。


**布局约束**  
竖屏单列；荧光绿只作行动色；底栏留白；避免多色霓虹并存。

**交互约束**  
主/次/描边/幽灵按钮态齐全：主钮悬停微抬并强化投影，次与描边用强调色浅染，幽灵不抬升；主钮按下 `scale(0.95)`；触控高度建议 ≥ `44px`（或沿用主题默认 `.btn` 高度）；聚焦环与品牌色协调。


**避免项**  
- 禁止青/粉替换主色。  
- 禁止荧光绿大面积铺背景。  
- 禁止青底式白字（本风格 on-primary 为黑）。  
- 禁止浅色模式作为默认 DNA。  
- 禁止同时使用亮青与荧光绿双主色。

### 组件提示词
**主按钮 `.btn-primary`**：`--brand-primary` → `#D9FF00` 底，`--text-on-primary` → `#000000` 字，投影 `--shadow-cta` → `0 8px 30px rgba(217, 255, 0, 0.2)`；悬停微抬；按下 `scale(0.95)`。
**次按钮 `.btn-secondary`**：软面/细边；悬停强调色浅底与边，微抬。
**描边 `.btn-outline`**：透明底 + 主题边；悬停强调色浅染。
**幽灵 `.btn-ghost`**：透明底，`--text-secondary` → `#6B7280` 字；悬停浅强调底，不抬升。
**尺寸族**：默认 / `.btn-sm` / `.btn-lg` / `.btn-pill`；另含 `.btn-link`、`.btn-icon`、`.btn-disabled`。

**卡片**：`#1A1A1A` + 弱白边 + 黑影 + `24px`。  
**徽章**：muted 酸底或酸描边 + 黑/白字按对比选；状态类对齐标签体系（信息柔边酸字 / 选中酸实底黑字）。  
**Tab**：选中酸色，未选中 `#4B5563`。


### 变体提示词

- **更暗**：卡面趋近 `#101010`，酸色不变。  
- **更酸**：主色略提亮但仍保持黑字对比。  
- **更密**：列表间距降档。  
- **弱光**：CTA 影 alpha 减半。

## 复用说明
- **必须保持不变**：黑底、荧光绿主色、黑 on-primary、酸影 CTA、大圆角卡/底栏、Inter。  
- **可弹性调整**：FAB 有无、模糊（若加玻璃）、文案与图标。  
- **风格跑偏风险**：与亮青风格混用、酸色铺底、白字贴酸色对比不足。

---

## 质量评分 / Quality Score
- **总分**：92/100
- **结论**：通过（可直接用于迭代与批量出稿）

## 分项得分 / Dimension Scores
- 风格一致性：19/20
- Token 可执行性：15/15
- 色彩与对比：14/15
- 排版层级：9/10
- 组件完整度：9/10
- 布局与间距：9/10
- 防跑偏约束：9/10
- 变体控制力：8/10

## 扣分说明 / Deductions
- 语义色未完整声明；与「暗黑亮青发光」骨架相近，变体需强调主色差异以防混用。

## 关键风险 / Key Risks
- 两套暗黑发光风格易被模型混淆；提示词须点名「荧光绿 vs 亮青」。

## 优先修订（三项）
1. 在提示词包首句加入「禁止青色主色」硬约束。  
2. 补语义色 Token。  
3. 增加与亮青风格的对照表（一页内）。
