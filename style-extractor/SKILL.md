---
name: style-extractor
description: 分析网页视觉系统并提取颜色、字体、背景、阴影、边框、圆角、按钮模式与布局等风格 tokens。适用于用户希望模仿站点风格、逆向 UI 美学或从现有网页生成可复用风格提示词的场景。旧名 vibepm-style-extractor：用户说 vibepm-style-extractor、/vibepm-style-extractor 时仍走本技能。
user-invocable: true
argument-hint: "[analyze|prompt]"
---

# 网页风格提取器 / Web Style Extractor

从网页中提取设计 DNA，并输出可复用的提示词，用于生成同一风格体系下的新页面。

## 输出语言与版式规范（默认）

除非用户明确要求其他语言，**生成的 `*-style.md` 全文以简体中文为主**，并与下列版式保持一致：

1. **叙述与解释**：风格快照 bullet、Tokens 旁注、风格原则、提示词正文、复用说明、质量评分中的说明性文字——一律中文。
2. **保留英文（不翻译）**：Token 键名（如 `color.surface.base`）、十六进制与函数色值（`#0A0A0A`、`rgba(...)`）、CSS/Tailwind 类名与属性片段、字体族专名（如 `Inter`）、业内通用缩写首次出现可采用「中文（FAB）」「主行动按钮（Primary CTA）」形式。
3. **避免中英混杂词**：正文不要用 `accent`、`shadow` 等英文单词代替语义——改用「强调色」「投影 / 外发光」等；组件状态写「悬停 / 聚焦 / 按下」等中文，必要时括号标注 `hover` / `focus` / `active`。
4. **小节标题**：
   - `## 风格快照`、`## 设计 Tokens`、`### 颜色` 等各节：**保留「中文 / English」双语标题**（与下列固定格式模板一致），便于检索与对齐历史文档。
   - `## 提示词包` 下的三级标题：**仅中文**——`### 基础提示词`、`### 组件提示词`、`### 变体提示词`（不再写 `/ Foundation Prompt` 等英文重复）。
   - `## 复用说明`：**仅中文标题**；下列三条 bullet 使用加粗中文引导词——**必须保持不变**、**可弹性调整**、**风格跑偏风险**（不要使用 `What must stay unchanged` 等英文并列）。
5. **提示词包内部结构**：基础提示词下须包含且标题为中文——**审美方向**、**Token 约束**、**布局约束**、**交互约束**、**避免项**（不要用 `Aesthetic direction`、`Anti-patterns` 等英文小节标题）。组件 / 变体提示词用小节或加粗中文条目组织，避免英文段落起头。
6. **质量评分**：生成文件末尾必须附评分；区块标题、分项名称、结论用语遵循 [scoring-rubric.md](scoring-rubric.md) 中的**中文输出模板**（`## 质量评分`、`## 优先修订（三项）` 等）。结论中的档位使用中文：**通过** / **需修订** / **不通过**（可与括号内简短说明连用）。

## 输入来源 / Input Sources

使用用户提供的任意一种来源：
- URL（公开页面优先）
- 本地 HTML/CSS/JS 文件
- 页面截图
- 局部片段（组件级提取）

如果缺少关键信息，先补齐最小必需输入再继续。

## 工作流程 / Workflow

按以下顺序执行。

### 1) 采集视觉清单 / Capture Visual Inventory

识别并列出以下要素：
- **色彩系统 / Color system**：主色、次色、强调色、中性色、语义色
- **字体系统 / Typography**：字体族、字号阶梯、字重阶梯、行高、字距
- **背景 / Backgrounds**：纯色、渐变、覆盖层、纹理
- **层次系统 / Depth system**：阴影层级、模糊使用、抬升逻辑
- **边框 / Borders**：边框宽度、颜色、样式、分割线处理
- **圆角 / Radii**：圆角尺度及按组件类型的映射
- **按钮 / Buttons**：尺寸变体、视觉变体、hover/focus/active 状态
- **布局 / Layout**：容器宽度、栅格策略、间距节奏、分区密度

### 2) 规范化为 Tokens / Normalize Into Tokens

将发现结果转为明确可复用的 tokens。优先按语义意图命名，而不是直接使用原始数值。

使用以下 token 命名风格：
- `color.brand.primary`
- `color.surface.base`
- `font.family.heading`
- `font.size.300`
- `radius.md`
- `shadow.card`
- `space.4`

当精确数值不确定时，给出最接近的估算值，并用 `~` 标注。

### 3) 提炼风格原则 / Infer Style Principles

提炼 6-12 条简洁原则，说明该风格“为什么成立”。覆盖：
- 对比策略
- 密度与留白
- 视觉层级
- 交互语气（沉稳、锐利、活泼、高级等）
- 动效个性（若可见）
- 组件几何特征（柔和、锐利、混合）

### 4) 生成风格提示词包 / Generate Style Prompt Pack

