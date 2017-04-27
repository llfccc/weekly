// 引用模板
import index from '../page/index.vue'
import login from '../page/login.vue'
// 配置路由
export default [
  {
    path: '/',
    component: index
  },
  {
    path: '/login',
    component: login
  },
]
