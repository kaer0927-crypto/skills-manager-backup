# 亮色科技蓝 · 视觉规范

## 风格快照 / Style Snapshot
- **整体风格 / Overall style**：浅灰页 `#F4F5F7`、白卡、品牌蓝 **`#4C75F2`** / 深 **`#3A5CCC`**。Inter 无衬线；大圆角卡片 **`20–24px`**；主 CTA / FAB 带蓝色长投影。头图对角蓝渐变 + 半透明装饰。完整反馈：字段错误红环、清空、提交行、顶中 Toast、浅蓝提示条，以及 **`24px` 圆角、不透明、柔影**弹窗。
- **语气关键词 / Tone keywords**：清爽、可信、轻仪式感、消费级 App、友好。
- **适配产品类型 / Suitable product types**：心愿清单、会员中心、权益网格、定价条、底部 Tab / FAB 类 H5 与轻应用。

> 来源：本地预览页 `亮色科技蓝-preview.html`。备份 DNA 已按当前预览补全弹窗 / 表单 / 提示规则。

## 设计 Tokens / Design Tokens
### 颜色 / Colors

**浅色（默认）**
- `color.brand.primary` → `#4C75F2`；`deep` → `#3A5CCC`
- `color.brand.rgb` → `76, 117, 242`
- `color.text.primary` → `#1A1A1A`
- `color.text.secondary` → `#999999`
- `color.text.muted` → `#A0A4B0`（Tab 未选中）
- `color.surface.base` → `#FFFFFF`
- `color.surface.soft` → `#F8F9FB`
- `color.surface.page` → `#F4F5F7`
- `color.line.soft` → `#EAECEF`；`card` → `#F3F4F6`
- `color.glow.blue` → `rgba(76, 117, 242, 0.14)`
- `color.glow.indigo` → `rgba(224, 231, 255, 0.45)`
- `color.semantic.success` → `#10B981`
- `color.semantic.warning` → `#F5A623`
- `color.semantic.danger` → `#EF4444`
- `color.semantic.premium` → `#8B5CF6`
- `color.tint.blue` → `#EEF2FF`；`amber` → `#FFF9EE`；`violet` → `#F2EEFF`；`green` → `#EEFFF5`
- `color.overlay.scrim` → `rgba(15, 23, 42, 0.55)` + `blur(12px)`

### 字体 / Typography
- `font.family.ui` → **Inter** + system-ui / PingFang / 微软雅黑
- `font.size.caption` → `11px`；`body` → `13–16px`；`title` → `17–22px`；价格可 `28px`
- `font.size.label` → `14px` / `600`
- `font.size.field-error` → `12px` / `500`
- `font.size.dialog.title` → `16px` / `700`
- `font.weight.cta` → `600`/`700`

### 背景 / Backgrounds
- 页全屏 `#F4F5F7`
- Hero：对角渐变 `#4C75F2` → `#3A5CCC`
- 头图内玻璃：白 `10–20%` + blur + 白半透明描边
- 弹窗：不透明白；禁止面板玻璃

### 阴影 / Shadows
- `shadow.card` → `0 8px 32px rgba(0,0,0,0.06)`
- `shadow.button` → `0 10px 25px rgba(76,117,242,0.3)`
- `shadow.input` → `0 4px 14px rgba(0,0,0,0.05)`
- `shadow.dropdown` → `0 12px 28px rgba(0,0,0,0.08)`
- `shadow.dock` → `0 8px 32px rgba(0,0,0,0.08)`
- `shadow.fab` → `0 12px 24px rgba(76,117,242,0.35)`
- Toast / 弹窗：双层柔影

### 边框 / Borders
- 发丝 `#EAECEF`；卡 `#F3F4F6`
- FAB 外环：`5px` 白边
- 错误：红边 + `3px`/`4px` 红环；聚焦建议蓝环

### 圆角 / Radii
- `radius.sm` → `12px`；`md` → `16px`；`lg` → `18px`；`xl` → `20px`
- `radius.card-lg` → **`24px`**（大卡 / 弹窗）
- `radius.dock` → `40px`；`pill` → `999px`
- 输入跟 `md`/`lg`（约 `16–18px`）

### 滚动条 / Scrollbar
- **Token**：`--scrollbar-size` `8px`；`--scrollbar-track` `transparent`；`--scrollbar-thumb` `rgba(0, 0, 0, 0.18)`；悬停 `rgba(0, 0, 0, 0.28)`；按下 `rgba(0, 0, 0, 0.36)`。
- **Firefox**：`scrollbar-width: thin`；`scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track)`。
- **WebKit**：`*::-webkit-scrollbar` 宽/高 `8px`；滑块圆角 `999px`，`border: 2px solid transparent`，`background-clip: padding-box`；轨道透明；转角透明。
- **状态**：默认 thumb → 悬停 `--scrollbar-thumb-hover` → 按下 `--scrollbar-thumb-active`。
- **暗色覆盖**：thumb `rgba(255, 255, 255, 0.14)`；悬停 `rgba(255, 255, 255, 0.26)`；按下 `rgba(255, 255, 255, 0.34)`。


