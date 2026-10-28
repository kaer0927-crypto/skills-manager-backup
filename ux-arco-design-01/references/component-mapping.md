# Arco 组件 ↔ vibepm 规范对照

> 原则：**能用 Arco 原生就用原生，vibepm 只补业务规则与缺失组件**。所有 API 以 `@arco-design/web-vue@2.59.0` 的 `README.zh-CN.md` 为准。
> 本文替代此前基于 Ant Design 记忆写下的写法（`type="link"`、`danger: true`、`position="top-center"`、`:styles` 等**均不存在**）。

---

## 一、决策矩阵

| 场景 | 方案 | 理由 |
|---|---|---|
| 数据表格 | `a-table` + vibepm CRUD 规则 | 列设置/固定列/虚拟滚动/汇总行开箱即用 |
| 新建/编辑表单 | `a-form` + vibepm 栅格与校验规则 | `label-col-props`、`rules`、`scroll-to-first-error` 已足够 |
| 确认弹窗 | `a-modal` / `Modal.confirm` + vibepm 实色面板 | 只需覆盖圆角与背景 |
| Toast | `Message` + vibepm 视觉覆盖 | API 够用，动画细节用 CSS 调 |
| 分页 | `a-pagination`（表格内建） | `show-total` / `show-page-size` 全覆盖 |
| 筛选区 | `a-grid`（非 `a-row`） | `cols` + `collapsed` + `suffix` 天然满足“一行 6 个 + 折叠 + 按钮同行” |
| KPI 指标卡 | **vibepm 自研** | Arco `a-statistic` 只有数值，无 12 种变体 |
| 图表 | vibepm 色板 + ECharts | Arco Vue 不含图表组件 |
| 富文本 | vibepm 自研 | Arco 无富文本组件 |
| 结果页 | `a-result` + 主题插画 | `status` 支持 success/warning/info/error/403/404/500 |
| 空状态 | `a-empty` | 支持全局 `#empty` 插槽统一文案 |
| 加载骨架 | `a-skeleton` | 列表/详情首屏优于 Spin |
| 侧滑详情 | `a-drawer` | 主从详情首选 |

---

## 二、Button

Arco 只有 5 种 `type`：`primary | secondary | outline | dashed | text`，**没有 `link` 和 `ghost`**。

| vibepm 家族 | Arco 写法 |
|---|---|
| primary | `<a-button type="primary">` |
| secondary | `<a-button>`（默认即 secondary）或 `type="secondary"` |
| outline | `<a-button type="outline">` |
| ghost | `<a-button type="text">` |
| link | `<a-button type="text" class="btn-link">` + 主色文字（原生无 link 型） |
| 图标按钮 | `<a-button shape="circle">` + `#icon` 插槽 |
| 危险 | `<a-button status="danger">`（与 `type` 正交，可叠加） |
| 尺寸 | `size="mini|small|medium|large"`（24/28/32/36px） |

```vue
<a-button type="primary" :loading="saving" @click="submit">保存</a-button>
<a-button type="text" @click="edit(record)">编辑</a-button>
<a-button type="text" status="danger" @click="remove(record)">删除</a-button>
```

vibepm 补充（主题层覆盖，不在业务页写）：

```css
.arco-btn-primary { font-weight: 600; }
.arco-btn-primary:hover { transform: translateY(-1px); }
.btn-link { color: rgb(var(--primary-6)); }
```

---

## 三、Table

### 关键 Props

| 需求 | 写法 |
|---|---|
| 行选择 | `:row-selection="{ type: 'checkbox' }"` |
| 仅全选当前页 | `:row-selection="{ type: 'checkbox', onlyCurrent: true }"` |
| 跨页保留选择 | 受控 `:selected-keys="keys"` + `@select` / `@select-all` |
| 固定操作列 | 列上 `fixed: 'right'` |
| 斑马纹 | `stripe`（默认 `false`） |
| 边框 | `bordered`（默认 `true`） |
| 汇总行 | `summary` + `#summary-cell` |
| 列宽拖拽 | `column-resizable` |
| 横向滚动 | `:scroll="{ x: 1200 }"` |
| 虚拟滚动 | `:virtual-list-props="{ height: 520 }"` + 唯一 `row-key` |
| 分页位置 | `page-position="br"`（默认右下） |
| 空状态 | `#empty` 插槽 |
| 分页工具区 | `#pagination-left` / `#pagination-right` |

