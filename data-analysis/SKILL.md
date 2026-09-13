---
name: data-analysis
description: |
  CSV 智能数据分析 + 单文件离线可视化报告 Skill（v2 精简版）。
  接收一份 CSV + 用户自然语言需求，自动完成字段角色识别、核心指标计算、图表选型，
  并由 Claude 以「数据分析专家」视角产出结构化 AI 洞见，最终渲染成单文件离线 HTML 报告。
  拿到数据先探查字段语义（--explore），由 Claude 尽可能多地拆解候选分析指标与维度，
  以提问沟通的方式与用户确认本次分析目标和方案，确认结果落成 focus.json 后再正式分析。
  支持用户用自然语言指定分析目标 / 重点维度 / 度量 / 时间粒度（Claude 解析为 focus.json 传给 analyze.py）。
  报告只含四个板块：核心指标、AI 智能洞见、可视化分析、可视化分析数据（每张图表底层数据，支持一键导出 CSV）。
  报告内嵌 ECharts、零远程依赖，双击即可离线打开，并自适应桌面 / 平板 / 手机（H5 移动端）。
  触发场景：用户上传 / 指定一份 .csv 文件并说「分析 / 出一份报告 / 帮我看看 / 做个可视化看板」等。
---

# data-analysis —— CSV 智能分析可视化报告

> **设计原则（唯一保留）**：数据先落地为可分析结构 → 专家视角 AI 洞见 → 单文件离线 HTML 报告。
> 相比 v1，本版**大幅精简**：只支持 CSV、只有两个脚本、报告只有四个板块。
>
> **新能力**：① 报告自适应桌面 / 平板 / 手机（H5 移动端）；② 支持用户用自然语言指定分析目标 / 维度 / 度量 / 时间粒度（`focus.json`）；③ **拿到数据先分析字段语义**（金额/单价/数量/标识/分类/日期等细粒度），用户可提供字段语义说明（`schema.json`），以其为权威依据覆盖自动推断；④ 报告渲染成功后**自动清理中间文件**，仅保留 HTML 与原始 CSV；⑤ **先确认方案再分析**：探查字段语义后，Claude 尽可能多地拆解候选分析指标与维度，以提问沟通的方式与用户确认本次分析目标和方案，按确认结果定后续分析（`--explore` + 第 ⓪ 步）。


---

## 1. 主流程（⓪ 方案确认 + 三步执行）

```
  一份 CSV
     │  ⓪ python scripts/analyze.py <data.csv> --explore    （只探查，不产文件）
     ▼
  字段语义画像 ──► Claude 拆解候选指标 / 维度 ──► 提问式与用户确认分析目标和方案
     │             确认结果 → focus.json（分析意图）/ schema.json（字段语义纠正）
     │  ① python scripts/analyze.py <data.csv>              （带 --focus / --schema）
     ▼
  <data>.analysis.json      ← 字段语义 + 字段角色 + 核心指标(KPI) + 图表数据 + 字段画像
     │  ② Claude 读取它，以数据分析专家视角写 AI 洞见（五段式）
     ▼
  <data>.insights.json      ← 核心结论 / 支撑数据 / 异常与风险 / 可执行建议 / 下一步
     │  ③ python scripts/report.py <data>.analysis.json --insights <data>.insights.json
     ▼                            （默认 --clean：渲染后删除中间 JSON，仅留 HTML 与原始 CSV）
  <data>_报告.html          ← 单文件离线报告，四板块，双击即开
```

**关键分工**：
- **分析方案由用户确认**——第 ⓪ 步 Claude 先拆解、再提问，确认的目标与方案是后续所有步骤的依据。
- `analyze.py` 做**确定性数据处理**（pandas）——不臆造结论；**先做字段语义分析**，再做角色识别 / KPI / 图表。
- **AI 洞见由 Claude 亲自写**——这是本 Skill 的价值核心，不交给脚本模板。
- `report.py` 只做**渲染**——把数据 + 洞见拼成离线 HTML，并清理中间文件。

---

## 2. 环境准备

只依赖 `pandas`。若环境已有 pandas 可直接用；否则：

