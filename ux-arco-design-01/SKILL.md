---
name: ux-arco-design-01
description: UX Arco Design 01（原 vibepm-frame-ui）——基于 VibePM / Frame「中后台原型及前端交付解决方案」组件库的前端界面生产规范。当需要生产或改造前端界面——中后台/管理后台/Web 产品页/登录页/看板/列表/表单/详情/移动端页面——且要求遵循该模板的组件规范与 UI 风格时使用；也适用于用户提到「按 Frame / vibepm 模板做」「用 vibepm 风格」「中后台原型」「Vibecoding 组件调用」等场景。使用本 Skill 可拿到完整的组件索引（后台 50 页 + 移动端 8 壳）、12 套视觉主题规范（设计 Tokens/提示词包/防跑偏约束）与源项目引用，保证其他 agent 产出的前端界面与模板保持一致的组件体系和 UI 风格。**本 Skill 基于 Arco Design Vue 构建，所有实现必须同时遵守 Arco 原生组件规范和 Vibepm 业务规则**。
---

# UX Arco Design 01（VibePM / Frame 中后台原型及前端交付解决方案）

**技术栈**: Vue 3 + TypeScript + **Arco Design Vue**  
**定位**: UX Arco Design 01 是基于 Arco Design Vue 的**业务抽象层**,保留业务规则 (CRUD/表单/筛选区),底层使用 Arco 原生组件实现；内容源自 VibePM / Frame 模板体系。

> **事实基线**：references 中的 Arco API、Token 名、断点、暗黑模式用法均对照 `arco-design/arco-design-vue` 源码与 `@arco-design/web-vue@2.59.0` 核对。若与官方文档冲突，以官方文档为准，并同步回改本文，不得凭印象补 API。

本 Skill 让 agent 用 VibePM / Frame 模板的组件体系与 UI 风格生产前端界面：**组件选型必须来自组件索引，样式必须来自主题规范，禁止自由发挥设计 Token**。

## 前置准备：确认任务类型

1. **确认适用**: 任务是生产/改造前端界面（后台、管理端、SaaS 页、移动端壳等）→ 继续。纯文案/逻辑任务不适用。
2. **了解技术栈**: 本 Skill 基于 Arco Design Vue,所有界面必须同时遵守:
   - [arco-integration.md](references/arco-integration.md) - Arco Design Vue 集成规范
   - [arco-tokens.md](references/arco-tokens.md) - Arco Token 实测值与主题映射
   - [component-mapping.md](references/component-mapping.md) - Arco vs Vibepm 组件对照决策矩阵
   - [dark-mode-tokens.md](references/dark-mode-tokens.md) - 暗黑模式完整 Token 集

## 使用流程