### CRUD 表格骨架

```vue
<script setup lang="ts">
import { ref, reactive } from 'vue';
import { Message, Modal } from '@arco-design/web-vue';

const loading = ref(false);
const rows = ref<any[]>([]);
const selectedKeys = ref<(string | number)[]>([]);
const pager = reactive({ current: 1, pageSize: 10, total: 0 });

const columns = [
  { title: '名称', dataIndex: 'name', ellipsis: true, tooltip: true },
  { title: '状态', slotName: 'status', width: 120 },
  { title: '操作', slotName: 'action', width: 160, fixed: 'right' as const },
];

const fetchList = async () => {
  loading.value = true;
  try {
    const res = await api.list({ page: pager.current, size: pager.pageSize });
    rows.value = res.items;
    pager.total = res.total;
  } finally {
    loading.value = false;
  }
};

const remove = (record: any) => {
  Modal.confirm({
    title: '删除确认',
    content: `确定删除「${record.name}」？此操作不可恢复。`,
    okText: '删除',
    cancelText: '取消',
    okButtonProps: { status: 'danger' },
    onBeforeOk: async (done) => {
      try {
        await api.remove(record.id);
        Message.success('删除成功');
        await afterDelete();
        done(true);
      } catch {
        Message.error('删除失败');
        done(false);
      }
    },
  });
};

// 删空回退：先重查，再判断是否回退
const afterDelete = async () => {
  await fetchList();
  if (rows.value.length === 0 && pager.current > 1) {
    pager.current -= 1;
    await fetchList();
  }
};
</script>

<template>
  <a-table
    row-key="id"
    :data-source="rows"
    :columns="columns"
    :loading="loading"
    :row-selection="{ type: 'checkbox', onlyCurrent: true }"
    v-model:selected-keys="selectedKeys"
    :pagination="{
      current: pager.current,
      pageSize: pager.pageSize,
      total: pager.total,
      showTotal: true,
      showPageSize: true,
      pageSizeOptions: [10, 20, 50],
    }"
    @page-change="(p: number) => { pager.current = p; fetchList(); }"
    @page-size-change="(s: number) => { pager.pageSize = s; pager.current = 1; fetchList(); }"
  >
    <template #status="{ record }">
      <a-tag :color="record.enabled ? 'green' : 'gray'">
        {{ record.enabled ? '启用' : '停用' }}
      </a-tag>
    </template>
    <template #action="{ record }">
      <a-button type="text" @click="edit(record)">编辑</a-button>
      <a-button type="text" status="danger" @click="remove(record)">删除</a-button>
    </template>
  </a-table>
</template>
```

> `pagination` 对象内是 **Pagination 的 Props**（`showTotal`、`showPageSize`、`pageSizeOptions`），不是 Ant 的 `showSizeChanger`。

---

## 四、Form

### 关键 Props

| 需求 | 写法 |
|---|---|
| 标签宽度 | `:label-col-props="{ span: 6 }"`（默认 5） |
| 控件宽度 | `:wrapper-col-props="{ span: 18 }"`（默认 19） |
| 标签右对齐 | `label-align="right"`（默认值，无需写） |
| 标签自动宽度 | `auto-label-width`（2.13+） |
| 校验规则 | `:rules="{ name: [{ required: true, message: '请输入名称' }] }"` |
| 校验失败滚动 | `scroll-to-first-error`（2.51+，**默认 false，vibepm 要求开启**） |
| 提交 | `@submit="onSubmit"` + Form 的 `submit` 事件 |
| 必填星号 | FormItem `required`，`asterisk-position="start"`（默认在标签前） |
| 帮助文案 | FormItem `help`（错误位）/ `extra`（常规说明） |
| 反馈图标 | FormItem `feedback`（2.16+） |
| 触发时机 | `validate-trigger="change|input|focus|blur"`（默认 change） |

