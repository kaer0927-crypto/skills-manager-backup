---
name: drawio-generator
description: >
  AI draw.io 原生生成器。用户要求在文档中生成、创建、绘制或插入任何类型图表时必须使用本技能。
  输出标准 .drawio XML（完整 mxfile 包装），交付可编辑源文件供 draw.io / diagrams.net 导入。
  触发场景：
  (1) 流程图/活动图: "生成流程图" "画流程图" "重新生成流程图" "插入流程图" "生成活动图" "用户操作流程图",
  (2) 架构图: "生成架构图" "画架构图" "插入架构图" "系统架构图",
  (3) 时序图: "生成时序图" "画时序图" "插入时序图" "系统交互时序",
  (4) 泳道图: "生成泳道图" "画泳道图" "插入泳道图",
  (5) ER图: "生成ER图" "实体关系图" "数据库设计图",
  (6) UML图: "生成UML" "类图" "用例图" "状态图",
  (7) 组织结构图: "组织架构图" "组织结构" "人员架构",
  (8) 思维导图: "生成思维导图" "画思维导图" "脑图" "心智图" "知识梳理",
  (9) BPMN: "生成BPMN" "业务流程建模",
  (10) draw.io / diagrams.net 原生 XML、.drawio 文件,
  (11) 任何需要将业务流程、系统架构、数据流或其他内容可视化为图表的请求。
---

# drawio-generator

## 核心原则

**所有图表统一使用 draw.io XML 格式。**

- 不使用 Mermaid、PlantUML、D2 或任何其他图表语言
- 源文件为完整 `<mxfile>...</mxfile>` 包装的 `.xml` / `.drawio`，可直接导入 draw.io / diagrams.net
- **交付物仅为可编辑源文件**；不调用外部 API，不生成 PNG/SVG 等位图或矢量导出
- 生成前先在内部完成节点拆解、坐标计算、连接关系规划和避障路由，避免元素重叠、连线穿透、布局错乱

## 角色定义

你是业务架构师 / 图表架构师，负责将需求转化为清晰、可编辑的可视化图表。输出必须：

1. 准确表达业务逻辑和系统结构
2. 遵循本 Skill 中的 draw.io XML 结构与样式规则
3. 保存完整 XML 并确认文件可被 draw.io 导入后才算完成

## 使用流程

### 单张图表生成

```
1. 确定图表类型 → 查阅类型对照表
2. 读取本技能 `examples/` 下对应类型的模板 XML（作结构与样式参考）
3. 按本 Skill 内部执行流程生成 XML
4. 保存 XML 源文件 → docs/images/src/<名称>.xml
5. 调用本地校验脚本验证结构（见「本地校验脚本」）
6. 向用户说明文件路径及 draw.io 导入方式
```

### 批量生成（需求文档 / PRD 场景）

```
1. 分析文档中所有需要图表的位置
2. 逐张读取对应模板并生成 XML
3. 保存所有 XML 源文件至 docs/images/src/
4. 批量调用本地校验脚本验证每个源文件
5. 在文档中注明各 .xml 路径，或引导用户在 draw.io 中打开编辑
```

## 输入规范

- 用户会提供需要可视化的业务流、状态机、系统架构、数据流或组织结构。
- 需要识别节点层级、节点类型、连接方向、条件分支、循环关系和特殊形状需求。
- 如果用户没有指定方向：流程图 / BPMN / 时序图默认主流程从左到右；纵向泳道图自上而下；系统功能架构图按层自上而下排列；分支节点向下展开，异常/失败路径放在主流程下方；思维导图默认左右平衡（`mindmap.xml`），用户要求层级拆解 / WBS 时用自上而下（`mindmap-vertical.xml`），brainstorm 时用放射状（`mindmap-radial.xml`），正式汇报或打印时用简约线框（`mindmap-minimal.xml`）。

## 输出规范

### 交付物：可编辑源文件

- 输出完整 XML，必须从 `<mxfile>` 开始，到 `</mxfile>` 结束（含 `<?xml version="1.0"?>` 声明亦可）。
- 保存至 `docs/images/src/<模块>-<描述>.xml`（或 `.drawio`），须能被 draw.io / diagrams.net 直接导入。
- 节点内容可用中文；**文件名必须用英文**。

