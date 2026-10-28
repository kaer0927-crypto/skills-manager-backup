# 暗粉霓虹潮 · 视觉规范

## 风格快照 / Style Snapshot
- **整体风格 / Overall style**：近黑品红底（`#07040B` 系）与骨白浅色主题可切换；主强调热粉洋红（暗 `#FF3A8C` / 亮 `#E41874`），电黄点缀数据与徽章；Space Grotesk 展示 + Inter 正文 + JetBrains Mono 标签；圆角偏锐（2–6px），街头潮牌与暗色 SaaS 混合。 完整反馈与 **`6px` 不透明柔影**弹窗。
- **语气关键词 / Tone keywords**：锐利、霓虹、低多边形张力、大小写混排、系统感标签、editorial 节奏。
- **适配产品类型 / Suitable product types**：潮流电商、寄售/拍卖、创作者工具、暗色品牌官网、强调时间戳/账本感的落地页。

> 来源：本地预览页 `暗粉霓虹潮-preview.html`。备份 DNA 已按当前预览补全弹窗 / 表单。

## 设计 Tokens / Design Tokens

### 颜色 / Colors
**浅色主题**
- `color.surface.page`：`#F7F5F8`；`surface`：`#FFFBFE`；`surface1`：`#F1EAEF`
- `color.text.primary`：`#07040B`；`secondary`：`#45404D`；`tertiary`：`#6B6574`
- `color.brand.primary`：`#E41874`；`hover`：`#C41466`；`subtle`：`rgba(228,24,116,0.18)`；`tint`：`#FFECF4`
**暗色主题**
- `color.surface.page`：`#07040B`；`surface`：`#141118`；`surface1`：`#221F26`
- `color.text.primary`：`#F7F5F8`；`secondary`：`#D8D3DE`；`tertiary`：`#B2ABBC`
- `color.brand.primary`：`#FF3A8C`；`hover`：`#FF6BA7`；`subtle`：`rgba(255,58,140,0.22)`
**共用**
- `color.accent.electric`：`#E5D300`；`color.accent.electric-soft`：`#F8F06A`
- `color.semantic.danger`：`#E5484D`；`color.semantic.success`：`#5CB13E`
- `color.border.muted`：浅 `#E4DAE4` / 暗 `#35303A`

### 字体 / Typography
- `font.family.display`：`Space Grotesk`
- `font.family.body`：`Inter`
- `font.family.mono`：`JetBrains Mono`
- 展示标题：紧字距、可全大写；等宽标签：`9–11px`、大写、字距 `0.08–0.18em`
- 正文约 `15px`、行高 `~1.55`

### 背景 / Backgrounds
- 暗色首屏：近黑底 + 径向洋红光晕 + 斜向暗角
- 面板：`color-mix` 半透明表面或实心 elevated
- 浅色：骨白/藕粉灰分层，强调色作点缀而非铺底

### 阴影 / Shadows
**浅**：`shadow-1` `0 4px 22px rgba(7,4,11,0.08)` → `shadow-3` `0 16px 48px rgba(7,4,11,0.16)`；强调 `0 8px 28px rgba(228,24,116,0.28)`
**暗**：黑影 alpha `0.45–0.55`；强调 `0 8px 40px rgba(255,58,140,0.45)`
- Hero 卡：`shadow-hero-card` 大范围深影

### 边框 / Borders
- 细 `1px`；暗色用 elevated 灰紫边；浅色用藕灰 `#E4DAE4`
- 强调态可用洋红 subtle 内光/描边

### 圆角 / Radii
- `radius.el`：`2px`；`card`：`6px`；`panel`：`4px`；`pill`：`100px`（仅标签/开关）
- 主按钮与卡片保持**小圆角锐利感**，勿全面胶囊化

### 滚动条 / Scrollbar
- **Token**：`--scrollbar-size` `8px`；`--scrollbar-track` `transparent`；`--scrollbar-thumb` `rgba(0, 0, 0, 0.18)`；悬停 `rgba(0, 0, 0, 0.28)`；按下 `rgba(0, 0, 0, 0.36)`。
- **Firefox**：`scrollbar-width: thin`；`scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track)`。
- **WebKit**：`*::-webkit-scrollbar` 宽/高 `8px`；滑块圆角 `999px`，`border: 2px solid transparent`，`background-clip: padding-box`；轨道透明；转角透明。
- **状态**：默认 thumb → 悬停 `--scrollbar-thumb-hover` → 按下 `--scrollbar-thumb-active`。
- **暗色覆盖**：thumb `rgba(255, 255, 255, 0.14)`；悬停 `rgba(255, 255, 255, 0.26)`；按下 `rgba(255, 255, 255, 0.34)`。


