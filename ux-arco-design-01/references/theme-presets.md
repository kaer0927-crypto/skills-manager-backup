# 主题落地 Preset（圆角 / 高度 / 字重）

> 目的：把 vibepm 的 3–6 档圆角、46px 按钮、彩色投影落到 Arco 上。
> 事实来源：`@arco-design/web-vue@2.59.0` 编译产物 `es/index.css` 逐条统计。
> 可直接使用的成品：`assets/frame-presets.css`（圆角/按钮/弹窗/滚动条/筛选区栅格），在 `@arco-design/web-vue/dist/arco.css` 之后引入即可。本文是它的说明与变体。

```ts
// main.ts —— 顺序不能反，Arco 基础样式必须在前面
import '@arco-design/web-vue/dist/arco.css';
import '<skill>/assets/frame-presets.css';
import '<skill>/assets/frame-themes.css';   // 12 套主题圆角，按需
```

### 12 套主题一键切换（`assets/frame-themes.css`）

12 个主题块已经写好，用 `body` 的属性启用，不用改代码：

```ts
// 必须在 app.mount() 之前设，否则首屏会先闪一下默认主题（FOUC）
document.body.dataset.frameTheme = 'semi';
```

| `data-frame-theme` | 主题 | small（控件） | medium（浮层） | card | modal |
|---|---|---|---|---|---|
| `semi` | SemiDesign | 3 | 6 | 12 | 12 |
| `minimal` | 亮色现代极简 | 10 | 14 | 16 | 16 |
| `electric-blue` | 亮色电光蓝 | 10 | 14 | 18 | 18 |
| `tech-blue` | 亮色科技蓝（消费向） | 16 | 16 | 20 | 24 |
| `coral` | 绯雾轻写 | 6 | 14 | 16 | 16 |
| `neon-pink` | 暗粉霓虹潮 | 2 | 4 | 6 | 6 |
| `violet` | 暗紫色科技感 | 10 | 12 | 20 | 20 |
| `graphite` | 暗色低饱和黑灰 | 10 | 14 | 18 | 18 |
| `cyan-glow` | 暗黑亮青发光 | 6 | 6 | 24 | 18 |
| `lime` | 暗黑荧光绿 | 6 | 6 | 24 | 18 |
| `glass` | 电光玻璃 | 16 | 24 | 24 | 24 |
| `caramel` | 焦糖暗艺 | 8 | 12 | 18 | 18 |

文件里同时处理了各主题的特例：科技蓝按钮 18px/小按钮 12px/标签胶囊、绯雾 CTA 12px、极简复选框 4px、焦糖标签 6px、暗粉标签 100px、玻璃弹窗强制实色。

> 主色**不在**这个文件里：CSS 覆盖 `--primary-6` 会破坏 10 阶派生（hover/active 串色），主色一律走构建期 `modifyVars` 改 `arcoblue-6`。
> 已用无头 Chrome 逐主题实测：12 套的控件/卡片/弹窗圆角与主按钮投影均按表生效。

---

## 一、Arco 圆角的真实使用情况（必须先知道）

对 `es/index.css` 全量统计：

| 变量 | 被引用规则数 | 主要消费组件 |
|---|---|---|
| `--border-radius-small` | 59 | 按钮、输入框、选择器、文本域、Tag、Alert、Checkbox、分页项、面包屑、多选 |
| `--border-radius-medium` | 29 | Modal、Select 下拉、Cascader 面板、Picker 容器、Collapse、Descriptions 边框、方形 Avatar、轮播指示器、图片预览工具条、**Table 外角** |
| `--border-radius-large` | **0** | 无任何组件使用 |
| `--border-radius-none` | 1 | `.arco-card`（默认 0，卡片是直角） |

结论（决定落地方式）：

1. **只有两个有效档位**：`small` = 控件，`medium` = 浮层。
2. `large` 改了不生效，不要在 `modifyVars` 里指望它。
3. **卡片默认直角**，主题要圆角必须显式覆盖 `.arco-card`。
4. 想表达第 3 档以上（如按钮 18、输入 16、卡片 20、弹窗 24），**只能逐组件覆盖**；两个变量做不到。
5. 部分组件硬编码圆角：`.arco-switch` 12px、Tabs rounded 32px、抽屉无圆角，需单独处理。