### 输出纪律

- 向用户交付时：说明图表类型、文件路径，以及如何在 draw.io / diagrams.net 中打开（文件 → 打开 → 选择该 XML）。
- 纯 XML 生成场景可不输出额外推演过程；须确认源文件已写入且结构完整。

### 在 Markdown 文档中引用源文件

不插入渲染图片，改用路径或链接指向源文件，便于后续在 draw.io 中编辑：

```markdown
**登录流程图**（draw.io 源文件）：[`docs/images/src/login-flow.xml`](docs/images/src/login-flow.xml)
```

## 图表类型对照表

| 业务场景 | DIAGRAM_TYPE | 模板文件 | 适用情况 |
| --- | --- | --- | --- |
| 流程图 / 活动图 | flowchart | `examples/flowchart.xml` | 单角色线性流程：开始→步骤→判断→分支→结束 |
| 技术架构图 | architecture | `examples/architecture.xml` | 技术分层：接入/网关/微服务/存储/第三方 |
| 系统功能架构图 | system-arch | `examples/system-arch.xml` | 业务功能分层：左侧层标签 + 模块矩阵 + 图例 |
| 时序图 | sequence | `examples/sequence.xml` | 系统间交互、API 调用链 |
| 纵向泳道图 | swimlane | `examples/swimlane.xml` | 多角色纵向泳道、审批驳回回路 |
| 横向泳道图 | cross-functional | `examples/cross-functional.xml` | 跨职能横向泳道（如请假：员工→主管→HR→财务） |
| 矩阵泳道图 | matrix-swimlane | `examples/matrix-swimlane.xml` | 角色 × 阶段二维矩阵（如订单履约多环节） |
| BPMN 流程图 | bpmn | `examples/bpmn-flow.xml` | 含排他/并行网关的标准 BPMN 建模 |
| ER 图 | er | `examples/er-diagram.xml` | 数据库表关系、实体建模 |
| 类图 | class | `examples/uml-class.xml` | 数据模型、继承与关联 |
| 用例图 | usecase | `examples/uml-usecase.xml` | 角色用例、include 关系 |
| 状态图 | state | `examples/uml-state.xml` | 状态机、订单/审批生命周期 |
| 组织结构图 | orgchart | `examples/orgchart.xml` | 部门层级、汇报关系 |
| 思维导图（左右平衡） | mindmap | `examples/mindmap.xml` | 中心主题左右展开、彩色分支：产品规划、需求拆解 |
| 思维导图（自上而下） | mindmap-vertical | `examples/mindmap-vertical.xml` | 主题置顶、层级向下：功能模块、WBS 拆解 |
| 思维导图（放射状） | mindmap-radial | `examples/mindmap-radial.xml` | 中心向四周辐射、高饱和配色：brainstorm、立项发散 |
| 思维导图（简约线框） | mindmap-minimal | `examples/mindmap-minimal.xml` | 灰阶无阴影直角：OKR、汇报材料、正式文档 |

模板路径相对于 `{PROJECT_PATH}/.agents/skills/drawio-generator/`。

### 模板选型指南

| 用户意图 | 推荐模板 | 勿混用 |
| --- | --- | --- |
| 「画流程图 / 用户操作步骤」 | `flowchart.xml` | 多角色协作应选泳道类 |
| 「系统架构 / 技术架构 / 微服务」 | `architecture.xml` | 功能模块清单应选 `system-arch.xml` |
| 「功能架构 / 系统功能模块 / 业务能力分层」 | `system-arch.xml` | 技术栈分层应选 `architecture.xml` |
| 「泳道图 / 跨部门协作」且角色纵向排列 | `swimlane.xml` | 横向职能流选 `cross-functional.xml` |
| 「跨职能流程 / 横向泳道」 | `cross-functional.xml` | 角色×阶段矩阵选 `matrix-swimlane.xml` |
| 「多角色 × 多阶段矩阵」 | `matrix-swimlane.xml` | 简单审批流选 `swimlane.xml` |
| 「BPMN / 业务流程建模 / 网关分支」 | `bpmn-flow.xml` | 普通审批不含网关时选 `swimlane.xml` |
| 「思维导图 / 脑图 / 知识梳理 / 主题拆解」 | 见下方思维导图风格表 | 有汇报关系的层级应选 `orgchart.xml`；有先后顺序应选 `flowchart.xml` |

