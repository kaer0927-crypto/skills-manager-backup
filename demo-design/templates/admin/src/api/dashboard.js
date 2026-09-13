import request from './request'

/**
 * 获取首页看板 KPI
 * @returns {Promise<{ kpis: KpiEntry[] }>}
 */
export function fetchDashboard() {
  return request.get('/dashboard')
}

/**
 * 获取常用功能入口
 * @returns {Promise<QuickAction[]>}
 */
export function fetchQuickActions() {
  return request.get('/quick-actions')
}
