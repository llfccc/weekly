import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import Test from '@/components/Test'
import GetWeekly from '@/components/GetWeekly'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Hello',
      component: Hello
    },
    {
      path: '/GetWeekly',
      name: 'GetWeekly',
      component: GetWeekly
    }
  ]
})