### 按钮 / Buttons
- **基础 `.btn`**：高 `46px`，`padding` `12px 24px`，圆角 `var(--r-panel)`，边框 `1px solid transparent`，字号 `16px`，字重 `500`，过渡 `all 250ms ease-in-out`。
- **尺寸 / 形态**：`.btn-sm` 高 `36px` / `10px 20px` / `14px`；`.btn-lg` 高 `52px` / `16px 32px` / `18px`；`.btn-pill` 圆角 `var(--r-pill)`。
- **主按钮 `.btn-primary`**：背景 `--accent` → `#E41874`，文字 `#030105`，边色 `--accent` → `#E41874`。
- **主按钮悬停**：投影 `--shadow-accent` → `0px 8px 28px rgba(228, 24, 116, 0.28)`，位移 `translateY(-1px)`。
- **主按钮按下**：`scale(0.97) translateY(0)`。
- **次按钮 `.btn-secondary`**：背景 `--surface1` → `#F1EAEF`，边色 `--n-200` → `#E4DAE4`，文字 `--text1` → `#07040B`。
- **次按钮悬停**：强调色边/字 + 浅强调底（`color-mix` ≈18%）+ `translateY(-1px)` + 轻投影。
- **描边 `.btn-outline`**：透明底，边色 `--n-200` → `#E4DAE4`，文字 `--text1` → `#07040B`。
- **描边悬停**：强调色边/字 + 浅强调底（`color-mix` ≈14%）+ `translateY(-1px)` + 轻投影。
- **幽灵 `.btn-ghost`**：透明底，边框 `1px solid var(--n-200)`，文字 `--text2` → `#45404D`，字重 `500`。
- **幽灵悬停**：背景 `--b-50` → `#FFECF4`，文字 `--accent` → `#E41874`，`transform` `none`。
- **链接 `.btn-link`**：无边无底，色 `--accent` → `#E41874`，字号 `14px`，`gap` `6px`。
- **图标 `.btn-icon`**：`40px×40px`，圆角 `var(--r-el)`；悬停浅强调填充。
- **禁用 `.btn-disabled`**：`not-allowed`，透明度 `0.75`。
- **暗色覆盖**：暗色主色 `--accent` → #FF3A8C（浅色为 #E41874）。
- **交互通则**：主钮悬停微抬并强化投影；次/描边悬停强调色浅染；幽灵悬停不抬升；按下 `scale(0.97) translateY(0)`。


### 表单与反馈 / Forms & Feedback
- **标签**：`14px` / `600`，主文色，下距约 `6～10px`
- **标签体系**：中性 = 表面底 + 细边 + 次文色、锐角；强调 `.chip-accent` = 洋红实底 + 近黑字 `#030105`；信息 `.chip-marked` = 浅底、柔边 `color-mix(accent 45%, n-200)`、洋红字；选项组统一信息色系，选中 = 洋红实底近黑字 + 轻彩影；徽章可电黄软底或洋红描边
- **输入**：圆角 **`4px`**，表面底 + 细边；占位弱文色
- **聚焦**：边转强调 `#E41874`；`0 0 0 3～4px` 透明环
- **错误**：`.is-error` 边 `#E5484D` + 红透明环；`.field-error` `12px/500` 短句，`role="alert"`
- **清空**：约 `28px` 圆/方圆钮；有值且聚焦/悬停出现
- **提交行**：上距 `20px`，`gap 12`，`min-width 120px`
- **提示条 `.alert`**：圆角 `4px`，浅强调底或软面 + 细边
- **Toast**：顶中，实面 + 双层柔影，`220ms` 显隐

### 弹窗 / Dialog
- **遮罩**：半透明 + `blur(12px)`；打开锁滚动
- **面板**：宽 `440px`（内容型 `560px`），圆角 **`6px`**，不透明表面，柔影；禁止面板玻璃半透明
- **结构**：顶栏（弱面 + 标题 + 关闭）/ 正文 / 脚部右对齐按钮；头脚 `1px` 分割
- **关闭**：`28×28`，圆角 `2px`；悬停浅底
- **消息型**：左圆图标——警告/信息语义，带柔影
- **内容型**：内嵌面板、列表、芯片、表单
- **动效**：遮罩 `200ms`；面板 `translateY(10px) scale(0.98)` → 归位 `220ms`

### 布局 / Layout
- 首屏可「巨型展示字 + 底部磨砂信息条」叠层
- 内容宽栏与窄栏交替；等宽元信息行增强系统感
- 桌面大留白与高密度信息块交替，避免均匀网格填满

## 风格原则 / Style Principles
1. **洋红为情绪锚**：主 CTA / 关键词高亮统一热粉系。
2. **电黄只作数据点缀**：涨跌、new 徽章，面积严格受限。
3. **锐角几何**：2–6px 圆角是 DNA，不能改成大圆角软 UI。
4. **三字体分工**：展示 / 正文 / 等宽标签各司其职。
5. **明暗双主题共骨架**：只换表面与强调明度，不改圆角与字体。
6. **光晕克制**：洋红光斑服务层次，禁止满屏闪烁动画。
7. **大小写叙事**：展示可用全大写，章节标题可小写制造张力。
8. **对比优先**：暗底骨白字、浅底近黑字，辅文降一级。
9. **表单与弹窗圆角/柔影与卡片 DNA 同构，面板保持不透明。**

