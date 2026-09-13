import { generateSeed } from './customerSeed'
import {
  SOURCE_MAP,
  STATUS_MAP,
  STATUS_TAG_TYPE,
  ASSIGNEE_OPTIONS,
  AREA_DATA,
  DEFAULT_COLUMNS
} from './customerOptions'

// 模块级 export let，CRUD 操作在内存中改；重启 vite 恢复
export let customers = generateSeed()
export let nextId = Math.max(0, ...customers.map(c => c.id)) + 1

function pad(n) { return String(n).padStart(2, '0') }
function formatNow() {
  const d = new Date()
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
}

export default [
  // 列表
  {
    url: '/api/customer',
    method: 'get',
    response: ({ query }) => {
      let list = customers.filter(c => !c.isDeleted)
      if (query.name)        list = list.filter(c => c.name.includes(query.name))
      if (query.phone)       list = list.filter(c => c.phone.includes(query.phone))
      if (query.source)      list = list.filter(c => c.source === query.source)
      if (query.status)      list = list.filter(c => c.status === query.status)
      if (query.city)        list = list.filter(c => c.city === query.city)
      if (query.region)      list = list.filter(c => c.region === query.region)
      if (query.assignedTo)  list = list.filter(c => c.assignedTo === query.assignedTo)
      if (query.createdAtStart) list = list.filter(c => c.createdAt >= query.createdAtStart)
      if (query.createdAtEnd)   list = list.filter(c => c.createdAt <= query.createdAtEnd)
      const page = Number(query.page) || 1
      const pageSize = Number(query.pageSize) || 20
      const start = (page - 1) * pageSize
      return {
        code: 0,
        data: {
          list: list.slice(start, start + pageSize),
          total: list.length,
          page,
          pageSize
        },
        message: 'ok'
      }
    }
  },
  // options — 必须排在 /api/customer/:id 之前：path-to-regexp 把 :id 匹配到 'options'
  {
    url: '/api/customer/options',
    method: 'get',
    response: () => ({
      code: 0,
      data: {
        sources: Object.keys(SOURCE_MAP),
        statuses: Object.keys(STATUS_MAP),
        assignees: ASSIGNEE_OPTIONS,
        sourceMap: SOURCE_MAP,
        statusMap: STATUS_MAP,
        statusTagType: STATUS_TAG_TYPE,
        columns: DEFAULT_COLUMNS
      },
      message: 'ok'
    })
  },
  // 详情
  {
    url: '/api/customer/:id',
    method: 'get',
    response: ({ query }) => {
      const c = customers.find(c => c.id === Number(query.id))
      if (!c) return { code: 404, data: null, message: '客户不存在' }
      return { code: 0, data: c, message: 'ok' }
    }
  },
  // 新增
  {
    url: '/api/customer',
    method: 'post',
    response: ({ body }) => {
      if (!body.phone) {
        return { code: 1002, data: null, message: '手机号必填' }
      }
      if (customers.some(c => !c.isDeleted && c.phone === body.phone)) {
        return { code: 1001, data: null, message: '该手机号已存在' }
      }
      const now = formatNow()
      // 排除服务端字段，body 任何尝试覆盖都不会生效
      const allowed = { ...body }
      delete allowed.id
      delete allowed.isDeleted
      delete allowed.createdAt
      delete allowed.updatedAt
      delete allowed.lastFollowedAt
      const created = {
        id: nextId++,
        isDeleted: false,
        lastFollowedAt: null,
        createdAt: now,
        updatedAt: now,
        wechatOpenid: null,
        remark: null,
        assignedTo: null,
        ...allowed
      }
      customers.push(created)
      return { code: 0, data: created, message: 'ok' }
    }
  },
  // 编辑
  {
    url: '/api/customer/:id',
    method: 'put',
    response: ({ query, body }) => {
      const idx = customers.findIndex(c => c.id === Number(query.id))
      if (idx === -1) return { code: 404, data: null, message: '客户不存在' }
      if (body.phone && customers.some(c => c.id !== Number(query.id) && !c.isDeleted && c.phone === body.phone)) {
        return { code: 1001, data: null, message: '该手机号已存在' }
      }
      // 保护 id/isDeleted/createdAt 不被 body 覆盖
      const allowed = { ...body }
      delete allowed.id
      delete allowed.isDeleted
      delete allowed.createdAt
      customers[idx] = { ...customers[idx], ...allowed, updatedAt: formatNow() }
      return { code: 0, data: customers[idx], message: 'ok' }
    }
  },
  // 软删除
  {
    url: '/api/customer/:id',
    method: 'delete',
    response: ({ query }) => {
      const idx = customers.findIndex(c => c.id === Number(query.id))
      if (idx === -1) return { code: 404, data: null, message: '客户不存在' }
      customers[idx].isDeleted = true
      customers[idx].updatedAt = formatNow()
      return { code: 0, data: { id: customers[idx].id }, message: 'ok' }
    }
  },
  // 区域字典
  {
    url: '/api/dict/area',
    method: 'get',
    response: () => ({ code: 0, data: AREA_DATA, message: 'ok' })
  }
]
