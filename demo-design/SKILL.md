---
name: demo-design
description: 快速创建与迭代产品原型 Demo（Vue3 + Vite + Mock，纯前端、不接真实后端）。预制「移动端(Vant4)」与「PC管理后台(Element Plus)」两种类型，支持初始化、开发迭代、构建静态产物发布。当用户输入 /demo-design，或提出"做/新建/初始化一个 Demo/原型""移动端 H5 demo""管理后台 demo""迭代/继续开发某个 demo""把 demo 构建/发布"等诉求时触发。
---

# demo-design

用于**快速搭建与迭代产品原型 Demo**，供演示与在线预览。核心命令 `/demo-design`。

**铁律**：极简克制，纯前端，Mock 数据，**不对接真实后端 API**；只做「Demo + Mock」必需的事。

## 关键路径

- Demo 实例目录：`<项目根>/demo-code/<project-name>/`（一项目一子目录，kebab-case 命名）。
- 「项目根」= 当前工作目录（即含 `.claude/` 的目录）。脚本默认取 `$PWD`，可用环境变量 `DEMO_DESIGN_ROOT` 覆盖。
- 规范文档：`specs/common.md`（通用）、`specs/<type>.md`（类型专属）。
- 模板：`templates/<type>/`。脚本：`scripts/`。

## 类型清单（可扩展）

| type | 场景 | UI/技术栈 | 规范 | 模板 |
|------|------|-----------|------|------|
| `mobile` | 移动端 H5 / App 类 | Vue3+Vite+**Vant4**+vue-router+mockjs | `specs/mobile.md` | `templates/mobile/` |
| `admin` | PC 管理后台 | Vue3+Vite+**Element Plus**+vue-router+Pinia+mock | `specs/admin.md` | `templates/admin/` |

> 新增类型见 `specs/common.md`「扩展新 Demo 类型」。

---

## 工作流

每次被触发时，**先执行自检**，再根据结果分支。

### 步骤 0 · 自检（必做）

运行：
```bash
bash .claude/skills/demo-design/scripts/list-demos.sh
```
输出首行是状态：
- `STATE=NO_DEMO_CODE` 或 `STATE=EMPTY_DEMO_CODE` → 无可用 Demo，走**步骤 A（初始化引导）**。
- `STATE=HAS_PROJECTS` → 已有项目（后面列出名称/类型/是否装依赖），走**步骤 B（选择继续开发或新建）**。

### 步骤 A · 初始化引导（无项目时）

1. 告知用户当前没有 Demo，询问要创建哪种类型（列出类型清单表），并请其给一个 kebab-case 项目名。
2. 先读对应 `specs/<type>.md` + `specs/common.md`，向用户简述该类型将用什么技术栈。
3. 执行初始化：
   ```bash
   bash .claude/skills/demo-design/scripts/init-demo.sh <type> <project-name>
   ```
   脚本会：把 `templates/<type>/` 原样复制到 `demo-code/<name>/`（仅排除 node_modules/dist，不改写任何文件）→ `npm install`。
4. 装完后按需 `npm run dev` 让用户预览，进入开发迭代（步骤 C）。

### 步骤 B · 已有项目（继续 or 新建）

1. 展示自检列出的现有项目，询问用户：**继续开发某个已有项目** 还是 **新建项目**。
2. 选「新建」→ 回到步骤 A 的第 1~4 步（同一类型可多实例，名字不同即可）。
3. 选「继续」→ 进入步骤 C。

### 步骤 C · 开发迭代

1. **先读上下文**：`demo-code/<name>/CLAUDE.md` + `src/`，确认项目**当前真实状态**（文档可能滞后于代码）。
2. **读规范**：对应 `specs/<type>.md` + `specs/common.md`，遵循其技术栈、UI 框架、Mock 风格、目录约定。
3. 按用户需求改代码，`npm run dev` 本地验证。
4. 有实质进度时，更新该项目 `CLAUDE.md` 的「当前进度」。

### 步骤 D · 构建 / 发布

```bash
bash .claude/skills/demo-design/scripts/build-demo.sh <project-name>
```
产出 `demo-code/<name>/dist/` 纯静态文件，并打印 Nginx / Apache 发布说明。

---

## 手动新建

用户可随时要求「在 demo-code 下新建一个 X 类型的 demo」，直接走步骤 A 的初始化脚本即可，无需先自检为空。

## 约束回顾

- 纯前端 + Mock，不接真实后端。
- 极简：不引入演示无关的功能/依赖。
- 类型规范分离在 `specs/`，主文件只做编排。
- 目录/命名严格按 `common.md`。
