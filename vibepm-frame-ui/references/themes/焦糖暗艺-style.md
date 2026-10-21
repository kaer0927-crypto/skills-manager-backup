# 焦糖暗艺 · 视觉规范

## 风格快照 / Style Snapshot
- **整体风格 / Overall style**：焦糖暗艺——近黑暖棕画布 `#0d0a06` + 双层暖橙径向光晕 + 米白主字 `#f3ead8`；**Fraunces** 展示 / **JetBrains Mono** 标签 / **Inter** 正文；卡片内高光 + 重外影，轻拼贴杂志感。完整反馈：字段错误环、清空、提交行、Toast、橙浅底提示条，以及 **`18px` 圆角、不透明、柔影**弹窗（遮罩可 blur）。
- **语气关键词 / Tone keywords**：焦糖、文艺、编辑感、轻拼贴、克制高光、暗场暖橙。
- **适配产品类型 / Suitable product types**：开源工具封面、设计系统推介单页、暗色落地页首屏、含确认流的暗色营销页。

> 来源：本地预览页 `焦糖暗艺-preview.html`。已合并工程对照表与技能版式，并补全弹窗 / 表单。

## 设计 Tokens / Design Tokens
### 颜色 / Colors
- `color.surface.base` → `#0d0a06`；`deep` → `#14100a`；`card` → `#1a140d`
- `color.ink.primary` → `#f3ead8`；`lede` → `#d8cdb6`；`muted` → `#9b8f78`
- `color.brand.accent` → `#f0833f`；`accent-strong` → `#e85a2c`
- `color.border.rule` → `#4a3f2c`
- `color.paper.highlight` → `#f6efdd` / 药丸字 `#f6e9d4`
- `color.tag.ink` → `#ffd9b6`；`badge.ink` → `#2a1408`
- `color.semantic.danger` → `#e85a4a`
- `color.overlay.scrim` → `rgba(0, 0, 0, 0.62)` + `blur(12px)`
- 药丸底 `rgba(240,131,63,0.16)` / 边 `rgba(240,131,63,0.45)`；面板底 `rgba(20,16,10,0.45)`

### 字体 / Typography
- `font.family.display` → `Fraunces, serif`（标题 / 导语）
- `font.family.mono` → `JetBrains Mono, ui-monospace, monospace`（标签 / 元信息，常大写宽字距）
- `font.family.sans` → `Inter, system-ui, sans-serif`（段落）
- 主标题：Fraunces `500`，`clamp(32px, 4vw, 48px)`，`line-height: 1.1`，`letter-spacing: -0.02em`；关键词斜体 + accent
- 导语：Fraunces `300`，`17～20px`，色 `--lede`
- 正文：Inter `15px` / `1.55`
- 等宽元信息：`11px`，`letter-spacing: 0.2em`，uppercase
- 标签 / 错误：`14px/600`；`field-error` `12px/500`；弹窗标题 `16px/700`（Inter，不用英雄展示字）

### 背景 / Backgrounds
- 底叠：`linear-gradient(180deg, #0e0b07, #0a0805)` + 右上径向 `rgba(240,131,63,0.14)` + 左下 `rgba(232,90,44,0.08)`
- 面板半透明深底；弹窗改为不透明 `--card-surface` / `#1a140d`
- 禁止纯平面 `#000` 无光晕

### 阴影 / Shadows
- `shadow.card` → `inset 0 1px 0 rgba(255,255,255,0.04), 0 24px 60px rgba(0,0,0,0.55), 0 6px 18px rgba(0,0,0,0.45)`
- 徽章：`0 12px 26px rgba(232,90,44,0.45)`
- Toast / 弹窗：沿用双层暗场柔影；禁止硬偏移

### 边框 / Borders
- 发线 `#4a3f2c`；面板 / 卡 `rgba(255,255,255,0.06)`
- 输入聚焦橙边 + 透明环；错误红边 + `3～4px` 环
- 弹窗头脚 `1px` rule 分割

### 圆角 / Radii
- `radius.card` / 弹窗 → `18px`；`pill` → `999px`；`tag` → `6px`；色板 `12px`；下划线装饰 `4px`
- 关闭钮约 `6px`；输入约 `8px`

### 滚动条 / Scrollbar
- **Token**：`--scrollbar-size` `8px`；`--scrollbar-track` `transparent`；`--scrollbar-thumb` `rgba(255, 255, 255, 0.14)`；悬停 `rgba(255, 255, 255, 0.26)`；按下 `rgba(255, 255, 255, 0.34)`。
- **Firefox**：`scrollbar-width: thin`；`scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track)`。
- **WebKit**：`*::-webkit-scrollbar` 宽/高 `8px`；滑块圆角 `999px`，`border: 2px solid transparent`，`background-clip: padding-box`；轨道透明；转角透明。
- **状态**：默认 thumb → 悬停 `--scrollbar-thumb-hover` → 按下 `--scrollbar-thumb-active`。
- **主题倾向**：浅色半透明滑块（适暗底）；若派生亮色模式，需改用深色半透明滑块。


