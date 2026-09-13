<template>
  <el-form
    ref="formRef"
    :model="form"
    :rules="rules"
    :disabled="isView"
    label-width="100px"
    class="case-form"
  >
    <!-- 顶部 banner:编辑/查看时若已删除 -->
    <el-alert
      v-if="showDeletedBanner"
      :title="`该案例已于 ${form.updatedAt} 被删除`"
      type="warning"
      :closable="false"
      show-icon
      class="deleted-banner"
    />

    <!-- 分组 1:基本信息 -->
    <div class="form-group-title">基本信息</div>
    <el-row :gutter="20">
      <el-col :span="24">
        <el-form-item label="主图" prop="cover">
          <MainImageUploader v-model="form.cover" :disabled="isView" />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入案例名称" maxlength="50" show-word-limit />
        </el-form-item>
      </el-col>
    </el-row>

    <!-- 分组 2:标签 -->
    <div class="form-group-title">标签</div>
    <el-row :gutter="20">
      <el-col :span="24">
        <el-form-item label="标签" prop="tags">
          <TagEditor v-model="form.tags" :disabled="isView" />
        </el-form-item>
      </el-col>
    </el-row>

    <!-- 分组 3:介绍 -->
    <div class="form-group-title">介绍</div>
    <el-row :gutter="20">
      <el-col :span="24">
        <el-form-item label="介绍" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            maxlength="100"
            show-word-limit
            placeholder="请输入案例介绍,不超过 100 字"
          />
        </el-form-item>
      </el-col>
    </el-row>

    <!-- 分组 4:图文详情 -->
    <div class="form-group-title">图文详情</div>
    <el-form-item prop="content" label-width="0">
      <RichTextEditor v-model="form.content" :disabled="isView" />
    </el-form-item>

    <!-- 分组 5:配置 -->
    <div class="form-group-title">配置</div>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="排序" prop="sort">
          <el-input-number v-model="form.sort" :min="0" :max="9999" controls-position="right" style="width: 100%" />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="启用" prop="enabled">
          <el-switch v-model="form.enabled" active-text="启用" inactive-text="禁用" />
        </el-form-item>
      </el-col>
    </el-row>

    <!-- 系统字段:edit + view 模式显示 -->
    <template v-if="!isCreate">
      <div class="form-group-title">系统信息</div>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="创建时间">
            <span>{{ form.createdAt || '—' }}</span>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="更新时间">
            <span>{{ form.updatedAt || '—' }}</span>
          </el-form-item>
        </el-col>
      </el-row>
    </template>

    <!-- 提交按钮:仅 create/edit 显示 -->
    <div v-if="!isView" class="form-actions">
      <el-button type="primary" :loading="submitting" @click="onSubmit">保存</el-button>
      <el-button @click="$router.back()">取消</el-button>
    </div>
  </el-form>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { createCase, updateCase } from '@/api/case'
import MainImageUploader from '@/components/case/MainImageUploader.vue'
import RichTextEditor from '@/components/case/RichTextEditor.vue'
import TagEditor from '@/components/case/TagEditor.vue'

const props = defineProps({
  mode: { type: String, required: true, validator: v => ['create', 'edit', 'view'].includes(v) },
  initialData: { type: Object, default: () => ({}) }
})
const emit = defineEmits(['saved'])

const isView = computed(() => props.mode === 'view')
const isCreate = computed(() => props.mode === 'create')
const showDeletedBanner = computed(() =>
  (props.mode === 'view' || props.mode === 'edit') && props.initialData?.isDeleted === true
)

const defaultForm = () => ({
  cover: '',
  name: '',
  tags: [],
  description: '',
  content: '',
  sort: 0,
  enabled: true
})

const form = ref(defaultForm())
const formRef = ref(null)
const submitting = ref(false)
const router = useRouter()

watch(
  () => props.initialData,
  (v) => { if (v && Object.keys(v).length) form.value = { ...defaultForm(), ...v } },
  { immediate: true }
)

// 校验:content 去标签后非空
function isContentEmpty(html) {
  if (typeof html !== 'string') return true
  return html.replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').trim().length === 0
}

const rules = {
  cover: [
    { required: true, message: '请上传主图', trigger: 'change' }
  ],
  name: [
    { required: true, message: '请输入名称', trigger: 'blur' },
    { min: 1, max: 50, message: '1-50 字', trigger: 'blur' }
  ],
  tags: [
    {
      validator: (rule, value, cb) => {
        if (!Array.isArray(value) || value.length === 0) return cb(new Error('请至少添加 1 个标签'))
        if (value.length > 5) return cb(new Error('最多 5 个标签'))
        if (value.some(t => !t || !t.trim() || t.length > 10)) {
          return cb(new Error('单个标签 1-10 字'))
        }
        cb()
      },
      trigger: 'change'
    }
  ],
  description: [
    { required: true, message: '请输入介绍', trigger: 'blur' },
    { max: 100, message: '介绍不超过 100 字', trigger: 'blur' }
  ],
  content: [
    {
      validator: (rule, value, cb) => {
        if (isContentEmpty(value)) return cb(new Error('请填写图文详情'))
        cb()
      },
      trigger: 'change'
    }
  ],
  sort: [
    { required: true, message: '请输入排序值', trigger: 'change' },
    { type: 'number', message: '排序值必须为数字', trigger: 'change' }
  ]
}

async function onSubmit() {
  await formRef.value.validate()
  submitting.value = true
  try {
    const payload = { ...form.value }
    payload.tags = Array.from(new Set((payload.tags || []).map(t => (t || '').trim()).filter(Boolean)))
    if (props.mode === 'create') {
      await createCase(payload)
      ElMessage.success('新增成功')
    } else {
      await updateCase(props.initialData.id, payload)
      ElMessage.success('保存成功')
    }
    emit('saved')
    router.push('/case/list')
  } catch (err) {
    const msg = err?.message || ''
    ElMessage.error(msg || '保存失败')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.case-form { max-width: 100%; }
.deleted-banner { margin-bottom: 16px; }
.form-group-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary, #303133);
  margin: 16px 0 12px 0;
  padding-left: 8px;
  border-left: 3px solid var(--el-color-primary);
}
.form-group-title:first-of-type { margin-top: 0; }
.form-actions { margin-top: 20px; }
</style>
