import request from './request'

/**
 * 获取客户列表（分页 + 过滤）
 * @param {Object} params - { page, pageSize, name?, phone?, source?, status?, city?, region?, assignedTo?, createdAtStart?, createdAtEnd? }
 * @returns {Promise<{ list: Array, total: number, page: number, pageSize: number }>}
 */
export function fetchCustomerList(params = {}) {
  return request.get('/customer', { params })
}

/**
 * 获取客户详情
 * @param {number} id
 * @returns {Promise<Object>}
 */
export function fetchCustomerDetail(id) {
  return request.get(`/customer/${id}`)
}

/**
 * 新增客户
 * @param {Object} body - { name, phone, source, province, city, region, status, wechatOpenid?, assignedTo?, remark? }
 */
export function createCustomer(body) {
  return request.post('/customer', body)
}

/**
 * 编辑客户
 * @param {number} id
 * @param {Object} body
 */
export function updateCustomer(id, body) {
  return request.put(`/customer/${id}`, body)
}

/**
 * 软删除客户
 * @param {number} id
 */
export function deleteCustomer(id) {
  return request.delete(`/customer/${id}`)
}
