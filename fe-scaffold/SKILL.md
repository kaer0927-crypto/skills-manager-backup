---
name: fe-scaffold
description: 前端 Demo/MVP 快速搭建流水线（需求理解→技术方案→任务拆解→多Agent并行开发→验收修复，共5个阶段）。当用户要搭前端 Demo、做产品原型、快速出 MVP、给客户做演示系统，或对现有前端项目做大版本重构时使用。主 Agent 当架构师，编码工作拆给多个并行子任务执行。
---

# 前端 Demo 搭建流水线（P1–P5）

> 作者：liuyz | 版本：V2.0（可移植版）| 复盘来源：AI Frontend Scaffold 重构实战

## 核心理念

**主 Agent 是架构师，不是码农。** 主 Agent 负责理解需求、定方案、拆任务、写子任务 Prompt；真正的编码由多个子 Agent 并行执行。优势：主 Agent 保持全局视野；子 Agent 文件零重叠、并行不冲突；每个子任务 Prompt 自包含、不依赖对话历史。

## 流水线全景

```
P1 需求理解与技术方案   → implementation_plan.md   🔴 GATE 确认方案
P2 任务拆解            → task.md                  🔴 GATE 确认任务
P3 并行分析+Prompt生成  → subagent_prompts.md      🔴 GATE 确认分工
P4 并行执行            → 代码产出（自动派发 或 手动多窗口，见下）
P5 验收与修复          → 验收报告 + Memory.md
```

## 阶段路由

执行某阶段前**必须先读取**对应阶段文件：

| 用户意图 | 阶段 | 规程文件 |
|---------|:---:|---------|
| 搭个 Demo / 做原型 / 出技术方案 | P1 | `phases/p1-plan.md` |
| 拆任务 / 出任务清单 | P2 | `phases/p2-task.md` |
| 拆子Agent / 生成并行 Prompt | P3 | `phases/p3-subagent.md` |
| 开始执行 / 跑起来 | P4 | `phases/p4-execute.md` |
| 验收 / 检查 / 修复 | P5 | `phases/p5-qa.md` |

**跳阶段**：小项目 P1+P2 可合并；任务量小（≤4 文件）可跳过 P3/P4 由主 Agent 直接编码；**P5 永不可跳过**。

## P4 执行模式（按环境能力二选一）

| 环境 | 模式 |
|------|------|
| 有原生子 Agent/并行任务能力（如 Claude Code 的 Task、Antigravity 的 subagent） | **模式 A 自动派发**：主对话按轮次自动派发子任务，轮内并行 |
| 无（普通对话工具、或用户想手动控制） | **模式 B 手动多窗口**：用户复制 P3 的 Prompt 到多个新对话窗口执行 |

两种模式的共同铁律：**文件互斥、轮次顺序（Round 1 基础层跑完才能跑 Round 2）**。

## 技术栈预设

**先探测项目实际技术栈**（读 package.json）——已有项目跟随现状。全新项目默认：

Vite + React + TypeScript · UI 用 Ant Design（企业级）或 Shadcn/UI（现代风）· 状态 Zustand · 样式 Tailwind 或原生 CSS · 图表优先 CSS/SVG 手写，复杂场景用图表库。版本以 `npm create vite` 当期最新为准，不锁死具体大版本号。

## 质量红线（全阶段有效）

1. **必须遵守 `references/quality-redlines.md`**（10 条红线 + B 端交互规范，随本技能自带）——写代码前读一遍，P3 生成的每个子任务 Prompt 中必须**内嵌其摘要**（不是引用路径）
2. 不跳过需求理解：P1 必须读完所有需求文档再动手
3. 子任务之间文件零重叠
4. Mock 数据必须真实可信，禁止 lorem ipsum / 占位文字
5. 面向中国客户的 Demo，UI 全中文
6. 每阶段结束 `npx tsc --noEmit` 零错误
7. 子任务 Prompt 必须自包含（完整接口定义 + Mock 结构 + 风格要求 + 红线摘要）

## 通用执行约定

**门禁（🔴 GATE）**：停下，列出待确认内容，等用户明确表态；不得把"没回复"当同意。

**能力自适应**：Shell 可用 → 直接执行编译/启动命令；不可用 → 输出命令块请用户执行回贴。浏览器工具可用 → 自动功能验证；不可用 → 输出人工验证清单。

**Memory.md**：项目根目录维护，P5 验收通过后按统一格式追加里程碑记录（见 p5-qa.md）。

## 本技能目录结构

```
fe-scaffold/
├── SKILL.md                          ← 本文件（调度器）
├── phases/p1-plan.md … p5-qa.md
└── references/quality-redlines.md    ← 10条红线+B端规范（自包含，不依赖外部路径）
```
