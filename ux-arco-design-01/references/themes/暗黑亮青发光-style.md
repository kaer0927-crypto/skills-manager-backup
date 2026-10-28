# 暗黑亮青发光 · 视觉规范

## 风格快照 / Style Snapshot
- **整体风格 / Overall style**：深夜蓝黑底 `#0B0F19`，亮青 `#22D3EE` 作主强调与外发光；半透明 slate 玻璃表面；Inter；卡片大圆角可达 24px，底栏 40px；气质未来感、冷静发光、偏移动端壳内原型。 完整反馈与 **`18px` 不透明柔影**弹窗。
- **语气关键词 / Tone keywords**：亮青、夜空、玻璃、发光 CTA、科技移动端。
- **适配产品类型 / Suitable product types**：暗色 App 原型、物联网/监测 H5、夜间模式工具、AI 助手移动端、带 FAB/底栏的壳内页。

> 来源：本地预览页 `暗黑亮青发光-preview.html`。备份 DNA 已按当前预览补全弹窗 / 表单。

## 设计 Tokens / Design Tokens

### 颜色 / Colors
- `color.brand.primary`：`#22D3EE`；`muted`：`rgba(34,211,238,0.1)`；`strong`：`#06B6D4`
- `color.text.primary`：`#FFFFFF`；`body`：`#E2E8F0`；`secondary`：`#94A3B8`；`muted`：`#64748B`
- `color.text.tab-inactive`：`#64748B`；`on-primary`：`#083344`（青底上的深青字）
- `color.surface.base`：`rgba(30,41,59,0.55)`；`soft`：`rgba(15,23,42,0.65)`
- `color.surface.page`：`#0B0F19`
- `color.border.subtle`：`rgba(255,255,255,0.05)`；`default`：`rgba(255,255,255,0.10)`
- `color.divider`：`rgba(255,255,255,0.05)`

### 字体 / Typography
- `font.family.ui`：`Inter`，回退 `system-ui, PingFang SC, Microsoft YaHei, Helvetica Neue, Arial, sans-serif`
- 字号台阶：辅文 `11–13px`，正文 `14–16px`，标题 `18–24px+`
- 字重 CTA `600`/`700`

### 背景 / Backgrounds
- 页面实色 `#0B0F19`
- 卡片/面板：半透明 slate + 可选 `backdrop-filter` 模糊
- 主按钮/FAB：实心亮青，形成发光焦点

### 阴影 / Shadows
- `shadow.card`：`0 25px 50px -12px rgba(0,0,0,0.45), 0 8px 16px rgba(0,0,0,0.35)`
- `shadow.dock`：`0 8px 32px rgba(0,0,0,0.4)`
- `shadow.control`：`0 1px 2px rgba(0,0,0,0.15)`
- `shadow.cta`：`0 8px 20px rgba(34,211,238,0.2)`
- `shadow.fab`：`0 12px 24px rgba(34,211,238,0.3)`
- `shadow.input`：`0 8px 24px rgba(0,0,0,0.35)`
- `shadow.dropdown`：`0 18px 34px rgba(0,0,0,0.45)`

### 边框 / Borders
- 弱白边 `0.05–0.10` alpha；分割同系
- 强调态可用青色 muted 描边

### 圆角 / Radii
- `radius.sm`/`md`：`6px`（控件可更紧）
- `radius.lg`：`16px`；`xl`：`18px`；`card`：`24px`；`dock`：`40px`；`pill`：`999px`

### 滚动条 / Scrollbar
- **Token**：`--scrollbar-size` `8px`；`--scrollbar-track` `transparent`；`--scrollbar-thumb` `rgba(255, 255, 255, 0.14)`；悬停 `rgba(255, 255, 255, 0.26)`；按下 `rgba(255, 255, 255, 0.34)`。
- **Firefox**：`scrollbar-width: thin`；`scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track)`。
- **WebKit**：`*::-webkit-scrollbar` 宽/高 `8px`；滑块圆角 `999px`，`border: 2px solid transparent`，`background-clip: padding-box`；轨道透明；转角透明。
- **状态**：默认 thumb → 悬停 `--scrollbar-thumb-hover` → 按下 `--scrollbar-thumb-active`。
- **主题倾向**：浅色半透明滑块（适暗底）；若派生亮色模式，需改用深色半透明滑块。


