import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// 引入 Vant 样式（按需引入下方有说明）
import 'vant/lib/index.css'

// 引入 Vant 按需组件（这里用全量引入方便 demo 演示，可按需改为 unplugin-vue-components）
import {
  Button,
  Cell,
  CellGroup,
  Tabbar,
  TabbarItem,
  Icon,
  NavBar,
  Toast,
  Search,
  Swipe,
  SwipeItem,
  Lazyload,
  List,
  PullRefresh,
  Tag,
  Card,
  Field,
  Form,
  Dialog,
  Notify,
  Image as VanImage,
  Grid,
  GridItem,
  Divider,
  Empty
} from 'vant'

// 引入 mock 数据（自动拦截请求）
import './mock'

const app = createApp(App)

// 注册 Vant 组件
const vantComponents = [
  Button, Cell, CellGroup, Tabbar, TabbarItem, Icon, NavBar, Toast,
  Search, Swipe, SwipeItem, List, PullRefresh, Tag, Card,
  Field, Form, Dialog, Notify, VanImage, Grid, GridItem, Divider, Empty
]
vantComponents.forEach((comp) => app.use(comp))

app.use(router)
app.use(Lazyload)

app.mount('#app')
