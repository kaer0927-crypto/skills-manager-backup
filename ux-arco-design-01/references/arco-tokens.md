# Arco Design Token 对照表（vibepm ↔ Arco）

> 数据来源：`@arco-design/web-vue@2.59.0` 的 `es/index.css` 与 `components/style/theme/global.less`，逐项核对，非推断。
> 用途：vibepm 主题落地到 Arco 时，把主题 Token 映射到 Arco 真实变量；不要发明变量名。

---

## 一、Arco 变量命名规则

| 层 | 形态 | 示例 | 可否运行时改 |
|---|---|---|---|
| 色板（Less 粒子） | `@弧色-阶` | `@arcoblue-6`、`@green-6`、`@red-6` | ❌ 编译期 |
| 语义色（CSS 变量，RGB 三元组） | `--primary-1..10`、`--success-*`、`--warning-*`、`--danger-*`、`--link-*` | `--primary-6: var(--arcoblue-6)` | ✅ |
| 文字 | `--color-text-1..4` | `--color-text-1` | ✅ |
| 背景 | `--color-bg-1..5` | `--color-bg-1` | ✅ |
| 填充 | `--color-fill-1..4` | `--color-fill-2` | ✅ |
| 边框 | `--color-border`、`--color-border-1..4` | `--color-border-2` | ✅ |
| 圆角 | `--border-radius-small|medium|circle` | `--border-radius-medium` | ✅（`large` 未被使用；部分组件硬编码） |
| 字号/字重/间距/阴影 | `@font-size-*`、`@font-weight-*`、`@spacing-*`、`@shadow*` | `@shadow2-down` | ❌ 仅 Less |

> 关键：**语义色存的是 `R, G, B` 三元组**，组件用 `rgb(var(--primary-6))` 消费。直接写 `--primary-6: #0064FA` 会失效。
>
> 关键之二：**所有 CSS 变量声明在 `body` 上，不在 `:root`**（`dist/arco.css` 第 731 行 `body { ... }`）。在 `html` 上读 `--primary-6` 会得到空值；自定义样式要覆盖变量时写 `body`，且暗色下需用 `body, body[arco-theme='dark']` 或内联样式，否则会被特异性更高的暗黑块盖掉。

---

## 二、默认主色板（Less 粒子）

| 名称 | 值 | 说明 |
|---|---|---|
| `arcoblue-6` | `#165DFF` | **默认主色**，`--primary-6` 指向它 |
| `blue-6` | `#3491FA` | 备选蓝 |
| `green-6` | `#00B42A` | 成功 |
| `orange-6` | `#FF7D00` | 警告 |
| `red-6` | `#F53F3F` | 危险 |
| `gold-6` | `#F7BA1E` | 提醒 |
| `cyan-6` | `#14C9C9` | 辅助 |
| `purple-6` | `#722ED1` | 辅助 |
| `gray-1/2/3/4/6/8/10` | `#f7f8fa` / `#f2f3f5` / `#e5e6eb` / `#c9cdd4` / `#86909c` / `#4e5969` / `#1d2129` | 中性阶 |

---

## 三、亮色 Token 实测值

| Token | 值 | 用途 |
|---|---|---|
| `--color-bg-1` ~ `--color-bg-5` | `#fff` | 页面 / 容器 / 浮层（亮色下同为白） |
| `--color-text-1` | `gray-10` `#1d2129` | 标题、正文主色 |
| `--color-text-2` | `gray-8` `#4e5969` | 次级说明 |
| `--color-text-3` | `gray-6` `#86909c` | 辅助/占位符 |
| `--color-text-4` | `gray-4` `#c9cdd4` | 禁用 |
| `--color-fill-1` | `gray-1` `#f7f8fa` | 最浅底 |
| `--color-fill-2` | `gray-2` `#f2f3f5` | 表头 / 悬停底 |
| `--color-fill-3` | `gray-3` `#e5e6eb` | 选中底 |
| `--color-fill-4` | `gray-4` `#c9cdd4` | 深度填充 |
| `--color-border` | `gray-3` `#e5e6eb` | 默认分割线 |
| `--color-border-1..4` | `gray-2/3/4/6` | 由浅到深 |
| `--border-radius-small` | `2px` | 控件：按钮、输入、选择、文本域、Tag、Alert、Checkbox、分页项 |
| `--border-radius-medium` | `4px` | 浮层：弹窗、下拉、Cascader、Picker、Collapse、表格外角 |
| `--border-radius-large` | `8px` | **编译产物中无任何组件引用（改了不生效）** |