### 按钮 / Buttons
- **基础 `.btn`**：高 `46px`，`padding` `0 22px`，圆角 `var(--radius-xl)`，边框 `1px solid transparent`，字号 `14px`，字重 `600`，过渡 `background-color .15s ease, border-color .15s ease, transform .15s ease`。
- **尺寸 / 形态**：`.btn-sm` 高 `36px` / `0 14px` / `12px`；主色小钮字号 `13px`、字重 `700`；`.btn-lg` 高 `52px` / `0 26px` / `15px`；`.btn-pill` 圆角 `var(--radius-pill)`。
- **主按钮 `.btn-primary`**：背景 `--brand-primary` → `#22D3EE`，文字 `--text-on-primary` → `#083344`，边色 `--brand-primary` → `#22D3EE`，字重 `700`，字号 `16px`，圆角 `--radius-xl` → `18px`，投影 `--shadow-cta` → `0 8px 20px rgba(34, 211, 238, 0.2)`。
- **主按钮悬停**：背景 `--brand-primary-strong` → `#06b6d4`，边色 `--brand-primary-strong` → `#06b6d4`，投影 强调色浅底（约 32% → #22D3EE），位移 `translateY(-1px)`。
- **主按钮按下**：`scale(0.95)`。
- **次按钮 `.btn-secondary`**：背景 `--surface-soft` → `rgba(15, 23, 42, 0.65)`，边色 `--border-default` → `rgba(255, 255, 255, 0.10)`，文字 `--text-primary` → `#FFFFFF`。
- **次按钮悬停**：强调色边/字 + 浅强调底（`color-mix` ≈18%）+ `translateY(-1px)` + 轻投影。
- **描边 `.btn-outline`**：透明底，边色 `--border-default` → `rgba(255, 255, 255, 0.10)`，文字 `--text-primary` → `#FFFFFF`。
- **描边悬停**：强调色边/字 + 浅强调底（`color-mix` ≈14%）+ `translateY(-1px)` + 轻投影。
- **幽灵 `.btn-ghost`**：透明底，边框 `1px solid var(--border-default)`，文字 `--text-secondary` → `#94A3B8`，字重 `500`。
- **幽灵悬停**：强调色边/字 + 浅强调底；`transform` `none`，通常无抬升投影。
- **链接 `.btn-link`**：无边无底，色 `--brand-primary` → `#22D3EE`，字号 `14px`，`gap` `6px`。
- **图标 `.btn-icon`**：`40px×40px`，圆角 `50%`；悬停浅强调填充。
- **禁用 `.btn-disabled`**：`not-allowed`，透明度 `0.65`。
- **交互通则**：主钮悬停微抬并强化投影；次/描边悬停强调色浅染；幽灵悬停不抬升；按下 `scale(0.95)`。


### 表单与反馈 / Forms & Feedback
- **标签**：`14px` / `600`，浅字，下距约 `6～10px`
- **输入**：圆角约 `6～16px`，深面 + 细浅边；聚焦 **#22D3EE** 边 + 外发光环
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
- 移动优先竖屏；水平 `px-4`–`px-5`；底栏悬浮大圆角
- 主区底部留白给 dock/FAB
- 卡片纵向堆叠，间距 `12–16px`

## 风格原则 / Style Principles
1. **亮青为唯一发光源**：CTA/FAB/关键高亮回 `#22D3EE`。
2. **夜空底固定**：`#0B0F19` 不轻易改成纯黑或紫黑。
3. **玻璃表面半透明**：slate alpha 面板，配弱白边。
4. **青影只给行动控件**：卡片用深黑影。
5. **on-primary 深青字**：保证亮青底上的对比。
6. **大圆角壳**：卡 24 / 底栏 40 强化移动端亲和。
7. **辅文降饱和灰蓝**：`#94A3B8` / `#64748B`。
8. **发光克制**：禁止整页描边闪烁。
9. **表单与弹窗圆角/柔影与卡片 DNA 同构，面板保持不透明。**

