# 源项目结构与使用（参考实现）

## 源项目位置

**用户确认位置（2026-10-21 确认，Mac 本地）**：

```
/Users/shuziniuma/Desktop/学习资料/Coding资料/html模板/中后台原型及前端交付解决方案
```

- VibePM / Frame 全量离线镜像（抓取自 https://www.vibepm.top/frame/，2026-09-10）
- 含 gallery.html 母版库总入口 + admin/ 后台 50 页 + app/ 设备壳 8 页 + .style/ 12 套主题 + web/
- 全部资源本地化，file:// 双击可离线打开
- 演示账号：admin / 123456（或 URL 加 `?galleryPreview=1` 跳过登录）

> **【沙箱访问说明】**
> Agent 运行在云端 Linux 沙箱，**无法直接读取上述 Mac 本地路径**（沙箱内不存在 `/Users`）。
> 引用真实实现前，必须先确认该目录内容已同步到沙箱内可访问的位置（用户上传/打包传输），并在本文档记录同步后的沙箱路径。
> 沙箱内历史镜像：`/home/user/Doubao/chats/38440939649486850/vibepm_site/`（抓取于 2026-09-10，可能随会话清理失效；若不可用需向用户确认后重新同步）。
> 工作区 `/home/user/.doubao/agent_mode/workspace/vibepm_site/` 是残缺版本（仅 dashboard.html），勿用作源。
>
> **【路径失效处理 · 强制规则】**
> 若本 Skill 记录的源项目路径不可用、被移动、被清理或发生变化，**禁止**自行猜测新路径、禁止静默退回内置 references 继续生产。
> 必须**先向用户发起确认**：说明当前记录路径已失效（给出记录的路径与失效现象），请用户提供新的模板位置，在用户明确确认新路径后再引用。
> 用户未确认前，不得开始或继续前端界面生产。

## 引用确认时机

使用本 Skill 前应先校验源项目路径是否存在（`ls` 或 `Read` 记录路径）；不存在即视为「路径已变」，走上面的强制规则。

## 目录结构

```
vibepm_site/
├── gallery.html            母版库总入口（浏览/预览全部页面）
├── admin/                  后台 50 个页面（可直接打开任意 HTML）
│   ├── <页面>.html         页面壳（Vue SPA，内容由 js 渲染）
│   ├── css/                共享样式（arco-theme-pro.css / layout.css / pages-common.css …）
│   ├── js/pages/           各页面渲染逻辑与组件实现（component-basic.js 等）
│   ├── js/                 共享逻辑（shell.js / boot.js / routes.js / mock-data.js …）
│   ├── vendor/             第三方库（arco / fontawesome / vue）
│   └── _meta/pages.catalog.json   页面清单（type / label / html / desc / layout 字段）
├── app/                    移动端设备壳 8 页（ios_frame*.html / wechat-frame*.html）
├── .style/                 12 套主题（<主题>-preview.html 预览页 + <主题>-style.md 规范）
├── style/                  Gallery 外壳配色（明暗/强调色，仅改颜色）
└── web/                    WEB 端资源（占位）
```

## 读真实组件实现的方式

页面 HTML 是壳，控件实际在 `admin/js/pages/` 与 `admin/css/`。需要参考真实实现时：

1. 打开 `admin/<页面>.html` 确认引用的 js/css；
2. 用 `Grep` 在 `admin/js/pages/<页面>.js` 里搜组件类名（如 `.btn`、`.card`、`.input`、`.table`）定位实现；
3. 用 `Grep` 在 `admin/css/*.css` 里搜同名类，拿到完整样式（颜色/圆角/阴影/状态）；
4. 需要的色板/Token 直接从 `.style/<主题>-style.md` 取（已内置在 references/themes/）。

## 主题预览

每套主题在 `.style/<主题>-preview.html`，可直接打开看落地效果；规范见同名 `-style.md`（已内置）。

## 常见修改场景

| 场景 | 做法 |
|---|---|
| 换主题色 | 改 `<主题>-style.md` 的 Token 表对应变量（如 `--accent`、`--brand-primary`） |
| 换页面骨架 | 从 catalog 选同类别组件，复制其 HTML/JS 结构调整 |
| 移动端适配 | 用 app/ 设备壳包内容页 |
| 保持一致性 | 按钮/表单/弹窗/滚动条一律走主题文档的公共规范 |