```bash
pip install -r .claude/skills/data-analysis/scripts/requirements.txt
```

> 建议在 Claude Code 会话里先 `python -c "import pandas"` 确认可用。

---

## 3. 执行步骤（Claude 按此操作）

设数据文件为 `D:/work/orders.csv`，工作目录为 skill 根目录。

### 第 ⓪ 步：探查字段语义 → 拆解候选指标/维度 → 与用户确认分析方案（提问沟通式）

**拿到数据后不要直接跑完整分析**，先用探查模式了解数据、再和用户对齐「分析什么、怎么看」：

```bash
python scripts/analyze.py D:/work/orders.csv --explore
```

探查模式**不写任何文件**，只在终端打印：逐列画像（`列名 | role@semantic | dtype | 非空/唯一 | 统计或样本`）、
候选度量、适合分组的维度（基数适中）、高基数/标识类维度、时间列与时间跨度。

**1）Claude 基于画像拆解候选分析方向——尽可能多**。按「度量 × 维度 × 时间」组合展开，例如：

- **核心指标（KPI）**：每个度量的合计 / 均值 / 最大值（如销售金额合计、平均单价）
- **趋势**：每个度量 × 时间列，按日 / 月 / 季（如销售金额月度趋势）
- **对比 / 占比**：每个度量 × 每个适合分组的维度（如各大区销售金额对比、渠道占比）
- **交叉视角**：结合字段语义提出的业务问题（如「高单价商品集中在哪个品类」「退款是否集中在某渠道」）

**2）用提问沟通的方式与用户确认**。把拆解结果整理成候选清单，用 `AskUserQuestion`（或直接提问）组织 2~4 个问题让用户挑选与补充，选项**只用真实列名**、不臆造：

- **本次分析目标**：从拆解出的业务问题中列 3~4 个候选方向（可多选 / 可自填）
- **重点度量**：候选度量列表（多选）
- **重点维度**：适合分组的维度列表（多选）
- **时间粒度 / TopN**：有时间列时问粒度（日 / 月 / 季 / 自动）

同时把探查发现的**疑似语义问题**一并确认（如「`订单号` 是数值列但看起来是标识，将不作为度量，对吗？」）。

**3）按用户确认的内容定后续分析方案**：

- 确认的目标 / 度量 / 维度 / 粒度 → 写成 `focus.json`（`goal` 填用户确认的分析目标原话）
- 用户对字段含义的说明或纠正 → 写成 `schema.json`
- 两个文件都落在**与数据同目录**，进入第 ① 步

**跳过确认的例外**（避免为问而问）：

- 用户在最初请求里**已经说清**分析目标和重点维度 / 度量 → 直接解析成 `focus.json`，向用户简要复述方案后进入第 ① 步，不再重复提问
- 用户明确表示「直接出报告 / 都行 / 你看着办」，或处于**无法交互的场景**（批处理、定时任务）→ 跳过提问，走全自动分析（不带 `--focus`）

### 第 ① 步：分析字段语义 → 再跑自动分析

**字段语义在第 ⓪ 步探查时已初步呈现**——不只是 time/measure/dimension 三类粗角色，
而是金额 / 单价 / 数量 / 标识 / 分类 / 日期 等细粒度业务语义。正式分析时语义有两种来源：

1. **用户提供字段语义说明**（权威依据）：用户用自然语言说明了字段含义 / 单位 / 哪些是标识列，
   Claude 把它转译成结构化的 `schema.json`（落在**与数据同目录**）传给 `analyze.py --schema`，
   脚本以用户语义为准覆盖自动推断。
2. **自动推断**（用户未提供时）：脚本按列名 / dtype / 值域自动给出语义标签，Claude 在终端输出
   核对，若有误可改 `schema.json` 重新分析。

`schema.json` 格式（**每个字段任一键均可缺省**，缺省键自动推断；用户填的键为权威依据）：

```json
{
  "销售金额": {"role": "measure", "semantic": "amount", "unit": "元", "desc": "订单实付金额"},
  "单价":     {"semantic": "price", "unit": "元"},
  "订单号":   {"role": "dimension", "semantic": "identifier", "desc": "业务订单编号，非度量"},
  "是否退款": {"semantic": "flag"}
}
```

