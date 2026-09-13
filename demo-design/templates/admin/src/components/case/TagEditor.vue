<template>
  <div class="tag-editor" :class="{ 'is-disabled': disabled }">
    <div class="tag-list">
      <el-tag
        v-for="(tag, idx) in modelValue"
        :key="tag"
        closable
        :disable-transitions="true"
        @close="removeAt(idx)"
      >
        {{ tag }}
      </el-tag>
      <input
        v-if="!disabled"
        ref="inputRef"
        v-model="input"
        class="tag-input"
        :maxlength="MAX_LEN"
        :placeholder="placeholder"
        :disabled="disabled || atMax"
        @keydown.enter.prevent="commit"
        @keydown.delete="onBackspace"
        @blur="commit"
      />
    </div>
    <div v-if="!disabled" class="tag-meta">
      <span>{{ modelValue.length }} / {{ MAX_ITEMS }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, ref } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: { type: Array, default: () => [] },
  disabled: { type: Boolean, default: false },
  placeholder: { type: String, default: '按回车添加标签' }
})
const emit = defineEmits(['update:modelValue'])

const MAX_ITEMS = 5
const MAX_LEN = 12

const input = ref('')
const inputRef = ref(null)

const atMax = computed(() => props.modelValue.length >= MAX_ITEMS)

function commit() {
  const raw = input.value.trim()
  if (!raw) return
  if (props.modelValue.includes(raw)) {
    ElMessage.warning(`标签「${raw}」已存在`)
    input.value = ''
    return
  }
  if (props.modelValue.length >= MAX_ITEMS) {
    ElMessage.warning(`标签最多 ${MAX_ITEMS} 个`)
    input.value = ''
    return
  }
  emit('update:modelValue', [...props.modelValue, raw])
  input.value = ''
  nextTick(() => inputRef.value?.focus())
}

function removeAt(idx) {
  if (props.disabled) return
  const next = props.modelValue.slice()
  next.splice(idx, 1)
  emit('update:modelValue', next)
}

function onBackspace() {
  if (input.value === '' && props.modelValue.length) {
    removeAt(props.modelValue.length - 1)
  }
}
</script>

<style scoped>
.tag-editor {
  width: 100%;
}
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
  min-height: 32px;
  padding: 4px 6px;
  border: 1px solid var(--el-border-color);
  border-radius: 4px;
  background: var(--el-input-bg-color, #fff);
}
.tag-list:focus-within {
  border-color: var(--el-color-primary);
}
.is-disabled .tag-list {
  background: var(--el-fill-color-light, #f5f7fa);
}
.tag-input {
  flex: 1;
  min-width: 100px;
  border: 0;
  outline: 0;
  background: transparent;
  font-size: 13px;
  padding: 2px 4px;
}
.tag-input:disabled {
  cursor: not-allowed;
}
.tag-meta {
  margin-top: 4px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
  text-align: right;
}
</style>