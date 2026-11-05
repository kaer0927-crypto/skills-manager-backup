# drawio-generator

**draw.io 原生 XML 图表生成技能**——面向产品、架构与研发协作，将业务流程、系统结构、数据关系等描述转化为可直接导入 draw.io 编辑器中的**可编辑源文件**。

内置 17 种业务模板，覆盖单角色流程、多角色协作、系统架构、数据建模与 4 种思维导图风格等场景。Agent 按技能规范选取模板，结合 B 端配色与布局规则，在内部完成节点拆解、坐标计算、正交连线与 Waypoints 避障，输出完整 `.xml`源文件，可直接导入 draw.io 继续编辑或与团队共享。

推荐使用 VibePM 在线图表编辑器对产出的 XML 文件进行编辑导出，它基于成熟的 draw.io 能力打造，可搭配技能形成闭环：AI 先产出可编辑源文件 → 浏览器里打开微调 → 再导出分享。

**VibePM 在线图表编辑器地址：**  
[https://www.vibepm.net/drawio/](https://www.vibepm.net/drawio/)

**适用场景：**

- **PRD / 需求文档配图** — 为登录流程、审批链路、系统架构等章节生成 draw.io 源文件，在 Markdown 中以链接引用，读者可一键打开编辑
- **可编辑优先** — 图表需反复调整版式、配色或文案时，保留 XML 比固定位图更灵活、可追溯
- **离线 / 零依赖** — 无网络或不便调用第三方服务时，仅需 Python 3 即可完成生成与校验
- **全类型业务图** — 流程图与活动图、技术/功能架构、时序图、纵向/横向/矩阵泳道、BPMN、ER 图、UML（类/用例/状态）、组织结构图、思维导图等

技能目录自包含（模板库 + 校验脚本），可独立复制到 Cursor、Codex、Claude Code 等 Agent 环境。图表统一采用 draw.io XML，**不使用** Mermaid、PlantUML、D2 等替代格式。

## 能力特点

- 内置 17 种业务模板（含 4 种思维导图风格），覆盖从单角色流程到主题发散梳理的常见场景
- 强制绝对坐标、节点间距、正交连线，降低元素重叠、连线穿模与布局错乱
- 附带 B 端配色方案与节点/泳道/连线样式库，输出风格一致
- 本地校验脚本（`validate-diagram.py`）验证 `mxfile` 结构、根节点、边引用等质量红线，无需联网

## 图表示例

<img width="1060" height="740" alt="architecture" src="https://github.com/user-attachments/assets/d4f07224-63ff-4fa6-a8f2-180a0e6e444d" />

<img width="2120" height="1480" alt="matrix-swimlane" src="https://github.com/user-attachments/assets/87a7d4da-863c-4fc3-85ab-4993b818b5ee" />

<img width="1060" height="700" alt="swimlane" src="https://github.com/user-attachments/assets/29e8de81-28d8-43c7-8d3a-364fadb2bd5e" />

<img width="1260" height="690" alt="system-arch" src="https://github.com/user-attachments/assets/8609f781-8702-4530-a3ad-5062267faafc" />

<img width="922" height="1151" alt="flowchart" src="https://github.com/user-attachments/assets/0249320c-39f2-4df9-8843-524dd4bb5caf" />


## 触发关键词

用户消息命中以下任一表述时，Agent 应加载本技能（完整规则见 SKILL.md）：

- **流程图 / 活动图：** 生成流程图、画流程图、插入流程图、用户操作流程图 …
- **架构图：** 生成架构图、系统架构图、技术架构 …
- **时序图：** 生成时序图、系统交互时序 …
- **泳道图：** 生成泳道图、跨部门协作流程 …
- **ER 图：** 实体关系图、数据库设计图 …
- **UML：** 类图、用例图、状态图 …
- **组织：** 组织架构图、人员架构 …
- **思维导图：** 生成思维导图、脑图、知识梳理、主题拆解 …
- **BPMN：** 业务流程建模 …
- **原生格式：** draw.io XML、`.drawio` 文件 …

## 目录结构

```
drawio-generator/
├── SKILL.md                  # Agent 执行规则（类型对照、布局、样式、质量红线）
├── README.md                 # 本文件（人类阅读）
├── LICENSE                   # MIT
├── .gitignore
├── scripts/                  # 本地校验（无 API）
│   ├── validate-diagram.py
│   ├── validate-diagram.ps1
│   └── validate-diagram.sh
└── examples/                 # 17 种 draw.io 模板 XML
    ├── 模板索引.md             # 人类浏览用；Agent 以 SKILL.md 为准
    ├── flowchart.xml           # 流程图 / 活动图
    ├── architecture.xml        # 技术架构图
    ├── system-arch.xml         # 系统功能架构图
    ├── sequence.xml            # 时序图
    ├── swimlane.xml            # 纵向泳道图
    ├── cross-functional.xml    # 横向泳道图
    ├── matrix-swimlane.xml     # 角色 × 阶段矩阵泳道
    ├── bpmn-flow.xml           # BPMN（含网关）
    ├── er-diagram.xml          # ER 图
    ├── uml-class.xml           # UML 类图
    ├── uml-usecase.xml         # UML 用例图
    ├── uml-state.xml           # UML 状态图
    ├── orgchart.xml            # 组织结构图
    ├── mindmap.xml             # 思维导图（左右平衡）
    ├── mindmap-vertical.xml    # 思维导图（自上而下）
    ├── mindmap-radial.xml      # 思维导图（放射状）
    └── mindmap-minimal.xml     # 思维导图（简约线框）
```

> **完整性说明：** `SKILL.md` 类型对照表所列 17 个模板文件均已就绪；`examples/模板索引.md` 提供各模板示例内容概要；`scripts/` 提供本地 XML 校验。本技能仅交付可编辑源文件，不包含 PNG/SVG 渲染能力。

## 支持的图表类型

| 业务场景 | DIAGRAM_TYPE | 模板文件 |
| --- | --- | --- |
| 流程图 / 活动图 | `flowchart` | `examples/flowchart.xml` |
| 技术架构图 | `architecture` | `examples/architecture.xml` |
| 系统功能架构图 | `system-arch` | `examples/system-arch.xml` |
| 时序图 | `sequence` | `examples/sequence.xml` |
| 纵向泳道图 | `swimlane` | `examples/swimlane.xml` |
| 横向泳道图 | `cross-functional` | `examples/cross-functional.xml` |
| 矩阵泳道图 | `matrix-swimlane` | `examples/matrix-swimlane.xml` |
| BPMN 流程图 | `bpmn` | `examples/bpmn-flow.xml` |
| ER 图 | `er` | `examples/er-diagram.xml` |
| UML 类图 | `class` | `examples/uml-class.xml` |
| UML 用例图 | `usecase` | `examples/uml-usecase.xml` |
| UML 状态图 | `state` | `examples/uml-state.xml` |
| 组织结构图 | `orgchart` | `examples/orgchart.xml` |
| 思维导图（左右平衡） | `mindmap` | `examples/mindmap.xml` |
| 思维导图（自上而下） | `mindmap-vertical` | `examples/mindmap-vertical.xml` |
| 思维导图（放射状） | `mindmap-radial` | `examples/mindmap-radial.xml` |
| 思维导图（简约线框） | `mindmap-minimal` | `examples/mindmap-minimal.xml` |

### 思维导图风格速查

| 风格 | 模板 | 适用场景 |
| --- | --- | --- |
| 左右平衡（默认） | `mindmap.xml` | 产品规划、彩色 B 端分支 |
| 自上而下 | `mindmap-vertical.xml` | 功能模块、WBS 层级拆解 |
| 放射状 | `mindmap-radial.xml` | brainstorm、立项发散 |
| 简约线框 | `mindmap-minimal.xml` | OKR、汇报、打印友好 |

### 模板选型速查

| 用户意图 | 推荐模板 | 常见误选 |
| --- | --- | --- |
| 单角色操作步骤 / 线性流程 | `flowchart.xml` | 多角色协作应选泳道类 |
| 技术栈 / 微服务 / 网关分层 | `architecture.xml` | 功能模块清单应选 `system-arch.xml` |
| 业务能力 / 功能模块分层 | `system-arch.xml` | 技术分层应选 `architecture.xml` |
| 多角色纵向泳道 | `swimlane.xml` | 横向职能流选 `cross-functional.xml` |
| 跨职能横向流程 | `cross-functional.xml` | 二维矩阵选 `matrix-swimlane.xml` |
| 角色 × 阶段矩阵 | `matrix-swimlane.xml` | 简单审批选 `swimlane.xml` |
| BPMN 网关 / 并行会签 | `bpmn-flow.xml` | 无网关审批选 `swimlane.xml` |
| 思维导图 / 脑图 / 知识梳理 | 见「思维导图风格速查」 | 汇报层级选 `orgchart.xml`；有先后顺序选 `flowchart.xml` |

## 工作流程

### 单张图表

1. 确定图表类型 → 查阅上表
2. Agent 读取 `examples/` 下对应模板 XML（结构与样式参考）
3. 按 `SKILL.md` 内部流程：拆解节点 → 分配 id → 计算坐标 → 规划连线 → 输出 XML
4. 保存至 `docs/images/src/<模块>-<描述>.xml`（首次使用前创建该目录）
5. 运行本地校验脚本（见下方「本地校验」）
6. 向用户说明路径及 draw.io 导入方式

### 批量（PRD / 需求文档）

1. 扫描文档中所有需图表的位置
2. 逐张生成并保存至 `docs/images/src/`
3. 在 Markdown 中用链接引用各源文件（见下方「文档引用」）

## 本地校验

生成或修改 XML 后运行校验脚本（仅需 Python 3 标准库，无网络）：

**Windows（PowerShell）：**

```powershell
.agents/skills/drawio-generator/scripts/validate-diagram.ps1 docs/images/src/login-flow.xml
```

**Git Bash / Linux / macOS：**

```bash
.agents/skills/drawio-generator/scripts/validate-diagram.sh docs/images/src/login-flow.xml
```

**跨平台 / 批量：**

```bash
python .agents/skills/drawio-generator/scripts/validate-diagram.py --dir docs/images/src
python .agents/skills/drawio-generator/scripts/validate-diagram.py --check-overlap docs/images/src/login-flow.xml
```

校验通过时 exit code 为 `0`；存在 ERROR 级问题时为 `1`。Agent 须在声称交付完成前跑通校验。

| 级别 | 检查项 |
| --- | --- |
| ERROR | 非空、XML 合法、含 `mxfile` / `mxGraphModel` / `root`、`id="0"`/`"1"`、顶点/边结构完整、无重复 id、边引用有效；边需 source+target 或 sourcePoint+targetPoint |
| WARN | 非英文文件名、空图、顶点尺寸异常；`--check-overlap` 时报告可能重叠 |

## 安装与集成

本仓库即技能包根目录（顶层含 `SKILL.md`）。克隆或复制到 Agent 的技能目录即可使用。

### 自动安装：
把链接发给智能体，让它帮你安装。在 Cursor 等 Agent 对话里复制下面这句即可：
```text
请帮我安装这个技能：https://github.com/vibepm666/drawio-generator
克隆到个人技能目录（或项目技能目录）。
```

### 手动安装：

下载项目压缩包，解压后将整个 `drawio-generator` 文件夹放入技能目录即可。

### 目录说明：
技能目录分两种：**个人技能**（所有项目可用）与 **项目技能**（仅当前项目可用）。以 Cursor 为例：
| 类型 | 路径 |
| --- | --- |
| 个人技能 | `~/.cursor/skills/drawio-generator/` ~/是Cursor数据存储目录 |
| 项目技能 | `.cursor/skills/drawio-generator/` 或 `.agents/skills/drawio-generator/` |


## 输出规范

### 文件路径与命名

```
docs/images/src/<module>-<description>.xml
```

- **文件名必须英文**（kebab-case），节点文字可用中文
- 示例：`login-flow.xml`、`order-sequence.xml`、`crm-usecase.xml`

### 在 Markdown 中引用

本技能**不插入渲染图片**，用链接指向源文件：

```markdown
**登录流程图**（draw.io 源文件）：[`docs/images/src/login-flow.xml`](docs/images/src/login-flow.xml)
```

### 在 draw.io 中打开

1. 打开 [app.diagrams.net](https://app.diagrams.net/)
2. **文件 → 打开 from → Device**（或拖入 `.xml` / `.drawio`）
3. 选择 `docs/images/src/` 下对应文件继续编辑

## 示例请求

**流程图**

```text
请生成用户注册流程 draw.io 源文件：
访问注册页 → 输入手机号 → 校验验证码 → 创建账号 → 写入用户表 → 注册成功。
```

**技术架构图**

```text
画一张 SaaS 订单系统技术架构图（draw.io XML）：
接入层（Web/App）→ API 网关 → 订单/支付/库存微服务 → MySQL + Redis + MQ。
```

**纵向泳道图**

```text
生成费用报销审批泳道图，角色：员工、主管、财务、HR；含主管驳回回路。
```

**时序图**

```text
下单支付时序图：用户、订单服务、库存服务、支付网关、回调通知。
```

**思维导图**

```text
生成「AI 写作助手」产品规划思维导图：
中心主题 AI 写作助手；分支包括目标用户、核心功能、商业模式、技术栈、竞品差异，各分支下再拆 2～3 个子要点。
```

期望交付：完整可导入的 XML，保存路径如 `docs/images/src/user-register-flow.xml`。

## 质量红线（摘要）

完整规则见 [CODE0](SKILL.md)「质量红线」与「禁止行为」章节。

- 必须有 `mxCell id="0"` 与 `id="1"`；自定义 id 从 `2` 递增
- 节点不得重叠；连线不得穿透中间节点（需 Waypoints 绕障）
- 边必须含 `edge="1"`、`source`、`target`、`mxGeometry`
- 禁止 Mermaid / PlantUML / D2；禁止调用 API 生成 PNG/SVG
- 禁止中文文件名；禁止未验证就声称完成
- 敏感信息使用占位名（如 `Auth Service`、`Internal API`）

## 安全说明

- 不要把 API Key、Token、密码、Cookie、私钥写入 `SKILL.md`、输出 XML 或提交记录
- 公开发布前建议做一次敏感信息扫描
- `.gitignore` 已排除 `.env`、密钥与本地凭证类文件

## 许可

[MIT License](LICENSE) — Copyright (c) 2026 VibepPM.net
