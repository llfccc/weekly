import Vue from 'vue';
import Router from 'vue-router';
import Register from '../components/page/register.vue'
Vue.use(Router);

export default new Router({
    routes: [{
            path: '/',
            redirect: '/login'
        },
        // {
        //     path: '/register',
        //     name: 'Register',
        //     component: Register
        // },
        {
            path: '/readme',
            component: resolve => require(['../components/common/Home.vue'], resolve),
            children: [{
                    path: '/',
                    component: resolve => require(['../components/page/Readme.vue'], resolve)
                },
                {
                    path: '/downloadExcel',
                    component: resolve => require(['../components/page/DownloadExcel.vue'], resolve)
                },
                {
                    path: '/insertDevWork',
                    component: resolve => require(['../components/page/insertDevWork.vue'], resolve)
                },
                {
                    path: '/insertSaleEvent',
                    component: resolve => require(['../components/page/insertSaleEvent.vue'], resolve)
                },
                {
                    path: '/vuetable',
                    component: resolve => require(['../components/page/VueTable.vue'], resolve) // vue-datasource组件
                },
                {
                    path: '/insertWeekSummary',
                    component: resolve => require(['../components/page/insertWeekSummary.vue'], resolve) // vue-datasource组件
                },
                {
                    path: '/analysisWeeklyGraph',
                    component: resolve => require(['../components/page/analysisWeeklyGraph.vue'], resolve) // vue-datasource组件
                },
                {
                    path: '/analysisWeekly',
                    component: resolve => require(['../components/page/analysisWeekly.vue'], resolve) // vue-datasource组件
                },
                {
                    path: '/projectManage',
                    component: resolve => require(['../components/page/projectManage.vue'], resolve) // vue-datasource组件
                },
                {
                    path: '/analysisSaleEvent',
                    component: resolve => require(['../components/page/analysisSaleEvent.vue'], resolve) // vue-datasource组件
                },
                {
                    path: '/analysisSalePerformance',
                    component: resolve => require(['../components/page/analysisSalePerformance.vue'], resolve) // vue-datasource组件
                },

                {
                    path: '/saleTarget',
                    component: resolve => require(['../components/page/saleTarget.vue'], resolve) // vue-datasource组件
                },
                {
                    path: '/saleCustmoer',
                    component: resolve => require(['../components/page/saleCustmoer.vue'], resolve) // vue-datasource组件
                },
                {
                    path: '/baseform',
                    component: resolve => require(['../components/page/BaseForm.vue'], resolve)
                },
                {
                    path: '/vueeditor',
                    component: resolve => require(['../components/page/VueEditor.vue'], resolve) // Vue-Quill-Editor组件
                },
                {
                    path: '/markdown',
                    component: resolve => require(['../components/page/Markdown.vue'], resolve) // Vue-Quill-Editor组件
                },
                {
                    path: '/upload',
                    component: resolve => require(['../components/page/Upload.vue'], resolve) // Vue-Core-Image-Upload组件
                },
                {
                    path: '/basecharts',
                    component: resolve => require(['../components/page/BaseCharts.vue'], resolve) // vue-echarts-v3组件
                },
                {
                    path: '/mixcharts',
                    component: resolve => require(['../components/page/MixCharts.vue'], resolve) // vue-echarts-v3组件
                }
            ]
        },
        {
            path: '/login',
            component: resolve => require(['../components/page/Login.vue'], resolve)
        },
    ]
})