## 提示词包

### 基础提示词

**审美方向**  
生成**暗黑亮青发光**移动界面：夜空底 `#0B0F19`、半透明 slate 玻璃卡、主色亮青 `#22D3EE`。Inter 字体，大圆角卡片与悬浮底栏，主按钮/FAB 带青色柔光。

**Token 约束**  
- 主色 `#22D3EE` / `#06B6D4`，on-primary `#083344`。  
- 文字白到 slate 灰阶；面 `rgba(30,41,59,0.55)` 等。  
- CTA 影 `0 8px 20px rgba(34,211,238,0.2)`；FAB 更强。  
- 圆角：控件 6、卡 24、dock 40。
- 滚动条：宽 `8px`，轨道透明，滑块 `rgba(255, 255, 255, 0.14)`（悬停/按下加深）；胶囊滑块 + Firefox `thin`。


**布局约束**  
竖屏单列；底栏预留；卡片堆叠；首屏避免多色霓虹。

**交互约束**  
主/次/描边/幽灵按钮态齐全：主钮悬停微抬并强化投影，次与描边用强调色浅染，幽灵不抬升；主钮按下 `scale(0.95)`；触控高度建议 ≥ `44px`（或沿用主题默认 `.btn` 高度）；聚焦环与品牌色协调。


**避免项**  
- 禁止改用荧光绿/洋红作主色。  
- 禁止浅色日间默认。  
- 禁止青底白字导致刺眼（优先深青字）。  
- 禁止直角厚实实色卡替代玻璃面。  
- 禁止满屏青色发光描边。

### 组件提示词
**主按钮 `.btn-primary`**：`--brand-primary` → `#22D3EE` 底，`--text-on-primary` → `#083344` 字，投影 `--shadow-cta` → `0 8px 20px rgba(34, 211, 238, 0.2)`；悬停微抬；按下 `scale(0.95)`。
**次按钮 `.btn-secondary`**：软面/细边；悬停强调色浅底与边，微抬。
**描边 `.btn-outline`**：透明底 + 主题边；悬停强调色浅染。
**幽灵 `.btn-ghost`**：透明底，`--text-secondary` → `#94A3B8` 字；悬停浅强调底，不抬升。
**尺寸族**：默认 / `.btn-sm` / `.btn-lg` / `.btn-pill`；另含 `.btn-link`、`.btn-icon`、`.btn-disabled`。

**卡片**：半透明 slate + 弱白边 + 深黑影 + `24px` 圆角。  
**输入**：soft 面 + 深影；聚焦青 muted。  
**Tab**：选中亮青，未选中 `#64748B`。


### 变体提示词

- **更暗**：底趋近 `#070A12`，玻璃 alpha 略降。  
- **更亮青**：主色向 `#67E8F9` 微调，on-primary 仍保持深色对比。  
- **更密**：移动列表间距降档。  
- **弱光**：CTA 影 alpha 减半，色相不变。

## 复用说明
- **必须保持不变**：夜空底、亮青主色、on-primary 深青字、玻璃 slate 面、青影 CTA、大圆角卡/底栏。  
- **可弹性调整**：是否 FAB、模糊强度、字号台阶、栅格。  
- **风格跑偏风险**：换成荧光绿 DNA、白字贴青底、去掉玻璃变纯黑实块。

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
- 语义色未在预览变量中完整展开，变体控制力略留余量。

## 关键风险 / Key Risks
- 亮青大面积使用易导致视觉疲劳；需限制为行动色。

## 优先修订（三项）
1. 增补成功/警告语义色（建议低饱和青绿/琥珀）。  
2. 明确 `backdrop-filter` 模糊 px 建议值。  
3. 补齐桌面断点下的最大宽度规则。
