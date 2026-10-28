# 暗黑模式规范（Arco 原生 + vibepm 主题）

> 机制以 `@arco-design/web-vue@2.59.0` 官方文档与源码为准：暗黑通过 `body[arco-theme='dark']` 切换 CSS 变量，组件零改动。
> 下表「暗黑」列是 Chrome 实测 `getComputedStyle(document.body)` 的值，不是推导值。
> 基础取值见 [`arco-tokens.md`](arco-tokens.md) 第四节。

---

## 一、切换机制（唯一正确做法）

```ts
document.body.setAttribute('arco-theme', 'dark'); // 开
document.body.removeAttribute('arco-theme');      // 关
```

- 没有 `setTheme()` API，`ConfigProvider` 也没有 `theme` prop。
- 选择器是 `body[arco-theme='dark']`，**只能整页切换**；局部“暗色卡片”请用 `--color-*` 变量自行配色，不要试图嵌套。
- 切换后 `--color-bg-*`、`--color-text-*`、`--color-fill-*`、`--color-border*` 自动反转。
- **整套色板都会重映射**：暗黑块重新定义了 `--red-*`、`--arcoblue-*`、`--gray-*` 等 10 阶调色板，因此 `--primary-6` 在暗色下会变成 `60,126,255`（`#3C7EFF`），不是亮色的 `22,93,255`。自定义色若要跨明暗稳定，必须自己写死，不能指望 `--primary-6` 不变。

### 两个高频踩坑（实测）

1. **Token 声明在 `body` 上，不在 `:root`**：`dist/arco.css` 把全部变量写在 `body { ... }` 与 `body[arco-theme='dark'] { ... }`。给 `html` 设变量、或在 `:root` 里读 `--primary-6` 会拿到空值。
2. **只写 `body { --primary-6: ... }` 在暗色下会失效**：暗黑块选择器 `body[arco-theme='dark']` 的特异性（0,1,1）高于 `body`（0,0,1），会盖掉你的覆盖。安全写法二选一：

```css
/* A. 同时命中两种状态 */
body,
body[arco-theme='dark'] {
  --primary-6: 0, 100, 250;
}
```

```ts
// B. 运行时改色用内联样式（优先级最高，能压过暗黑块）
document.body.style.setProperty('--primary-6', '0, 100, 250');
```

### 跟随系统 + 手动覆盖

```ts
type ThemePref = 'light' | 'dark' | 'auto';

const media = matchMedia('(prefers-color-scheme: dark)');

function applyTheme(pref: ThemePref) {
  const dark = pref === 'dark' || (pref === 'auto' && media.matches);
  document.body.removeAttribute('arco-theme');
  if (dark) document.body.setAttribute('arco-theme', 'dark');
}

media.addEventListener('change', () => {
  if (localStorage.getItem('theme') === 'auto') applyTheme('auto');
});

applyTheme((localStorage.getItem('theme') as ThemePref) ?? 'auto');
```

### 与主题的配合

主题切换（改主色/圆角）与明暗切换是**两条正交链路**：

| 链路 | 手段 | 生效时机 |
|---|---|---|
| 明暗 | `body[arco-theme]` | 运行时 |
| 主色/圆角 | `modifyVars` 或 Design Lab 主题包 | 构建期 |
| 主色热切换（可选） | 覆写 `--primary-1..10` | 运行时 |

两条链路都做，才能既换主题又支持暗色。

---

## 二、暗黑基础映射（Arco 实测值）

| 用途 | 亮色 | 暗黑 | 变量 |
|---|---|---|---|
| 页面底 | `#fff` | `#17171a` | `--color-bg-1` |
| 主容器 | `#fff` | `#232324` | `--color-bg-2` |
| 二级容器 | `#fff` | `#2a2a2b` | `--color-bg-3` |
| 三级容器 | `#fff` | `#313132` | `--color-bg-4` |
| 浮层/下拉 | `#fff` | `#373739` | `--color-bg-5` |
| 主文字 | `#1d2129` | `rgba(255,255,255,.90)` | `--color-text-1` |
| 次文字 | `#4e5969` | `rgba(255,255,255,.70)` | `--color-text-2` |
| 辅助文字 | `#86909c` | `rgba(255,255,255,.50)` | `--color-text-3` |
| 禁用文字 | `#c9cdd4` | `rgba(255,255,255,.30)` | `--color-text-4` |
| 填充 1–4 | `gray-1..4` | 白 4/8/12/16% | `--color-fill-1..4` |
| 分割线 | `#e5e6eb` | `#333335` | `--color-border` |
| 边框 1–4 | `#f2f3f5` / `#e5e6eb` / `#c9cdd4` / `#86909c` | `#2e2e30` / `#484849` / `#5f5f60` / `#929293` | `--color-border-1..4` |
| 遮罩 | `rgba(29,33,41,.6)` | `rgba(23,23,26,.6)` | `--color-mask-bg` |

> 注意：暗黑下边框**不是**白色透明度梯度，而是重映射后的实色灰阶；写 `rgba(255,255,255,.1)` 会得到比原生更虚的边框。直接用变量。

### 容器色和组件默认底的对应关系（别记反）

| 组件 | 默认取用的变量 | 暗色实际值 |
|---|---|---|
| 页面背景 | `--color-bg-1` | `#17171a` |
| 卡片 / 表格容器 | `--color-bg-2` | `#232324` |
| **Modal / Drawer 面板** | `--color-bg-3` | `#2a2a2b` |
| 下拉 / Tooltip / 浮层 | `--color-bg-5` | `#373739` |

### 暗色下页面大块露白（实测最高频）

