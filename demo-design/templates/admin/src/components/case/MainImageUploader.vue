<template>
  <div class="main-image-uploader">
    <div v-if="modelValue" class="img-box">
      <img :src="modelValue" class="thumb" alt="主图" />
      <div v-if="!disabled" class="overlay">
        <label class="action">
          <input
            type="file"
            accept="image/jpeg,image/png"
            hidden
            @change="onFile"
          />
          更换
        </label>
        <button class="action danger" type="button" @click="remove">删除</button>
      </div>
    </div>
    <label
      v-else-if="!disabled"
      class="upload-box"
    >
      <input
        type="file"
        accept="image/jpeg,image/png"
        hidden
        @change="onFile"
      />
      <el-icon :size="24"><Plus /></el-icon>
      <span>上传主图</span>
    </label>
    <div v-else class="upload-box upload-box-empty">
      <span>—</span>
    </div>
    <div class="hint">JPEG / PNG,≤ 2MB,推荐 16:9</div>
  </div>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { fileToDataUrl } from '@/utils/fileToDataUrl'

defineProps({
  modelValue: { type: String, default: '' },
  disabled: { type: Boolean, default: false }
})
const emit = defineEmits(['update:modelValue'])

async function onFile(e) {
  const file = e.target.files?.[0]
  e.target.value = ''
  if (!file) return
  try {
    const dataUrl = await fileToDataUrl(file, { maxSizeMB: 2, accept: ['image/jpeg', 'image/png'] })
    emit('update:modelValue', dataUrl)
  } catch (err) {
    ElMessage.error(err.message || '上传失败')
  }
}

function remove() {
  emit('update:modelValue', '')
}
</script>

<style scoped>
.main-image-uploader { width: 100%; }
.img-box {
  position: relative;
  width: 240px;
  height: 160px;
  border: 1px solid var(--color-border, #dcdfe6);
  border-radius: 6px;
  overflow: hidden;
  background: #fff;
}
.thumb { width: 100%; height: 100%; object-fit: cover; display: block; }
.overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  opacity: 0;
  transition: opacity 0.2s;
}
.img-box:hover .overlay { opacity: 1; }
.action {
  background: rgba(255, 255, 255, 0.92);
  color: var(--color-text-primary, #303133);
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  border: none;
  line-height: 1.6;
}
.action.danger { color: var(--el-color-danger); }
.action:hover { background: #fff; }

.upload-box {
  border: 2px dashed var(--color-border, #dcdfe6);
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 240px;
  height: 160px;
  color: var(--color-text-secondary, #909399);
  cursor: pointer;
  transition: border-color 0.2s, color 0.2s;
  gap: 6px;
  font-size: 13px;
}
.upload-box:hover {
  border-color: var(--el-color-primary);
  color: var(--el-color-primary);
}
.upload-box-empty {
  cursor: default;
  background: var(--el-fill-color-light, #f5f7fa);
}
.upload-box-empty:hover {
  border-color: var(--color-border, #dcdfe6);
  color: var(--color-text-secondary, #909399);
}
.hint {
  margin-top: 8px;
  font-size: 12px;
  color: var(--color-text-secondary, #909399);
}
</style>
