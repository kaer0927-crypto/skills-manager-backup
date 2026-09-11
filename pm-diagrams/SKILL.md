---
name: pm-diagrams
description: 产品经理画图 skill，覆盖五种常用图：产品架构 / 业务流程 / 系统泳道 / 时序 / ER。每次输出 2 个文件：ASCII 草图文件 + 代码文件（产品架构/泳道 → drawio；业务流程/时序/ER → mermaid）。工作流：先画 ASCII、subagent 审查迭代，再转代码、再 subagent 审查迭代。当用户要求画这五类图中的任意一种时触发。
---

# Skill：产品经理画图（pm-diagrams）

## 触发词
/pm-diagrams

## 一句话描述
按"ASCII 草图 → 审查 → 代码转写（drawio 或 mermaid） → 审查"的两段式流程，输出五种图（产品架构 / 业务流程 / 系统泳道 / 时序 / ER）的最终文件，每张图产出 2 个文件（ASCII + 代码）。

## 适用范围（本 skill 仅支持以下 5 种图）

| 图类型 | 英文 key | 表现内容 | 代码格式 | 代码文件后缀 |
|---|---|---|---|---|
| 产品架构图 | `product-architecture` | 系统模块、技术层级、依赖关系 | drawio XML | `.drawio` |
| 业务流程图 | `business-process` | 业务活动流转、判断与分支 | mermaid `flowchart` | `.md`（含 mermaid 代码块） |
| 系统泳道图 | `swimlane` | 按角色/系统划分泳道，跨泳道协作 | drawio XML | `.drawio` |
| 时序图 | `sequence` | 对象间消息交互顺序 | mermaid `sequenceDiagram` | `.md`（含 mermaid 代码块） |
| ER 图 | `er` | 实体、属性、实体间关系 | mermaid `erDiagram` | `.md`（含 mermaid 代码块） |

不在上述范围内的图（用例图、状态机、类图、组织架构、思维导图、原型线框、UML 其他类型、PPT 排版等）一律拒绝并提示用户换用其他工具。

### mermaid 节点 ID 命名约定

| 图类型 | 节点 ID 风格 | 示例 |
|---|---|---|
| flowchart（业务流程） | 短字母 + 数字，步骤用 `S1/S2A/S3B`、判断用 `D1/D2`、起止用 `Start/End` | `S1`、`D1`、`S2A`、`Lock`、`End1` |
| sequenceDiagram（时序） | 单字母 + `participant` 别名声明 | `participant U as 用户`、`participant C as 客户端` |
| erDiagram（ER） | 实体名全大写（无别名） | `USER`、`POST`、`ORDER_ITEM` |

## 输入约定
- 必填：图类型（5 选 1，必须在上述白名单内）+ 画图需求描述（可口头、可文档链接）
- 可选：参考文件路径（--ref=<path>）、输出文件名（--out=<basename>，不填则用 `<图类型>-<需求简述>` 作为 basename，最终落盘 2 个文件 `<basename>.ascii.md` + `<basename>.<code-ext>`）

## 执行步骤
1. **澄清与定边界**（最多 2 轮提问）：确认图类型、读者、抽象层级（高层/详细）、是否需要标注非功能需求
2. **加载模板与示例**（按图类型分别读 ASCII 文件和代码文件）：
   - ASCII 阶段：读 `templates/<type>.ascii.md` + `examples/<type>.ascii.md`
   - 代码阶段：读 `templates/<type>.<code-ext>` + `examples/<type>.<code-ext>`
3. **绘制 ASCII 草图**：基于需求在 markdown 代码块中写一份 ASCII 草图
4. **派 subagent 审查 ASCII 草图**：检查元素完整性、命名一致性、连接正确性、读者可读性；不通过则修改草图，循环到通过
5. **将 ASCII 草图转写为代码**（按图类型分支）：
   - **A 路**（产品架构 / 泳道）→ 输出 drawio XML（mxGraphModel 容器，可被 drawio / diagrams.net 直接打开）
   - **B 路**（业务流程 / 时序 / ER）→ 输出 mermaid 语法（flowchart / sequenceDiagram / erDiagram）
6. **派第二个 subagent 审查代码**：检查语法合法性、节点/边是否与 ASCII 草图一致、可读性；不通过则修改，循环到通过
7. **输出最终 2 个文件**到指定目录：
   - `<basename>.ascii.md`（含 ASCII 草图，markdown 代码块包裹）
   - `<basename>.drawio` 或 `<basename>.md`（代码文件，A 路纯 XML，B 路含 mermaid 代码块的 markdown）

## 输出契约

每次画图产出 **2 个文件**（路径 = `{用户指定目录}/<basename>.<ext>`，basename = `<图类型>-<需求中文简述>`）：