### 思维导图风格选型

| 用户意图 / 风格偏好 | 推荐模板 | 勿混用 |
| --- | --- | --- |
| 默认 / 左右平衡 / 彩色 B 端 | `mindmap.xml` | 层级向下拆解选 `mindmap-vertical.xml` |
| 功能清单 / WBS / 模块自上而下 | `mindmap-vertical.xml` | 发散 brainstorm 选 `mindmap-radial.xml` |
| brainstorm / 立项发散 / 四周辐射 | `mindmap-radial.xml` | 正式汇报灰阶风选 `mindmap-minimal.xml` |
| 简约 / 线框 / 灰阶 / 打印友好 | `mindmap-minimal.xml` | 需要鲜艳分区配色选 `mindmap.xml` 或 `mindmap-radial.xml` |

## 模板参考流程

生成前自动完成：

1. 按 DIAGRAM_TYPE 读取 `examples/` 下对应模板 XML
2. 以模板为骨架，替换为实际业务内容
3. 对照本 Skill 质量红线自检后输出 XML
4. 保存至 `docs/images/src/` 并验证源文件

## Draw.io 核心结构规则

### 1. XML 结构生命线

必须遵循 draw.io 的基础 XML 树结构。`root` 节点必须包含 id 为 `0` 和 `1` 的系统层。自定义节点 id 从 `2` 开始递增。

除非元素是某个分组或泳道的子元素，否则必须写 `parent="1"`。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="draw.io">
  <diagram name="图表名称" id="唯一ID">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- 自定义节点从 id="2" 开始 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### 2. 画布边距（推荐）

在内容边界外保留至少 30px 视觉留白，避免在 draw.io 中打开时元素贴边：

```xml
<mxCell id="spacer" value="" style="fillColor=none;strokeColor=none;opacity=0;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="{内容最右边X + 60}" height="{内容最底部Y + 60}" as="geometry"/>
</mxCell>
```

### 3. 空域坐标机制

- 视口默认 `800x600` 或更大，按节点数量扩展 `pageWidth` / `pageHeight`。
- 常规节点：宽 `140–180px`，高 `50–80px`；最小宽 100px、高 40px。
- 横向主流程节点间距：`150–220px`（规范下限 50px）。
- 纵向分支间距：`100–160px`（规范下限 60px），为连线路由留出走廊。
- 同一逻辑层级的兄弟节点必须对齐在相同的 `x` 或 `y` 上。
- 任意两个节点的矩形占地区域不得相交。
- 画布内容起始坐标建议 ≥ 30px（x=40, y=40）。

### 4. 连线路由规则

1. 多条边不能共享完全相同的路径。
2. 每条边都要尽量明确 `exitX`、`exitY`、`entryX`、`entryY`。
3. 连接点优先使用边线中点，例如右侧 `exitX=1;exitY=0.5;`、下侧 `exitX=0.5;exitY=1;`。
4. 如果两个节点之间隔着第三个节点，必须添加 `Waypoints` 绕开障碍。
5. 默认使用正交连线，样式包含 `edgeStyle=orthogonalEdgeStyle;rounded=1;`。

Waypoints 示例：

```xml
<mxCell id="10" edge="1" parent="1" source="2" target="4"
  style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#adb5bd;strokeWidth=2;fontColor=#666;exitX=1;exitY=0.5;entryX=0;entryY=0.5;">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="360" y="80"/>
      <mxPoint x="360" y="220"/>
    </Array>
  </mxGeometry>
</mxCell>
```

### 5. 节点、连线、容器骨架

**节点（vertex）：**

```xml
<mxCell id="2" value="节点文字" style="样式字符串" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>
```

**连线（edge）：**