---

## 二、通用覆盖模板（粘到主题 CSS 末尾）

> 已实装为 `assets/frame-presets.css`，下面是它的可读版本，改主题时只换 `--frame-radius-*` 与 `--frame-primary-shadow`。

```css
/* ============ 圆角：两档变量 + 卡片 + 特例 ============ */
/* 必须写 body：Arco 的变量全部声明在 body 上，写在 :root 上读不到 */
:root,
body {
  --border-radius-small: 6px;   /* 控件：按钮/输入/标签/复选/分页 */
  --border-radius-medium: 12px; /* 浮层：弹窗/下拉/表格外角 */
  --border-radius-large: 12px;  /* 占位；Arco 未消费，保持与 medium 一致 */
}

/* 卡片默认是 0，必须显式给 */
.arco-card,
.arco-card-bordered { border-radius: 12px; }
.arco-card-bordered .arco-card-cover { border-radius: 12px 12px 0 0; }

/* 浮层统一 */
.arco-modal,
.arco-select-dropdown,
.arco-dropdown-menu,
.arco-picker-container,
.arco-cascader-panel { border-radius: 12px; }

/* 表格外框跟随卡片 */
.arco-table-container { border-radius: 12px; overflow: hidden; }

/* ============ 按钮高度（Arco 默认 24/28/32/36，硬编码） ============ */
.arco-btn-size-medium { height: 36px; padding: 0 16px; }
.arco-btn-size-large  { height: 40px; padding: 0 20px; }
.arco-btn-size-medium.arco-btn-only-icon,
.arco-btn-size-medium.arco-btn-shape-circle { width: 36px; height: 36px; padding: 0; }
.arco-btn-size-large.arco-btn-only-icon,
.arco-btn-size-large.arco-btn-shape-circle { width: 40px; height: 40px; padding: 0; }

/* ============ 按钮字重（Arco 默认 400） ============ */
.arco-btn-primary,
.arco-btn-outline { font-weight: 600; }

/* ============ 彩色投影只给主 CTA（Arco 无此 Token） ============ */
.arco-btn-primary {
  box-shadow: 0 2px 8px rgba(var(--primary-6), .22);
  transition: transform .18s ease, box-shadow .18s ease, background-color .18s ease;
}
.arco-btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 25px rgba(var(--primary-6), .30);
}
.arco-btn-primary:active { transform: translateY(0); }

/* 幽灵按钮不抬升 */
.arco-btn-text:hover { transform: none; }
```

> `rgba(var(--primary-6), .22)` 可用，因为 Arco 的语义色就是 `R,G,B` 三元组。

---

## 三、SemiDesign Preset（企业中后台默认）

圆角本身只有 3 档，直接对号，无需特例：

```css
:root, body {
  --border-radius-small: 3px;   /* 按钮 */
  --border-radius-medium: 6px;  /* 输入 / 下拉 */
  --border-radius-large: 6px;   /* 占位；Arco 无消费，卡片/弹窗靠下面两行 */
}
.arco-card, .arco-card-bordered { border-radius: 12px; } /* 卡片第 3 档 */
.arco-modal { border-radius: 12px; }                      /* 弹窗要 12 而非 6 */
```

高度保持 Arco 默认 32/36；主按钮字重补 600；投影用 `0 2px 8px rgba(0, 100, 250, .22)`（RGB 需与主题主色一致）。

---

## 四、亮色科技蓝 Preset（消费向 H5 / 轻应用，不用于政务企业中后台）

该主题原文即写明「竖屏约 390px 逻辑宽、FAB、底部 Tab」，适用「心愿清单、会员中心、H5 轻应用」。
按全局基线，**大圆角 + 彩色 CTA 长投影 + FAB 不得用于桌面政务/企业中后台**；此 Preset 只用于其声明场景。