| 文件 | 后缀 | 内容 | 工具可直接打开 |
|---|---|---|---|
| ASCII 草图文件 | `.ascii.md` | markdown 文档，正文含 1 个 `text` 代码块包裹完整 ASCII 草图 | 任何 markdown 阅读器 |
| 代码文件 | `.drawio` 或 `.md` | A 路纯 drawio XML；B 路含 1 个 `mermaid` 代码块 | drawio / VSCode mermaid 预览 |

**两文件 basename 必须完全相同**（仅后缀不同），便于人识别为"同一张图的两种形态"。

### 文件后缀规则
- A 路（产品架构 / 泳道）：代码文件后缀 `.drawio`（drawio 官方后缀）
- B 路（业务流程 / 时序 / ER）：代码文件后缀 `.md`（含 mermaid 代码块，VSCode 预览插件可渲染）

### 命名示例
- 用户画"电商订单系统产品架构" → 产出
  - `product-architecture-电商订单系统.ascii.md`
  - `product-architecture-电商订单系统.drawio`
- 用户画"用户登录业务流程" → 产出
  - `business-process-用户登录.ascii.md`
  - `business-process-用户登录.md`（含 mermaid 代码块）
- 用户画"O2O 订单履约泳道" → 产出
  - `swimlane-O2O订单履约.ascii.md`
  - `swimlane-O2O订单履约.drawio`
- 用户画"扫码支付时序" → 产出
  - `sequence-扫码支付.ascii.md`
  - `sequence-扫码支付.md`（含 mermaid 代码块）
- 用户画"内容社区 ER" → 产出
  - `er-内容社区.ascii.md`
  - `er-内容社区.md`（含 mermaid 代码块）

### basename 提取算法（**循环剥离直到不再变化**）

**算法思路**：
1. 取输入"需求中文简述"，去掉首尾空白
2. 循环剥离后缀直到不再变化（每次只剥一种后缀）
3. 拼接：`<图类型>-<中文简述>`

**待剥离的后缀类型**（按优先级，从右到左匹配）：

| 类型 | 正则模式 | 示例 |
|---|---|---|
| 日期 + 可选时间 | `[-_ ]?\d{4}-\d{2}-\d{2}(?:[-_ ]\d{2}[-_ ]\d{2}[-_ ]\d{2})?` | `-2026-06-26`、`-2026-06-26 08_26_28` |
| 紧凑日期/时间 | `[-_ ]?\d{8}(?:[-_ ]\d{6})?`、`[-_ ]?\d{6}$` | `20260626`、`082628` |
| 版本号 | `[-_ ]?v\d+(\.\d+)*` | `-v1.2`、`-v3` |
| 状态词 | `[-_ ]?(final\|draft\|rev\d+)` | `-final`、`-draft`、`-rev2` |

**Python 参考实现**（可直接运行）：

```python
import re

SUFFIX_PATTERNS = [
    r'[-_ ]?\d{4}-\d{2}-\d{2}(?:[-_ ]\d{2}[-_ ]\d{2}[-_ ]\d{2})?',
    r'[-_ ]?\d{8}(?:[-_ ]\d{6})?',
    r'[-_ ]?\d{6}$',
    r'[-_ ]?v\d+(\.\d+)*',
    r'[-_ ]?(final|draft|rev\d+)',
]

def extract_basename(type_key: str, raw: str) -> str:
    """从"需求中文简述"提取 basename，循环剥离后缀直到稳定。"""
    s = raw.strip()
    while True:
        prev = s
        for pat in SUFFIX_PATTERNS:
            s = re.sub(pat + '$', '', s, flags=re.IGNORECASE)
            s = s.strip()
        if s == prev:
            break
    if not s:
        s = raw.strip()  # 全部剥光时回退
    return f"{type_key}-{s}"

# 示例
print(extract_basename("product-architecture", "电商订单系统-v1.2-final"))
# → product-architecture-电商订单系统
print(extract_basename("swimlane", "O2O 订单履约-2026-06-26"))
# → swimlane-O2O订单履约
print(extract_basename("business-process", "用户登录-2026-06-26 08_26_28"))
# → business-process-用户登录
```

补充示例：
- "电商订单系统-v1.2-final" → basename = `product-architecture-电商订单系统`
- "O2O 订单履约-2026-06-26" → basename = `swimlane-O2O订单履约`
- "用户登录-2026-06-26 08_26_28" → basename = `business-process-用户登录`
- "周会-20260626" → basename = `meeting-minutes-周会`（仅作示例）

### ASCII 草图文件结构
```markdown
# <图类型> - <需求简述>

\`\`\`text
（完整 ASCII 草图）
\`\`\`
```

