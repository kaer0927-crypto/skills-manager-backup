# 可访问性基线（键盘 / 语义 / 对比度 / 动效）

> 目标不是「过认证」，而是让键盘用户、色觉障碍用户、低视力用户能完成核心任务。
> 与 `ui-style-guide.md`（视觉）、`forms-guide.md`（表单）、`assets/frame-presets.css`（焦点环 / reduced-motion）配合。

---

## 一、键盘可达（B 端最高频）

| 要求 | 说明 |
|---|---|
| 全部可操作元素可 Tab 到达 | 自定义 `div` 按钮必须 `tabindex="0"` + `role="button"` + 回车/空格触发 |
| 焦点顺序与视觉顺序一致 | 不要用 CSS `order` 打乱焦点 |
| 弹窗焦点陷阱 | `a-modal` 自带；自研弹窗必须实现：打开聚焦首元素、Esc 关闭、关闭后焦点返回触发元素 |
| Esc 关闭浮层 | 弹窗、抽屉、下拉、Popover 都要支持 |
| 表格操作可用键盘 | 行内按钮可 Tab，勾选用原生 checkbox |
| 不要 `outline: none` 了事 | 必须提供替代焦点样式（`frame-presets.css` 已内置 `:focus-visible` 环） |

---

## 二、表单语义

```vue
<a-form-item
  field="phone"
  label="手机号"
  :help="errors.phone"
  :validate-status="errors.phone ? 'error' : undefined"
>
  <a-input
    v-model="form.phone"
    aria-describedby="phone-help"
    :aria-invalid="!!errors.phone"
  />
</a-form-item>
```

- 错误短句容器加 `role="alert"`，确保屏幕阅读器播报。
- 必填除了红色 `*`，还要有文本/属性提示（`aria-required`），红色不是唯一信息。
- 校验失败除滚动外，把焦点移到第一个错误字段。
- `placeholder` 不能替代 `label`。

---

## 三、反馈播报

| 组件 | 要求 |
|---|---|
| Toast / Message | 容器 `aria-live="polite"`；错误用 `role="alert"`，不要滥用打断 |
| 加载态 | `aria-busy="true"`，并有文字状态（不要只有一个转圈） |
| 进度条 | `role="progressbar"` + `aria-valuenow/min/max` |
| 图标按钮 | 必须有 `aria-label`（如 `aria-label="刷新"`），不能只靠图标 |
| 图表 | 提供文字摘要或数据表替代；纯装饰图 `aria-hidden="true"` |

---

## 四、对比度与色彩

| 文本类型 | 最低对比度 |
|---|---|
| 正文（< 18.66px 非粗体） | 4.5:1 |
| 大字（≥ 18.66px 粗体 或 ≥ 24px） | 3:1 |
| 承载信息的图标/边框 | 3:1 |
| 禁用态 | 豁免，但仍需可辨认 |

- 状态不能只靠颜色：Tag 带文字、涨跌带 `+/-`、图表系列带图例。
- 暗色下重点复核 `--color-text-3/4` 在 `bg-2/bg-3` 上的对比，辅助文字最易不达标。
- 可点击文字除颜色外要有下划线或图标（hover 才出现不算）。

---

## 五、动效与触控

- 非必要动效在 `prefers-reduced-motion: reduce` 下关闭（基础过渡已内置，业务自定义动画需自己包一层）。
- 不用闪烁（> 3 次/秒）与无控制的自动播放。
- 触控目标 ≥ 44×44（移动端），桌面图标按钮 ≥ 32×32（vibepm 取 40×40）。
- 点击区域可大于视觉尺寸：小图标 + 大 padding。

---

## 六、验收方法（交付前 10 分钟）

1. **只用键盘**走一遍主流程：Tab 能到所有按钮、Esc 能关弹窗、关闭后焦点回到原处。
2. 把页面缩放到 200%，确认无内容被裁切、无横向抖动。
3. 用浏览器 DevTools 的对比度检查抽查正文/辅助文字。
4. 开启系统「减少动态效果」，确认没有残余动画。
5. 用读屏（macOS VoiceOver：`Cmd+F5`）听一遍表单错误与 Toast。

---

## 七、自查清单

1. 所有可操作元素可 Tab 到达，焦点可见？
2. 弹窗有焦点陷阱，关闭后焦点回原处？
3. 表单错误是否 `role="alert"` + `aria-invalid` + `aria-describedby`？
4. 图标按钮是否都有 `aria-label`？
5. 状态信息是否不只依赖颜色？
6. 正文对比度 ≥ 4.5:1（暗色 `text-3/4` 重点查）？
7. `prefers-reduced-motion` 下动画是否关闭？
