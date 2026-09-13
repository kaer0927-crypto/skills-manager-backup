<template>
  <el-form
    ref="formRef"
    :model="form"
    :rules="rules"
    :disabled="isView"
    label-width="100px"
    class="customer-form"
  >
    <!-- 顶部 banner：编辑/查看时若已删除 -->
    <el-alert
      v-if="showDeletedBanner"
      :title="`该客户已于 ${form.updatedAt} 被删除`"
      type="warning"
      :closable="false"
      show-icon
      class="deleted-banner"
    />

    <!-- 基本信息 -->
    <div class="form-group-title">基本信息</div>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="客户姓名" prop="name">
          <el-input v-model="form.name" placeholder="请输入客户姓名" maxlength="20" show-word-limit />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入 11 位手机号" maxlength="11" />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="来源" prop="source">
          <el-select v-model="form.source" placeholder="请选择来源" style="width: 100%">
            <el-option v-for="s in options.sources" :key="s" :label="options.sourceMap[s]" :value="s" />
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" placeholder="请选择状态" style="width: 100%">
            <el-option v-for="s in options.statuses" :key="s" :label="options.statusMap[s]" :value="s" />
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>

    <!-- 地址 -->
    <div class="form-group-title">地址</div>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-form-item label="省/直辖市" prop="province">
          <el-select v-model="form.province" placeholder="请选择省/直辖市" style="width: 100%">
            <el-option v-for="p in areaData" :key="p.code" :label="p.name" :value="p.code" />
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="8">
        <el-form-item label="城市" prop="city">
          <el-select v-model="form.city" placeholder="请选择城市" style="width: 100%" :disabled="!form.province">
            <el-option v-for="c in cityOptions" :key="c.code" :label="c.name" :value="c.code" />
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="8">
        <el-form-item label="区/县" prop="region">
          <el-select v-model="form.region" placeholder="请选择区/县" style="width: 100%" :disabled="!form.city">
            <el-option v-for="r in regionOptions" :key="r.code" :label="r.name" :value="r.code" />
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>

    <!-- 跟进（非 create 模式显示） -->
    <template v-if="!isCreate">
      <div class="form-group-title">跟进</div>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="跟进人">
            <el-select v-model="form.assignedTo" placeholder="未分配" clearable style="width: 100%">
              <el-option v-for="a in options.assignees" :key="a" :label="a" :value="a" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="最后跟进">
            <el-input :value="form.lastFollowedAt || '—'" disabled />
          </el-form-item>
        </el-col>
      </el-row>
    </template>

    <!-- 其他 -->
    <div class="form-group-title">其他</div>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="微信 OpenID">
          <el-input
            v-model="form.wechatOpenid"
            placeholder="手动新增可填，其他来源留空"
            :disabled="form.source !== 'manual'"
          />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="form.remark"
            type="textarea"
            :rows="3"
            placeholder="选填，200 字以内"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>
      </el-col>
    </el-row>

    <!-- view 模式展示系统字段 -->
    <template v-if="isView">
      <div class="form-group-title">系统</div>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="创建时间">{{ form.createdAt }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ form.updatedAt }}</el-descriptions-item>
      </el-descriptions>
    </template>

    <!-- 操作按钮 -->
    <div v-if="!isView" class="form-actions">
      <el-button @click="onCancel">取消</el-button>
      <el-button type="primary" :loading="submitting" @click="onSubmit">保存</el-button>
    </div>
  </el-form>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { createCustomer, updateCustomer } from '@/api/customer'
import { fetchCustomerOptions, fetchAreaDict } from '@/api/options'

const props = defineProps({
  mode: { type: String, required: true, validator: v => ['create', 'edit', 'view'].includes(v) },
  initialData: { type: Object, default: () => ({}) }
})

const emit = defineEmits(['saved'])
const router = useRouter()

