import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchMenu } from '@/api/menu'
import { menuFallbackData } from '@/mock/menuFallback'

export const useMenuStore = defineStore('menu', () => {
  const menuList = ref([])
  const loaded = ref(false)
  const usingFallback = ref(false)

  async function loadMenu() {
    if (loaded.value) return menuList.value
    try {
      const data = await fetchMenu()
      menuList.value = data || []
      usingFallback.value = false
    } catch (err) {
      console.warn('[menu store] 接口失败，使用降级数据:', err?.message || err)
      menuList.value = menuFallbackData
      usingFallback.value = true
    }
    loaded.value = true
    return menuList.value
  }

  return { menuList, loaded, usingFallback, loadMenu }
})
