# P2 任务拆解

> **角色**：仍是架构师。把大方案拆成可原子化执行的小任务。
> **产出**：`task.md`

## 前置输入

- `implementation_plan.md`（P1 产出，**必须已经用户确认**）

## 执行步骤

### Step 2.1 — 任务提取

从 implementation_plan 的 Proposed Changes 提取任务：

- 一个任务 = 一个文件的一组相关改动；新建文件 = 一个任务
- 单文件改动过大（> 200 行）→ 拆子任务
- 琐碎改动（import 路径调整）→ 并入上级任务

动作关键词：`新建` / `重写` / `修改` / `追加` / `配置`

### Step 2.2 — 按 Phase 分组

```markdown
## Phase N: [阶段名]

- [ ] N.1 [动作] `src/路径/文件` — [描述]
  - [ ] 子任务
```

### Step 2.3 — 头部标注依赖与基线

```markdown
> 预计工作量：X 个 Phase，约 N+ 文件变更
> 关键依赖：Phase 1/2（基础层）→ Phase 3/4/5（功能层）→ Phase 6（收尾）
> 基线：[git commit / 目录快照，是否可回退]
```

**基线检查**：是 git 仓库 → 记录当前 commit；不是 → 建议用户先备份目录或 `git init`，在头部如实标注回退能力。

### Step 2.4 — 收尾 Phase 必含验收任务

```markdown
## Phase N: 收尾与验收
- [ ] N.1 编译验证：`npx tsc --noEmit` 零错误；dev 启动页面渲染正常
- [ ] N.2 浏览器验证（从 implementation_plan 的 Verification Plan 逐项复制）
- [ ] N.3 更新 Memory.md（本次变更里程碑）
```

## 交付物：`task.md`

## 阻断规则

- implementation_plan.md 不存在或未经确认 → 不得拆任务
- 🔴 GATE：task.md 产出后等用户确认才进 P3