---

## 四、暗黑 Token 实测值

| Token | 暗黑值 | 备注 |
|---|---|---|
| `--color-bg-1` | `#17171a` | 页面底 |
| `--color-bg-2` | `#232324` | 主容器（“白卡”） |
| `--color-bg-3` | `#2a2a2b` | 二级容器 |
| `--color-bg-4` | `#313132` | 三级容器 |
| `--color-bg-5` | `#373739` | 下拉/Tooltip |
| `--color-border` | `#333335` | 分割线 |
| `--color-border-1..4` | `#2e2e30` / `#484849` / `#5f5f60` / `#929293` | 由浅到深的实色灰阶（**不是**白色透明度） |
| `--color-text-1` | `rgba(255,255,255,.90)` | 主文字 |
| `--color-text-2` | `rgba(255,255,255,.70)` | 次文字 |
| `--color-text-3` | `rgba(255,255,255,.50)` | 辅助 |
| `--color-text-4` | `rgba(255,255,255,.30)` | 禁用 |
| `--color-fill-1..4` | `4% / 8% / 12% / 16%` 白 | 填充层级 |
| `--color-mask-bg` | `rgba(23,23,26,.6)` | 遮罩（亮色为 `rgba(29,33,41,.6)`） |
| `--primary-6` | `60,126,255` | **暗色下主色会被重映射**（亮色 `22,93,255`） |

> 常见错误：把 `--color-text-2` 写成 `0.65`、`--color-text-3` 写成 `0.35`、`--color-bg-2` 写成 `#222225`。以上为官方实测值，按表抄。
>
> 暗色不是“亮色加透明度”：Arco 在 `body[arco-theme='dark']` 里重新定义了整条色板（`--red-*` / `--arcoblue-*` / `--gray-*` 共 10 阶），所以边框是重映射后的实色灰阶，主色也会更亮一档。

---

## 五、尺寸 / 排版 / 阴影（Less 变量）

| 类别 | Token | 值 |
|---|---|---|
| 控件高度 | `@size-mini/small/default/large` | `24 / 28 / 32 / 36px` |
| 间距 | `@spacing-1..` | `2 / 4 / 6 / 8 / 10 / 12 / 16 / 20 / 24 …`（4px 基准） |
| 正文字号 | `@font-size-body-3` | `14px` |
| 小字号 | `@font-size-body-2 / body-1` | `13 / 12px` |
| 标题 | `title-1/2/3` | `16 / 20 / 24px` |
| 展示 | `display-1/2/3` | `36 / 48 / 56px` |
| 行高 | `@line-height-base` | `1.5715` |
| 字体族 | `@font-family` | `Inter, -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "noto sans", "Microsoft YaHei", …` |
| 按钮字重 | `@btn-font-weight` | `400` |
| 阴影 1 | `@shadow1-down` | `0 2px 5px rgba(0,0,0,.1)` |
| 阴影 2 | `@shadow2-down` | `0 4px 10px rgba(0,0,0,.1)` |
| 阴影 3 | `@shadow3-down` | `0 8px 20px rgba(0,0,0,.1)` |
| 过渡 | `@transition-duration-1/2/3` | `.1s / .2s / .3s` |
| 弹窗圆角 | `.arco-modal` | `var(--border-radius-medium)` |
| 卡片圆角 | `.arco-card` | `var(--border-radius-none)`（需显式给圆角） |

---

## 六、vibepm 主题 → Arco `modifyVars` 映射

通用写法（Vite）：

