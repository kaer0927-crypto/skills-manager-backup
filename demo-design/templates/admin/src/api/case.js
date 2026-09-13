import request from './request'

/**
 * 获取案例列表(分页 + 过滤)
 * @param {Object} params - { page, pageSize, name?, enabled? }
 *   - name: 字符串模糊搜索
 *   - enabled: 'true' | 'false' | undefined(undefined 视为不过滤)
 * @returns {Promise<{ list: Array, total: number, page: number, pageSize: number }>}
 */
export function fetchCaseList(params = {}) {
  return request.get('/case', { params })
}

/**
 * 获取案例详情
 * @param {number|string} id
 * @returns {Promise<Object>}
 */
export function fetchCaseDetail(id) {
  return request.get(`/case/${id}`)
}

/**
 * 新增案例
 * @param {Object} body - { cover, name, tags, description, content, sort?, enabled? }
 */
export function createCase(body) {
  return request.post('/case', body)
}

/**
 * 编辑案例
 * @param {number|string} id
 * @param {Object} body
 */
export function updateCase(id, body) {
  return request.put(`/case/${id}`, body)
}

/**
 * 软删除案例
 * @param {number|string} id
 */
export function deleteCase(id) {
  return request.delete(`/case/${id}`)
}
