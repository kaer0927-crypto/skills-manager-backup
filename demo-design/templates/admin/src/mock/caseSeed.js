// 100 条预置数据:10 条手工真实内容 + 90 条确定性生成
// 生成规则:循环 name/cover 池并加序号后缀,保证 100 条全部唯一
// 介绍和图文详情也用模板拼装,避免 100 个手写大块 HTML

// 主图使用 Unsplash 外链(与小程序端一致);
// 富文本 content 是 HTML 字符串,允许外链 <img>

// 10 条真实数据(原 spec 改造自 yunding-home/src/mock/cases.json)
const realCases = [
  {
    name: '翡翠湾 150㎡ 现代轻奢',
    cover: 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=750&q=80',
    tags: ['现代', '轻奢', '大户型'],
    description: '本案以现代轻奢为主题,融合金属、大理石、丝绒等材质,营造优雅品质生活空间。',
    content: '<p><strong>设计理念:</strong>本案以现代轻奢为主题,融合金属、大理石、丝绒等材质,营造优雅品质生活空间。设计师以开放式手法打通客餐厅,引入自然光与开阔视野。</p><p>在材料选择上,地面铺设爵士白大理石,背景墙辅以香槟金金属线条勾勒,搭配丝绒质感的家具软装,形成层次分明的视觉节奏。</p><p><img src="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=750&q=80" style="max-width:100%;border-radius:8px;display:block;margin:12px 0;" alt="客厅" /></p><p>客厅作为家庭核心区域,采用 L 型沙发围合出亲密的交流空间。主卧延续整体的轻奢气质,床头背景墙以木格栅与皮革硬包组合,呈现出温润而精致的休憩氛围。</p><p><strong>施工亮点:</strong>墙面木格栅预埋龙骨精准定位,金属线条与石材接缝处采用 1mm 倒角处理。</p>'
  },
  {
    name: '龙湖天街 125㎡ 新中式',
    cover: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=750&q=80',
    tags: ['中式', '禅意', '品质'],
    description: '新中式风格,传承古典东方美学,融入现代生活方式。',
    content: '<p><strong>设计理念:</strong>新中式风格,传承古典东方美学,融入现代生活方式。设计师以"留白"为骨,"写意"为魂,让居所承载东方生活的诗性。</p><p>整体色调以胡桃木、月白、黛灰为主,局部点缀铜质金属与水墨纹石材,传统元素经过现代转译后呈现克制的高级感。</p><p><img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=750&q=80" style="max-width:100%;border-radius:8px;display:block;margin:12px 0;" alt="客厅" /></p><p>客厅以博古架替代电视墙;餐厅圆形餐桌呼应"圆满"寓意。</p>'
  },
  {
    name: '万科公园 105㎡ 奶油风',
    cover: 'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=750&q=80',
    tags: ['奶油', '温馨', '刚需'],
    description: '温柔的奶油色调,营造温馨舒适的居家氛围。',
    content: '<p><strong>设计理念:</strong>温柔的奶油色调,营造温馨舒适的居家氛围。整体以低饱和的米白、奶咖、浅木色为基调,让空间在视觉上得到放松。</p><p>硬装部分尽量简洁,墙面与顶面以奶油色艺术漆通刷,地面铺贴奶油色木纹砖,温润不冰凉。</p><p><img src="https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=750&q=80" style="max-width:100%;border-radius:8px;display:block;margin:12px 0;" alt="客厅" /></p>'
  },
  {
    name: '绿城玫瑰园 150㎡ 现代简约',
    cover: 'https://images.unsplash.com/photo-1600607687644-c7171b42498f?w=750&q=80',
    tags: ['现代', '简约', '大户型'],
    description: '化繁为简的空间哲学,打造通透敞亮的现代居所。',
    content: '<p><strong>设计理念:</strong>化繁为简的空间哲学,打造通透敞亮的现代居所。设计师以"减"为设计语言,让每一件家具、每一条线都有明确的存在理由。</p><p>黑白灰与木色构成主色调,材质以哑光烤漆、岩板、原木为主,整体克制而高级。</p><p><img src="https://images.unsplash.com/photo-1600607687644-c7171b42498f?w=750&q=80" style="max-width:100%;border-radius:8px;display:block;margin:12px 0;" alt="客厅" /></p>'
  },
  {
    name: '保利中央公园 125㎡ 轻奢风',
    cover: 'https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=750&q=80',
    tags: ['轻奢', '品质', '三居'],
    description: '低调奢华的空间氛围,彰显品位与格调。',
    content: '<p><strong>设计理念:</strong>低调奢华的空间氛围,彰显品位与格调。本案以"意式轻奢"为基调,材质与细节共同讲述品质故事。</p><p>电视墙采用潘多拉岩板整面铺贴,自然纹理成为空间视觉焦点。</p><p><img src="https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=750&q=80" style="max-width:100%;border-radius:8px;display:block;margin:12px 0;" alt="客厅" /></p>'
  },
  {
    name: '华润橡树湾 105㎡ 现代中式',
    cover: 'https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=750&q=80',
    tags: ['中式', '现代', '刚需'],
    description: '传统与现代的融合,打造有文化底蕴的现代居所。',
    content: '<p><strong>设计理念:</strong>传统与现代的融合,打造有文化底蕴的现代居所。本案取宋代美学之"雅"与现代极简之"净",兼容并蓄。</p><p><img src="https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=750&q=80" style="max-width:100%;border-radius:8px;display:block;margin:12px 0;" alt="客厅" /></p>'
  },
  {
    name: '金地自在城 150㎡ 奶油风',
    cover: 'https://images.unsplash.com/photo-1617325247661-675ab4b64ae2?w=750&q=80',
    tags: ['奶油', '大户型', '温馨'],
    description: '浪漫温柔的奶油色调,让家充满治愈感。',
    content: '<p><strong>设计理念:</strong>浪漫温柔的奶油色调,让家充满治愈感。设计师在 150㎡ 的大空间里通过色彩统一,让每个角落都散发柔软气质。</p><p><img src="https://images.unsplash.com/photo-1617325247661-675ab4b64ae2?w=750&q=80" style="max-width:100%;border-radius:8px;display:block;margin:12px 0;" alt="客厅" /></p>'
  },
  {
    name: '万达华府 125㎡ 工业风',
    cover: 'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=750&q=80',
    tags: ['工业风', 'LOFT', '个性'],
    description: '裸露的水泥与金属管道,演绎硬朗的工业美学。',
    content: '<p><strong>设计理念:</strong>裸露的水泥墙与金属管道,演绎硬朗的工业美学。客厅以原木家具中和金属的冷感。</p><p><img src="https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=750&q=80" style="max-width:100%;border-radius:8px;display:block;margin:12px 0;" alt="客厅" /></p>'
  },
  {
    name: '中海寰宇 105㎡ 北欧风',
    cover: 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=750&q=80',
    tags: ['北欧', '极简', '刚需'],
    description: '原木与白色调,北欧极简的温馨感。',
    content: '<p><strong>设计理念:</strong>原木与白色调,北欧极简的温馨感。空间布局通透,自然光最大化引入。</p><p><img src="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=750&q=80" style="max-width:100%;border-radius:8px;display:block;margin:12px 0;" alt="客厅" /></p>'
  },
  {
    name: '招商雍景湾 150㎡ 法式轻奢',
    cover: 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=750&q=80',
    tags: ['法式', '轻奢', '大户型'],
    description: '法式优雅与轻奢质感交织,营造浪漫的居家体验。',
    content: '<p><strong>设计理念:</strong>法式优雅与轻奢质感交织,营造浪漫的居家体验。客厅以米白与香槟金为主色,辅以丝绒沙发。</p><p><img src="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=750&q=80" style="max-width:100%;border-radius:8px;display:block;margin:12px 0;" alt="客厅" /></p>'
  }
]

