# 表单规范（Form）

> 基于模板 `component-form.js` / `component-form-extended.js`（控件）与 `form-basic` / `form-group` / `form-step` / `form-step-vertical`（页面）提炼。适用于所有表单场景：新建/编辑弹窗、独立表单页、分步流程。

## 表单控件全清单（模板内置，按需选用）

| 控件 | 模板组件 | 用途 |
|---|---|---|
| 单行输入 | a-input | 文本/名称/编码等单行字段 |
| 多行文本 | a-textarea | 描述、备注、长文本 |
| 数字输入 | a-input-number | 数量、金额、数值字段 |
| 下拉选择 | a-select | 单选枚举（状态、类型、负责人） |
| 级联选择 | a-cascader | 多级分类（地区、组织树） |
| 穿梭框 | a-transfer | 左右分配（权限、成员） |
| 单选组 | a-radio-group | 2–5 个互斥选项 |
| 复选框 | a-checkbox | 多选、协议勾选 |
| 开关 | a-switch | 布尔状态（启用/停用） |
| 评分 | a-rate | 打分 |
| 日期选择 | a-date-picker | 单个日期 |
| 时间选择 | a-time-picker | 单个时间 |
| 日期范围 | a-range-picker | 起止区间 |
| 上传 | a-upload | 附件/图片上传 |
| 富文本 | contenteditable + 工具栏 | 富文本内容（见 components-guide） |

## 表单布局

- **栅格排布**：表单区用 `a-row` + `a-col` 栅格，常规表单按**每行 2–3 列**排布（24 栅格中每字段 8–12 格）；窄屏（≤900px）自动降为单列。
- **标签对齐**：标签位于控件左侧、文字**右对齐**（`label-align="right"`，Arco 默认值），标签列固定约 6em，控件列 `flex: 1` 自适应；移动端/窄屏标签置顶（控件占满整行）。
- **何时改竖排（`layout="vertical"`）**：满足任一条件就整表改竖排，不要只把个别字段改掉造成基线错位。
  - 标签文字 **> 6 个汉字**（如「是否纳入年度预算统筹范围」）且字段占比高；
  - 单列表单字段 **> 12 个**，横排标签列会把控件压到 <260px；
  - 控件本身需要整行宽度：富文本、代码编辑、地址/地图、多选穿梭框、明细子表；
  - 弹窗宽度 < 520px（窄弹窗横排必然挤）；
  - 移动端/≤900px（此时本来就是单列，直接竖排）。
  - 竖排时标签左对齐、14/600，标签与控件间距 8px，字段间距 20–24px；必填 `*` 仍在标签前。
- **标签样式**：14px / 600，不强制大写；横排超 6em 用省略号并补 `a-tooltip`，竖排允许两行不截断。
- **分组表单**（form-group）：同类字段放同一卡片分组，组间用卡片 + 组标题区分，卡片内栅格排布。
- **必填标记**：必填字段 label 前加红色 `*`；校验未过时红环 + 错误短句。
- **行间距**：表单项间距约 16–24px；提交行上距 20px、gap 12、按钮 min-width 120px。

### Arco 表单实现要点（`a-form` / `a-form-item`）

| 需求 | 写法 | 默认值提醒 |
|---|---|---|
| 标签列宽 | `:label-col-props="{ span: 6 }"` | 默认 `span: 5` |
| 控件列宽 | `:wrapper-col-props="{ span: 18 }"` | 默认 `span: 19` |
| 标签右对齐 | `label-align="right"` | 已是默认，无需书写 |
| 标签自动宽度 | `auto-label-width`（2.13+） | 默认 `false` |
| 校验规则 | `:rules="{ name: [{ required: true, message: '请输入名称' }] }"` | 也可写在 FormItem 上，优先级更高 |
| 失败滚动定位 | `scroll-to-first-error`（2.51+） | **默认 `false`，vibepm 要求显式开启** |
| 错误文案 | FormItem `help` / `extra` | 用内建插槽即可，不要再手写一份 `.field-error` |
| 反馈图标 | FormItem `feedback`（2.16+） | 默认 `false` |
| 校验时机 | FormItem `validate-trigger` | 默认 `change`；提交型表单建议 `blur` |
| 必填星号位置 | FormItem `required` + `asterisk-position` | 默认 `start`（在标签前，符合 vibepm） |
| 清空按钮 | Input/Select 的 `allow-clear` | **默认 `false`，必须显式开启** |

