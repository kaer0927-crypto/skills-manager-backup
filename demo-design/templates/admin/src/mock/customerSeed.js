// 100 条预置客户数据(项目规范:列表类菜单页 mock 默认 100 条,见 CLAUDE.md)。
// 通过生成器函数产生,确定性可重复:
//   - 4 个 source、4 个 status、9 个省/市/区组合、3 个跟进人
//   - createdAt 跨度最近 100 天
//   - 部分 lastFollowedAt 为 null(潜在客户)
//   - 名字池扩到 100 条,保证每条 name 唯一
//   - 循环使用 area/source/status/assignee/remark 池,生成足够多变化

const NAMES = [
  '张明', '李娜', '王刚', '刘芳', '陈晨', '杨柳',
  '黄磊', '周杰', '吴丽', '徐峰', '孙宇', '马超',
  '朱琳', '胡静', '郭强', '林涛', '何静', '高远',
  '罗杰', '梁红', '宋丹', '韩磊', '冯宇', '邓敏',
  '曹杰', '彭丽', '蒋峰', '沈静', '蔡伟', '袁芳',
  '潘涛', '秦月', '毛宁', '范琳',
  // 扩充池(补到 100 个,保证 100 条 id 1-100 name 全部唯一)
  '丁磊', '魏然', '蒋雯', '余飞', '钱江', '侯亮',
  '曹敏', '彭涛', '苏静', '潘琳', '葛超', '段峰',
  '雷杰', '万红', '卢丹', '陈伟', '韩冰', '唐宁',
  '冯超', '邓杰', '苏峰', '蒋敏', '蔡琳', '潘超',
  '伍杰', '余敏', '钱涛', '梁峰', '沈超', '何杰',
  '谢明', '邹娜', '喻强', '柏静', '水兰', '窦明',
  '章宇', '云峰', '苏红', '巫娜', '归敏', '闾芳',
  '亢伟', '明杰', '仉静', '厍强', '昝敏', '束杰',
  '宫涛', '阙明', '连峰', '鄢红', '习杰', '尉迟静',
  '羊侃', '詹娜', '栾强', '蚁杰', '初敏', '都红',
  '鲜于峰', '訾杰', '亓官明', '南宫涛', '濮阳静', '呼延杰',
  '公西敏', '赫连峰', '皇甫红', '东方杰', '令狐涛', '宇文静',
  '长孙敏', '慕容峰', '鲜于明', '闾丘杰', '司徒静', '司空敏',
  '仲孙强', '申屠杰'
]

const SOURCES = ['mini_register', 'mini_quote', 'mini_assess', 'manual']
const STATUSES = ['potential', 'following', 'won', 'lost']
const ASSIGNEES = ['刘销售', '王销售', '张设计师']

// [province, city, region]
const AREA_COMBOS = [
  ['SH', 'SH', 'Pudong'],
  ['SH', 'SH', 'Xuhui'],
  ['SH', 'SH', 'Jingan'],
  ['BJ', 'BJ', 'Chaoyang'],
  ['BJ', 'BJ', 'Haidian'],
  ['GD', 'SZ', 'Nanshan'],
  ['GD', 'SZ', 'Futian'],
  ['GD', 'GZ', 'Tianhe'],
  ['GD', 'GZ', 'Yuexiu']
]

const REMARK_POOL = [
  null,
  null,
  null,
  '客户对设计风格有明确偏好,希望现代简约',
  '客户意向强烈,希望尽快安排量房',
  '需关注报价预算,倾向中端方案',
  '老客户转介绍,沟通顺畅',
  '房屋在装修前阶段,需要整体规划',
  '客户在比较多家装修公司,价格敏感',
  '客户有海外背景,偏好感性化设计',
  '客户希望保留部分旧家具,需要混搭方案',
  '二套房装修,经验充足,要求较高'
]

function pad(n) { return String(n).padStart(2, '0') }
// seed 记录固定在 09:00:00 产生,保证跨调用确定性
function formatDate(daysAgo) {
  const d = new Date()
  d.setDate(d.getDate() - daysAgo)
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} 09:00:00`
}

export function generateSeed() {
  const seed = []
  for (let i = 0; i < 100; i++) {
    const id = i + 1
    const name = NAMES[i]
    const combo = AREA_COMBOS[i % AREA_COMBOS.length]
    const source = SOURCES[i % SOURCES.length]
    const status = STATUSES[i % STATUSES.length]
    const assignee = ASSIGNEES[i % ASSIGNEES.length]
    const daysAgo = (i % 100) + 1
    const createdAt = formatDate(daysAgo)
    const lastFollowedAt = (status === 'potential' || (i % 7 === 0))
      ? null
      : formatDate(Math.max(daysAgo - 5, 0))

    seed.push({
      id,
      name,
      phone: `138${String(10000000 + id).padStart(8, '0')}`,
      wechatOpenid: source === 'manual' ? null : `mock_openid_${id}`,
      source,
      province: combo[0],
      city: combo[1],
      region: combo[2],
      status,
      lastFollowedAt,
      // 已流失的客户不指派跟进人;其余分配
      assignedTo: status === 'lost' ? null : assignee,
      remark: REMARK_POOL[i % REMARK_POOL.length],
      createdAt,
      updatedAt: createdAt,
      isDeleted: false
    })
  }
  return seed
}
