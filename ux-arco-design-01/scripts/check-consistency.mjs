#!/usr/bin/env node
/**
 * UX Arco Design 01 一致性检查
 *
 * 用法: node scripts/check-consistency.mjs [--fix-hint]
 * 退出码: 0 = 通过, 1 = 有错误
 *
 * 检查项:
 *  1. 12 套主题主色在 themes/*.md 与 ui-style-guide.md 速查表是否一致
 *  2. 顶栏高度是否统一为 60px（禁止 52/56）
 *  3. 断点是否混入 1920（1920×1080 画布尺寸不算）
 *  4. --border-radius-large 是否被当成有效圆角档
 *  5. Markdown 相对链接是否断链
 *  6. 代码围栏是否配对
 *  7. SKILL.md 是否可达全部规范文件
 *  8. frame-presets.css 筛选栅格是否为自适应最小列宽
 */
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs'
import { dirname, join, normalize, relative } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = normalize(join(dirname(fileURLToPath(import.meta.url)), '..'))
const errors = []
const warnings = []

const read = (p) => readFileSync(join(root, p), 'utf8')
const walk = (dir, out = []) => {
  for (const name of readdirSync(join(root, dir))) {
    if (name.startsWith('.')) continue
    const rel = join(dir, name)
    const abs = join(root, rel)
    if (statSync(abs).isDirectory()) walk(rel, out)
    else if (name.endsWith('.md')) out.push(rel)
  }
  return out
}

/* 1. 主题主色一致性 */
const guide = read('references/ui-style-guide.md')
const themeFiles = readdirSync(join(root, 'references/themes')).filter((f) => f.endsWith('-style.md'))
const guidePrimary = new Map()
for (const line of guide.split('\n')) {
  const m = line.match(/\|\s*([^|]+?)\s*\|\s*`(#[0-9A-Fa-f]{6})`\s*\|/)
  if (m && line.includes('themes/')) guidePrimary.set(m[1].trim(), m[2].toUpperCase())
}

// 主题的 token 命名并不统一（brand.primary / brand.accent / brand.light / brand.purple），
// 因此校验「速查表主色是否出现在该主题 Token 区」而不是依赖固定键名。
for (const file of themeFiles) {
  const name = file.replace(/-style\.md$/, '')
  const text = read(join('references/themes', file))
  const expected = guidePrimary.get(name)
  if (!expected) {
    errors.push(`[主题] ${name}: ui-style-guide.md 速查表缺少该主题行`)
    continue
  }
  const tokens = text.split(/###\s*字体\s*\/\s*Typography|###\s*Typography/)[0]
  if (!tokens.toLowerCase().includes(expected.toLowerCase())) {
    errors.push(`[主题] ${name}: 速查表主色 ${expected} 未出现在主题 Token 区`)
  }
}
for (const name of guidePrimary.keys()) {
  if (!themeFiles.some((f) => f === `${name}-style.md`)) errors.push(`[主题] ${name}: 速查表有记录但 themes/ 下无文件`)
}

/* 2/3/4. 文案级一致性 */
const mdFiles = walk('.')
for (const file of mdFiles) {
  const lines = read(file).split('\n')
  lines.forEach((line, i) => {
    const at = `${file}:${i + 1}`
    if (/顶栏/.test(line) && /(?:52|56)\s*px/.test(line) && !/禁止|不要|52\/56/.test(line)) {
      errors.push(`[顶栏] ${at}: 顶栏高度出现 52/56px，应为 60px`)
    }
    if (/(?:断点|@media|breakpoint)/i.test(line) && /1920/.test(line) && !/1920\s*[×x*]\s*1080|未写|不是|禁止/.test(line)) {
      errors.push(`[断点] ${at}: 断点中出现 1920（真实断点只到 1600）`)
    }
    if (/border-radius-large/.test(line) && !/不生效|0 处|无效|没有|禁止|不存在|无组件消费|占位|无任何组件使用|保持与|没用/.test(line)) {
      errors.push(`[圆角] ${at}: --border-radius-large 在 2.59.0 无引用，不能当有效档使用`)
    }
  })
  if ((read(file).match(/^```/gm) || []).length % 2 !== 0) errors.push(`[围栏] ${file}: 代码围栏未配对`)

  /* 5. 链接 */
  const text = read(file)
  for (const m of text.matchAll(/\[[^\]]*\]\(([^)\s]+)\)/g)) {
    const target = m[1].split('#')[0]
    if (!target || /^(https?:|mailto:|codex:)/.test(target)) continue
    const abs = normalize(join(root, dirname(file), decodeURIComponent(target)))
    if (!existsSync(abs)) errors.push(`[链接] ${file}: 断链 → ${m[1]}`)
  }
}

/* 7. SKILL.md 可达性 */
const skillMd = read('SKILL.md')
const requiredRefs = [
  'references/ui-style-guide.md',
  'references/forms-guide.md',
  'references/components-guide.md',
  'references/pages-guide.md',
  'references/crud-guide.md',
  'references/component-catalog.md',
  'references/state-machine.md',
  'references/permission-guide.md',
  'references/feedback-patterns.md',
  'references/content-guide.md',
  'references/data-security.md',
  'references/accessibility.md',
  'references/extensions/README.md',
]
for (const ref of requiredRefs) {
  const base = ref.split('/').pop()
  if (!skillMd.includes(ref) && !skillMd.includes(base)) errors.push(`[导航] SKILL.md 未引用 ${ref}`)
  if (!existsSync(join(root, ref))) errors.push(`[导航] 文件不存在 ${ref}`)
}

/* 8. 筛选栅格 */
const css = read('assets/frame-presets.css')
if (!/auto-fit\s*,\s*minmax\(220px/.test(css)) errors.push('[CSS] frame-presets.css 筛选栅格未使用 auto-fit minmax(220px, 1fr)')
if (
  /repeat\(6\s*,/.test(css) &&
  !/@media\s*\(min-width:\s*1600px\)\s*\{[^}]*repeat\(6\s*,/.test(css)
) {
  errors.push('[CSS] frame-presets.css 的 repeat(6, …) 只允许出现在 min-width:1600px 的宽屏兜底块内')
}

/* 输出 */
const label = (list, tag) => list.forEach((msg) => console.log(`${tag} ${msg}`))
console.log(`\n检查范围: ${mdFiles.length} 个 Markdown + frame-presets.css + ${themeFiles.length} 套主题`)
if (warnings.length) label(warnings, '⚠️ ')
if (errors.length) {
  label(errors, '❌')
  console.log(`\n结果: ${errors.length} 个错误`)
  process.exit(1)
}
console.log('\n结果: 通过（主色 / 顶栏 / 断点 / 圆角 / 链接 / 围栏 / 导航 / 筛选栅格）')
console.log(`主题主色: ${[...guidePrimary.entries()].map(([k, v]) => `${k} ${v}`).join(' · ')}`)