### 表单骨架

```vue
<script setup lang="ts">
import { ref, reactive } from 'vue';
import type { FormInstance } from '@arco-design/web-vue';

const formRef = ref<FormInstance>();
const form = reactive({ name: '', type: '', remark: '' });
const saving = ref(false);

const rules = {
  name: [{ required: true, message: '请输入名称' }],
  type: [{ required: true, message: '请选择类型' }],
};

const submit = async () => {
  const errors = await formRef.value?.validate();
  if (errors) return; // 校验失败：保留表单与错误态，绝不关闭
  saving.value = true;
  try {
    await api.save(form);
    Message.success('保存成功');
    emit('saved');
  } catch {
    Message.error('保存失败，请重试');
  } finally {
    saving.value = false;
  }
};
</script>

<template>
  <a-form
    ref="formRef"
    :model="form"
    :rules="rules"
    :label-col-props="{ span: 6 }"
    :wrapper-col-props="{ span: 18 }"
    scroll-to-first-error
  >
    <a-row :gutter="[24, 16]">
      <a-col :xs="24" :md="12" :xl="8">
        <a-form-item field="name" label="名称" required>
          <a-input v-model="form.name" allow-clear placeholder="请输入名称" />
        </a-form-item>
      </a-col>
      <a-col :xs="24" :md="12" :xl="8">
        <a-form-item field="type" label="类型" required>
          <a-select v-model="form.type" allow-clear placeholder="请选择类型" :options="typeOptions" />
        </a-form-item>
      </a-col>
      <a-col :span="24">
        <a-form-item field="remark" label="备注" extra="最多 200 字">
          <a-textarea v-model="form.remark" :max-length="200" show-word-limit />
        </a-form-item>
      </a-col>
      <a-col :span="24">
        <div class="form-actions">
          <a-button type="primary" :loading="saving" @click="submit">保存</a-button>
          <a-button @click="emit('cancel')">取消</a-button>
        </div>
      </a-col>
    </a-row>
  </a-form>
</template>

<style scoped>
.form-actions { display: flex; gap: 12px; margin-top: 20px; }
.form-actions .arco-btn { min-width: 120px; }
</style>
```

要点：

- `validate()` 返回 `undefined` 表示通过，返回对象表示失败——**不要用 try/catch 判断**。
- `allow-clear` 默认 `false`，vibepm 要求输入/选择类显式开启。
- 错误短句优先用 FormItem 内建 `help`，不要再手写 `.field-error`（重复渲染两份）。
- 未保存保护：进入编辑即置 `dirty`，路由/弹窗/Tab 切换前用 `Modal.confirm` 拦截。

---

## 五、Modal

### 关键 Props（注意命名）

| 需求 | 正确写法 | 错误写法 |
|---|---|---|
| 面板样式 | `:modal-style="{ borderRadius: '12px', background: 'var(--color-bg-3)' }"` | `:styles` |
| 内容区样式 | `:body-style`（2.31+） | — |
| 遮罩样式 | `:mask-style` | `:maskStyle`（模板中须连字符） |
| 标题左对齐 | `title-align="start"`（默认 center） | — |
| 关闭卸载 | `unmount-on-close` | — |
| 点遮罩不关 | `:mask-closable="false"` | — |
| 异步确认 | `:on-before-ok="onBeforeOk"` | `onOk` 里做异步不 loading |

```vue
<a-modal
  v-model:visible="visible"
  title="新增记录"
  :width="560"
  title-align="start"
  :mask-closable="false"
  :modal-style="{
    borderRadius: '12px',
    background: 'var(--color-bg-3)',
    boxShadow: '0 4px 16px rgba(0,0,0,.12)',
  }"
  :mask-style="{ backgroundColor: 'var(--color-mask-bg)', backdropFilter: 'blur(12px)' }"
  :on-before-ok="onBeforeOk"
>
  <record-form @saved="visible = false" />
</a-modal>
```

