# Frame UI 风格规范（12 套视觉主题）

> 每套主题的完整规范（设计 Tokens、按钮/表单/弹窗细节、提示词包、防跑偏约束、质量评分）见
> `themes/<主题名>-style.md`。本文件是速查总览与选择指引。

## 12 套主题速查

| 主题名 | 主色 | 亮度 | 风格关键词 | 适合产品类型 | 规范文件 |
|---|---|---|---|---|---|
| 亮色现代极简 | `#000000` | 亮 | 冷静、留白、低彩度、近黑主按钮、Manrope+Inter | 现代 SaaS、设置页、B2B | themes/亮色现代极简-style.md |
| 亮色电光蓝 | `#0052FF` | 亮 | 电光蓝、清新 | 科技感轻量产品 | themes/亮色电光蓝-style.md |
| 亮色科技蓝 | `#4C75F2` | 亮 | 科技蓝、大圆角、FAB | 消费向 H5 / 会员中心 / 轻应用（**不用于政务企业中后台**） | themes/亮色科技蓝-style.md |
| 绯雾轻写 | `#E74C3C` | 亮 | 珊瑚红、轻写 | 内容/品牌向 | themes/绯雾轻写-style.md |
| SemiDesign | `#0064FA` | 亮 | 工程感、克制圆角 3/6/12、字节系 | 管理后台、设计系统、中台控制台 | themes/SemiDesign-style.md |
| 暗粉霓虹潮 | `#E41874` | 暗 | 霓虹、潮流 | 潮流/娱乐向 | themes/暗粉霓虹潮-style.md |
| 暗紫色科技感 | `#6867F7` | 暗 | 紫、科技 | 科技感产品 | themes/暗紫色科技感-style.md |
| 暗色低饱和黑灰 | `#FAFAFA` | 暗 | 低饱和、沉稳 | 数据密集型后台 | themes/暗色低饱和黑灰-style.md |
| 暗黑亮青发光 | `#22D3EE` | 暗 | 亮青、发光 | 炫技向/大屏 | themes/暗黑亮青发光-style.md |
| 暗黑荧光绿 | `#D9FF00` | 暗 | 荧光绿、高对比 | 电竞/监控 | themes/暗黑荧光绿-style.md |
| 电光玻璃 | `#A855F7` | 暗 | 玻璃拟态、紫 | 潮流/视觉向 | themes/电光玻璃-style.md |
| 焦糖暗艺 | `#F0833F` | 暗 | 焦糖橙、暖 | 内容/创意向 | themes/焦糖暗艺-style.md |

## 主题选择指引

1. **政务/企业中后台（默认）**：`SemiDesign`（专业克制、字节系工程感）；暗色中后台选 `暗色低饱和黑灰`（数据密集）或 `暗紫色科技感`（AI/开发者控制台）。**不要用 `亮色科技蓝`**——该主题是 46px 按钮 + 20–24px 大圆角 + FAB 的消费向风格，违反“消费向大圆角/彩色投影/FAB 不得用于桌面政务企业中后台”。
2. **SaaS/B2B 产品页**：`亮色现代极简`（近黑主色、现代感强）。
3. **消费向 H5 / 会员中心 / 轻应用**：`亮色科技蓝`、`绯雾轻写`。
   其余主题（暗粉霓虹潮、暗黑亮青发光、暗黑荧光绿、电光玻璃、焦糖暗艺）偏落地页/移动端/潮流向，**不得默认套到后台上**。
4. **用户指定场景或品牌**：先按产品语气对号入座——冷静克制选亮色系，科技潮流选暗色系。
5. **拿不准时问用户**：给出 2～3 个候选主题及差异（亮/暗、主色、圆角风格），不要擅自定。
6. **同一界面只用一个主题**：主题是整套 token 体系，禁止混搭不同主题的主色与圆角。

## 通用规范（所有主题一致，细节以主题文档为准）

### 字体栈
- 西文：Inter（SemiDesign 全栈）或 Manrope 标题 + Inter 正文（现代极简）
- 中文回退：`PingFang SC`、`Hiragino Sans GB`、`Microsoft YaHei`
- 正文 14–16px / line-height 1.5–1.6；标签 14px / 600；错误短句 12px / 500