1. **确认适用**：任务是生产/改造前端界面（后台、管理端、SaaS 页、移动端壳等）→ 继续。纯文案/逻辑任务不适用。
2. **定主题**：读 `references/ui-style-guide.md` 选主题（默认推荐 SemiDesign 或亮色科技蓝；拿不准问用户，给出 2–3 个候选差异）。
3. **读主题细节**：读 `references/themes/<主题名>-style.md` 全文，拿到该主题完整 Token（颜色/字体/圆角/阴影/按钮/表单/弹窗/滚动条/提示词包/避免项）。
4. **查 Arco 集成**: 阅读 [arco-integration.md](references/arco-integration.md) 与 [arco-tokens.md](references/arco-tokens.md)，确认安装方式、Token 名、暗黑切换、断点与密度对齐。
5. **选组件方案**: 查阅 [component-mapping.md](references/component-mapping.md),决定哪些用 Arco 原生组件，哪些用 Vibepm 规范包装。
6. **暗黑模式准备**（如需要）: 参考 [dark-mode-tokens.md](references/dark-mode-tokens.md) 获取对应主题的暗黑版配色表。
7. **选组件与页面骨架**: 读 `references/component-catalog.md` 按页面类型选骨架；再读 `references/pages-guide.md` 确认该类型页面的结构规范、`references/components-guide.md` 选控件并确认控件规范。
8. **表单场景读表单规范**: 涉及表单（新建/编辑/表单页/分步）时，读 `references/forms-guide.md` 按表单控件与布局规范实现。
9. **状态与动作**: 列表/详情/审批/工单类页面必读 `references/state-machine.md`，先产出「状态 → 动作」矩阵，再由矩阵推导行按钮、批量按钮与禁用原因；禁止在模板里散写 `v-if` 判断状态。
10. **权限场景**: 涉及角色差异、越权、数据范围时读 `references/permission-guide.md`，按「隐藏 / 禁用+原因 / 403」三态决策表判定，先定页面级，再定按钮级与字段级。
11. **反馈与文案**: 涉及空态、批量、导出、导入、长任务、并发编辑时读 `references/feedback-patterns.md`；所有可见文案按 `references/content-guide.md` 的语气与动词表统一。
12. **敏感数据**: 出现手机号/身份证/银行卡/住址/金额/健康信息等字段时读 `references/data-security.md`，脱敏、按需展开、导出与水印按该文执行。
13. **生产**: 按主题 Token 实现界面，复用组件骨架结构，填充真实业务内容。
14. **自查**: 对照主题文档的「避免项」与「必须保持不变」,以及各规范文档的「自查清单」逐条检查；可访问性按 `references/accessibility.md` 的「交付前 10 分钟验收法」跑一遍键盘路径。
15. **扩展登记**: 现有规范确实覆盖不了的模式，按 `references/extensions/README.md` 登记，不许私下另立一套 Token 或组件。
16. **（可选）参考真实实现**: 需要抄具体控件写法时，按 `references/source-layout.md` 从源项目读真实 HTML/CSS/JS。**若记录路径失效（被移动/清理/变化）:禁止猜测新路径或静默兜底，必须先向用户发起确认，拿到用户确认的新位置后再引用。**

## 生产硬规则

- **同一界面只用一个主题**: 禁止混搭主题主色与圆角档位。
- **严格跟随 Token**: 主色、悬停/按下色、文字色阶、表面色、边框色、圆角档、阴影、字体栈，全部取主题文档值，不自行换色。
- **按钮五态齐全**: primary / secondary / outline / ghost / link-icon，每态悬停、按下、禁用都要有明确行为（Arco 映射：primary→`type="primary"`、secondary→默认、outline→`type="outline"`、ghost→`type="text"`、link→`type="text"` + 主色）。
- **表单反馈完整**: 错误红环 + 短句、清空钮、提交行、Toast、提示条，缺一不可（Arco 表单优先用 FormItem `help` 呈现短句，自研控件才用 `.field-error`）。
- **弹窗不透明**: 面板不透明 + 柔影 + 主题圆角档；遮罩可 blur，面板禁止玻璃半透明。
- **滚动条统一**: 宽 8px、胶囊滑块、透明轨道（WebKit + Firefox 双写）,见主题文档。
- **排版**: 正文 14–16px，标签 14px/600，标题字重 600–800；中文回退 PingFang SC / 微软雅黑。
- **响应式断点**: 采用 Arco Grid 真实断点（`xs <576`、`sm ≥576`、`md ≥768`、`lg ≥992`、`xl ≥1200`、`xxl ≥1600`），配合 vibepm 业务规则（筛选区≤980px 隐藏标签、表单≤900px 单列、侧栏 `breakpoint="xl"`）。
- **密度对齐**: Arco 默认偏紧凑（控件 24/28/32/36，按钮字重 400，圆角 2/4/8）。落地前用 `modifyVars` 对齐主题圆角与主色，主按钮字重补到 600，勿在业务页写死像素。
- **国际化**: 文案走 `ConfigProvider :locale`；函数式 `Message`/`Modal` 必须设 `Message._context = app._context` 或给 ConfigProvider 加 `global`，否则语言不生效。
- **暗黑模式支持**: 如需暗黑模式，严格遵守 [dark-mode-tokens.md](references/dark-mode-tokens.md) 的各主题配色映射。
- **路径失效必须向用户确认**: 记录在 `references/source-layout.md` 的源模板路径不可用/被移动/变化时，禁止猜测新路径、禁止静默退回内置 references 继续生产；必须先向用户发起确认，经用户确认新位置后才可引用。
- **筛选区单行栅格**: 列表页筛选区按「最小列宽 220px、列数上限 6」的栅格排布，桌面列数 = `clamp(2, floor(容器宽 / 220), 6)`，≤576px 单列；区间/树/多选控件占 2 格，查询/重置按钮跟随字段流不单独占行；禁止人为拉宽字段把条件与按钮拆成两行（详见 ui-style-guide.md「筛选区布局」）。
- **列表 CRUD 规范**: 数据列表的新增/编辑用弹窗表单（回填 + 校验 + loading + Toast + 重查）,删除/批量删除用 danger 确认弹窗，未勾选时批量按钮禁用，删空回退页码，分页条完整（详见 references/crud-guide.md）。
- **表单规范**: 表单字段按栅格排布（常规 2–3 列，窄屏单列），标签在控件左侧且文字右对齐 14/600、必填红 *，`scroll-to-first-error` 开启、`allow-clear` 显式设置，校验失败不关表单，提交行按钮完整（详见 references/forms-guide.md）。
- **组件与页面规范**: 控件用法、表格/列表/图表/指标卡/富文本/扩展组件遵守 references/components-guide.md；页面骨架与结构遵守 references/pages-guide.md（按布局类型 shell/center/split/phone 选型）。
- **状态驱动动作**: 状态名称、编码、色彩语义、是否终态必须成组定义；每个动作标注允许的状态与失败原因，禁用按钮必须给出可读原因（详见 references/state-machine.md）。
- **权限三态**: 无权入口先按「隐藏 / 禁用+原因 / 403」判定，不得一律隐藏；前端隐藏不替代后端鉴权（详见 references/permission-guide.md）。
- **反馈分层**: 空态分首次/无结果/无权限/出错四类；批量操作必须处理部分成功；超过 3 秒的任务进任务中心或通知，不用一个转圈等到底（详见 references/feedback-patterns.md）。
- **敏感数据**: 手机号/证件/银行卡/地址等按字段分级脱敏展示，查看原值与导出都必须二次确认并留痕（详见 references/data-security.md）。