## 提示词包

### 基础提示词

**审美方向**  
生成**暗粉霓虹潮**界面：默认暗色近黑品红底，主强调热粉洋红，电黄作数据点缀。使用 **Space Grotesk + Inter + JetBrains Mono**，小圆角（2–6px），气质锐利、潮、带 editorial 排版张力。支持切换浅色骨白主题。

**Token 约束**  
- 暗：底 `#07040B`，面 `#141118`/`#221F26`，强调 `#FF3A8C`。  
- 浅：底 `#F7F5F8`，强调 `#E41874`。  
- 电黄 `#E5D300` / `#F8F06A` 仅小面积。  
- 圆角 el/card/panel = 2/6/4；阴影用主题对应阶梯；强调按钮带洋红影。
- 滚动条：宽 `8px`，轨道透明，滑块 `rgba(0, 0, 0, 0.18)`（悬停/按下加深）；胶囊滑块 + Firefox `thin`。


**布局约束**  
允许巨型展示标题与暗角叠层；信息条可用磨砂；正文栏宽可读；元数据用等宽小标签。勿做成圆角气泡社交 App。

**交互约束**  
主/次/描边/幽灵按钮态齐全：主钮悬停微抬并强化投影，次与描边用强调色浅染，幽灵不抬升；主钮按下 `scale(0.97) translateY(0)`；触控高度建议 ≥ `44px`（或沿用主题默认 `.btn` 高度）；聚焦环与品牌色协调。


**避免项**  
- 禁止大圆角（≥16px）作为默认卡片语言。  
- 禁止紫靛渐变替换洋红主色。  
- 禁止电黄大面积铺底。  
- 禁止去掉等宽标签导致「系统感」流失。  
- 禁止亮暗 Token 混用在同一未声明主题的页面。

### 组件提示词
**主按钮 `.btn-primary`**：`--accent` → `#E41874` 底，`#030105` 字，投影 —；悬停微抬；按下 `scale(0.97) translateY(0)`。
**次按钮 `.btn-secondary`**：软面/细边；悬停强调色浅底与边，微抬。
**描边 `.btn-outline`**：透明底 + 主题边；悬停强调色浅染。
**幽灵 `.btn-ghost`**：透明底，`--text2` → `#45404D` 字；悬停浅强调底，不抬升。
**尺寸族**：默认 / `.btn-sm` / `.btn-lg` / `.btn-pill`；另含 `.btn-link`、`.btn-icon`、`.btn-disabled`。

**徽章**：电黄软底或洋红描边，文案可全大写等宽；状态类优先走标签体系（信息柔边洋红字 / 选中洋红实底）。  
**卡片**：elevated 面 + 细边 + 小圆角；悬停加深影。  
**输入**：深/浅面，聚焦洋红 subtle。  
**导航**：近透明底，选中洋红字或短下划线。


### 变体提示词

- **更暗**：底趋近 `#030105`，光晕 alpha 略增，文字保持骨白。  
- **更亮（浅主题）**：表面更接近 `#FFFBFE`，强调仍 `#E41874`。  
- **更密**：缩小区块间距，展示字号可略降但保持紧字距。  
- **更暖**：仅允许背景光晕偏玫红，不改主 Token 色相命名。

## 复用说明
- **必须保持不变**：洋红主色、小圆角、三字体栈、电黄点缀逻辑、明暗两套表面阶梯。  
- **可弹性调整**：光晕强度、展示字大小写、是否启用浅色主题、信息密度。  
- **风格跑偏风险**：改成大圆角粉嫩风、用电光蓝替换洋红、满屏霓虹描边。

---

## 质量评分 / Quality Score
- **总分**：93/100
- **结论**：通过（可直接用于迭代与批量出稿）

## 分项得分 / Dimension Scores
- 风格一致性：19/20
- Token 可执行性：15/15
- 色彩与对比：14/15
- 排版层级：9/10
- 组件完整度：9/10
- 布局与间距：9/10
- 防跑偏约束：9/10
- 变体控制力：9/10

## 扣分说明 / Deductions
- 预览含双主题，文档已覆盖；个别组件态需落地时再核对，故组件完整度留 1 分。

## 关键风险 / Key Risks
- 小圆角 + 霓虹在无障碍场景需确认对比；浅色主题洋红 `#E41874` 与正文对比需实测。

## 优先修订（三项）
1. 输出无障碍对比检查表（正文/按钮）。  
2. 明确主题切换时阴影与玻璃透明度切换表。  
3. 为表格/列表补充斑马纹与悬停态 Token。
