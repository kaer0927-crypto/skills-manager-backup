# 反馈模式：空态 / 部分成功 / 长任务 / 并发冲突

> 这四类场景是「原型感」和「产品感」的分水岭：组件都对，但反馈没设计，用户就会卡住。
> 与 `crud-guide.md`（增删改查）、`components-guide.md`（组件用法）配合使用。

---

## 一、空态必须分四类（不要一律「暂无数据」）

| 类型 | 触发 | 文案骨架 | 主操作 |
|---|---|---|---|
| 首次空（还没数据） | 新建系统/新模块，从未创建 | 「还没有<对象>」+ 一句能带来什么价值 | **新建**（primary） |
| 无结果空（筛掉了） | 有条件但命中 0 条 | 「没有符合条件的结果」+ 显示已生效条件数 | **清除筛选**（secondary） |
| 无权限空 | 有页面权限、无数据范围 | 「暂无数据权限」+ 说明数据范围 | **申请权限 / 联系管理员** |
| 出错空 | 请求失败 | 「加载失败」+ 简短原因（不暴露堆栈） | **重试**（primary） |

```vue
<a-empty v-if="state === 'first'">
  <template #description>还没有制度文件，创建后可在此统一维护</template>
  <a-button type="primary" @click="openCreate">新建制度</a-button>
</a-empty>

<a-empty v-else-if="state === 'no-result'">
  <template #description>没有符合条件的结果（已应用 3 个筛选条件）</template>
  <a-button @click="resetFilters">清除筛选</a-button>
</a-empty>

<a-empty v-else-if="state === 'no-permission'">
  <template #description>当前账号暂无数据查看权限（数据范围：本部门）</template>
  <a-button @click="applyPermission">申请权限</a-button>
</a-empty>

<a-result v-else status="error" title="加载失败" subtitle="网络异常，请稍后重试">
  <template #extra><a-button type="primary" @click="reload">重试</a-button></template>
</a-result>
```

规则：

- 空态**必须有且只有一个主操作**；「暂无数据」四个字不算设计。
- 无结果空态要告诉用户「是筛掉了」，否则会被当成系统没数据。
- 出错空态与「无数据」必须视觉可区分（图标 + 文案 + 重试）。
- 表格空态用 `#empty` 插槽，图表空态用覆盖层（见 `chart-theme.md`）。

---

## 二、批量操作：必须处理「部分成功」

一次批量操作 N 条，现实里经常是「成功 N-M，失败 M」。只弹「操作成功」是错误反馈。

| 结果 | 反馈 |
|---|---|
| 全部成功 | Toast「已删除 5 条」+ 重查列表 |
| 全部失败 | 错误 Toast + 失败原因摘要（不要只写「操作失败」） |
| 部分成功 | **结果弹窗**：成功数 / 失败数 / 失败原因列表（可下载 CSV）+ 列表保留失败行高亮 |

```vue
<a-modal v-model:visible="resultVisible" title="批量作废结果" :footer="false">
  <a-alert type="warning" v-if="result.failed.length">
    成功 {{ result.success }} 条，失败 {{ result.failed.length }} 条
  </a-alert>
  <a-table :data="result.failed" :pagination="false" size="small">
    <template #columns>
      <a-table-column title="编号" data-index="code" />
      <a-table-column title="失败原因" data-index="reason" />
    </template>
  </a-table>
  <div class="modal-actions">
    <a-button @click="downloadFailed">下载失败清单</a-button>
    <a-button type="primary" @click="retryFailed">重试失败项</a-button>
  </div>
</a-modal>
```

- 失败清单至少包含：业务编号、失败原因（后端返回的可读文案）、可定位信息。
- 「重试失败项」只重发失败的那部分，不要整批重来。
- 批量前若会跳过部分行，必须在确认弹窗里写明「将跳过 2 条（已作废）」。

---

## 三、长任务：按耗时选反馈形态

| 耗时 | 形态 |
|---|---|
| < 1s | 按钮 loading + 成功 Toast |
| 1–3s | 按钮 loading + 列表局部 loading，禁止整页白屏 |
| > 3s 或不可预估 | **任务中心**：立即返回任务 ID，Toast「已提交，可在任务中心查看进度」 |
| > 30s | 任务中心 + 完成通知（站内信/Notification）+ 失败可重试 |

任务中心条目结构：

```
任务名称 | 类型（导入/导出/批量） | 创建时间 | 进度（x/y 或 %） | 状态 | 操作（查看结果/下载/重试/取消）
```

- 进度不要假进度条（`setInterval` 涨到 99% 再卡住），只展示后端真实进度或不确定态（`indeterminate`）。
- 导出类任务完成后给下载链接并标有效期。
- 离开页面任务不中断，回来后从任务中心恢复查看。

---

## 四、并发冲突：别人已经改过了

场景：用户 A 打开编辑弹窗，用户 B 已保存，A 再提交 → 不能静默覆盖。

| 方案 | 做法 |
|---|---|
| 乐观锁（推荐） | 打开时带 `version`/`updatedAt`，提交时回传；后端版本不一致返回 409 |
| 冲突时 UI | 弹窗：「该记录已被 张三 于 14:32 修改」+ 三选项：查看最新 / 对比差异 / 用我的覆盖（高危，需权限） |
| 表单未保存保护 | 见 `forms-guide.md`「未保存编辑保护」 |

```ts
// 409 处理
if (err.code === 409) {
  Modal.confirm({
    title: '内容已被他人修改',
    content: `${err.data.operator} 于 ${err.data.time} 修改了这条记录，请选择处理方式。`,
    okText: '查看最新',
    cancelText: '保留我的编辑',
  });
}
```

其他一致性细节：

- 提交按钮必须有 loading 与防重（幂等键由后端生成或前端传 `requestId`）。
- 保存成功后重查列表，不要只改本地数组。
- 多处入口修改同一数据时，详情页要能手动刷新（`icon-refresh`）。

---

## 五、自查清单

1. 空态是否区分了首次 / 无结果 / 无权限 / 出错，且各自有主操作？
2. 批量操作是否处理了部分成功（成功数/失败数/原因/重试）？
3. 超过 3 秒的任务是否有任务中心与完成通知，而不是一个长 loading？
4. 进度条是否来自真实进度，没有假动画？
5. 编辑提交是否处理 409 并发冲突，且不静默覆盖？
6. 写操作是否有防重复提交（loading + 幂等）？