// 90 条生成记录的名称/封面/标签池
// 名称通过模板拼装:小区名 + 面积 + 风格
const COMMUNITIES = ['翡翠湾', '龙湖天街', '万科公园', '绿城玫瑰园', '保利中央公园', '华润橡树湾',
  '金地自在城', '万达华府', '中海寰宇', '招商雍景湾', '恒大御景', '碧桂园凤凰城',
  '融创滨江府', '雅居乐花园', '富力城', '世茂滨江', '正荣府', '阳光城',
  '建发央著', '新城金郡', '泰禾院子', '龙光天瀛', '中粮祥云', '旭辉御府',
  '金茂府', '华润润府', '保利香槟', '万科城', '招商花园城', '中海世家']
const AREAS = ['89㎡', '105㎡', '125㎡', '150㎡', '180㎡', '220㎡']
const STYLES = ['现代轻奢', '新中式', '奶油风', '现代简约', '轻奢风', '现代中式',
  '奶油风', '工业风', '北欧风', '法式轻奢', '北欧极简', '现代极简',
  '日式和风', '美式乡村', '地中海', '新古典', '工业 LOFT', '极简北欧',
  '法式浪漫', '新中式禅意']
const TAG_POOL = [
  ['现代', '轻奢'], ['中式', '禅意'], ['奶油', '温馨'], ['现代', '简约'],
  ['轻奢', '品质'], ['中式', '现代'], ['奶油', '大户型'], ['工业风', 'LOFT'],
  ['北欧', '极简'], ['法式', '轻奢'], ['北欧', '极简', '刚需'], ['现代', '极简', '大户型'],
  ['日式', '和风'], ['美式', '乡村'], ['地中海', '儿童房'], ['新古典', '复古'],
  ['工业', 'LOFT'], ['极简', '北欧'], ['法式', '浪漫'], ['新中式', '禅意']
]
const COVER_POOL = realCases.map(c => c.cover)