### 按钮 / Buttons
- **基础 `.btn`**：高 `46px`，`padding` `0 22px`，圆角 `var(--radius-lg)`，边框 `1px solid transparent`，字号 `14px`，字重 `600`，过渡 `background-color .18s ease, border-color .18s ease, color .18s ease, transform .15s ease, box-shadow .18s ease`。
- **尺寸 / 形态**：`.btn-sm` 高 `36px` / `0 14px` / `12px`；`.btn-lg` 高 `52px` / `0 26px` / `15px`；`.btn-pill` 圆角 `var(--radius-pill)`。
- **主按钮 `.btn-primary`**：背景 `--brand-primary` → `#4c75f2`，文字 `#fff`，边色 `--brand-primary` → `#4c75f2`，投影 `--shadow-button` → `0 10px 25px rgba(76, 117, 242, 0.3)`。
- **主按钮悬停**：背景 `--brand-primary-deep` → `#3a5ccc`，边色 `--brand-primary-deep` → `#3a5ccc`，投影 强调色浅底（约 32% → #4c75f2），位移 `translateY(-1px)`。
- **次按钮 `.btn-secondary`**：背景 `--surface-soft` → `#f8f9fb`，边色 `--line-soft` → `#eaecef`，文字 `--text-primary` → `#1a1a1a`。
- **次按钮悬停**：强调色边/字 + 浅强调底（`color-mix` ≈18%）+ `translateY(-1px)` + 轻投影。
- **描边 `.btn-outline`**：透明底，边色 `#d1d5db`，文字 `--text-primary` → `#1a1a1a`。
- **描边悬停**：强调色边/字 + 浅强调底（`color-mix` ≈14%）+ `translateY(-1px)` + 轻投影。
- **幽灵 `.btn-ghost`**：透明底，边框 `1px solid var(--line-soft)`，文字 `--text-secondary` → `#999999`，字重 `500`。
- **幽灵悬停**：背景 `--surface-soft` → `#f8f9fb`，文字 `--brand-primary` → `#4c75f2`，`transform` `none`。
- **链接 `.btn-link`**：无边无底，色 `--brand-primary` → `#4c75f2`，字号 `14px`，`gap` `6px`。
- **图标 `.btn-icon`**：`40px×40px`，圆角 `var(--radius-sm)`；悬停浅强调填充。
- **禁用 `.btn-disabled`**：`not-allowed`。
- **交互通则**：主钮悬停微抬并强化投影；次/描边悬停强调色浅染；幽灵悬停不抬升；按下可微缩放或下沉。


### 表单与反馈 / Forms & Feedback
- **标签**：`14px` / `600`，下距 `6～10px`
- **标签体系**：中性 = 浅底 + 细边 + 次文色；强调 `.chip-accent` = 品牌蓝 `#4C75F2` 实底白字；信息 `.chip-marked` = 蓝浅底、柔边 `rgba(76,117,242,0.35)`、蓝字；选项组统一信息色系，选中 = 蓝实底白字 + 蓝柔影
- **输入**：大圆角（`16px` 级）、白底、浅边；可带 `shadow.input`；聚焦蓝环
- **错误**：`.is-error` 红边 + 红透明环；`.field-error` 短句，`role="alert"`
- **清空**：圆钮 `28px`；**提交行** 上距 `20px`，`gap 12`，`min-width 120px`
- **提示条**：圆角 `12–16px`，`--tint-blue-soft` 或 soft 面；强提示蓝实底白字
- **Toast**：顶中、大圆角、柔影，`220ms`

### 弹窗 / Dialog
- **遮罩**：半透明 + `blur(12px)`；锁滚动
- **面板**：`440px` / 内容 `560px`，圆角 **`24px`**，不透明白，柔影
- **结构**：顶栏 soft 底 / 正文 / 脚部右对齐
- **关闭**：`28×28`；消息图标圆底（警告橙 / 信息蓝）
- **动效**：遮罩 `200ms`；面板归位 `220ms`

### 布局 / Layout
- 竖屏约 `390px` 逻辑宽；`px-4`～`px-5`；`space-y-4` / `gap-3`
- 权益 `grid-cols-2 gap-3`；底栏 fixed，主区底留白 ≥`100px`
- 弹窗演示双列；`≤900px` 单列