Arco 的 `--color-fill-*`、`--color-border-*` 在暗色下是**白色透明度**，浏览器默认白底会直接透出来，表现为「卡片是黑的、卡片之间和页面边缘是白的」。Arco 不会替你设 `body` 背景，必须自己写：

```css
body {
  background-color: var(--color-bg-1);
  color: var(--color-text-1);
}
```

`assets/frame-presets.css` 已包含这条。业务里如果换了根容器（`#app`、`.frame-layout`），也要给它一个 `--color-bg-1` 实色底，不要留透明。

### 滚动条（vibepm 统一，双写）

```css
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, .18);
  border-radius: 999px;
  border: 2px solid transparent;
  background-clip: padding-box;
}
::-webkit-scrollbar-thumb:hover { background: rgba(0, 0, 0, .28); }
::-webkit-scrollbar-thumb:active { background: rgba(0, 0, 0, .36); }

/* Firefox */
* { scrollbar-width: thin; scrollbar-color: rgba(0,0,0,.18) transparent; }

body[arco-theme='dark'] ::-webkit-scrollbar-thumb { background: rgba(255,255,255,.14); }
body[arco-theme='dark'] ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,.26); }
body[arco-theme='dark'] ::-webkit-scrollbar-thumb:active { background: rgba(255,255,255,.34); }
body[arco-theme='dark'] * { scrollbar-color: rgba(255,255,255,.14) transparent; }
```

> 更省事的写法：滑块直接用 `var(--color-fill-4)`（亮 `#c9cdd4`、暗 白 16%，自动反转），就**不需要**上面那组暗色覆盖。可直接用 `assets/frame-presets.css` 里的滚动条实现。

---

## 三、12 套主题的暗黑策略

Arco 已经负责背景/文字/边框反转，主题侧只需要决定三件事：
1. 主色在暗底上要不要提亮（对比度）；
2. 语义色（成功/警告/危险）要不要换更亮的阶；
3. 有没有必须关闭的装饰效果（大面积发光、玻璃、彩色投影）。

| 主题 | 主色（亮） | 暗黑主色 | 关键调整 |
|---|---|---|---|
| SemiDesign | `#0064FA` | `#3C8CFF` | 暗底上提亮主色，否则按钮对比不足；圆角不变 |
| 亮色科技蓝 | `#4C75F2` | `#6B8CFF` | 降低彩色投影强度，改内发光描边 |
| 亮色现代极简 | `#1C1F23` | `#F2F3F5` | 主色反转为浅色，按钮改“浅底深字” |
| 亮色电光蓝 | `#38BDF8` | `#38BDF8` | 保持，暗底反而更清晰；减弱大面积浅蓝底 |
| 绯雾轻写 | `#E74C3C` | `#FF7A6B` | 珊瑚红提亮；暗红底改深紫灰 |
| 暗粉霓虹潮 | `#DB64A8` | `#F472B6` | 暗底可回用原粉；霓虹仅描边，不铺底 |
| 暗紫色科技感 | `#A573FF` | `#B98CFF` | 提亮；渐变点缀降低透明度 |
| 暗色低饱和黑灰 | `#7A8A9E` | `#94A3B8` | 数据密集场景，优先保证文字 4.5:1 |
| 暗黑亮青发光 | `#22D3EE` | `#22D3EE` | 保持；发光仅用于关键数值，不用于整卡 |
| 暗黑荧光绿 | `#C2E600` | `#D9FF00` | 仅描边/图标，禁止大面积填充 |
| 电光玻璃 | `#9348D4` | `#A855F7` | 玻璃仅装饰区；**弹窗、表单、表格必须实色** |
| 焦糖暗艺 | `#FF9A5A` | `#FFB07A` | 暖色提亮；阴影改深棕描边 |

> 表内暗黑主色为对比度推导建议值，落地时按主题文档复核，并用 WCAG 工具验证。

### 主色热切换（如需运行时换主题）

```ts
// 10 阶色板需完整给出，否则 hover(--primary-5)/active(--primary-7) 会串色
const steps = [/* 1..10 的 R,G,B 字符串 */];
steps.forEach((rgb, i) => {
  document.body.style.setProperty(`--primary-${i + 1}`, rgb);
});
```

---

## 四、暗黑下必须复核的组件

| 组件 | 检查点 |
|---|---|
| Button | primary 文字对比 ≥4.5:1；outline 边框在暗底可见 |
| Table | 表头底色（`--color-fill-2`）、斑马纹、固定列阴影 |
| Modal/Drawer | 面板实色（`--color-bg-3`，暗色 `#2a2a2b`），遮罩用 `--color-mask-bg`，禁止玻璃面板 |
| Form | 输入框底 `--color-bg-2`，错误红环在暗底仍可辨 |
| Tag/Badge | 浅色语义底在暗底会发光过强，改用描边或降透明度 |
| Chart | 网格线、轴文字、图例必须从 `--color-*` 取色 |
| Empty/Skeleton | 无自定义白底 |
| Image | 亮色图片加 1px 边框或轻微降亮，避免刺眼 |

---

## 五、自查清单

- [ ] 切换方式为 `body[arco-theme='dark']`，未使用不存在的 `setTheme`？
- [ ] 业务自定义样式全部使用 `var(--color-*)` / `var(--border-radius-*)`，无硬编码白底黑字？
- [ ] 主色在暗底对比度 ≥4.5:1？
- [ ] 主色热切换时 10 阶齐全？
- [ ] 表格、表单、弹窗、图表四类重点组件已逐项目检？
- [ ] 滚动条在暗色下为白 14% 滑块？
- [ ] 是否与主题切换（主色/圆角）互不干扰？
