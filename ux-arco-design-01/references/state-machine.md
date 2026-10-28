# 状态机与「状态 → 动作」矩阵

> B 端列表的主语不是「一行数据」，而是「一个处于某状态的对象」。状态没定义清楚，表格、按钮、权限、文案都会各自发挥。
> 本文是所有业务列表/详情页的前置规范：**先有状态机，再画界面**。

---

## 一、状态定义四件套（缺一不可）

每个状态必须同时给出：

| 项 | 说明 | 反例 |
|---|---|---|
| 业务名称 | 用户能说出口的词 | `status=3` |
| 编码 | 后端真实枚举值 | 前端自造 `pending2` |
| 色彩语义 | 成功 / 处理中 / 警告 / 失败 / 中性 | 用品牌色表示状态 |
| 是否终态 | 终态不可再流转，需显式提示 | 已归档还能「编辑」 |

### 色彩语义映射（Arco Tag）

| 语义 | 用色 | `a-tag color` | 适用 |
|---|---|---|---|
| 成功 / 已完成 | 绿 | `green` | 已通过、已办结、已发布 |
| 进行中 / 待处理 | 蓝 | `arcoblue` | 审核中、处理中、待受理 |
| 警告 / 需关注 | 橙 | `orange` | 待补充、即将超期、部分成功 |
| 失败 / 异常 | 红 | `red` | 已驳回、失败、已作废 |
| 中性 / 草稿 | 灰 | `gray` | 草稿、已停用、已归档 |

规则：

- 颜色**不能是唯一信息**，Tag 必须带文字（色盲可读）。
- 同一系统内同一语义只能用一种颜色，不允许「已驳回」一处红一处橙。
- 状态色不参与图表分类色序列（见 `chart-theme.md`）。

---

## 二、状态 → 动作矩阵（核心产出物）

在动手写页面前，先把这张表填满，它同时决定：按钮显示、按钮禁用、权限校验、批量可用性。

| 状态 | 查看 | 编辑 | 提交 | 撤回 | 审核 | 作废 | 删除 |
|---|---|---|---|---|---|---|---|
| 草稿 | ✓ | ✓ | ✓ | — | — | ✓ | ✓ |
| 待审核 | ✓ | ✗ | — | ✓ | — | ✗ | ✗ |
| 审核中 | ✓ | ✗ | — | ✗ | ✓（有权限者） | ✗ | ✗ |
| 已通过 | ✓ | ✗ | — | ✗ | — | ✓ | ✗ |
| 已驳回 | ✓ | ✓ | ✓ | — | — | ✓ | ✓ |
| 已作废（终态） | ✓ | ✗ | ✗ | ✗ | ✗ | — | ✗ |

填写规则：

1. **一格只能是三种值**：允许（✓）/ 不允许（—）/ 有条件允许（写明条件）。
2. 有条件允许必须写清条件，例如「仅创建人可撤回」「仅当无下游引用时可删除」。
3. 终态行除「查看」外全部为 `—`。
4. 矩阵是**单一事实源**：表格按钮、详情页按钮、批量操作都从这张表推导，不允许页面各写一套 `v-if`。

---

## 三、落地写法

### 1. 用一份配置推导所有按钮

```ts
// constants/order-actions.ts
export type ActionKey = 'view' | 'edit' | 'submit' | 'withdraw' | 'audit' | 'void' | 'delete';

export const ACTION_MATRIX: Record<string, Partial<Record<ActionKey, true | string>>> = {
  draft:    { view: true, edit: true, submit: true, void: true, delete: true },
  pending:  { view: true, submit: true }, // submit = 重新提交
  auditing: { view: true, withdraw: true, audit: '仅审核人' },
  approved: { view: true, void: true },
  rejected: { view: true, edit: true, submit: true, void: true, delete: true },
  voided:   { view: true },
};

/** 返回 { enabled, reason } —— 禁用必须有原因 */
export function resolveAction(status: string, action: ActionKey, ctx: { isOwner: boolean; canAudit: boolean }) {
  const rule = ACTION_MATRIX[status]?.[action];
  if (rule === undefined) return { enabled: false, reason: '当前状态不支持该操作' };
  if (rule === true) return { enabled: true, reason: '' };
  if (action === 'withdraw' && !ctx.isOwner) return { enabled: false, reason: '仅创建人可撤回' };
  if (action === 'audit' && !ctx.canAudit) return { enabled: false, reason: '需要审核权限' };
  return { enabled: true, reason: '' };
}
```

### 2. 按钮必须能解释「为什么不能点」

```vue
<a-tooltip :content="withdraw.reason" :disabled="withdraw.enabled">
  <span>
    <a-button :disabled="!withdraw.enabled">撤回</a-button>
  </span>
</a-tooltip>
```

- 禁用按钮不触发 hover 时，外层要包 `<span>` 才能显示 tooltip（原生 `disabled` 不冒泡事件）。
- 一次性解释不清楚的（如「需先处理 3 条下游数据」），点击后给引导弹窗，而不是静默禁用。
- 只对**业务上必须解释**的动作用「禁用 + 原因」；纯权限不足按 `permission-guide.md` 直接隐藏。

### 3. 批量操作按矩阵取交集

```ts
const canBatchVoid = computed(() =>
  selectedRows.value.length > 0 &&
  selectedRows.value.every((r) => resolveAction(r.status, 'void', ctx).enabled),
);
```

- 勾选的行里只要有一条不允许，批量按钮就禁用，并在 tooltip 说明「所选 5 条中有 2 条已作废，不可批量操作」。
- 不要「跳过不允许的行悄悄执行」，除非在确认弹窗里明确写出「将跳过 2 条」。

---

## 四、状态流转的可视化

- 详情页/审批页必须能一眼看到走到哪一步：`a-steps`（流程固定且节点 ≤ 7）或 `a-timeline`（有时间戳的审批记录）。
- 终态要有明确落点：通过 = 成功色 + 后续动作；驳回 = 失败色 + 修改入口 + 原因。
- 触发状态变化的动作，成功后要重查列表并高亮该行（`row-class` 或短暂 `bg` 提示）。
- 状态流转不可逆的场景（如作废），二次确认文案必须写清「不可恢复」。

---

## 五、自查清单

1. 每个状态都有业务名称、后端编码、色彩语义、是否终态？
2. 「状态 → 动作」矩阵是否填满，且页面按钮全部由它推导（没有散落 `v-if`）？
3. 禁用动作是否都给出了原因，且有 tooltip/引导？
4. 批量按钮是否按选中行的状态交集计算，并在 tooltip 里说明冲突？
5. 终态是否除查看外无其他动作，且不可逆操作有「不可恢复」提示？
6. 状态色是否统一（同一语义一种颜色），且 Tag 带文字？
7. 触发流转后是否重查并高亮该行？