## Arco Design Vue 核心整合点

### 1. 组件选型决策

| 场景 | 推荐方案 | 理由 |
|------|----------|------|
| 复杂 CRUD 表格 | Arco Table + Vibepm 规则 | Arco Table 是企业级强项 |
| 新建/编辑表单 | Vibepm Form 规范 + Arco Form | Vibepm 栅格布局优于 Arco |
| 指标卡/KPI 卡片 | Vibepm Metric Cards（数值部分可用 `a-statistic`） | Arco 只有数值组件，没有 12 种卡片变体 |
| 弹窗确认 | Vibepm Modal 规范 | Vibepm「不透明」规则必须遵守 |
| Toast 提示 | Vibepm Toast 规范 | Arco Message 需二次封装 |
| 基础输入框 | Arco Input/Select | 功能完善，无需重复造轮子 |
| 树形结构 | Arco Tree | 完整功能已提供 |

详细决策矩阵见 [component-mapping.md](references/component-mapping.md)。

### 2. 主题 Token 映射

映射目标是 Arco 的**真实变量**（`@arcoblue-6` / `--primary-*` / `--color-*` / `--border-radius-*`），不是自造名：

```less
// modifyVars（构建期，推荐）
'arcoblue-6'          : 主题主色
'border-radius-small' : 按钮圆角
'border-radius-medium': 输入 / 弹窗圆角
'font-family'         : 主题字体栈
```

- 语义色为 `R,G,B` 三元组：`--primary-6: 22, 93, 255`，组件用 `rgb(var(--primary-6))` 消费。
- 全部 Token 声明在 **`body`** 上（不是 `:root`）；暗色块 `body[arco-theme='dark']` 特异性更高，只写 `body { --primary-6 }` 在暗色下会失效。
- 圆角只有 **small（控件）/ medium（浮层）** 两档真实生效；`--border-radius-large` 在 2.59.0 中 **0 处引用**，改了不生效。卡片默认直角（`--border-radius-none`），必须显式覆盖 `.arco-card`。三档以上圆角只能走 [`theme-presets.md`](references/theme-presets.md) 的组件级覆盖。
- 阴影只有 Less 变量（`@shadow1-down` 等），没有 CSS 变量，无法运行时切换。
- 12 套主题的逐项映射、可映射/不可映射清单见 [`arco-tokens.md`](references/arco-tokens.md)。

