import { menuData } from './menu'
import customerEndpoints from './customer'
import caseEndpoints from './case'

/**
 * 单一来源:dev 给 viteMockServe 扫描,prod 给 inlineMockAdapter import
 * 注意: dev 期 viteMockServe 只用 default export;prod 期 main.js / request.js 只用 named
 *       两者指向同一数组,数据零分叉
 */
export const mockEndpoints = [
  {
    url: '/api/menu',
    method: 'get',
    response: () => {
      return {
        code: 0,
        data: menuData,
        message: 'ok'
      }
    }
  },
  {
    url: '/api/dashboard',
    method: 'get',
    response: () => ({
      code: 0,
      data: {
        kpis: [
          { key: 'customerTotal', label: '客户总数', value: '128', sub: '活跃 96 家', icon: 'UserFilled', accent: 'primary' },
          { key: 'caseTotal', label: '案例数', value: '10', sub: '本月新增 3', icon: 'Document', accent: 'warning' },
          { key: 'todoApproval', label: '待办审批', value: '3', sub: '2 项需我处理', icon: 'Bell', accent: 'danger' }
        ]
      },
      message: 'ok'
    })
  },
  {
    url: '/api/quick-actions',
    method: 'get',
    response: () => ({
      code: 0,
      data: [
        { id: 1, title: '案例管理', path: '/case/list' },
        { id: 2, title: '客户列表', path: '/customer/list' }
      ],
      message: 'ok'
    })
  },
  // === 客户管理（7 个端点） ===
  ...customerEndpoints,
  // === 案例管理（6 个端点） ===
  ...caseEndpoints
]

// 保留 default export(viteMockServe 默认扫描 ./index 的 default,行为不变)
export default mockEndpoints