import request from './request'

/**
 * 获取客户表单所需的 options（来源/状态/跟进人/默认列设置/中文映射）
 * @returns {Promise<{ sources, statuses, assignees, sourceMap, statusMap, statusTagType, columns }>}
 */
export function fetchCustomerOptions() {
  return request.get('/customer/options')
}

/**
 * 获取省/市/区三级字典
 * @returns {Promise<Array>}
 */
export function fetchAreaDict() {
  return request.get('/dict/area')
}