> `role` 取 `time` / `measure` / `dimension`（覆盖自动角色识别，影响 KPI 与图表）；
> `semantic` 取 `amount`/`price`/`quantity`/`datetime`/`identifier`/`category`/`flag`/`text`/`measure` 等；
> `unit` / `desc` 仅记录进 `profile`，供写洞见参考。Claude 只做「自然语言→现有列名」的映射，不臆造列名。

**默认自动分析 + 自动字段语义推断**（无需用户输入）：

```bash
python scripts/analyze.py D:/work/orders.csv --title "订单分析"
```

**用户提供字段语义说明时**（转成 `schema.json` 传入，作为权威依据）：

```bash
python scripts/analyze.py D:/work/orders.csv --title "订单分析" --schema D:/work/orders.schema.json
```

**同时指定字段语义 + 分析意图**（schema 决定字段怎么读，focus 决定怎么看）：

```bash
python scripts/analyze.py D:/work/orders.csv --title "订单分析" \
  --schema D:/work/orders.schema.json --focus D:/work/orders.focus.json
```

> 字段语义必须先于 focus 生效：`apply_schema` 覆盖 role 后，`focus` 里指定的 measures/dimensions
> 再按覆盖后的 role 校验。因此把 ID 类列在 schema 里标成 `dimension`，可避免它被误当度量。

**或：把分析意图解析成 `focus.json` 后再分析**——
第 ⓪ 步与用户确认的分析目标 / 度量 / 维度 / 粒度，以及用户直接用自然语言说明的
「分析什么 / 按什么维度 / 关注什么重点」，都解析成 `focus.json`
（落在**与数据同目录**），传给 `analyze.py --focus`：

`focus.json` 的字段（**全部可选**，未填/无效的键自动回退到自动识别，不会报错）：

```json
{
  "goal": "评估各区域销售表现与渠道贡献，找出增长和下滑来源",
  "measures": ["销售金额", "利润"],
  "dimensions": ["大区", "渠道"],
  "time_col": "下单日期",
  "granularity": "ME",
  "topn": 10
}
```

| 键 | 含义 | 约束 |
|---|---|---|
| `goal` | 分析目标，仅记入 `meta.analysis.goal` 供写洞见参考 | 任意文字 |
| `measures` | 指定主度量（按此顺序优先，影响 KPI 头卡与图表度量） | 必须为数值列；非数值列被静默过滤 |
| `dimensions` | 指定优先切分维度（强制排最前；高基数列按 `topn` 截断展示） | 必须为维度列 |
| `time_col` | 指定用作趋势的时间列 | 必须为可解析日期的时间列 |
| `granularity` | 趋势粒度：`D` 日 / `ME` 月 / `QE` 季 | 不填则按时间跨度自动选 |
| `topn` | 对比 / 占比图每张最多展示项数 | 整数，默认 12 |
| `max_charts` | 图表总数软上限（核心图优先保留，截尾不伤主图） | 整数；不填 / 0 = 不限，张数按数据实际情况灵活生成 |

> 解析原则：Claude 只做「把自然语言映射到现有列名与合法取值」的转译，不臆造列名；
> 用户说的「按地区看」就去找大区/省份列并写入 `dimensions`，用户没说的键一律不填。

- 产物默认与数据同目录：`D:/work/orders.analysis.json`
- 终端会打印识别到的**字段语义**（逐列 `列名:role@semantic`，如 `库存金额:measure@amount`、`SKU ID:dimension@identifier`）与**字段角色**，以及本次分析的**主度量 / 优先维度 / 时间列 / 粒度 / TopN**
- `meta.field_semantics.source` 标明本次字段语义的依据是 `schema.json`(用户提供) 还是 `auto-inferred`
- 若语义/角色识别有误（如把某 ID 数值列错当度量），用 `--schema` 提供字段语义说明覆盖后再继续

### 第 ② 步：Claude 写 AI 洞见（本 Skill 的核心）

