<template>
  <div class="rich-text-editor">
    <!-- view 模式:只读渲染 -->
    <div v-if="disabled" class="rt-readonly" v-html="sanitizedHtml" />

    <!-- edit/create 模式:wangEditor 5 -->
    <div v-else class="editor-wrap">
      <Toolbar
        :editor="editorRef"
        :default-config="toolbarConfig"
        mode="default"
        class="editor-toolbar"
      />
      <Editor
        :default-config="editorConfig"
        :model-value="modelValue"
        :style="{ minHeight: `${props.minHeight}px` }"
        mode="default"
        class="editor-body"
        @on-created="onCreated"
        @on-change="onChange"
      />
    </div>
  </div>
</template>

<script setup>
import '@wangeditor/editor/dist/css/style.css'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import { computed, onBeforeUnmount, shallowRef } from 'vue'
import { ElMessage } from 'element-plus'
import { fileToDataUrl } from '@/utils/fileToDataUrl'

const props = defineProps({
  modelValue: { type: String, default: '' },
  disabled: { type: Boolean, default: false },
  // 编辑区起始高度(px,作为 min-height);用户可拖右下角手柄手动调高
  // case 模块默认 360;package 模块传 480 以便编辑长内容
  minHeight: { type: Number, default: 360 }
})
const emit = defineEmits(['update:modelValue'])

const editorRef = shallowRef()

const toolbarConfig = {
  toolbarKeys: [
    'undo', 'redo',
    '|',
    'bold', 'italic', 'underline',
    '|',
    'headerSelect',
    '|',
    'bulletedList', 'numberedList',
    '|',
    'insertLink',
    'uploadImage',
    '|',
    'clearStyle'
  ]
}

const editorConfig = {
  placeholder: '请输入图文详情...',
  MENU_CONF: {
    uploadImage: {
      // 不走 server 上传,自定义:File -> dataURL -> 插入
      async customUpload(file, insertFn) {
        try {
          const dataUrl = await fileToDataUrl(file, { maxSizeMB: 2, accept: ['image/jpeg', 'image/png'] })
          insertFn(dataUrl, file.name, '')
        } catch (err) {
          ElMessage.error(err.message || '图片上传失败')
        }
      }
    }
  }
}

function onCreated(editor) {
  editorRef.value = editor
}

function onChange(editor) {
  emit('update:modelValue', editor.getHtml())
}

const sanitizedHtml = computed(() => props.modelValue || '<p style="color:#909399">(无内容)</p>')

onBeforeUnmount(() => {
  if (editorRef.value) {
    editorRef.value.destroy()
    editorRef.value = null
  }
})
</script>

<style scoped>
.rich-text-editor { width: 100%; }
.editor-wrap {
  border: 1px solid var(--color-border, #dcdfe6);
  border-radius: 4px;
  overflow: hidden;
}
.editor-toolbar {
  border-bottom: 1px solid var(--color-border, #dcdfe6);
}
.editor-body {
  /* 起始高度由 props.minHeight 传入(inline min-height);用户可拖右下角手柄手动调高 */
  resize: vertical;
  overflow: auto;
}
.rt-readonly {
  border: 1px solid var(--color-border, #dcdfe6);
  border-radius: 4px;
  padding: 12px 16px;
  min-height: 100px;
  background: #fff;
  line-height: 1.7;
  color: var(--color-text-primary, #303133);
  word-break: break-word;
}
.rt-readonly :deep(img) {
  max-width: 100%;
  border-radius: 4px;
  display: block;
  margin: 8px 0;
}
.rt-readonly :deep(p) { margin: 0 0 8px 0; }
.rt-readonly :deep(h1), .rt-readonly :deep(h2), .rt-readonly :deep(h3) {
  margin: 12px 0 6px 0;
  font-weight: 600;
}
.rt-readonly :deep(ul), .rt-readonly :deep(ol) {
  padding-left: 24px;
  margin: 8px 0;
}
.rt-readonly :deep(a) { color: var(--el-color-primary); text-decoration: underline; }
</style>
