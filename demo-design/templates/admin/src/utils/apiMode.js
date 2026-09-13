// src/utils/apiMode.js

const STORAGE_KEY = 'jzerp_api_mode'
const URL_PARAM = 'api'

/**
 * 决策优先级:
 *   1. URL 参数 ?api=real|mock(启动时读,会写 localStorage 持久化)
 *   2. localStorage 持久化('jzerp_api_mode' = 'real' | 'mock')
 *   3. import.meta.env.VITE_USE_MOCK('false' → real,其他 → 继续)
 *   4. 默认 'mock'
 *
 * @returns {'mock' | 'real'}
 */
export function resolveApiMode() {
  // 1. URL 参数
  const urlParam = new URLSearchParams(window.location.search).get(URL_PARAM)
  if (urlParam === 'real' || urlParam === 'mock') {
    localStorage.setItem(STORAGE_KEY, urlParam)
    return urlParam
  }
  // 2. localStorage
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored === 'real' || stored === 'mock') return stored
  // 3. build 时环境变量
  if (import.meta.env.VITE_USE_MOCK === 'false') return 'real'
  // 4. 默认
  return 'mock'
}

/**
 * 运行时切换 API 模式。必须 reload 才能生效,因为 adapter 在启动时挂载。
 * 用法: 控制台执行 setApiMode('real') 或 setApiMode('mock')
 *
 * @param {'mock' | 'real'} mode
 */
export function setApiMode(mode) {
  if (mode !== 'real' && mode !== 'mock') {
    throw new Error(`setApiMode: invalid mode '${mode}', must be 'real' or 'mock'`)
  }
  localStorage.setItem(STORAGE_KEY, mode)
  window.location.reload()
}

// 暴露到 window,方便浏览器控制台调用
if (typeof window !== 'undefined') {
  window.setApiMode = setApiMode
}
