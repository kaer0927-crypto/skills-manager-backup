# {{PROJECT_NAME}} 原型项目 — 工作守则

> 本文件由 prototype-design skill 在项目 init 时一次性生成；此后按需手改。
> skill 升级不会自动同步本文件——老项目想用新版请新建项目。

## 1. 项目概述

这是一个 PRD 原型项目（三栏查看器：左目录 / 中 iframe / 右描述）。

- **数据源**：`nav.json`；离线产物：`nav.js` + `desc/<id>.html`
- **离线打开**：双击 `index.html`（file:// 协议）

### 1.1 真实项目约定（红线）

1. **只改业务内容，不动查看器框架与维护脚本**：只能修改「原型页（`pages/`）、描述文档（`desc/`）、目录（`nav.json`）」相关内容。
   **不得**修改最外层页面的框架文件 —— `index.html`、`assets/viewer.css`、`assets/viewer.js`、`assets/viewer-bridge.js`、
   `assets/desc-enhance.css`、`assets/desc-enhance.js` 及 `assets/` 下第三方库；`nav.js` 是 `nav.json` 的生成产物，勿手改。
   `scripts/` 是标准维护工具，真实项目中**不需要手改**（改脚本会连带影响整个项目的目录同步与描述渲染）；脚本升级请从原 skill 的
   `assets/scaffold/scripts/` 拷贝替换。以上都属于改变整体结构/行为的越界操作。
2. **原型与文档分开撰写**：两者互不自动触发，**不强制自动写** ——
   - 只有用户**明确要求**写/改描述文档时，才编写或修改 `desc/*.md` 并触发 `build_desc`；
   - （`add_page` 自动生成的「占位 md」是唯一例外，仅保证右侧描述区不空白，见 §4.1）
   - 只有用户**明确要求**开发/修改原型时，才编写或修改 `pages/*.html`。

## 2. 写原型的规范

### 2.1 nav.json 节点约定

**节点类型**：叶子（有 `htmlPath`+`mdPath`，点击切换 iframe）、分组（无 `htmlPath`，只有 `children`）、混合（两者皆有，点击行开页面、点击 ▾/▸ 展开）——区别见字段表 `htmlPath`/`mdPath` 列。

**字段表**：

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | string | 全局唯一，kebab-case，与文件名 stem 一致 |
| `title` | string | 目录/页面显示名 |
| `htmlPath` | string \| null | 相对项目根的路径；分组节点为 null/省略 |
| `mdPath` | string \| null | 相对项目根的路径；与 htmlPath 同前缀 |
| `templateType` | string | 取值对应 `templates/` 下文件类型（如 `list` / `mobile-list` / `custom`）；仅展示用 |
| `order` | number | 同级排序，小者靠前 |
| `children` | array | 子节点 |

**命名规范**：

- `id` 用 kebab-case（如 `user-list`），文件名一律 `<id>.html` / `<id>.md`
- `order` 顶层常用 0（业务概览）、1、2...；同层子节点用 1、2、3...
- `templateType` 必须是小写英文，与 templates/ 里的文件名一致

### 2.2 pages/<id>.html 写法

每个原型页是**独立完整 HTML**，必须引这些资源（按顺序）：

```html
<head>
  ...
  <script src="../assets/vue.global.prod.js"></script>
  <script src="../assets/element-plus.full.min.js"></script>
  <script src="../assets/icons-vue.iife.min.js"></script>
  <!-- 在 element-plus 之后引入 -->
  <script src="../assets/viewer-bridge.js"></script>
  <!-- PC 页中文语言包 -->
  <script src="../assets/zh-cn-locale.js"></script>
</head>
```

**设备声明**：

- PC 页：`<meta name="device" content="pc" />`（不写缺省视为 pc）
- 移动页：`<meta name="device" content="mobile" />` + viewport meta（防止 iframe 内 pinch-zoom 出戏）

**Element Plus 短 API**（已通过 viewer-bridge 注入到 iframe 内 `window.*`）：

- `ElMessage` = `ElementPlus.ElMessage`
- `ElMessageBox` = `ElementPlus.ElMessageBox`
- `gotoNode(id, fallback?)` 走 `window.parent.postMessage` 通知父 viewer 切节点

模板根节点包 `<el-config-provider :locale="zhCnLocale">`，分页 / 日期 / 弹窗文案即全中文。

### 2.3 templates 用法