### 按钮家族（五态齐全）
- 主按钮 `.btn-primary`：实底主色 + 白字；悬停微抬（translateY(-1px)）+ 强化投影；按下 translateY(1px) 或 scale 微缩
- 次按钮 `.btn-secondary`：浅底细边；悬停强调色浅染 + 微抬
- 描边 `.btn-outline`：透明底 + 主题边；悬停强调色浅染
- 幽灵 `.btn-ghost`：透明底、次文色；悬停浅强调底、不抬升
- 链接 `.btn-link` / 图标 `.btn-icon`（40×40）/ 禁用 `.btn-disabled`
- 尺寸族：默认 / `.btn-sm` / `.btn-lg` / `.btn-pill`

### 表单与反馈
- 输入：主题圆角档、白底 + 细边；悬停边加深，聚焦边转主色（或灰环）
- 错误：`.is-error` 红环（0 0 0 3px 红透明）+ `.field-error` 短句（role="alert"）
- 清空钮：圆钮，有值且聚焦/悬停时出现
- 提交行：上距 20px、gap 12、按钮 min-width 120px
- 提示条 `.alert`：主题静音底或浅色底；强提示实底主色白字
- Toast：顶中、双层柔影、220ms 显隐

### 弹窗（Dialog）
- 遮罩：半透明 + blur(12px)，打开锁滚动
- 面板：宽 440px（内容型 560px）、主题圆角档（12px 或 16px）、**不透明**、柔影（禁止玻璃半透明面板）
- 结构：顶栏（浅灰底 + 标题 + 关闭钮 28×28）/ 正文 / 脚部右对齐；头脚 1px 分割
- 动效：遮罩 200ms；面板 translateY(10px) scale(0.98) → 归位 220ms

### 滚动条（所有界面统一）
- 宽 8px，轨道透明，滑块 `rgba(0,0,0,0.18)`，悬停 `rgba(0,0,0,0.28)`，按下 `rgba(0,0,0,0.36)`
- Firefox：`scrollbar-width: thin` + `scrollbar-color`
- WebKit：胶囊滑块 `border: 2px solid transparent; background-clip: padding-box`
- 暗色覆盖：thumb `rgba(255,255,255,0.14)`，悬停 0.26，按下 0.34

### 布局
- 容器 1120–1200px，水平 16–32px；区块间距 24–48px；卡片内边距 16–24px；8pt 节奏
- 顶栏 sticky 高 **60px**（与 `pages-guide.md` shell 骨架一致，全站统一，不要写成 52/56）
- 弹窗演示双列 gap 20；≤900px 单列

### 响应式断点（Arco 真实断点，禁止自创）

Arco Grid 的断点是 `576 / 768 / 992 / 1200 / 1600`，不是「768/992/1200/1600/1920」：

| 断点 | 宽度 | 典型设备 |
|---|---|---|
| `xs` | `< 576px` | 手机 |
| `sm` | `≥ 576px` | 大手机 / 小平板 |
| `md` | `≥ 768px` | 平板 |
| `lg` | `≥ 992px` | 小桌面 |
| `xl` | `≥ 1200px` | 标准桌面（vibepm 默认容器上限） |
| `xxl` | `≥ 1600px` | 大屏 |

```vue
<a-row :gutter="[16, 16]">
  <a-col :xs="24" :sm="12" :md="8" :lg="6">…</a-col>
</a-row>
```

- `gutter`、`a-grid` 的 `cols/rowGap/colGap` 均可传响应式对象：`:gutter="{ xs: 8, md: 16, xl: 24 }"`。
- 业务固定断点（与上表配合，不另立标准）：筛选区 `≤980px` 隐藏标签；表单 `≤900px` 单列；侧边栏 `breakpoint="xl"`（<1200px 折叠，移动端换 `a-drawer`）。

### 密度与尺寸（Arco 默认偏紧凑）

| 项 | Arco 默认 | vibepm 要求 | 做法 |
|---|---|---|---|
| 控件高度 | 24 / 28 / **32** / 36（mini→large） | 主操作 ≥36；图标按钮 40×40 | 主按钮 `size="large"`；图标按钮用 40×40 自定义 |
| 按钮字重 | 400 | 主按钮 600 观感 | `.arco-btn-primary { font-weight: 600 }` |
| 圆角 | small 2 / medium 4 / large 8 | 主题圆角档 | `modifyVars` 覆盖三个圆角变量 |
| 行高 | 1.5715 | 1.5–1.6 | 与 Arco 一致，无需改 |

> 不要为“看起来更大”在业务页逐个写 `height: 40px`；先改 `modifyVars` 与组件级 token，再补例外。

### 无障碍基线（Arco 已覆盖一部分，其余必须自补）

