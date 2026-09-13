import { generateSeed } from './caseSeed'

let records = generateSeed()
let nextId = Math.max(0, ...records.map(r => r.id)) + 1

// === 校验工具 ===

// 校验 tags:1-5 项,每项 trim 后 1-10 字
function validateTags(tags) {
  if (!Array.isArray(tags)) return '标签必须是数组'
  if (tags.length < 1 || tags.length > 5) return '标签数量需 1-5 个'
  for (const t of tags) {
    if (typeof t !== 'string' || !t.trim() || t.length > 10) {
      return '单个标签 1-10 字'
    }
  }
  return null
}

// tags 归一化:trim + 去重
function normalizeTags(tags) {
  if (!Array.isArray(tags)) return []
  return Array.from(new Set(tags.map(t => (t || '').trim()).filter(Boolean)))
}

// 校验 content:HTML 去标签后非全空白
function isContentEmpty(html) {
  if (typeof html !== 'string') return true
  return html.replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').trim().length === 0
}

function pad(n) { return String(n).padStart(2, '0') }
function formatNow() {
  const d = new Date()
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
}

export default [
  // === 列表 ===
  {
    url: '/api/case',
    method: 'get',
    response: ({ query }) => {
      let list = records.filter(r => !r.isDeleted)
      if (query.name) list = list.filter(r => r.name.includes(query.name))
      if (query.enabled !== undefined && query.enabled !== '') {
        list = list.filter(r => r.enabled === (query.enabled === 'true'))
      }
      // 排序:sort ASC, createdAt DESC
      list.sort((a, b) => a.sort - b.sort || (a.createdAt < b.createdAt ? 1 : -1))
      const page = Number(query.page) || 1
      const pageSize = Number(query.pageSize) || 20
      const start = (page - 1) * pageSize
      return {
        code: 0,
        data: { list: list.slice(start, start + pageSize), total: list.length, page, pageSize },
        message: 'ok'
      }
    }
  },
  // === options ===(字面量子路径必须排在 :id 之前)
  {
    url: '/api/case/options',
    method: 'get',
    response: () => ({
      code: 0,
      data: {
        enabledOptions: [
          { value: true, label: '启用' },
          { value: false, label: '禁用' }
        ]
      },
      message: 'ok'
    })
  },
  // === 详情 ===
  {
    url: '/api/case/:id',
    method: 'get',
    response: ({ query }) => {
      const r = records.find(r => r.id === Number(query.id))
      if (!r) return { code: 404, data: null, message: '案例不存在' }
      return { code: 0, data: r, message: 'ok' }
    }
  },
  // === 新增 ===
  {
    url: '/api/case',
    method: 'post',
    response: ({ body }) => {
      if (!body.cover || typeof body.cover !== 'string' || !body.cover.trim()) {
        return { code: 1003, data: null, message: '请上传主图' }
      }
      if (!body.name || typeof body.name !== 'string' || !body.name.trim()) {
        return { code: 1002, data: null, message: '请输入名称' }
      }
      if (body.name.length > 50) {
        return { code: 1002, data: null, message: '名称需 1-50 字' }
      }
      const tagsErr = validateTags(body.tags)
      if (tagsErr) return { code: 1005, data: null, message: tagsErr }
      if (!body.description || typeof body.description !== 'string' || !body.description.trim()) {
        return { code: 1006, data: null, message: '请输入介绍' }
      }
      if (body.description.length > 100) {
        return { code: 1006, data: null, message: '介绍不超过 100 字' }
      }
      if (isContentEmpty(body.content)) {
        return { code: 1004, data: null, message: '请填写图文详情' }
      }
      if (records.some(r => !r.isDeleted && r.name === body.name)) {
        return { code: 1001, data: null, message: '该案例名称已存在' }
      }
      const now = formatNow()
      const id = nextId++
      const allowed = { ...body }
      delete allowed.id
      delete allowed.isDeleted
      delete allowed.createdAt
      delete allowed.updatedAt
      const created = {
        sort: 0,
        enabled: true,
        ...allowed,
        id,
        tags: normalizeTags(body.tags),
        isDeleted: false,
        createdAt: now,
        updatedAt: now
      }
      records.push(created)
      return { code: 0, data: created, message: 'ok' }
    }
  },
  // === 编辑 ===
  {
    url: '/api/case/:id',
    method: 'put',
    response: ({ query, body }) => {
      const idx = records.findIndex(r => r.id === Number(query.id))
      if (idx === -1) return { code: 404, data: null, message: '案例不存在' }
      if (body.cover !== undefined && (!body.cover || !body.cover.trim())) {
        return { code: 1003, data: null, message: '请上传主图' }
      }
      if (body.name !== undefined) {
        if (!body.name || !body.name.trim()) {
          return { code: 1002, data: null, message: '请输入名称' }
        }
        if (body.name.length > 50) {
          return { code: 1002, data: null, message: '名称需 1-50 字' }
        }
        if (records.some(r => r.id !== Number(query.id) && !r.isDeleted && r.name === body.name)) {
          return { code: 1001, data: null, message: '该案例名称已存在' }
        }
      }
      if (body.tags !== undefined) {
        const tagsErr = validateTags(body.tags)
        if (tagsErr) return { code: 1005, data: null, message: tagsErr }
      }
      if (body.description !== undefined) {
        if (!body.description || !body.description.trim()) {
          return { code: 1006, data: null, message: '请输入介绍' }
        }
        if (body.description.length > 100) {
          return { code: 1006, data: null, message: '介绍不超过 100 字' }
        }
      }
      if (body.content !== undefined && isContentEmpty(body.content)) {
        return { code: 1004, data: null, message: '请填写图文详情' }
      }
      const allowed = { ...body }
      delete allowed.id
      delete allowed.isDeleted
      delete allowed.createdAt
      const update = { ...allowed, updatedAt: formatNow() }
      if (body.tags !== undefined) update.tags = normalizeTags(body.tags)
      records[idx] = { ...records[idx], ...update }
      return { code: 0, data: records[idx], message: 'ok' }
    }
  },
  // === 软删除 ===
  {
    url: '/api/case/:id',
    method: 'delete',
    response: ({ query }) => {
      const idx = records.findIndex(r => r.id === Number(query.id))
      if (idx === -1) return { code: 404, data: null, message: '案例不存在' }
      records[idx].isDeleted = true
      records[idx].updatedAt = formatNow()
      return { code: 0, data: { id: records[idx].id }, message: 'ok' }
    }
  }
]
