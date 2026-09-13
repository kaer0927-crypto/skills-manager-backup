// 与 menu.js 同结构；接口失败时使用
export const menuFallbackData = [
  {
    id: 5,
    parentId: null,
    title: '内容管理[Fallback]',
    icon: 'PictureFilled',
    children: [
      {
        id: 51,
        parentId: 5,
        title: '小程序',
        children: [
          {
            id: 512,
            parentId: 51,
            title: '案例管理',
            path: '/case/list',
            name: 'CaseList'
          }
        ]
      }
    ]
  },
  {
    id: 4,
    parentId: null,
    title: '客户管理[Fallback]',
    icon: 'UserFilled',
    children: [
      {
        id: 41,
        parentId: 4,
        title: '客户档案',
        children: [
          {
            id: 411,
            parentId: 41,
            title: '客户列表',
            path: '/customer/list',
            name: 'CustomerList'
          }
        ]
      }
    ]
  }
]