import request from './request'

/**
 * 获取菜单
 * @returns {Promise<Array>} 菜单树
 */
export function fetchMenu() {
  return request.get('/menu')
}