- 图标按钮必须有可读名称：`<a-button aria-label="关闭">`，纯图标 `<button>` 禁止无 aria-label。
- 键盘可达：所有自定义可点击元素用 `<button>` / `<a href>`，不要用 `<div @click>`；禁止 `outline: none` 无替代。
- 焦点可见：统一 `:focus-visible { outline: 2px solid rgba(var(--primary-6), .45); outline-offset: 2px; }`。
- 表单：label 必须与控件关联（用 `a-form-item` 的 `label`/`field` 自动关联，勿手写裸 `<label>`），错误提示用 FormItem `help`；不要只靠红框传达错误。
- 状态：颜色 + 文案/图标双重编码，不能只有颜色差。
- 弹窗：Arco 已做基础焦点处理，自定义弹层结构时需自行补齐“打开聚焦面板、关闭回焦触发元素”，勿覆盖 `tabindex`。
- 对比度：正文 ≥ 4.5:1，大字 ≥ 3:1；暗黑模式单独复核。

### 筛选区布局（列表页筛选面板，强制规范）

筛选区一律用**栅格单行排布 + 自动换行**，禁止把字段人为拉宽导致条件与按钮拆成两行。

- **6 是上限，不是目标**：每列（标签 + 控件）**最小可用宽度 220px**，低于这个宽度日期范围、机构树、多选就会挤成没法用。桌面列数 = `clamp(2, floor(容器宽 / 220), 6)`，≤576px 单列：1440px 屏（内容区约 1190px）排 **5** 列，1280px 屏（约 1030px）排 **4** 列，1600px 以上才排到 6 列。
- **区间/树/多选占 2 格**：`a-range-picker`、`a-tree-select`、多选标签类控件的 `:span="2"`（`a-grid-item` 支持 `span`），否则控件会被压成一条缝。
- **查询/重置按钮**：放进 `<a-grid-item suffix>`，Arco 会把它固定在该行末尾，字段换行时按钮随最后一行走，天然满足“按钮不单独占一行”。
- **字段宽度**：由 `cols` 均分，不要在单个字段上写死 `width`；**禁止**单个字段宽超 50% 把剩余条件挤到下一行。
- **行/列间距**：`row-gap: 16px`、`col-gap: 16px`（`a-grid` 的 `row-gap` / `col-gap`）。
- **窄屏响应式**：`≤980px` 时标签列隐藏、控件占满整行（容器查询 `@container pro-search (max-width: 980px)`）。
- **字段过多**：超过 6 个时用 `a-grid` 的 `collapsed` + `collapsed-rows="1"`，由组件收起第 2 行起，不要自己算索引。
- **自查**：产出后检查——单列实宽是否 ≥220px；区间类控件是否占满 2 格；是否出现「条件一行 + 按钮一行」；1440px 下是否挤成 6 列细条（挤成即不合规）。

```vue
<a-grid
  :cols="{ xs: 1, sm: 2, md: 3, lg: 4, xl: 5, xxl: 6 }"
  :col-gap="16"
  :row-gap="16"
  :collapsed="collapsed"
  :collapsed-rows="1"
  class="pro-search"
>
  <a-grid-item v-for="f in fields" :key="f.key">
    <a-form-item :label="f.label" :hide-label="narrow">
      <component :is="f.control" v-model="filters[f.key]" />
    </a-form-item>
  </a-grid-item>

  <!-- suffix：始终排在本行末尾 -->
  <a-grid-item suffix>
    <a-space>
      <a-button type="primary" @click="query">查询</a-button>
      <a-button @click="reset">重置</a-button>
      <a-button v-if="fields.length > 6" type="text" @click="collapsed = !collapsed">
        {{ collapsed ? '展开' : '收起' }}
      </a-button>
    </a-space>
  </a-grid-item>
</a-grid>
```

## 生产时要做的
1. **先定主题**：从 `themes/` 读对应 `<主题>-style.md` 全文，拿到该主题的完整 Token 与提示词包。
2. **再选组件**：按 `component-catalog.md` 选页面骨架与控件参考。
3. **严格跟随 Token**：主色、圆角档、阴影、字体、滚动条、弹窗规则全部按主题文档，不自由发挥。
4. **遵守主题「避免项」**：每个主题文档都列了跑偏风险（如 SemiDesign 禁止 Ant 蓝、禁止按钮圆角 >6px），逐条自查。
5. **同一界面主题一致**：不混搭。
