# demo-design 自测报告

- 日期：2026-07-04
- 环境：Node v22.20.0 / npm 10.9.3
- 项目根：`/d/AICode/AIskills`（`demo-code/` 位于此）

## 交付物（Skill 层）

```
.claude/skills/demo-design/
├── SKILL.md                 # 编排：自检 → 初始化/继续 → 迭代 → 构建发布
├── specs/
│   ├── common.md            # 通用规范（目录/命名/发布/扩展点）
│   ├── mobile.md            # 移动端 Vant4 规范
│   └── admin.md             # PC 后台 Element Plus 规范
├── scripts/
│   ├── list-demos.sh        # 自检：探测 demo-code 及项目类型
│   ├── init-demo.sh         # 初始化：复制模板(排除node_modules)+写CLAUDE.md记录+npm install
│   └── build-demo.sh        # 构建静态产物 + 输出 Nginx/Apache 发布说明
└── templates/
    ├── mobile/CLAUDE.md      # 既有
    └── admin/CLAUDE.md       # 本次补齐
```

## 验证结果

| # | 验证项 | 结果 |
|---|--------|------|
| 1 | 无 `demo-code` 时自检 | ✅ 输出 `STATE=NO_DEMO_CODE`，触发初始化引导 |
| 2 | 初始化移动端 `mobile-sample` | ✅ 结构正确、node_modules 未复制而是 `npm install`（38 包/4s）、CLAUDE.md 追加初始化记录 |
| 3 | 移动端 `npm run build` | ✅ 产出 `dist/`（11 文件）、打印发布说明 |
| 4 | 初始化 PC 后台 `admin-sample` | ✅ 结构正确、`npm install`（311 包/13s，仅 deprecation warning）、CLAUDE.md（含类型专属正文 + 初始化记录） |
| 5 | 后台 `npm run build` | ✅ 产出 `dist/`（35 文件）、发布说明 |
| 6 | 再次自检 | ✅ `STATE=HAS_PROJECTS`，正确识别两项目的类型与依赖安装状态 |
| 7 | 初始化参数校验 | ✅ 未知类型 / 非 kebab-case / 目标已存在 / 缺参 均报错并非零退出 |

## 结论

Skill 全流程（自检 → 初始化 → 构建发布 → 复检）在真实 npm 环境下端到端通过。移动端与 PC 后台两类模板均可安装并构建为纯静态产物，适配 Nginx/Apache 子路径部署。

## 备注

- 自测生成的 `demo-code/mobile-sample`、`demo-code/admin-sample` 为测试产物，可保留作示例或删除。
- 项目根遗留的 `demo/` 目录按约定保留不动，Skill 仅使用 `demo-code/`。
