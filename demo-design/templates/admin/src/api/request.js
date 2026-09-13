// src/api/request.js

import axios from 'axios'
import { installInlineMock } from '@/utils/inlineMockAdapter'
import { resolveApiMode } from '@/utils/apiMode'

const request = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' }
})

// 响应拦截器：统一处理 { code, data, message } 格式
request.interceptors.response.use(
  (response) => {
    const res = response.data
    if (res && typeof res === 'object' && 'code' in res) {
      if (res.code === 0) {
        return res.data
      }
      return Promise.reject(new Error(res.message || `业务错误 code=${res.code}`))
    }
    return res
  },
  (error) => {
    console.error('[request error]', error)
    return Promise.reject(error)
  }
)

// 生产模式 + mock 启用 → 挂 inline adapter（拦截在 axios 层，请求不进网络）
// dev 模式继续走 vite-plugin-mock（HTTP 层拦截），不动
if (import.meta.env.PROD) {
  const mode = resolveApiMode()
  if (mode === 'mock') {
    installInlineMock(request)
  }
}

export default request
