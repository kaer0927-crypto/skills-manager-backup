# style-extractor

**网页风格提取器（Web Style Extractor）** — 从网页中提取设计 DNA，输出可落地的 Design Tokens 与可复用风格提示词，用于生成同一视觉体系下的新页面。

分析公开 URL、本地 HTML/CSS、截图或局部组件，提取颜色、字体、背景、阴影、边框、圆角、按钮与布局等风格 tokens；再按固定中文版式生成「基础 / 组件 / 变体」三套提示词，并附带质量评分与防跑偏约束。

> 适合「想模仿某站气质、逆向 UI 美学、或把现有网页沉淀成可复用风格包」的场景；不适合「完全没有参考视觉、希望 AI 凭空定品牌调性」。

官网：[www.VibePM.net](https://www.vibepm.net)

## 安装

本仓库即技能包根目录（顶层含 `SKILL.md`）。克隆或复制到 Agent 的技能目录即可使用。

### 自动安装

把链接发给智能体，让它帮你安装。在 Cursor 等 Agent 对话里复制下面这句即可：

```text
请帮我安装这个技能：https://github.com/vibepm666/style-extractor
克隆到个人技能目录（或项目技能目录）。
```

### 手动安装

下载项目压缩包，解压后将整个 `style-extractor` 文件夹放入技能目录即可。

### 目录说明

技能目录分两种：**个人技能**（所有项目可用）与 **项目技能**（仅当前项目可用）。以 Cursor 为例：

| 类型 | 路径 |
| --- | --- |
| 个人技能 | `~/.cursor/skills/style-extractor/` |
| 项目技能 | `.cursor/skills/style-extractor/` 或 `.agents/skills/style-extractor/` |

> **说明**：具体目录以你所用 Agent 的文档为准；VibePM 用户推荐 `.agents/skills/style-extractor/`。

## 使用方式

**推荐用法**：在对话中调用 `/style-extractor`，或让 Agent 读取本技能的 `SKILL.md` 后按流程执行。

```text
/style-extractor
请分析这个网页并输出完整风格包（含评分）：
https://example.com
目标页面类型：SaaS 仪表盘
```

**Skill 名称**

| 项 | 值 |
| --- | --- |
| 中文名 | 网页风格提取器 |
| 英文名 | Web Style Extractor |
| 调用命令 | `/style-extractor` |
| 旧名兼容 | `/vibepm-style-extractor` 仍走本技能 |

**触发关键词**（任一命中即可）：提取网页风格、分析站点视觉、Design Tokens、风格提示词、模仿某网站 UI、逆向 UI 美学、风格 DNA、同风格生成页面、style extractor

### 调用模式

| 模式 | 说明 |
| --- | --- |
| **完整流程**（默认，无参数） | 采集 → Tokens → 风格原则 → 提示词包 → 复用说明 → 质量评分 |
| **`analyze`** | 仅提取与 token 化，在「风格原则」后停止 |
| **`prompt`** | 基于已有提取结果，生成/优化提示词包与复用说明 |

## 适用场景

| 你是谁 | 典型诉求 |
| --- | --- |
| 设计师 / 设计系统维护者 | 把参考站沉淀成可复用 tokens 与原则 |
| 独立开发者 / Vibe coding 用户 | 模仿喜欢的站点气质，生成同风格页面提示词 |
| 产品 / 前端协作 | 对齐视觉语言，减少「看起来差不多但实现跑偏」 |
| 需要 A/B 视觉变体的人 | 在同一 DNA 下做更亮 / 更暗 / 更暖等可控变体 |

**不适合**：没有参考 URL / 截图 / 本地页面，希望 AI 从零创造整套品牌视觉时 — 请先提供至少一种输入来源。

## 核心能力

### 输入来源

- 公开页面 URL
- 本地 HTML / CSS / JS
- 页面截图（不确定数值用 `~` 标注）
- 局部组件（按钮 / 卡片 / 表单等）

### 提取维度

色彩系统、字体阶梯、背景与层次、阴影、边框、圆角、按钮变体与状态、布局栅格与间距节奏。

### 提示词包（中文默认）

1. **基础提示词** — 整页风格基底（含：审美方向、Token 约束、布局约束、交互约束、避免项）
2. **组件提示词** — 按钮 / 卡片 / 表单等组件规则
3. **变体提示词** — 同一 DNA 下的可控变化

### 质量评分

按 `scoring-rubric.md` 对结果打分（满分 100，建议 ≥ 80 再批量生成）。结论档位：**通过** / **需修订** / **不通过**；未达标时输出「优先修订（三项）」与修订版提示词。

### 可选风格预览页

保存 `*-style.md` 后，可确认是否基于 `style-preview.html` 生成同风格预览 HTML（`*-preview.html`）。

## 工作流程

```text
输入（URL / 本地文件 / 截图 / 组件）
  → 采集视觉清单
  → 规范化为 Design Tokens
  → 提炼风格原则（6–12 条）
  → 生成提示词包 + 复用说明
  → 按 scoring-rubric 评分
  → 保存到项目根目录
  → （可选）生成风格预览页
```

## 产出路径

结果写入**当前工作区根目录**（不会写入技能包目录本身）。

| 产物 | 命名示例 |
| --- | --- |
| 风格包 | `2026-04-28-极简科技感-style.md` |
| 预览页（可选） | `2026-04-28-极简科技感-preview.html` |

固定输出结构见 `SKILL.md`：风格快照 → 设计 Tokens → 风格原则 → 提示词包 → 复用说明 → 质量评分。

## 使用示例

**URL 完整提取**

```text
/style-extractor
请分析这个网页并输出完整风格包（含评分）：
https://example.com
目标页面类型：SaaS 仪表盘
目标用户：中小团队运营人员
```

**仅提取 Tokens**

```text
/style-extractor analyze
请只提取该网站的风格 DNA 与设计 Tokens，不要生成提示词：
https://example.com
```

**截图输入**

```text
/style-extractor
请基于我上传的网页截图提取风格并生成可复用提示词。
如果参数不确定，用 ~ 标注估算值，并输出评分与修正建议。
```

**质量门禁（强制 ≥ 80）**

```text
/style-extractor
请执行完整流程，并将评分作为门禁：
- 低于 80 分不得通过
- 必须输出「优先修订（三项）」
- 直接给出修订版，直到结论为「通过」
```

更多一键示例见 [quickstart.md](./quickstart.md)。

## 文件结构

```text
.
├── SKILL.md              # 主入口：流程、输出规范、模式路由
├── quickstart.md         # 快速上手与常用调用示例
├── examples.md           # 输入/输出示例
├── prompt-library.md     # 中文风格提示词模板库
├── scoring-rubric.md     # 质量评分量表与中文输出模板
├── style-preview.html    # 可选风格预览页模板
├── README.md
├── LICENSE
└── .gitignore
```

**权威说明**：执行流程与输出版式以 `SKILL.md` 为准；评分以 `scoring-rubric.md` 为准。示例文档仅供参考，生成结果须遵循技能内的中文默认规范。

## 相关技能

| 场景 | 技能 |
| --- | --- |
| 从零写 / 评审 PRD | [`prd-writer`](https://github.com/vibepm666/prd-writer) |
| 生成可编辑 draw.io 源文件 | [`drawio-generator`](https://github.com/vibepm666/drawio-generator) |
| 提取网页风格并生成提示词 | 本技能 `style-extractor` |

## 许可证

MIT License — 详见 [LICENSE](./LICENSE)。