原主题 7 档圆角 → Arco 只有 2 个变量 + 特例，落地如下：

| 原 Token | 原值 | 承载组件 | Arco 落地 |
|---|---|---|---|
| `radius.sm` | 12px | 图标按钮、提示条、小控件 | `.arco-btn-only-icon` / `.arco-alert` 覆盖 12px |
| `radius.md` | 16px | 输入框、选择器 | `.arco-input-wrapper` 等覆盖 16px（若直接设 `--border-radius-small:16`，按钮与复选框会一起变圆） |
| `radius.lg` | 18px | 主按钮 | `.arco-btn` 覆盖 18px |
| `radius.xl` | 20px | 内容卡片 | `.arco-card` 覆盖 20px |
| `radius.card-lg` | 24px | 大卡、弹窗 | `.arco-modal` 覆盖 24px |
| `radius.dock` | 40px | 底部 dock | 自定义 `.dock` 类 |
| `radius.pill` | 999px | 标签、胶囊 | `.arco-tag` 或自定义 |

```css
/* 亮色科技蓝 · 仅在 H5/轻应用使用 */
:root, body {
  --border-radius-small: 16px;   /* 输入/选择/文本域 */
  --border-radius-medium: 24px;  /* 弹窗/下拉 */
}
.arco-btn { border-radius: 18px; height: 46px; padding: 0 22px; font-weight: 600; }
.arco-btn-size-small { height: 36px; border-radius: 12px; }
.arco-btn-size-large { height: 52px; border-radius: 18px; }
.arco-btn-only-icon { border-radius: 12px; width: 40px; height: 40px; }
.arco-input-wrapper,
.arco-select-view,
.arco-textarea-wrapper { border-radius: 16px; }
.arco-card, .arco-card-bordered { border-radius: 20px; }
.arco-modal { border-radius: 24px; }
.arco-tag { border-radius: 999px; }
.arco-alert { border-radius: 16px; }

/* CTA 长投影（消费向才允许） */
.arco-btn-primary {
  box-shadow: 0 10px 25px rgba(76, 117, 242, .30);
}
```

注意：`--border-radius-small` 同时被 Tag/Alert/Checkbox/分页项消费，设成 16px 会让复选框变“胶囊”，所以上面对每个组件再单独覆盖一次——这是 Arco 双档模型的必然代价。

---

## 五、深色主题 Preset（示例：暗色低饱和黑灰，4 档）

原主题：`sm 10 / md 14 / lg·xl 18`。

```css
:root, body {
  --border-radius-small: 10px;  /* 控件 */
  --border-radius-medium: 14px; /* 浮层 */
}
.arco-btn { border-radius: 10px; }
.arco-input-wrapper,
.arco-select-view,
.arco-textarea-wrapper { border-radius: 10px; }
.arco-modal,
.arco-select-dropdown,
.arco-cascader-panel { border-radius: 14px; }
.arco-card, .arco-card-bordered { border-radius: 18px; }
.arco-tag, .arco-checkbox-icon, .arco-pagination-item { border-radius: 10px; } /* 防被 small 连带放大 */
```

---

## 六、落地顺序（照做即可）

1. 先 `modifyVars` 改主色（`arcoblue-6`）与字体族——这是唯一能正确派生 10 阶的入口。
2. 用 `--border-radius-small` / `--border-radius-medium` 定两档基线。
3. 按主题档位，为 **按钮 / 输入 / 卡片 / 弹窗 / 标签** 五类做组件级覆盖。
4. 补高度、字重、CTA 投影（严格按是否消费向）。
5. 打开暗黑，逐项复核卡片、弹窗、表格外框、复选框。

## 七、自查

- [ ] 是否知道 `--border-radius-large` 是无效变量，没有只改它？
- [ ] `.arco-card` 是否显式给了圆角（默认 0）？
- [ ] 改 `--border-radius-small` 后，Checkbox / Tag / 分页项是否被误放大？
- [ ] 按钮高度是否按 36/40 或主题值覆盖，而不是只改 padding？
- [ ] 消费向的大圆角/长投影是否被误用到政务企业中后台？