const isView = computed(() => props.mode === 'view')
const isCreate = computed(() => props.mode === 'create')
const showDeletedBanner = computed(() => !isCreate.value && props.initialData?.isDeleted)

const formRef = ref(null)
const submitting = ref(false)
const areaData = ref([])

// options: { sources, statuses, assignees, sourceMap, statusMap }
const options = reactive({
  sources: [],
  statuses: [],
  assignees: [],
  sourceMap: {},
  statusMap: {}
})

// 表单数据
const emptyForm = () => ({
  name: '',
  phone: '',
  source: 'manual',
  status: 'potential',
  province: '',
  city: '',
  region: '',
  assignedTo: null,
  wechatOpenid: null,
  remark: null,
  lastFollowedAt: null,
  createdAt: '',
  updatedAt: ''
})
const form = reactive(emptyForm())

// 地址级联 options
const cityOptions = computed(() => {
  if (!form.province) return []
  return areaData.value.find(p => p.code === form.province)?.children?.[0]?.children || []
})
const regionOptions = computed(() => {
  if (!form.city) return []
  return cityOptions.value.find(c => c.code === form.city)?.children || []
})

// 切换省/市时清空下级
watch(() => form.province, () => {
  if (!isCreate.value && form.city) return // 初始化时只设置一次
  form.city = ''
  form.region = ''
})
watch(() => form.city, () => {
  if (!isCreate.value && form.region) return
  form.region = ''
})

// 校验
const rules = {
  name:     [
    { required: true, message: '请输入客户姓名', trigger: 'blur' },
    { min: 1, max: 20, message: '1-20 字', trigger: 'blur' }
  ],
  phone:    [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入 11 位有效手机号', trigger: 'blur' }
  ],
  source:   [{ required: true, message: '请选择来源', trigger: 'change' }],
  status:   [{ required: true, message: '请选择状态', trigger: 'change' }],
  province: [{ required: true, message: '请选择省/直辖市', trigger: 'change' }],
  city:     [{ required: true, message: '请选择城市', trigger: 'change' }],
  region:   [{ required: true, message: '请选择区/县', trigger: 'change' }],
  remark:   [{ max: 200, message: '备注不超过 200 字', trigger: 'blur' }]
}

// 初始化：拉 options + area；如果有 initialData，填充
async function loadInitial() {
  try {
    const [opts, area] = await Promise.all([fetchCustomerOptions(), fetchAreaDict()])
    Object.assign(options, opts)
    areaData.value = area
  } catch (err) {
    ElMessage.error('基础数据加载失败，请刷新重试')
    return
  }
  if (!isCreate.value && props.initialData && props.initialData.id) {
    Object.assign(form, props.initialData)
  }
}

onMounted(loadInitial)

async function onSubmit() {
  if (!formRef.value) return
  await formRef.value.validate()
  submitting.value = true
  try {
    const payload = {
      name: form.name,
      phone: form.phone,
      source: form.source,
      status: form.status,
      province: form.province,
      city: form.city,
      region: form.region,
      wechatOpenid: form.wechatOpenid || null,
      assignedTo: form.assignedTo || null,
      remark: form.remark || null
    }
    if (isCreate.value) {
      await createCustomer(payload)
      ElMessage.success('新增成功')
    } else {
      await updateCustomer(props.initialData.id, payload)
      ElMessage.success('保存成功')
    }
    emit('saved')
    router.push('/customer/list')
  } catch (err) {
    const msg = err?.message || ''
    ElMessage.error(msg.includes('已存在') ? msg : '保存失败')
  } finally {
    submitting.value = false
  }
}

function onCancel() {
  router.push('/customer/list')
}
</script>

<style scoped>
.customer-form {
  max-width: 960px;
}
.deleted-banner {
  margin-bottom: 16px;
}
.form-group-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 16px 0 12px;
  padding-left: 8px;
  border-left: 3px solid var(--color-primary);
}
.form-actions {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
  text-align: right;
}
</style>