### 3. 暗黑模式

详见 [dark-mode-tokens.md](references/dark-mode-tokens.md):
- 通用暗黑配色表（背景/文字/边框/滚动条）
- 12 个主题各自的暗黑版调整策略
- 切换实现代码（`document.body.setAttribute('arco-theme','dark')` + 消费 `--color-*` 变量）

### 4. 响应式断点

采用 Arco Grid 系统:
| 断点 | 宽度 | vibepm 对应规则 |
|------|------|----------------|
| xs | <576px | 移动优先，表格横向滚动 |
| sm | ≥576px | 双列表单可用 |
| md | ≥768px | 三列筛选区开始可用 |
| lg | ≥992px | 内容区常规宽度（容器 1120–1200px） |
| xl | ≥1200px | 侧栏展开（`breakpoint="xl"`），195–200px 侧栏 |
| xxl | ≥1600px | 宽屏，最多 4 列 KPI |

vibepm 业务阈值（与断点共存，不是断点本身）：筛选区 ≤980px 隐藏标签、表单 ≤900px 单列。

详见 [ui-style-guide.md](references/ui-style-guide.md)「响应式断点」部分。

## 常用命令式提示词（给其他 agent 用）

- 选组件：`我要做<页面类型>,从 UX Arco Design 01 组件索引选对应骨架，并按<主题>主题规范改造。`
- 换主题：`把界面换成<主题>主题，按 themes/<主题>-style.md 的 Token 重做颜色/圆角/阴影。`
- 抄控件：`参考 admin/js/pages/<页面>.js 与 admin/css/*.css 中 <类名> 的实现，保持类名体系。`
- **Arco 集成**: `查看 arco-integration.md 了解 Arco Design Vue 组件用法。`
- **组件决策**: `参考 component-mapping.md 决定用 Arco 原生还是 Vibepm 规范包装。`
- **暗黑模式**: `按需 dark-mode-tokens.md 获取<主题>的暗黑版配色表。`
- **响应式**: `按 ui-style-guide.md 的 Arco Grid 断点系统实现响应式。`

## 文件导航

**可直接引入的资产**（`assets/`）:
- [frame-presets.css](assets/frame-presets.css) — 圆角两档 + 卡片/弹窗/表格外框 + 按钮高度字重投影 + 不透明弹窗 + 8px 滚动条 + 自适应筛选区栅格（`auto-fit, minmax(220px, 1fr)`，真实 Vite 构建 + Chrome 计算样式已验证）
- [frame-themes.css](assets/frame-themes.css) — 12 套主题圆角/按钮/投影覆盖，`body[data-frame-theme='semi']` 一行启用（12 套均已在 Chrome 实测）
- [arco-echarts-theme.ts](assets/arco-echarts-theme.ts) — ECharts 读 Arco 变量、`body[arco-theme]` 变更自动重绘
- [skeletons/visualization-screen.vue](assets/skeletons/visualization-screen.vue) — 大屏/多维分析骨架（1920×1080 等比缩放，事件流轮播，实测两档分辨率）