读取 `orders.analysis.json`，**重点看 `kpis`、`charts`、`profile` 三个字段**（`profile` 现含每列的 `semantic` 细粒度语义与 `desc` 业务含义，写洞见时以用户提供的字段语义为准），然后**以资深数据分析专家的视角**写一个 `orders.insights.json`，严格包含以下五个键：

```json
{
  "core_conclusion": "一句话点明最重要的结论（可含关键数字与趋势判断）",
  "supporting_data": ["用具体数字支撑上面的结论", "……"],
  "risks": ["数据中暴露的异常、集中度、下滑、缺失等风险", "……"],
  "recommendations": ["可落地、可执行的具体建议（谁做什么）", "……"],
  "next_steps": ["为把分析做深，下一步需要补的数据 / 要验证的假设", "……"]
}
```

**洞见撰写要求**：
- **结论先行**：`core_conclusion` 必须是判断，不是数据复述。
- **用数据说话**：`supporting_data` 每条都要带具体数字 / 占比 / 变化幅度。
- **敢于指出风险**：`risks` 关注集中度、异常波动、下滑、样本不足、数据质量。
- **建议可执行**：`recommendations` 落到具体动作，避免「加强管理」这类空话。
- **有下一步**：`next_steps` 指出当前数据的盲区与要补的分析。
- 字符串或字符串数组均可；除 `core_conclusion` 建议用整段文字外，其余建议用数组。

> 也可以不单独建文件，直接把这段 JSON 写进 `analysis.json` 的 `insights` 字段，第 ③ 步就不用 `--insights`。

### 第 ③ 步：渲染离线报告

```bash
python scripts/report.py D:/work/orders.analysis.json --insights D:/work/orders.insights.json
```

- 产物：`D:/work/订单分析_报告.html`（默认与数据同目录）
- 用 `--out <路径>` 可自定义输出位置
- 报告内嵌 ECharts，**无任何远程引用**，拷给任何人双击即开
- **默认 `--clean`**：渲染成功后自动删除中间文件（`analysis.json` / `insights.json` / `focus.json` / `schema.json`，仅删 `.json`），**只保留 HTML 与原始 CSV**。需保留中间文件调试时加 `--no-clean`

---

## 4. 报告的四个板块（固定）

| 板块 | 内容 |
|---|---|
| **核心指标** | KPI 卡片：总记录数 + 各度量的合计 / 均值 / 最大值 |
| **AI 智能洞见** | Claude 写的五段式洞见（核心结论 / 支撑数据 / 异常与风险 / 可执行建议 / 下一步） |
| **可视化分析** | ECharts 图表，**张数不固定、按数据实际情况灵活生成**：每个度量的时间趋势（折线）、每个适合分组维度的对比（柱状）、低基数维度的占比（饼图），自动选型；可用 `focus.max_charts` 设软上限 |
| **可视化分析数据** | 每张图表所依据的底层数据小表 + 「⬇ 导出 CSV」按钮（纯前端 Blob 下载，离线可用，带 BOM 兼容 Excel；导出含全部图表数据） |

> **移动端自适应**：报告 CSS 以流式布局 + 媒体查询实现；≤640px 时栅格降为单列、`<480px` 时 KPI 双列、
> 字号/间距/圆角收紧、图表高度降到 280px、ECharts tooltip 限定容器内不溢出、坐标轴标签 45° 倾斜，
> 并适配刘海屏安全区（`viewport-fit=cover` + `env(safe-area-inset-*)`）。手机浏览器直接打开即可阅读。

---

## 5. 字段角色与语义识别规则（analyze.py 自动）

**字段语义分析先于角色识别**：先按列名 / dtype / 值域推断每列 `semantic`（amount 金额 / price 单价 /
quantity 数量 / datetime 时间 / identifier 标识 / category 类别 / flag 标志 / text 文本 / measure 通用度量），
再由 `semantic` + 规则归纳 `role`（time / measure / dimension）。

| 角色 | 判定 |
|---|---|
| **time 时间** | 列名含 date/时间/日期/月/年… 且可解析为日期；或整列 ≥90% 可解析为日期 |
| **measure 度量** | 数值类型，且**不是** ID（列名不含 id/编号/code…，且非近乎唯一） |
| **dimension 维度** | 其余（文本 / 类别 / ID 列） |

