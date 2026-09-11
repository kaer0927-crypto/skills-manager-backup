---
name: prototype-design
description: 初始化一个 PRD 原型项目。当用户提到"新建原型项目 / 初始化原型 / 做一个原型 / 原型项目 / 给开发看原型 / 原型链接 / mockup / prototype"时使用本 skill，即使用户没有明说"用 skill"。skill 只负责初始化；初始化完成后，用户在原型项目目录里的"加页面 / 改描述 / 删节点"等需求，由项目自带的 CLAUDE.md + scripts/ 接管，本 skill 不再触发。
---

# prototype-design

在用户指定目录初始化一个 PRD 原型项目骨架（三栏 viewer / 示例页 / templates / scripts / CLAUDE.md）。
用户已在原型项目目录里要加页面 / 改描述 / 删节点时，走项目内 `CLAUDE.md` 工作流，**不要**调 init_project.py。

## 30 秒上手

```bash
# 1. 初始化一个新项目
python .claude/skills/prototype-design/scripts/init_project.py my-prototype --name "我的原型"

# 2. 双击 my-prototype/index.html 查看
```

## 关键约束

1. **只能 init 一次**：目标目录必须为空或不存在；已存在 `nav.json` / `CLAUDE.md` 会**报错退出**。不提供覆盖或升级——老项目想用新版请**新建项目**。
2. **离线可用**：element-plus / vue / echarts / vant / viewer-bridge 等全部本地化，`file://` 双击即跑，无 CDN 依赖。
3. **产物位置**：项目建在用户当前工作目录下，命名为 `<项目名>/`；**禁止**在 skill 自身目录里创建业务项目。

## 项目结构（init 后）

```
<项目名>/
├── index.html              # 三栏 viewer（左目录 / 中 iframe / 右描述）
├── nav.json                # 目录唯一权威
├── nav.js                  # nav.json 同步产物
├── CLAUDE.md               # 项目工作守则（写原型 / 写描述规范、工作流、常见陷阱）
├── assets/                 # 共享资源（element-plus / vue / echarts / vant / viewer-bridge）
├── components/             # 历史片段（已被 templates/ 取代）
├── templates/              # 页面模板源（pc/ × 4 + mobile/ × 4）
├── pages/                  # 原型页 HTML（每页独立完整 HTML）
├── desc/                   # 描述文件（.md + 渲染出的 .html）
└── scripts/                # 维护脚本（add / remove / rename / sync_nav / build_desc / sync_desc / validate）
```
