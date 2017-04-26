// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import VueRouter from 'vue-router'
import routes  from './router/index'

import api from './config/api'
import axios from 'axios'
Vue.prototype.$http = axios;

Vue.prototype.$api = api


Vue.use(VueRouter)

const router = new VueRouter({
  routes
});

// 跑起来吧
new Vue({
  router,
  el: '#app',
  render: (h) => h(App)
});
//
// Vue.config.productionTip = false
//
// import GetWeekly from '@/components/GetWeekly'

// const routes = [
//     // { path: '/index', component: index },
//     { path: '/GetWeekly', component: GetWeekly },
// ]
//
// const router = new VueRouter({
//   routes
// })
// const app = new Vue({
//     router,
//     render: h => h(App)
// }).$mount('#app')

//
// /* eslint-disable no-new */
// new Vue({
//   el: '#app',
//   router,
//   template: '<App/>',
//   components: { App }
// })