**核心规范**（必读）:
- [arco-integration.md](references/arco-integration.md) — Arco Design Vue 集成规范（安装/主题/图标/暗黑/断点）⭐**新增 P0**
- [arco-tokens.md](references/arco-tokens.md) — Arco Token 实测值（亮/暗）、尺寸密度、12 主题映射表
- [theme-presets.md](references/theme-presets.md) — 圆角/高度/字重落地 Preset（含 SemiDesign、亮色科技蓝、暗色主题）
- [component-mapping.md](references/component-mapping.md) — Arco vs Vibepm 组件对照决策矩阵 ⭐**新增 P0**
- [arco-pro-pages.md](references/arco-pro-pages.md) — 官方 Arco Pro 19 页逐页实现比对（可吸收 7 点 / 不要照抄 5 点）
- [dark-mode-tokens.md](references/dark-mode-tokens.md) — 暗黑模式完整 Token 集（12 主题映射） ⭐**新增 P1**
- [chart-theme.md](references/chart-theme.md) — ECharts 接 Arco 变量（亮/暗自动切换、配色与结构规则）
- `references/ui-style-guide.md` — 12 套主题速查与选择指引、通用规范（按钮/表单/弹窗/滚动条/布局/筛选区/**响应式断点**）
- `references/forms-guide.md` — 表单规范（控件全清单/栅格布局/4 种表单页结构/校验反馈）
- `references/components-guide.md` — 组件规范总览（基础组件/表格/列表/图表/指标卡/富文本/扩展组件）
- `references/pages-guide.md` — 页面模板规范（登录/看板/列表/表单/详情/结果/异常/个人中心/移动端壳）
- `references/crud-guide.md` — 数据列表增删改查规范（操作列/弹窗表单/确认删除/批量/分页/自查清单）
- `references/state-machine.md` — 状态机与「状态 → 动作」矩阵（状态四件套/Tag 色彩映射/按钮禁用原因/批量取交集）⭐**新增 P0**
- `references/permission-guide.md` — 权限降级规范（隐藏/禁用+原因/403 三态、按钮/页面/数据/字段四级）⭐**新增 P0**
- `references/feedback-patterns.md` — 反馈模式（四类空态/部分成功/长任务分档/并发冲突 409）⭐**新增 P1**
- `references/content-guide.md` — 文案规范（语气基线/错误三段式/动词表/空态模板/数字日期/中英混排）⭐**新增 P1**
- `references/data-security.md` — 数据安全与合规（字段分级/脱敏/按需展开/导出确认/水印/留痕）⭐**新增 P2**
- `references/accessibility.md` — 可访问性基线（键盘/表单语义/反馈播报/对比度/动效/10 分钟验收）⭐**新增 P2**
- `references/extensions/README.md` — 扩展与例外登记（何时登记/登记模板/命名存放/回灌机制）⭐**新增 P3**
- `references/component-catalog.md` — 组件索引（admin 50 页 + app 8 壳）、选型速查表
- `references/themes/<主题名>-style.md` — 各主题完整规范（Token/提示词包/防跑偏/评分）
- `references/source-layout.md` — 源项目路径、目录结构、读真实实现的方法

## 质量检查清单

**P0 - Arco 集成检查**:
- [ ] 是否正确引入 `@arco-design/web-vue` 和样式？
- [ ] 自定义样式读的变量是否落在 `body` 作用域（写在 `:root` 上取不到值）？
- [ ] 是否已注册插件 `app.use(ArcoVue)`?
- [ ] 组件选型是否遵循 component-mapping.md 决策矩阵？
- [ ] 是否命中 component-mapping.md 第九节“禁止写法”（`type="link"`、`danger: true`、`top-center`、`showSizeChanger`、`:styles`）？
- [ ] 图标是否使用 Arco IconBox 而非第三方？
- [ ] 主题是否走 `modifyVars` / Design Lab 主题包，Token 名是否为 Arco 真实变量？
- [ ] 是否遵循 Vue 3 Composition API Props 语法？

**P1 - 暗黑模式检查（如启用）**:
- [ ] 各主题配色是否参照 dark-mode-tokens.md？
- [ ] 文字对比度符合 WCAG AA 标准（4.5:1+）?
- [ ] 滚动条颜色正确反转？
- [ ] 是否通过 `body[arco-theme='dark']` 切换（未使用不存在的 `setTheme`）？
- [ ] 自定义样式是否全部消费 `var(--color-*)`，无硬编码白底黑字？
- [ ] 页面根容器（`body` / `#app` / 布局壳）是否设了 `background: var(--color-bg-1)`？漏设会导致暗色下黑卡片配白页面。

**P2 - 响应式检查**:
- [ ] 是否使用 576/768/992/1200/1600 真实断点（未写成 1920）？
- [ ] 筛选区≤980px 是否隐藏标签？
- [ ] 表单≤900px 是否单列布局？
- [ ] 表格<768px 是否开启横向滚动？
- [ ] 侧栏是否 `breakpoint="xl"`，移动端是否切 `a-drawer`？

**业务必查 - 状态与权限**:
- [ ] 每个状态是否有名称、编码、色彩语义、是否终态四项齐备（state-machine.md）？
- [ ] 行按钮、批量按钮是否由「状态 → 动作」矩阵推导，而不是模板里散写 `v-if`？
- [ ] 禁用按钮是否带可读原因（`a-tooltip` / 文案），批量操作是否按所选行状态取交集？
- [ ] 无权入口是否按「隐藏 / 禁用+原因 / 403」三态判定，而不是一律隐藏（permission-guide.md）？
- [ ] 页面级、数据级、字段级权限是否分别有落点，前端限制之外是否确认后端鉴权？

**反馈与文案**:
- [ ] 空态是否区分首次 / 无结果 / 无权限 / 出错四类（feedback-patterns.md）？
- [ ] 批量、导入、导出是否处理「部分成功」并展示失败行与原因？
- [ ] 超过 3 秒的任务是否进任务中心或通知栏，而不是只留一个转圈？
- [ ] 编辑冲突（409 / 版本号不一致）是否提示并给出刷新或另存选择？
- [ ] 可见文案是否统一动词（新建/新增/创建只选一个）、错误是否三段式（content-guide.md）？

**安全与可访问性**:
- [ ] 敏感字段是否按分级脱敏，查看原值/导出是否二次确认并留痕（data-security.md）？
- [ ] 导出范围是否与当前筛选或勾选一致，导出按钮是否防重复点击？
- [ ] 自定义可点击元素是否用 `<button>` / `<a>`，图标按钮是否有 `aria-label`（accessibility.md）？
- [ ] 表单错误是否 `aria-invalid` + `aria-describedby`，反馈是否 `role="alert"` / `aria-live`？
- [ ] 是否用键盘完整走通「筛选 → 打开弹窗 → 提交 → 关闭」主路径？

**扩展治理**:
- [ ] 新增模式是否按 `extensions/README.md` 登记，而不是私自立 Token 或组件？
- [ ] 扩展是否只影响登记范围，未改动主题 Token 与既有页面？

**原有检查**（继续保留）:
- [ ] 同一界面只用一个主题？
- [ ] 按钮五态齐全、危险操作红色？
- [ ] 表格操作列宽度是否按动作数给足（2 个文本按钮 ≥160px，推荐 180px），没有折行把行高撑到 80px+？
- [ ] 表单验证后表单保持打开？
- [ ] 弹窗不透明无玻璃态？
- [ ] 筛选区列数按容器宽计算（上限 6）、单列实宽 ≥220px、按钮同行？
- [ ] CRUD 分页回退页码逻辑完整？
- [ ] Toast 220ms 动画、双层阴影？
- [ ] 滚动条 WebKit+Firefox 双写？

## 总结

**UX Arco Design 01 的核心价值**:
✅ **业务规则完善**: CRUD、筛选区栅格、表单验证等业务规则远超 Arco 原生  
✅ **质量保障体系**: 16 步工作流 + 分主题自查清单 + 一键一致性脚本（`scripts/check-consistency.mjs`）  
✅ **12 套主题系统**: 完整的 Token 体系和防跑偏约束  

**相比 Arco Design Vue 的增强**:
🚀 **业务抽象层**: 在 Arco 成熟组件基础上叠加业务规则  
🚀 **Theme Mapping**: 12 套主题的主色可完全映射；圆角受 Arco 双档模型限制，需 `theme-presets.md` 的组件级覆盖补齐  
🚀 **生态利用**: 充分利用 Design Lab、IconBox 等 Arco 生态工具  

**最佳实践路径**:
```
Vibepm 业务规范 (顶层) → CRUD/表单/筛选区规则
    ↓
Arco Design Vue 组件实现 (底层) → 60+ 预制组件
    ↓
Design Lab / modifyVars (视觉层) → 主色映射 + theme-presets 圆角补齐
```
