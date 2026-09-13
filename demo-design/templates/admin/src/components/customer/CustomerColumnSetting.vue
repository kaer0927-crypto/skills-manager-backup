<template>
  <el-dialog
    :model-value="visible"
    title="列设置"
    width="420px"
    @update:model-value="$emit('update:visible', $event)"
    @open="syncLocal"
  >
    <draggable
      v-model="localColumns"
      item-key="prop"
      :animation="150"
      handle=".drag-handle"
      class="col-list"
    >
      <template #item="{ element }">
        <div class="col-row">
          <el-icon class="drag-handle"><Rank /></el-icon>
          <el-checkbox v-model="element.visible">{{ element.label }}</el-checkbox>
          <el-checkbox v-model="element.fixed" class="fixed-check">固定左侧</el-checkbox>
        </div>
      </template>
    </draggable>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="$emit('reset-default')">恢复默认</el-button>
        <div>
          <el-button @click="$emit('update:visible', false)">取消</el-button>
          <el-button type="primary" @click="onSave">保存</el-button>
        </div>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import draggable from 'vuedraggable'
import { Rank } from '@element-plus/icons-vue'

const props = defineProps({
  visible: { type: Boolean, default: false },
  columns: { type: Array, required: true }
})
const emit = defineEmits(['update:visible', 'update:columns', 'reset-default'])

const localColumns = ref([])

function syncLocal() {
  localColumns.value = JSON.parse(JSON.stringify(props.columns))
}

watch(() => props.columns, () => { if (props.visible) syncLocal() })

function onSave() {
  emit('update:columns', localColumns.value)
  emit('update:visible', false)
}
</script>

<style scoped>
.col-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.col-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  background: #fafbfc;
  border: 1px solid var(--color-border);
  border-radius: 4px;
}
.drag-handle {
  cursor: move;
  color: var(--color-text-secondary);
  font-size: 16px;
}
.fixed-check {
  margin-left: auto;
}
.dialog-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