## 风格原则 / Style Principles
1. **蓝为锚点**：强交互与选中回到 `#4C75F2`。
2. **大圆角友好**：卡 `20–24px`，弹窗跟 `24px`。
3. **彩色投影只给 CTA/FAB**：内容卡低对比黑影。
4. **语义色点状**：紫/绿/橙仅小图标底。
5. **头图仪式感**：蓝渐变 + 半透明圆 + 白字。
6. **中等密度**：`11px` 辅文到 `22px` 标题台阶清晰。
7. **动效克制**：缩放反馈与轻脉冲。
8. **浅灰白分层**：页灰卡白，层次靠表面。
9. **表单消费级**：大圆角输入 + 红环短句错误。
10. **弹窗同构**：大圆角、不透明、柔影，勿直角工具风。

## 提示词包
### 基础提示词

**审美方向**  
生成竖屏移动端界面：浅灰 `#F4F5F7` + 白卡 + 品牌蓝 `#4C75F2` 与深蓝渐变头图。Inter、大圆角、主钮蓝长影。含表单校验、浅蓝提示条、Toast、`24px` 不透明柔影弹窗。

**Token 约束**  
页 `#F4F5F7`；文 `#1A1A1A` / `#999`；蓝 `#4C75F2`/`#3A5CCC`；圆角卡 20–24、钮 18–20；钮影蓝、卡影黑灰；tint 仅小面积。
- 滚动条：宽 `8px`，轨道透明，滑块 `rgba(0, 0, 0, 0.18)`（悬停/按下加深）；胶囊滑块 + Firefox `thin`。


**布局约束**  
全宽 + `px-5`；底栏/FAB 留白；弹窗 `440～560px` 脚钮右对齐。

**交互约束**  
主/次/描边/幽灵按钮态齐全：主钮悬停微抬并强化投影，次与描边用强调色浅染，幽灵不抬升；主钮按下可微缩放；触控高度建议 ≥ `44px`（或沿用主题默认 `.btn` 高度）；聚焦环与品牌色协调。


**避免项**  
禁止同屏混金棕会员主色与科技蓝（除非主题切换）；禁止高饱和大底；禁止直角主 CTA、去蓝影；禁止正文 <`10px`；禁止弹窗玻璃半透明。

### 组件提示词
**主按钮 `.btn-primary`**：`--brand-primary` → `#4c75f2` 底，`#fff` 字，投影 `--shadow-button` → `0 10px 25px rgba(76, 117, 242, 0.3)`；悬停微抬；按下 `scale(0.95)`。
**次按钮 `.btn-secondary`**：软面/细边；悬停强调色浅底与边，微抬。
**描边 `.btn-outline`**：透明底 + 主题边；悬停强调色浅染。
**幽灵 `.btn-ghost`**：透明底，`--text-secondary` → `#999999` 字；悬停浅强调底，不抬升。
**尺寸族**：默认 / `.btn-sm` / `.btn-lg` / `.btn-pill`；另含 `.btn-link`、`.btn-icon`、`.btn-disabled`。

**会员头图**：蓝对角渐变、`24px` 圆角、白字。  
**权益卡**：白底 `20px` 圆角、tint 图标底。  
**输入**：大圆角；错误红环；圆清空。  
**底栏**：中心蓝 FAB + 灰 Tab。  
**弹窗**：`24px`、不透明、柔影；脚部蓝主钮。


### 变体提示词

- **更亮**：页趋近 `#F8F9FB`。  
- **更暗（浅色内）**：页 `#EAECEF`。  
- **更密**：`p-4→p-3`。  
- **表单确认流**：校验 + `24px` 确认弹窗。  
- **会员金棕**：仅主题切换时整套替换，勿与默认蓝混屏。

## 复用说明
- **必须保持不变**：`#4C75F2`、大圆角卡、蓝 CTA 影、浅灰白分层、Inter、字段红环、弹窗 `24px` 不透明柔影。
- **可弹性调整**：是否 FAB、权益列数、头图文案。
- **风格跑偏风险**：直角工具风、去蓝影、蓝紫混主色、弹窗毛玻璃。

---

## 质量评分 / Quality Score
- **总分**：90/100
- **结论**：通过（可直接用于 H5 / 轻应用与表单确认流）

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
- 桌面宽屏布局规范弱于竖屏 DNA。
- 聚焦环需在落地写死。

## 关键风险 / Key Risks
- 生成器易把大圆角改成 Semi 式 `3px`。
- 会员金棕皮肤易与默认蓝混用。
- 弹窗易做成小圆角后台模态。

## 优先修订（三项）
1. 写死 `focus-visible` 蓝环规格。
2. 明确输入圆角取 `16` 还是 `18`。
3. 补充宽屏断点下头图与底栏的降级规则。