```ts
// 校验返回值：undefined = 通过；对象 = 失败。不要用 try/catch 判断
const errors = await formRef.value?.validate();
if (errors) return; // 保留表单与错误态
```

## 表单页结构（4 种模板）

| 模板 | 结构 |
|---|---|
| 基础表单 form-basic | 页面标题 + 说明（title/desc）→ 单区块表单（body）→ 提交行（actions） |
| 分组表单 form-group | 多分组表单（每组一卡片）→ 底部提交行（actions） |
| 横向分步 form-step | 顶部步骤条（steps）→ 当前步表单体（body）→ 上一步/下一步/提交（actions）；全部完成后显示成功页（success） |
| 纵向分步 form-step-vertical | 左侧步骤导航 + 右侧内容区（split 布局）→ 提交行 |

### 长表单：固定底栏（官方 form/group 写法）

分组表单字段多时，提交行贴在视口底部，滚动过程中始终可点：

```css
.form-actions {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  height: 60px;
  padding: 14px 20px;
  background: var(--color-bg-2);   /* 必须实色，否则内容从底下透出 */
  border-top: 1px solid var(--color-border-2);
  text-align: right;
  z-index: 10;
}
```

- 用了固定底栏，表单容器要给 `padding-bottom: 80px`，避免最后一行被盖住。
- 只有「一屏放不下的表单页」才用；弹窗表单、短表单仍用普通提交行（上距 20px、gap 12）。

### 分步表单：`keep-alive` 保住已填内容

官方 `form/step` 的写法值得照抄：步骤内容用 `keep-alive` 包裹，回退上一步不丢数据；外层再套 `a-spin :loading` 处理提交等待。

```vue
<a-steps v-model:current="step" :style="{ width: '580px' }" line-less>
  <a-step description="填写基础信息">基础信息</a-step>
  <a-step description="配置渠道">渠道配置</a-step>
  <a-step description="提交完成">完成</a-step>
</a-steps>

<keep-alive>
  <BaseInfo v-if="step === 1" @change-step="changeStep" />
  <ChannelInfo v-else-if="step === 2" @change-step="changeStep" />
  <Success v-else @change-step="changeStep" />
</keep-alive>
```

- `keep-alive` 要求每个步骤是**独立组件**；三个步骤写在一个组件里用 `v-show` 也行，但会失去按步校验的清晰边界。
- 步骤间传递数据用父组件的汇总对象（`submitModel = { ...submitModel, ...model }`），不要靠组件内部 state。

## 校验与反馈（强制）

- 提交前整表校验；失败：字段红环 + `.field-error` 短句（role="alert"），**不关闭表单**
- 提交中按钮 loading，防重复提交
- 成功后 Toast 提示 → 关闭/跳转 → 刷新关联列表
- 失败/异常：Toast 错误提示，保持表单内容不丢失
- 清空钮：有值且聚焦/悬停时出现（输入类控件）
- 所有控件宽 100%（栅格内），占位符用次文灰

## 未保存编辑保护（强制）

- 表单存在**未保存的修改**时，触发以下动作必须先确认，禁止静默丢弃：
  - 切换 Tab / 切换分组项 / 新增另一条 / 离开页面 / 关闭弹窗
- 确认弹窗文案模板：「未保存的编辑内容，是否放弃并切换到其它项？」/「是否放弃并继续…」
- 确认「放弃」→ 丢弃未保存内容并继续；「取消」→ 留在当前编辑，内容不丢失
- 编辑态进入即标记 dirty，保存/放弃成功后清除标记

## 自查清单

1. 字段栅格排布（常规 2–3 列，窄屏单列）而非一个字段占满整行？
2. 标签位于控件左侧且文字右对齐、14px/600，必填有红 * 标记？
3. 校验错误红环 + 短句、不关闭表单、提交中 loading？
4. 提交行按钮完整（保存/取消或上一步/下一步），间距符合规范？
5. 分步表单有步骤条 + 完成后成功态？
6. `scroll-to-first-error` 已开启、`allow-clear` 已显式设置？
