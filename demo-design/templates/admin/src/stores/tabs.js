import { defineStore } from 'pinia'
import { ref } from 'vue'

const HOME_TAB = {
  path: '/home',
  name: 'Home',
  title: '首页',
  closable: false,
  affix: true
}

/**
 * 过滤掉 affix tab 后再操作
 */
function filterClosable(tabs) {
  return tabs.filter((t) => t.affix)
}

export const useTabsStore = defineStore(
  'tabs',
  () => {
    const tabs = ref([{ ...HOME_TAB }])
    const activeTab = ref('/')

    /**
     * 初始化：恢复持久化数据，但保证首页存在
     * 迁移：清理旧版本中 path:'/' 的首页 tab（bug fix: 避免双首页）
     */
    function init() {
      // migration: 移除旧版首页（path:'/'）
      const oldHomeIdx = tabs.value.findIndex((t) => t.path === '/' && t.affix)
      if (oldHomeIdx !== -1) {
        tabs.value.splice(oldHomeIdx, 1)
      }
      const exists = tabs.value.some((t) => t.path === HOME_TAB.path)
      if (!exists) {
        tabs.value.unshift({ ...HOME_TAB })
      }
      if (!activeTab.value) {
        activeTab.value = HOME_TAB.path
      }
    }

    /**
     * 添加 tab（已存在则不重复）
     */
    function addTab(tab) {
      if (!tab || !tab.path) return
      const exists = tabs.value.findIndex((t) => t.path === tab.path)
      if (exists === -1) {
        tabs.value.push({
          path: tab.path,
          name: tab.name || '',
          title: tab.title || tab.path,
          closable: tab.affix ? false : tab.closable ?? true,
          affix: !!tab.affix
        })
      }
      activeTab.value = tab.path
    }

    /**
     * 关闭当前 tab；当前 tab 是 affix 时 no-op
     */
    function removeTab(path) {
      const idx = tabs.value.findIndex((t) => t.path === path)
      if (idx === -1) return
      if (tabs.value[idx].affix) return
      tabs.value.splice(idx, 1)
      // 如果关闭的是激活 tab，激活前一个
      if (activeTab.value === path) {
        const next = tabs.value[idx - 1] || tabs.value[idx] || tabs.value[0]
        if (next) activeTab.value = next.path
      }
    }

    /**
     * 关闭其他：保留所有 affix + 当前
     */
    function removeOthers(path) {
      tabs.value = tabs.value.filter((t) => t.affix || t.path === path)
      activeTab.value = path
    }

    /**
     * 关闭左侧：移除所有位于当前 path 左侧的非 affix tab
     */
    function removeLeft(path) {
      const idx = tabs.value.findIndex((t) => t.path === path)
      if (idx <= 0) return
      const keep = filterClosable(tabs.value.slice(0, idx))
      tabs.value = [...keep, ...tabs.value.slice(idx)]
    }

    /**
     * 关闭右侧：移除所有位于当前 path 右侧的非 affix tab
     */
    function removeRight(path) {
      const idx = tabs.value.findIndex((t) => t.path === path)
      if (idx === -1) return
      const left = tabs.value.slice(0, idx + 1)
      const right = filterClosable(tabs.value.slice(idx + 1))
      tabs.value = [...left, ...right]
    }

    /**
     * 关闭全部：仅保留 affix
     */
    function removeAll() {
      tabs.value = filterClosable(tabs.value)
      activeTab.value = tabs.value[0]?.path || HOME_TAB.path
    }

    function setActive(path) {
      if (tabs.value.some((t) => t.path === path)) {
        activeTab.value = path
      }
    }

    return {
      tabs,
      activeTab,
      init,
      addTab,
      removeTab,
      removeOthers,
      removeLeft,
      removeRight,
      removeAll,
      setActive
    }
  },
  {
    persist: {
      key: 'jzerp_tabs',
      pick: ['tabs', 'activeTab']
    }
  }
)