```xml
<mxCell id="10" value="标签" style="edgeStyle=orthogonalEdgeStyle;rounded=0;" edge="1" source="2" target="3" parent="1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

**容器（泳道/分组）：**

```xml
<mxCell id="2" value="泳道名" style="swimlane;startSize=30;" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="700" height="100" as="geometry"/>
</mxCell>
<mxCell id="3" value="子节点" style="rounded=1;" vertex="1" parent="2">
  <mxGeometry x="20" y="40" width="100" height="40" as="geometry"/>
</mxCell>
```

## B 端图表样式库

### 节点样式

| 类型 | style 值 |
| --- | --- |
| 常规动作/模块 | `rounded=1;shadow=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontColor=#333333;fontSize=12;` |
| 判断菱形 | `rhombus;shadow=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#333333;fontSize=12;` |
| 开始圆形 | `ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=12;` |
| 结束圆形 | `ellipse;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=12;` |
| 数据库/存储 | `shape=cylinder3;shadow=1;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;fillColor=#d5e8d4;strokeColor=#82b366;fontColor=#333333;fontSize=12;size=10;` |
| 强调/警告 | `rounded=1;shadow=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontColor=#333333;` |
| 思维导图中心主题 | `ellipse;shadow=1;whiteSpace=wrap;html=1;fillColor=#1565c0;strokeColor=#0d47a1;fontColor=#ffffff;fontSize=14;fontStyle=1;` |
| 思维导图一级分支 | `rounded=1;shadow=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontColor=#333333;fontSize=12;fontStyle=1;arcSize=12;` |
| 思维导图二级节点 | `rounded=1;shadow=1;whiteSpace=wrap;html=1;fillColor=#e3f2fd;strokeColor=#90caf9;fontColor=#333333;fontSize=11;` |
| 思维导图简约中心 | `rounded=0;whiteSpace=wrap;html=1;fillColor=#fafafa;strokeColor=#424242;fontColor=#212121;fontSize=14;fontStyle=1;strokeWidth=2;` |
| 思维导图简约分支 | `rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#757575;fontColor=#424242;fontSize=12;fontStyle=1;` |

### 容器样式

| 类型 | style 值 |
| --- | --- |
| 泳道 | `swimlane;startSize=30;fillColor=#dae8fc;strokeColor=#6c8ebf;html=1;fontSize=13;fontStyle=1;` |
| 分层容器 | `swimlane;startSize=30;fillColor=#f5f5f5;strokeColor=#666666;html=1;fontSize=13;fontStyle=1;horizontal=1;` |
| 分组 | `swimlane;whiteSpace=wrap;html=1;rounded=1;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;` |

### 连线样式

| 类型 | style 值 |
| --- | --- |
| 默认正交 | `edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#adb5bd;strokeWidth=2;fontColor=#666;` |
| 正交（无圆角） | `edgeStyle=orthogonalEdgeStyle;rounded=0;` |
| 直线 | `rounded=0;` |
| 虚线 | `dashed=1;edgeStyle=orthogonalEdgeStyle;rounded=0;` |
| 思维导图分支线 | `curved=1;html=1;strokeColor=#6c8ebf;strokeWidth=2;endArrow=none;` |

## 配色方案

| 语义 | 填充色 | 边框色 | 用途 |
| --- | --- | --- | --- |
| 蓝色系 | #dae8fc | #6c8ebf | 主流程节点、表现层 |
| 绿色系 | #d5e8d4 | #82b366 | 开始节点、成功状态、数据存储 |
| 红色系 | #f8cecc | #b85450 | 结束节点、错误状态 |
| 黄色系 | #fff2cc | #d6b656 | 判断节点、数据层 |
| 紫色系 | #e1d5e7 | #9673a6 | 业务层、中间件 |
| 灰色系 | #f5f5f5 | #666666 | 容器背景、分隔 |

## 文件命名与路径

### 源文件（XML / .drawio）

首次使用前确保输出目录存在：`docs/images/src/`。

```
docs/images/src/<模块>-<描述>.xml
```

示例：`login-flow.xml`、`system-arch.xml`、`order-sequence.xml`

