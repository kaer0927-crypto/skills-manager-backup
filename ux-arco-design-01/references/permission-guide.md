# 权限降级规范（隐藏 / 禁用 / 403）

> 权限问题在 B 端/政务系统里不是「后端拦一下」，而是**界面上必须解释清楚、且不能骗人**。
> 本文定义：什么时候隐藏、什么时候禁用、什么时候整页 403。

---

## 一、三态决策（按顺序判定）

| 场景 | 处理 | 理由 |
|---|---|---|
| 用户角色**永远**不会用到该功能 | **隐藏** | 展示一堆永远点不动的按钮，只会增加噪音 |
| 用户角色能用，但**当前对象状态/数据范围**不允许 | **禁用 + 原因** | 用户需要知道「不是我权限不够，是这单不能改」 |
| 用户有入口权限，但**整页数据都无权限** | **403 结果页** | 让用户明确知道是权限问题，而不是「系统坏了/没数据」 |
| 直接访问无权 URL / 深链 | **403**，不要静默跳首页 | 静默跳转会让人以为是链接失效 |

判定顺序：先看「这个角色有没有该功能」→ 再看「当前这条数据允许吗」→ 最后看「整页是否可访问」。

---

## 二、按钮级权限

### 1. 指令式（小项目够用）

```ts
// directives/permission.ts
import type { Directive } from 'vue';
import { useUserStore } from '@/store/user';

export const permission: Directive<HTMLElement, string[]> = {
  mounted(el, binding) {
    const store = useUserStore();
    const need = binding.value ?? [];
    if (need.length && !need.some((p) => store.permissions.includes(p))) {
      el.parentNode?.removeChild(el);
    }
  },
};
```

```vue
<a-button v-permission="['order:delete']" status="danger">删除</a-button>
```

### 2. 组件式（推荐，能同时拿到 disabled 与原因）

```vue
<script setup lang="ts">
const { allowed, reason } = useAction('order:delete'); // 内部 = 权限 ∩ 状态
</script>

<template>
  <a-tooltip :content="reason" :disabled="allowed">
    <span><a-button status="danger" :disabled="!allowed">删除</a-button></span>
  </a-tooltip>
</template>
```

> 关键：**动作可用性 = 权限允许 ∩ 状态允许**（见 `state-machine.md`）。两者都通过才可点，原因要能区分「无权限」和「当前状态不允许」。

---

## 三、页面级权限

| 情况 | 表现 |
|---|---|
| 菜单无权限 | 菜单项不渲染（不是灰掉），避免用户反复点击 |
| 菜单有权限、数据全无 | 正常进入页面，展示「无数据权限」空态 + 申请入口 |
| 整页功能无权限（如无「系统设置」角色） | `a-result status="403"`，文案说明缺什么角色、找谁申请 |
| URL 直接访问无权页 | 403，路由守卫里判断，不要 `router.replace('/')` |

```vue
<a-result status="403" title="无访问权限" subtitle="当前账号缺少「系统管理员」角色，请联系管理员开通。">
  <template #extra>
    <a-button type="primary" @click="router.push('/')">返回首页</a-button>
    <a-button @click="copyAdminContact">联系管理员</a-button>
  </template>
</a-result>
```

---

## 四、数据权限（行级）

- 数据范围（本人 / 本部门 / 本部门及下级 / 全部）必须由后端过滤，前端**不要**用「拿到全量再 filter」假装做了权限。
- 前端可以做的：把「当前数据范围」显示出来（如筛选区上方一句「数据范围：本部门及下级」），避免用户误以为数据缺失。
- 跨范围导出必须走 `data-security.md` 的导出确认。

---

## 五、字段级权限

三种表现，按敏感度选：

| 表现 | 用法 |
|---|---|
| 不渲染该列/该项 | 该字段对该角色完全无意义 |
| 脱敏显示（`138****1234`） | 需要看到「有值」但不能看全，见 `data-security.md` |
| 只读展示（无编辑控件） | 可看不可改，标签旁加锁图标 + tooltip「无编辑权限」 |

禁止：字段无权限时显示空白或 `--`（用户会以为是数据缺失）。

---

## 六、自查清单

1. 每个受限功能都明确落在「隐藏 / 禁用+原因 / 403」三态之一？
2. 禁用原因能区分「无权限」和「状态不允许」？
3. 无权限菜单是否不渲染，而不是灰掉？
4. 直接访问无权 URL 是否给 403，而不是跳首页？
5. 403 页面是否写清缺什么角色、怎么申请？
6. 行级数据范围是否由后端过滤，前端只做展示说明？
7. 字段无权限时是否有明确表现（不渲染/脱敏/只读），而不是空白？