function pad(n) { return String(n).padStart(2, '0') }
function formatDate(d) {
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
}

// 模板化介绍与图文详情
function makeDescription(style) {
  return `${style}风格,搭配精选材料与软装,营造舒适且有格调的居家氛围。`
}
function makeContent(style, cover) {
  return `<p><strong>设计理念:</strong>本案以${style}为基调,材料选择注重质感与耐久性的平衡,软装搭配呼应整体色调,营造出层次丰富的居住空间。</p><p>在空间布局上,设计师充分考虑家庭成员的动线与互动需求,通过家具摆放和灯光设计划分功能区域,让空间既通透又有序。</p><p><img src="${cover}" style="max-width:100%;border-radius:8px;display:block;margin:12px 0;" alt="客厅" /></p><p>客厅作为家庭核心区域,采用开放式布局增强互动性。主卧延续整体调性,辅以柔和灯光与舒适床品,营造出温润的休憩氛围。</p><p><strong>施工亮点:</strong>墙面与顶面衔接严丝合缝,定制柜体与墙体齐平,收口细节精致到位。</p>`
}

export function generateSeed() {
  const now = Date.now()
  const day = 24 * 3600 * 1000

  // 10 条真实数据
  const real = realCases.map((c, i) => {
    const created = new Date(now - (99 - i) * day)
    const id = i + 1
    return {
      id,
      cover: c.cover,
      name: c.name,
      tags: c.tags,
      description: c.description,
      content: c.content,
      sort: 0,
      enabled: i !== 5,  // 第 6 条(华润橡树湾)禁用,测试禁用态
      createdAt: formatDate(created),
      updatedAt: formatDate(created),
      isDeleted: false
    }
  })

  // 90 条生成(id 11-100),确定性循环
  // enabled 规律:id % 11 === 0 的禁用(100/11≈9 条)
  // sort=id 升序,createdAt 倒序(id 越大 createdAt 越新)
  const generated = []
  for (let i = 0; i < 90; i++) {
    const id = 11 + i
    const community = COMMUNITIES[i % COMMUNITIES.length]
    const area = AREAS[i % AREAS.length]
    const style = STYLES[i % STYLES.length]
    const cover = COVER_POOL[i % COVER_POOL.length]
    const tags = TAG_POOL[i % TAG_POOL.length]
    const name = `${community} ${area} ${style}`
    const created = new Date(now - (89 - i) * day)
    generated.push({
      id,
      cover,
      name,
      tags,
      description: makeDescription(style),
      content: makeContent(style, cover),
      sort: id,
      enabled: id % 11 !== 0,
      createdAt: formatDate(created),
      updatedAt: formatDate(created),
      isDeleted: false
    })
  }

  return [...real, ...generated]
}