```ts
// before-ok：返回 false 阻止关闭，天然实现“校验失败不关窗 + loading 防重复提交”
const onBeforeOk = async (done: (closed: boolean) => void) => {
  const ok = await formRef.value?.validate().then((e) => !e);
  done(!!ok);
};
```

**vibepm 硬规则**：面板必须实色（`--color-bg-2`），只有遮罩可以 `backdrop-filter: blur()`。`background: rgba(255,255,255,.8)` 属违规。

---

## 六、Message / Notification

```ts
import { Message, Notification } from '@arco-design/web-vue';

Message.success({ content: '保存成功', duration: 3000 });
Message.error('保存失败');
Notification.warning({ title: '待处理', content: '有 3 条审批待办' });
```

| 项 | 实情 |
|---|---|
| `position` | 只有 `'top' \| 'bottom'`，默认顶部居中；**没有** `'top-center'` |
| 常用配置 | `content`、`duration`、`closable`、`showIcon`、`icon`、`resetOnHover`（2.39+）、`onClose` |
| 清空 | `Message.clear()` |
| 样式定制 | 全局覆写 `.arco-message` 阴影与动画；时长由 `duration` 控制，动画由 CSS 控制 |
| 函数式 i18n | `Message._context = app._context` 或 `ConfigProvider global` |

vibepm 要求：顶中、双层柔影、220ms 进出。用 CSS 落地：

```css
.arco-message {
  box-shadow: 0 2px 8px rgba(0,0,0,.10), 0 4px 16px rgba(0,0,0,.08);
  animation-duration: .22s;
}
```

---

## 七、Pagination

| 需求 | 写法 |
|---|---|
| 总数 | `show-total` |
| 每页条数 | `show-page-size` + `:page-size-options="[10,20,50]"`（默认 `[10,20,30,40,50]`） |
| 跳页 | `show-jumper` |
| 改条数自动调页码 | `auto-adjust`（2.34+，默认 true） |
| 单页隐藏 | `hide-on-single-page` |

在 `a-table` 中传对象：`:pagination="{ total, current, pageSize, showTotal: true, showPageSize: true }"`。

---

## 八、vibepm 必须自研的组件

| 组件 | 原因 | 最小实现要求 |
|---|---|---|
| Metric Card（12 变体） | Arco 只有 `a-statistic` 数值 | 标题 + 数值 + 趋势/迷你图/进度；栅格 2–4 列 |
| Chart 容器 + 色板 | Arco 无图表 | 标题 + 图例 + 空态 + 自适应；色板取主题 |
| Rich Text | Arco 无富文本 | 工具栏（加粗/斜体/列表/链接）+ contenteditable |
| Filter Bar 封装 | 需要“6 列 + 折叠 + 按钮同行” | 基于 `a-grid` 封装，见 `ui-style-guide.md` |
| 上传向导 | 无对应组件 | `a-upload` + `a-steps` + 校验结果表 |

---

## 九、禁止写法（历史踩坑）

| ❌ 错误 | ✅ 正确 |
|---|---|
| `<a-button type="link">` | `<a-button type="text">` |
| `Modal.confirm({ danger: true })` | `Modal.confirm({ okButtonProps: { status: 'danger' } })` |
| `Modal.confirm({ onOk: async () => … })` | `onBeforeOk: async (done) => { …; done(true) }` |
| `message.success({ position: 'top-center' })` | `position: 'top'` |
| `pagination: { showSizeChanger: true }` | `pagination: { showPageSize: true }` |
| `:styles="{...}"` on Modal | `:modal-style="{...}"` |
| `<a-table @change="...">` 取分页 | `@page-change` / `@page-size-change` |
| `useForm()` | `ref<FormInstance>()` + `formRef.value.validate()` |
| `import { setTheme } from '@arco-design/web-vue'` | `document.body.setAttribute('arco-theme','dark')` |
| 表格外层再套 `a-pagination` | 用表格内建 `pagination` |