- **用户提供 `schema.json` 时为权威依据**：用户指定的 `role` / `semantic` 覆盖自动推断，`unit` / `desc` 仅记录
- 趋势图用「时间列 × 每个度量」（主度量在前），按跨度自动选日/月/季粒度聚合（`focus.granularity` 可强制覆盖）
- 对比 / 占比图只选**基数适中**的维度（排除接近唯一的 ID 列）；**图表张数不设固定上限**：每个适合分组的维度出一张柱状，主维度及低基数（≤10 类）维度追加饼图，`focus.max_charts` 可设软上限（核心图优先保留）
- 传了 `focus.json` 时：用户指定的 `measures`/`dimensions`/`time_col` 优先级最高（基于 schema 覆盖后的 role 校验）——指定维度强制排最前（高基数列按 `topn` 截断展示），其余行为不变
- 识别不理想时，用 `--schema` 提供字段语义说明覆盖，或手工编辑 `analysis.json` 里的 `charts` / `kpis` 再渲染

---

## 6. 扩展其他数据源（保留的可能性）

只支持 CSV 是刻意的精简。要接入 Excel / API / MySQL 时，**唯一改动点**是
`scripts/analyze.py` 的 `load_dataframe()`：按后缀 / 协议返回一个 `DataFrame` 即可，
下游的角色识别、KPI、图表、字段画像、报告渲染**完全不用改**。文件内已标注扩展点位置。

---

## 7. 目录结构

```
data-analysis/
├── SKILL.md                     (本文件)
├── scripts/
│   ├── analyze.py               (CSV → analysis.json：字段语义分析 + 角色识别 + KPI + 图表 + 字段画像；支持 --focus / --schema；--explore 探查模式供方案确认)
│   ├── report.py                (analysis.json + insights → 单文件离线 HTML；默认 --clean 清理中间文件，仅留 HTML)
│   └── requirements.txt         (仅 pandas)
├── assets/
│   └── echarts.min.js           (离线 ECharts 5.5.1，渲染时内联进 HTML)
```

---

## 8. 常见问题

| 现象 | 原因 / 解法 |
|---|---|
| `ModuleNotFoundError: pandas` | `pip install -r scripts/requirements.txt` |
| 报告里 AI 洞见是黄色占位提示 | 没传 `--insights`，或 `analysis.json` 的 `insights` 为空——回到第 ② 步 |
| 中文乱码 | 源 CSV 非 UTF-8；脚本已自动尝试 utf-8-sig/gbk，仍失败请另存为 UTF-8 |
| 图表分组维度不合理 | ID 类被当维度；用 `--schema` 把该列标成 `identifier`，或用 `--focus` 指定想看的 `dimensions`，或手工编辑 `analysis.json` 的 `charts` 再渲染 |
| 字段语义被识别错（如 ID 被当度量） | 用 `--schema` 提供字段语义说明覆盖自动推断（见第 ① 步）；用户语义为权威依据 |
| 想固定看某些列 / 某种粒度 | 把自然语言意图解析成 `focus.json`，用 `--focus` 传给 `analyze.py`（见第 ① 步） |
| 不确定该分析什么 / 想先看看数据里有什么 | 跑 `--explore` 探查（不产文件），Claude 拆解候选指标 / 维度后与用户确认方案（见第 ⓪ 步） |
| 报告方向与用户预期不符 | 大概率跳过了第 ⓪ 步确认；回到第 ⓪ 步重新对齐目标，把确认结果写进 `focus.json` 重跑 |
| 渲染后想改洞见/图表重渲染却找不到 `analysis.json` | `report.py` 默认 `--clean` 已把它删掉；重跑需从第 ① 步开始，或之前用 `--no-clean` 保留中间文件 |
| 报告在手机上显示拥挤 | 报告已自适应移动端；若仍异常，确认浏览器未强制桌面模式，或检查是否被缓存旧版 HTML |
| 报告 HTML 体积偏大（约 1MB+） | 主要是内嵌的 `echarts.min.js`；如需更小可换用裁剪版 ECharts |
| 终端输出中文乱码 | Windows GBK 控制台显示问题，不影响生成的文件内容 |
