// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import VueRouter from 'vue-router'
//import router from './router'

Vue.config.productionTip = false
Vue.use(VueRouter)
import GetWeekly from '@/components/GetWeekly'

const routes = [
    // { path: '/index', component: index },
    { path: '/GetWeekly', component: GetWeekly },
]

const router = new VueRouter({
  routes
})
const app = new Vue({
    router,
    render: h => h(App)
}).$mount('#app')

//
// /* eslint-disable no-new */
// new Vue({
//   el: '#app',
//   router,
//   template: '<App/>',
//   components: { App }
// })