生成三类提示词变体（三级标题仅用中文，见上文「输出语言与版式规范」）：
1. **基础提示词**：用于生成整页风格基底
2. **组件提示词**：用于生成该风格下的按钮/卡片/表单
3. **变体提示词**：在同一 DNA 下进行可控变化（更亮、更暗、更暖、更密等）

**基础提示词**内必须包含下列五个小节，且**小节标题用中文**：
- **审美方向**
- **Token 约束**
- **布局约束**
- **交互约束**
- **避免项**（列出须禁止的视觉 / 布局模式，条目用中文表述）

### 5) 按固定格式输出 / Output In Fixed Format

始终按以下固定结构输出：

```markdown
## 风格快照 / Style Snapshot
- 整体风格 / Overall style:
- 语气关键词 / Tone keywords:
- 适配产品类型 / Suitable product types:

## 设计 Tokens / Design Tokens
### 颜色 / Colors
- ...
### 字体 / Typography
- ...
### 背景 / Backgrounds
- ...
### 阴影 / Shadows
- ...
### 边框 / Borders
- ...
### 圆角 / Radii
- ...
### 按钮 / Buttons
- ...
### 布局 / Layout
- ...

## 风格原则 / Style Principles
1. ...
2. ...

## 提示词包
### 基础提示词
（正文：五个小节 **审美方向**、**Token 约束**、**布局约束**、**交互约束**、**避免项**，全部为中文叙述，参数与类名保留英文原文。）

### 组件提示词
...

### 变体提示词
...

## 复用说明
- **必须保持不变**：...
- **可弹性调整**：...
- **风格跑偏风险**：...

---

## 质量评分 / Quality Score
（结构与用语必须符合 scoring-rubric.md 的中文模板。）

## 分项得分 / Dimension Scores
...

## 扣分说明 / Deductions
...

## 关键风险 / Key Risks
...

## 优先修订（三项）
...
```

## 质量门槛 / Quality Bar

最终输出前，请检查：
- Tokens 足够具体，可直接落地实现
- 提示词具备可执行性，而非仅有抽象形容词
- 按钮与布局规则具体明确
- 避免项能阻止明显的风格跑偏
- 输出至少可复用于同一品牌下 3 个不同页面
- **语言与版式**：符合本节「输出语言与版式规范（默认）」，提示词包与质量评分区块不得退回英文模板句式

## 结果保存规则 / Output Save Rule

- 提取结果必须自动保存到项目根目录。
- 文件名格式固定为：`日期-风格描述（4~6字左右）-style.md`。
- 示例：`2026-04-28-极简科技感-style.md`。
- 示例（无横杠日期）：`20260428-极简科技感-style.md`。
- **风格预览页（可选）**：`*.md` 保存完成后，**须询问用户**是否需要生成风格预览页。若用户确认需要，以本技能目录下的 [style-preview.html](style-preview.html) 为模板生成预览 HTML，并保存到**项目根目录**。生成时**保留模板中的页面结构**（区块划分、布局、组件与交互骨架不变），**替换与风格展示相关的文案、示例字句及页面内嵌的提示词**（与当次 `*-style.md` 中的快照、Tokens、原则与提示词包对齐），勿擅自删减或重组模板区块。
- 预览页文件名与上述 `*-style.md` **共用同一日期与风格描述片段**，仅将后缀由 `-style.md` 换为 `-preview.html`。示例：`2026-04-28-极简科技感-preview.html`、`20260428-极简科技感-preview.html`。

## 补充资源 / Additional Resources

- 示例模式： [examples.md](examples.md)
- 中文提示词模板： [prompt-library.md](prompt-library.md)
- 评分量表： [scoring-rubric.md](scoring-rubric.md)
- 快速上手示例： [quickstart.md](quickstart.md)

上述示例文档若仍出现英文小节标题或旧版评分区块标题，**仅作写作参考**；自动生成的 `*-style.md` 必须以本节「输出语言与版式规范（默认）」与 `scoring-rubric.md` 中文模板为准。

## 模式路由 / Mode Routing

若以 `analyze` 调用：
- 仅聚焦提取与 token 化。
- 在 `## 风格原则 / Style Principles` 后停止。

若以 `prompt` 调用：
- 假设提取已完成或已提供。
- 聚焦生成/优化 `## 提示词包` 与 `## 复用说明`，并遵守中文输出规范。

若无参数：
- 执行从提取到提示词包的完整流程。

## 评分步骤 / Scoring Step

生成最终输出后，必须使用 [scoring-rubric.md](scoring-rubric.md) 对结果评分：
- 按量表中的**中文输出模板**追加评分区块（`## 质量评分 / Quality Score`、`## 分项得分 / Dimension Scores`、`## 扣分说明 / Deductions`、`## 关键风险 / Key Risks`、`## 优先修订（三项）`）。
- **结论**使用中文档位：**通过**（建议 80–100）、**需修订**（60–79）、**不通过**（0–59）；量表原文中的 `Pass` / `Revise` / `Reject` 仅作语义对应，写入 `.md` 时以中文为主。
- 若结论为 **需修订** 或 **不通过**，须立即给出 `## 优先修订（三项）` 与修订后的提示词包（中文）。