```ts
css: {
  preprocessorOptions: {
    less: {
      modifyVars: {
        'arcoblue-6': '<主题主色>',
        'border-radius-small': '<控件圆角：按钮/输入/标签>',
        'border-radius-medium': '<浮层圆角：弹窗/下拉>',
        // 'border-radius-large' 无组件消费，不要指望它
        // 卡片默认直角，需 CSS 覆盖 .arco-card
        'font-family': `<主题字体栈>`,
      },
      javascriptEnabled: true,
    },
  },
},
```

### 12 套主题映射表

圆角列均取自各主题 `themes/<主题名>-style.md` 的 Radii 段：`small` 用于控件，`medium` 用于浮层，卡片因 Arco 默认 0 必须单独 CSS 覆盖。

| 主题 | `arcoblue-6` | `small`（控件） | `medium`（浮层） | 卡片（CSS 覆盖） | 备注 |
|---|---|---|---|---|---|
| SemiDesign | `#0064FA` | `3px` | `6px` | `12px` | 与 Arco 结构最接近，企业中后台默认 |
| 亮色科技蓝 | `#4C75F2` | `16px` | `24px` | `20px` | 按钮另有 18px 特例；**消费向 H5，不入政务企业中后台** |
| 亮色现代极简 | `#000000`→取 `#1C1F23` | `10px` | `14px` | `16px` | 纯黑在语义色里无 hover 层级，取近黑 |
| 亮色电光蓝 | `#38BDF8` | `10px` | `14px` | `18px` | — |
| 绯雾轻写 | `#E74C3C` | `6px` | `16px` | `16px` | CTA 12px、功能卡 14px 需组件级覆盖；品牌红同时改 `red-6` |
| 暗粉霓虹潮 | `#DB64A8` | `2px` | `4px` | `6px` | 保持锐利，勿胶囊化 |
| 暗紫色科技感 | `#A573FF` | `10px` | `12px` | `20px` | — |
| 暗色低饱和黑灰 | `#7A8A9E` | `10px` | `14px` | `18px` | 数据密集型，密度优先 |
| 暗黑亮青发光 | `#22D3EE` | `6px` | `18px` | `24px` | 发光用 box-shadow，Arco 无 Token |
| 暗黑荧光绿 | `#C2E600` | `6px` | `18px` | `24px` | 仅作强调色，勿大面积 |
| 电光玻璃 | `#9348D4` | `16px` | `24px` | `24px` | 大面板 40px 需自定义；弹窗必须实色 |
| 焦糖暗艺 | `#FF9A5A` | `8px` | `18px` | `18px` | Tag 6px、色板 12px 需组件级覆盖 |

> `border-radius-large` 不在此表：Arco 编译产物中无组件消费它，写了也不生效。具体覆盖代码见 [`theme-presets.md`](./theme-presets.md)。

### 无法映射的项（必须业务侧兜底）

| vibepm Token | 原因 | 兜底 |
|---|---|---|
| 5 档以上圆角 | Arco 只有 `small`(控件) / `medium`(浮层) 两个有效档，`large` 未被使用，卡片默认直角 | 按 [`theme-presets.md`](./theme-presets.md) 做两档基线 + 五类组件覆盖 |
| 彩色按钮投影 | Arco 无对应 Token | 组件级 CSS 覆盖 `box-shadow` |
| 玻璃态面板 | Arco 默认实色 | 装饰区可加 `backdrop-filter`，**弹窗禁止** |
| 自定义滚动条颜色 | Arco 用系统滚动条/自带 Scrollbar | 全局 `::-webkit-scrollbar` + `scrollbar-color`（见 ui-style-guide） |
| 发光/描边特效 | 无 Token | 自定义 class + 主题色变量 |

---

## 七、自定义组件必须消费的变量（暗黑自动适配）

```css
.my-card {
  background: var(--color-bg-2);
  color: var(--color-text-1);
  border: 1px solid var(--color-border-2);
  border-radius: var(--border-radius-medium);
}
.my-card:hover { background: var(--color-fill-2); }
.my-card .meta { color: var(--color-text-3); }
```

禁止在业务样式中写 `#fff` / `#000` / `rgba(0,0,0,.45)`，否则暗黑模式必出白块。
