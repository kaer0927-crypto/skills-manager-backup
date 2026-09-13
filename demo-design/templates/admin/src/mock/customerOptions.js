// 客户模块：字典、展示映射、跟进人、地区数据、默认列设置
// 注意：所有数据由 mock 端点返回；本文件供 customer.js / customerSeed.js import

export const SOURCE_MAP = {
  mini_register: '业主注册',
  mini_quote:    '预约报价',
  mini_assess:   '需求测评',
  manual:        '手动新增'
}

export const STATUS_MAP = {
  potential: '潜在',
  following: '跟进中',
  won:       '已成交',
  lost:      '已流失'
}

// el-tag type 映射
export const STATUS_TAG_TYPE = {
  potential: 'info',
  following: 'warning',
  won:       'success',
  lost:      'danger'
}

// 跟进人：mock 硬编码（用户体系未建立前）
export const ASSIGNEE_OPTIONS = ['刘销售', '王销售', '张设计师']

// 省/市/区三级。直辖市（如上海）在省市两层 code/name 都相同
export const AREA_DATA = [
  { code: 'SH', name: '上海市', children: [
    { code: 'SH', name: '上海市', children: [
      { code: 'Pudong', name: '浦东新区' },
      { code: 'Xuhui',  name: '徐汇区' },
      { code: 'Jingan', name: '静安区' }
    ]}
  ]},
  { code: 'BJ', name: '北京市', children: [
    { code: 'BJ', name: '北京市', children: [
      { code: 'Chaoyang', name: '朝阳区' },
      { code: 'Haidian',  name: '海淀区' }
    ]}
  ]},
  { code: 'GD', name: '广东省', children: [
    { code: 'SZ', name: '深圳市', children: [
      { code: 'Nanshan', name: '南山区' },
      { code: 'Futian',  name: '福田区' }
    ]},
    { code: 'GZ', name: '广州市', children: [
      { code: 'Tianhe', name: '天河区' },
      { code: 'Yuexiu', name: '越秀区' }
    ]}
  ]}
]

// 默认列设置（与 /api/customer/options 一同返回）
export const DEFAULT_COLUMNS = [
  { prop: 'name',           label: '客户姓名', visible: true, fixed: false, width: 120 },
  { prop: 'phone',          label: '手机号',   visible: true, fixed: false, width: 130 },
  { prop: 'source',         label: '来源',     visible: true, fixed: false, width: 110 },
  { prop: 'city',           label: '所在城市', visible: true, fixed: false, width: 120 },
  { prop: 'status',         label: '状态',     visible: true, fixed: false, width: 100 },
  { prop: 'assignedTo',     label: '跟进人',   visible: true, fixed: false, width: 110 },
  { prop: 'lastFollowedAt', label: '最后跟进', visible: true, fixed: false, width: 160 },
  { prop: 'createdAt',      label: '创建时间', visible: true, fixed: false, width: 160 }
]

// city code → 中文名（用于列表"所在城市"列展示）
export const CITY_NAME_MAP = (() => {
  const map = {}
  for (const p of AREA_DATA) {
    for (const c of p.children || []) {
      map[c.code] = c.name
    }
  }
  return map
})()

// region code → 中文名
export const REGION_NAME_MAP = (() => {
  const map = {}
  for (const p of AREA_DATA) {
    for (const c of p.children || []) {
      for (const r of c.children || []) {
        map[r.code] = r.name
      }
    }
  }
  return map
})()
