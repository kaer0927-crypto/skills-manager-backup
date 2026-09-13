import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'
import { viteMockServe } from 'vite-plugin-mock'

export default defineConfig({
  // 相对路径：让 build 产物能 file:// 双击或部署到任意子路径都工作
  base: './',
  plugins: [
    vue(),
    viteMockServe({
      prefix: '/api',
      mockPath: 'src/mock'
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 5173,
    open: true
  }
})