## 本地校验脚本

生成或修改 XML 后，**必须**运行校验脚本确认结构合法（不调用外部 API）。

**Windows（PowerShell，需 Python 3）：**

```powershell
.agents/skills/drawio-generator/scripts/validate-diagram.ps1 docs/images/src/login-flow.xml
```

**Git Bash / Linux / macOS：**

```bash
.agents/skills/drawio-generator/scripts/validate-diagram.sh docs/images/src/login-flow.xml
```

**跨平台（Python 3）：**

```bash
python .agents/skills/drawio-generator/scripts/validate-diagram.py docs/images/src/login-flow.xml
```

**批量校验目录：**

```bash
python .agents/skills/drawio-generator/scripts/validate-diagram.py --dir docs/images/src
```

**可选：** `--check-overlap` 检测顶点包围盒重叠（输出 WARN，不阻断通过）。

校验项（ERROR 级失败则 exit code 1）：

- 文件非空、XML 可解析
- 含 `<mxfile>`、`<mxGraphModel>`、`<root>`
- 含 `mxCell id="0"` 与 `id="1"`
- 顶点含 `parent` 与 `<mxGeometry>`；边含 `edge="1"`、`<mxGeometry>`，以及 **source+target** 或 **sourcePoint+targetPoint**（时序图/浮动连线）
- 无重复 id；边的 source/target 引用存在

WARN 级：非英文文件名、空图、顶点尺寸异常、重叠（启用 `--check-overlap` 时）。

## 布局规范

- 节点最小宽度：100px，高度：40px
- 节点间距：水平 50px，垂直 60px
- 泳道高度：至少 100px
- 字体大小：节点 12px，泳道标题 13px（fontStyle=1 加粗）
- 画布起始坐标：x=40, y=40

## 内部执行流程

收到请求后，在内部完成以下步骤（不必向用户输出推演过程）：

1. **读取模板**：按图表类型读取 `examples/` 下对应 XML 文件
2. **抽取节点**：识别模块、动作、判断、存储、外部系统和异常路径
3. **编排 id**：从 `2` 开始分配节点 id，再分配边 id
4. **计算画布**：按节点数量扩展 `pageWidth` / `pageHeight`；按需添加 spacer 留白
5. **计算坐标**：主流程横向排列，分支纵向排列，异常路径放下方
6. **规划连线**：为每条边选择连接点；遇到障碍时使用 Waypoints
7. **输出 XML**：确保所有节点和边都有合法 `mxGeometry`
8. **保存与验证**：写入 `docs/images/src/`，运行 `validate-diagram.py` 直至通过

## 安全规则

- 不要把用户的密钥、账号凭据、内部服务地址、真实客户数据写入 XML、注释或日志。
- 如需表达敏感系统，使用通用占位名，例如 `Internal API`、`Auth Service`、`Data Store`。

## 质量红线

- 不允许缺少 `mxCell id="0"` 或 `mxCell id="1"`。
- 不允许节点缺少 `parent`。
- 不允许边缺少 `edge="1"`、`source`、`target` 或 `mxGeometry`。
- 不允许 XML 标签不闭合、属性引号缺失或非法嵌套。
- 不允许节点重叠；不允许主流程连线直接穿透中间节点。
- 不允许把敏感凭据、真实密钥或私有路径写进输出。
- 不建议使用 emoji（部分环境显示不一致）。
- 不允许文字节点叠放（标题与描述应在同一 cell 的 value 中用 HTML 换行）。

## 禁止行为

1. **禁止使用 Mermaid / PlantUML / D2** — 所有图表必须是 draw.io XML
2. **禁止调用外部渲染 API 或生成 PNG/SVG** — 交付物仅为 `.xml` / `.drawio` 源文件
3. **禁止省略 id="0" 和 id="1"** — 这两个根节点是 draw.io 必需的
4. **禁止使用中文文件名** — 文件名用英文，节点内容可以用中文
5. **禁止不验证就声称完成** — 须运行 `validate-diagram` 脚本通过后再交付
6. **禁止输出不完整的 XML** — 必须有 mxfile 包装
