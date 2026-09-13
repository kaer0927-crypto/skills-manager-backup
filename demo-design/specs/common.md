# demo-design 通用规范（common）

所有 Demo 类型共享的约定。类型专属细节见 `mobile.md` / `admin.md`。

## 定位与原则

- **用途**：快速搭建、迭代产品原型 Demo，供演示与在线预览，**不是生产系统**。
- **极简克制**：仅保留「Demo + Mock」必需的功能与依赖；**不对接真实后端 API**，所有数据由 Mock 提供。
- **不引入多余能力**：不加登录鉴权、埋点、国际化框架、状态持久化等与演示无关的功能，除非该类型规范明确要求。

## 通用技术栈

- Vue 3（Composition API + `<script setup>`）
- Vite 5（dev server + 生产构建）
- Mock 数据（`mockjs` 或 `vite-plugin-mock`，见各类型规范）
- Vue Router 4

## 目录与命名约定

- 所有 Demo 实例统一放在**项目根目录**的 `demo-code/` 下。
- **一项目一子目录**：`demo-code/<project-name>/`。
- 项目名用 **kebab-case**（小写字母开头，仅含小写字母、数字、连字符），如 `sales-portal`、`crm-admin`。
- 同一类型可并存多个项目。
- Demo 实例目录**不纳入 skill 模板**，是运行期产物。

## 每个项目必备文件

- `CLAUDE.md`：初始化时生成，记录技术栈、目录结构、开发约定、当前进度。**后续迭代前必须先读它**。
- `package.json`：`dev` / `build` / `preview` 三个脚本齐全。
- `README.md`（可选）：面向使用者的说明。

## 生产发布（所有类型通用）

- 目标：`npm run build` 产出**纯静态文件**（`dist/`），可部署到 Nginx / Apache，供同事在线预览。
- 为兼容任意子路径部署：
  - 路由使用 **hash 模式**（`createWebHashHistory`），避免服务端 rewrite 依赖。
  - Vite `base` 用相对路径 `'./'`（或按部署路径设置），保证资源引用不写死绝对路径。
- 发布与验证细节见 `scripts/build-demo.sh` 输出的发布说明。

## 开发迭代总原则

1. 先读目标项目的 `CLAUDE.md` 与 `src/`，确认**当前真实状态**（README 描述可能滞后）。
2. 遵循该类型规范（技术栈、UI 框架、Mock 风格）。
3. 改动后本地 `npm run dev` 人工验证；交付前 `npm run build` 验证可构建。
4. 有实质进度变化时，更新项目内 `CLAUDE.md` 的「当前进度」。

## 扩展新 Demo 类型（预留扩展点）

新增类型 `<type>` 时按以下步骤，无需改动已有类型：

1. 在 `templates/<type>/` 放置该类型的项目模板（含 `CLAUDE.md`、`package.json`）。
2. 在 `specs/<type>.md` 写该类型规范，并在 `SKILL.md` 的「类型清单」表格登记一行。
3. 在 `scripts/list-demos.sh` 的类型识别分支补充该类型的判定依赖（如某个 UI 框架包名）。
4. 其余（init / build / 发布）脚本已类型无关，自动适用。