### 按钮 / Buttons
- **基础 `.btn`**：高 `46px`，`padding` `12px 24px`，圆角 `var(--r-panel)`，边框 `1px solid transparent`，字号 `16px`，字重 `500`，过渡 `all 250ms ease-in-out`。
- **尺寸 / 形态**：`.btn-sm` 高 `36px` / `10px 20px` / `14px`；`.btn-lg` 高 `52px` / `16px 32px` / `18px`；`.btn-pill` 圆角 `var(--r-pill)`。
- **主按钮 `.btn-primary`**：背景 `--accent` → `#f0833f`，文字 `--ink-on-accent` → `#2a1408`，边色 `--accent` → `#f0833f`。
- **主按钮悬停**：投影 `--shadow-accent` → `0px 10px 28px rgba(232, 90, 44, 0.35)`，位移 `translateY(-1px)`，滤镜 `brightness(1.06)`。
- **主按钮按下**：`scale(0.97) translateY(0)`。
- **次按钮 `.btn-secondary`**：背景 `--surface1` → `#14100a`，边色 `--n-200` → `#4a3f2c`，文字 `--text1` → `#f3ead8`。
- **次按钮悬停**：强调色边/字 + 浅强调底（`color-mix` ≈18%）+ `translateY(-1px)` + 轻投影。
- **描边 `.btn-outline`**：透明底，边色 `--n-200` → `#4a3f2c`，文字 `--text1` → `#f3ead8`。
- **描边悬停**：强调色边/字 + 浅强调底（`color-mix` ≈14%）+ `translateY(-1px)` + 轻投影。
- **幽灵 `.btn-ghost`**：透明底，边框 `1px solid var(--n-200)`，文字 `--text2` → `#d8cdb6`，字重 `500`。
- **幽灵悬停**：背景 `--b-50` → `rgba(240, 131, 63, 0.16)`，文字 `--accent` → `#f0833f`，`transform` `none`。
- **链接 `.btn-link`**：无边无底，色 `--accent` → `#f0833f`，字号 `14px`，`gap` `6px`。
- **图标 `.btn-icon`**：`40px×40px`，圆角 `var(--r-el)`；悬停浅强调填充。
- **禁用 `.btn-disabled`**：`not-allowed`，透明度 `0.75`。
- **交互通则**：主钮悬停微抬并强化投影；次/描边悬停强调色浅染；幽灵悬停不抬升；按下 `scale(0.97) translateY(0)`。


### 表单与反馈 / Forms & Feedback
- **表单辅助图标（统一偏小、偏淡）**：下拉 `.combo-chevron` 约 `9px`；步进器按钮约 `22×22` / 图标 `10px`；清空 `.input-clear` 约 `20×20` / `11px`；均用 muted + 透明度约 `0.72`
- **标签**：`14px` / `600` / 米白主字
- **标签体系**：中性 = 深表面 + 细边 + 次文色；强调 `.chip-accent` = 暖橙 `#f0833f` 实底 + `ink-on-accent`；信息 `.chip-marked` = 浅底、柔边 `color-mix(accent 42%, n-200)`、橙字；选项组统一信息色系，选中 = 橙实底 + 轻彩影（与药丸双态并存时保持同一橙轴）
- **输入**：圆角 `8px`，深表面 + 细边；占位 muted
- **聚焦**：边 `#f0833f` + `3～4px` 橙环
- **错误**：`.is-error` `#e85a4a` 边 + 红环；`.field-error` 短句
- **清空 / 提交行 / Toast**：同族暗场实面；Toast 顶中 `220ms`
- **提示条**：圆角 `8px`，橙浅底或 panel 面

### 弹窗 / Dialog
- **遮罩**：深半透明 + `blur(12px)`
- **面板**：`440～560px`，圆角 **`18px`**，不透明 `#1a140d`，柔影；禁止半透明吞字
- **结构**：顶栏弱面 + 关闭 / 正文 / 脚部右对齐
- **消息型**：左圆图标（警告可用橙谱）；**内容型**可嵌表单
- **动效**：遮罩 `200ms`；面板归位 `220ms`

### 布局 / Layout
- 页边：上 `56px`、左右 `72px`、下 `72px`
- 顶/底栏：`1fr auto 1fr`；主栅 ≥960px：`1.15fr 0.85fr`，`gap 24px`
- 拼贴区 `min-height ~320px`；间距台阶 `12/16/24`
- 弹窗演示 `≤900px` 单列

