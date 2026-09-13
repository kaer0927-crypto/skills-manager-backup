// src/utils/inlineMockAdapter.js

import { pathToRegexp } from 'path-to-regexp'
import { mockEndpoints } from '@/mock'

/**
 * 把 vite-plugin-mock 形态的 endpoint 数组转成 axios adapter
 * - 命中: 调用 endpoint.response({query, body, headers, url}),返回 200
 * - 不命中: throw Error(开发期不期望出现,等同 API 实现缺失;caller catch 走 error 分支)
 *
 * @param {import('axios').AxiosInstance} instance
 * @param {object} [opts]
 * @param {number} [opts.delay=100] 模拟网络延迟(ms)
 */
export function installInlineMock(instance, { delay = 100 } = {}) {
  // 预编译每个 endpoint 的 path-to-regexp v8
  // v8 API: 返回 {keys, regexp};捕获是位置的(m[1]...);end: false 必填
  const compiled = mockEndpoints.map((ep) => {
    const { keys, regexp } = pathToRegexp(ep.url, {
      end: false,
      decode: decodeURIComponent
    })
    return { ep, method: ep.method.toLowerCase(), regexp, keys }
  })

  instance.defaults.adapter = async (config) => {
    const { method, url, params, data, headers } = config
    // axios 1.x adapter 拿到的 url 是相对路径(baseURL 在 config.baseURL,未合并);
    // 真实 HTTP adapter 内部会调 buildFullPath 拼成完整 URL。inline adapter 必须
    // 做同样拼接,否则 endpoint patterns 里的 /api/ 前缀永远命中不上。
    // 修复:见 docs/superpowers/specs/* 关联或 git blame
    const baseURL = instance.defaults.baseURL || ''
    const path = baseURL + url

    for (const { ep, method: m, regexp, keys } of compiled) {
      if (m !== method.toLowerCase()) continue
      const match = regexp.exec(path)
      if (!match) continue

      // v8 位置捕获 → 用 keys 名字转成对象
      // 例: /api/customer/:id → match[1] = '42', keys[0].name = 'id'
      const pathParams = {}
      keys.forEach((key, i) => {
        if (typeof key.name === 'string') {
          pathParams[key.name] = match[i + 1]
        }
      })
      const query = { ...params, ...pathParams }
      const body = data && typeof data === 'string' ? safeParseJSON(data) : data

      // 模拟网络延迟(让 UI loading 状态有真实感)
      if (delay > 0) await new Promise((r) => setTimeout(r, delay))

      // 调用 endpoint.response —— 期待返回 {code, data, message} envelope
      const resBody = ep.response({ query, body, headers, url: path })

      return {
        data: resBody,
        status: 200,
        statusText: 'OK',
        headers: {},
        config,
        request: {}
      }
    }

    // 不命中:开发期不期望出现。caller catch 后 UI 表现为 ElMessage.error
    throw new Error(`[inline-mock] no endpoint for ${method.toUpperCase()} ${path}`)
  }
}

function safeParseJSON(s) {
  try {
    return JSON.parse(s)
  } catch {
    return s
  }
}