**templates/pc/**（4 个）：
- `list.html` —— 列表页（带搜索 + 表格 + 分页 + 新建按钮）
- `form.html` —— 表单页（新增/编辑）
- `detail.html` —— 详情页
- `dashboard.html` —— 仪表盘（带 ECharts 卡片）

**templates/mobile/**（4 个，与 PC 同名）：基于 Vant 4，适配 phone frame；`--template mobile-list` 等是别名写法。

**components/**（8 个）：历史片段，每个文件头有「⚠️ 不再使用」提示；新页用 templates/。

**新页流程**：从 `templates/` 拷贝对应模板到 `pages/<id>.html`，替换唯一占位符 `{{PAGE_TITLE}}`。

## 3. 写描述的规范

> 仅在用户**明确要求**撰写/修改描述文档时执行；不随原型开发自动触发（见 §1.1 约定）。

### 3.1 desc/<id>.md 四段模板

每个 `desc/<id>.md` 必须包含以下四段（顺序与命名固定）：

1. **页面目的**：解决什么业务问题，谁会用。
2. **交互说明**：用户从哪进、点哪里、会看到什么（含关键状态切换）。
3. **业务规则**：权限 / 校验 / 计算口径 / 默认值。
4. **异常情况**：网络错误 / 数据为空 / 边界值 / 权限拒绝。

参考示例：`<项目名>/desc/pc-list.md`（init 后自带）。
> 注意：init 自带的示例 desc 是「模板能力展示」，仅用于介绍模板功能；**实际页面描述**按上方四段结构撰写。

### 3.2 描述同步流程

```bash
# 改完一个或多个 desc/<id>.md 后：
python scripts/sync_nav.py .     # 同步 nav.js + 全部 desc/*.html

# 只渲染单个：
python scripts/build_desc.py . --id <id>

# 只渲染不重建 nav.js：
python scripts/sync_desc.py .
```

`build_desc.py` 把 `.md` 转 HTML：mermaid 代码块通过 `mmdc` 渲染成内联 SVG；`![alt](path)` 图片转 `data:image/...;base64,...`。结果写到 `desc/<id>.html`，右侧 iframe 直接加载。

依赖：

- `pip install markdown`（python-markdown）
- `npm i -g @mermaid-js/mermaid-cli`（mmdc；缺则 mermaid 降级为 `<pre>` 源码，不影响其他节点）

## 4. 常用工作流

### 4.1 加新页面

1. 决定层级位置（父节点 id）
2. 跑 `python scripts/add_page.py . --id <id> --title "..." [--parent X] [--template list|form|detail|dashboard|custom] [--order N] [--create-parent]`
3. 编辑 `pages/<id>.html`（基于 `templates/` 或重写）
4. 文档：`add_page.py` 会自动生成一份最小占位 `desc/<id>.md`（内容为「# 标题 / 请补充…」），保证右侧描述区不空白；**正式描述仍仅在用户要求写文档时**才按 §3.1 四段模板撰写并覆盖占位内容
5. `add_page.py` 内部已自动 `sync_nav` + `build_desc`，刷浏览器看效果

### 4.2 删页面

```bash
python scripts/remove_page.py . --id <id>
```

自动同步 html / md / desc/<id>.html / nav.json / nav.js，并清理空分组。

### 4.3 重命名 / 移动

```bash
python scripts/rename_page.py . --id <old> [--new-id X] [--new-title "..."] [--new-parent X] [--new-order N]
```

重命名物理文件 + nav.json 节点；后续 `sync_nav.py` 重新生成全部 desc html。

### 4.4 改描述

编辑 `desc/<id>.md` → `python scripts/sync_nav.py .` → 刷浏览器。

### 4.5 校验一致性

```bash
python scripts/validate.py .
```

查 nav.json / pages / desc 是否对齐。

### 4.6 预览不执行

`add_page.py` / `remove_page.py` / `rename_page.py` 支持 `--dry-run` 预览；`sync_nav` / `sync_desc` / `build_desc` 为同步类操作，不支持 dry-run。

### 4.7 删除示例页

- 示例页：`pages/pc-{list,form,detail,dashboard}.html` + `pages/mobile-{list,form,detail,dashboard}.html`
- 配套 desc 在 `desc/` 下；nav.json 里 `pc-templates` / `mobile-templates` 两个组
- 删一个：`python scripts/remove_page.py . --id pc-list`
- 删整组：`remove_page.py` 的 `--id` 支持分组节点，一条命令即可删掉整个组（含全部子页 + 文件 + nav 节点），无需手改 nav.json：

  ```bash
  python scripts/remove_page.py . --id pc-templates
  python scripts/remove_page.py . --id mobile-templates
  ```

  可先加 `--dry-run` 预览会删除的文件，确认后再执行。

### 4.8 项目不能"升级"

skill 升级后本项目**不会**自动获得新版 templates / scripts / CLAUDE.md。
- 想用新版模板 / 脚本：从原 skill 的 `assets/scaffold/` 手动拷贝替换。
- 想用新版 CLAUDE.md 模板：手改本文件，或参考新 skill 版本对照修改。
- 想"完全重来"：**新建一个项目**（不同的 `<项目名>`），不要在老项目上重跑 init_project.py。

## 5. 常见陷阱

- `pages/` 里删了文件但 `nav.json` 没同步 → `python scripts/validate.py .` 会报错（也用它兜底检查整体一致性）
- 手动删了 `nav.json` 或 `CLAUDE.md` 后跑 init → 会**绕过检测**当作新项目，整个 scaffold 覆盖进来；**不要**手动删这两个文件
- 想直接双击 `pages/<id>.html` 单独打开 → `ElMessage` / `ElMessageBox` 可用，`gotoNode(...)` 会退到 fallback（无父 viewer）