## 风格原则 / Style Principles
1. **底在场**：近黑暖棕 + 双径向光，避免纯平面黑。
2. **字色偏纸**：主字米白带暖，勿改冷白。
3. **强调只用暖橙谱系**，不引入冷紫青主强调。
4. **字族三角**：Fraunces / Mono / Inter 分工清晰。
5. **分割细而暖**：`#4a3f2c` 单像素线。
6. **卡片沉在景里**：内高光 + 重外影；拼贴微旋转 ≤±6°。
7. **表单反馈克制**：红环短句，不用大红底块。
8. **弹窗不透明**：与半透明 panel 刻意区分。
9. **药丸双态**：主橙 tint / 次 rule 边，勿两枚同权重；状态 Chip 走标签体系（信息柔边橙字 / 选中橙实底）。
10. **留白节奏**：页边与 `12/16/24` 台阶优先。

## 提示词包
### 基础提示词

**审美方向**  
生成「焦糖暗底、文艺展示字」界面：深暖棕 + 双团暖橙径向光；Fraunces 标题（一词斜体橙强调）+ Mono 标签 + Inter 段落。含表单错误环、Toast、以及 `18px` 不透明柔影弹窗。气质沉稳编辑感——非赛博霓虹、非玻璃泛滥。

**Token 约束**  
底 `#0d0a06`；字 `#f3ead8` / `#9b8f78`；强调 `#f0833f`；线 `#4a3f2c`；卡 `#1a140d` + 三段式 `shadow.card`。圆角卡/弹窗 `18px`。弹窗遮罩可 blur，面板必须不透明。
- 滚动条：宽 `8px`，轨道透明，滑块 `rgba(255, 255, 255, 0.14)`（悬停/按下加深）；胶囊滑块 + Firefox `thin`。


**布局约束**  
页边约 `56/72`；宽屏双列 `1.15/0.85`；弹窗 `440～560px` 脚钮右对齐。

**交互约束**  
主/次/描边/幽灵按钮态齐全：主钮悬停微抬并强化投影，次与描边用强调色浅染，幽灵不抬升；主钮按下 `scale(0.97) translateY(0)`；触控高度建议 ≥ `44px`（或沿用主题默认 `.btn` 高度）；聚焦环与品牌色协调。


**避免项**  
禁止冷蓝紫大底、纯黑无光晕、纯白正文、粗重冷灰分割、拼贴旋转过大、弹窗半透明玻璃、大红底块错误态。

### 组件提示词
**主按钮 `.btn-primary`**：`--accent` → `#f0833f` 底，`--ink-on-accent` → `#2a1408` 字，投影 —；悬停微抬；按下 `scale(0.97) translateY(0)`。
**次按钮 `.btn-secondary`**：软面/细边；悬停强调色浅底与边，微抬。
**描边 `.btn-outline`**：透明底 + 主题边；悬停强调色浅染。
**幽灵 `.btn-ghost`**：透明底，`--text2` → `#d8cdb6` 字；悬停浅强调底，不抬升。
**尺寸族**：默认 / `.btn-sm` / `.btn-lg` / `.btn-pill`；另含 `.btn-link`、`.btn-icon`、`.btn-disabled`。

顶底三栏 mono + 中缝 Fraunces 斜体橙点；主标题 Fraunces；panel 半透明深底；药丸双态；拼贴卡 + 角标 blur；圆形橙徽章；表单错误环；不透明弹窗。


### 变体提示词
- **更亮暗场**：底提至 `#12100c`，主字仍米白系。  
- **更暖**：径向略偏杏，accent 略向黄，勿荧光。  
- **更密 / 更疏**：只调 `gap` 与页边，色与字族不变。  
- **表单确认流**：保留封面叙事，加入校验 + 确认弹窗。

## 复用说明
- **必须保持不变**：暗暖棕 + 米白 + 暖橙三角；三字体分工；卡内高光重影；rule 分割；字段错误红环；弹窗不透明。
- **可弹性调整**：径向位置/透明度、标题 clamp、拼贴角度、panel 浓度。
- **风格跑偏风险**：强调改洋红/电青；去掉径向只剩扁平黑；弹窗做成玻璃半透明。

---

## 质量评分 / Quality Score
- **总分**：90/100
- **结论**：通过（可直接用于暗色封面与表单确认流）

## 分项得分 / Dimension Scores
- 风格一致性：18/20
- Token 可执行性：14/15
- 色彩与对比：13/15
- 排版层级：9/10
- 组件完整度：9/10
- 布局与间距：9/10
- 防跑偏约束：9/10
- 变体控制力：9/10

## 扣分说明 / Deductions
- 药丸等局部仍有硬编码 rgba，宜继续收进 `:root`。
- 需在落地补全全量 `hover` / `focus-visible` 示例。

## 关键风险 / Key Risks
- 长文全程 Fraunces 小字可读性不足，段落须回退 Inter。
- 高饱和摄影可能与径向光竞争。
- 弹窗若沿用半透明 panel 会吞字。

## 优先修订（三项）
1. 药丸 / 角标色迁入命名 token。
2. 为可交互控件补 `focus-visible` 与轻量悬停。
3. 暗场抽样复核对比度，优先微调 muted/lede 而非改强调色相。