### 代码文件结构
- `.drawio` 文件：标准 `<?xml version="1.0" encoding="UTF-8"?>` 开头，含 `<mxfile>` / `<mxGraphModel>` / `<root>` + `<mxCell>` 三大要素
- `.md` 文件（mermaid 路径）：markdown 文档正文含 1 个 `mermaid` 代码块包裹完整 mermaid 代码，VSCode 预览插件可直接渲染

---

## 约束
- **图类型白名单**：仅支持 5 种（产品架构 / 业务流程 / 系统泳道 / 时序 / ER），其他类型直接拒绝并提示
- **代码格式分流**：产品架构/泳道 → drawio XML；业务流程/时序/ER → mermaid；不得跨路混用
- **输出形态**：**每次产出 2 个文件**（`.ascii.md` + `.drawio`/`.md`），不输出单文件
- **两文件 basename 一致**：仅后缀不同，便于识别为同一张图
- **A 路代码文件纯代码**：`.drawio` 文件**只含 drawio XML**，不掺 ASCII 草图、不掺图表说明、不掺审查记录
- **B 路代码文件只含 1 个 mermaid 代码块**：`.md` 文件正文**只含 1 个 `mermaid` 代码块**，不掺 ASCII 草图、不掺说明、不掺其他代码块
- **ASCII 文件只含草图**：`.ascii.md` 文件正文**只含 1 个 ASCII 草图代码块**，不掺 mermaid/drawio 代码、不掺说明
- **ASCII 草图优先**：先画 ASCII 草图并通过 subagent 审查，再转代码，**禁止跳步**
- **代码语法合法**：
  - drawio XML 必须能被 drawio / diagrams.net 打开（mxfile / mxGraphModel / mxCell 三大要素齐全）
  - mermaid 必须能直接被 mermaid 渲染（flowchart TD/LR、sequenceDiagram、erDiagram 三大类）
- **drawio 连接采用正交+圆角风格**：所有边的 style 必须含 `edgeStyle=orthogonalEdgeStyle;rounded=1;...endArrow=classic;`，正交折线的转角用圆角而不是直角
- **drawio 节点默认尺寸 120x60**：所有内容节点（矩形、圆角矩形、椭圆、菱形、圆柱、六边形等）默认 `width=120, height=60`；只有容器（分层 / 分组）可以例外
- **自上而下连接端点（产品架构图）**：连接线起点从源节点**底部**出发（`exitX=0.5;exitY=1`），终点连到目标节点**顶部**（`entryX=0.5;entryY=0`），让架构图自上而下流向清晰
- **泳道无缝衔接**：泳道图中各泳道之间不留间隙，子泳道水平紧密相接、底部与外层泳道对齐（外层大泳道 width = 子泳道 width 之和）
- **跨泳道节点 y 对齐**：顺序相邻的跨泳道节点，y 坐标尽量对齐（让跨泳道连边画成水平线）；同泳道内的串行节点 y 不同（垂直堆叠）
- **两轮审查不可省**：ASCII 草图审查 + 代码审查，每轮至少 1 个独立 subagent
- **图与需求对应**：ASCII 与代码必须描述同一张图，元素/连接必须一一对应
- **中文术语一致**：同一个概念在同张图内命名一致（不要同时出现"用户/客户/buyer"）
- **不输出业务实现细节**：本 skill 只画图，不写代码、不生成 SQL、不写 PRD
- **模板与示例引用**：见 `templates/` 和 `examples/` 子目录，每个图类型按 ASCII 和代码两个文件拆开

## 目录组织

```
.claude/skills/pm-diagrams/
├── SKILL.md
├── templates/                                  模板（带填写说明 + checklist）
│   ├── product-architecture.ascii.md           ASCII 模板 + 说明
│   ├── product-architecture.drawio             drawio 模板
│   ├── business-process.ascii.md
│   ├── business-process.md                      mermaid 模板（.md 含代码块）
│   ├── swimlane.ascii.md
│   ├── swimlane.drawio
│   ├── sequence.ascii.md
│   ├── sequence.md                              mermaid 模板（.md 含代码块）
│   ├── er.ascii.md
│   └── er.md                                    mermaid 模板（.md 含代码块）
└── examples/                                   示例（只含纯 ASCII + 纯代码）
    ├── product-architecture.ascii.md           只含 ASCII 草图
    ├── product-architecture.drawio             只含 drawio XML
    ├── business-process.ascii.md
    ├── business-process.md                      只含 1 个 mermaid 代码块
    ├── swimlane.ascii.md
    ├── swimlane.drawio
    ├── sequence.ascii.md
    ├── sequence.md                              只含 1 个 mermaid 代码块
    ├── er.ascii.md
    └── er.md                                    只含 1 个 mermaid 代码块
```
