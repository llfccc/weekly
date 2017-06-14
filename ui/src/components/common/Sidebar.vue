<template>
    <div class="sidebar">
        <el-menu :default-active="onRoutes" class="el-menu-vertical-demo" theme="dark" unique-opened router>
            <el-menu-item index="readme">
                <i></i>说明
            </el-menu-item>
            <el-submenu index="2">
                <template slot="title">
                    <i class="el-icon-menu"></i>周报管理</template>
                <el-menu-item   index="insertDevWork" v-show="permission.tech_perm">添加事件</el-menu-item>
                <el-menu-item  index="insertSaleEvent" v-show="permission.sale_perm">添加拜访</el-menu-item>
                <el-menu-item index="insertWeekSummary">添加总结</el-menu-item>    
                <el-menu-item index="viewWeekly" v-show="permission.tech_perm">查看周报</el-menu-item>
                <el-menu-item index="viewSaleEvent" v-show="permission.sale_perm">查看拜访</el-menu-item>
            </el-submenu>
            <el-submenu index="3" v-show="permission.tech_mang_perm">
                <template slot="title">
                    <i class="el-icon-star-on"></i>周报分析</template>
                <el-menu-item index="analysisWeekly">员工周报</el-menu-item>
                <el-menu-item index="analysisDevDepart">部门分析</el-menu-item>
                <el-menu-item index="analysisDevProject">项目分析</el-menu-item>

            </el-submenu>
            <!--<el-submenu index="4">
                    <template slot="title">
                        <i class="el-icon-menu"></i>销售拜访</template>
       
                    <el-menu-item index="downloadExcel">导出Excel</el-menu-item>
                </el-submenu>-->
    
            <el-submenu index="5" v-show="permission.sale_mang_perm">
                <template slot="title">
                    <i class="el-icon-star-on"></i>销售分析</template>
                <el-menu-item index="analysisSaleEvent">拜访分析</el-menu-item>
                <el-menu-item index="analysisSalePerformance">拜访业绩</el-menu-item>
                <!--<el-menu-item index="basecharts">基础图表</el-menu-item>-->
                <!--<el-menu-item index="mixcharts">混合图表</el-menu-item>-->
            </el-submenu>
    
            <!--<el-submenu index="5">
                    <template slot="title">
                        <i class="el-icon-star-on"></i>文件下载</template>
                    <el-menu-item index="rulesDownload">制度下载</el-menu-item>
                    <el-menu-item index="notice">通知</el-menu-item>
                    <!--<el-menu-item index="basecharts">基础图表</el-menu-item>-->
            <!--<el-menu-item index="mixcharts">混合图表</el-menu-item>-->
            </el-submenu>
            <el-submenu index="6"  v-show="permission.sale_mang_perm">
                <template slot="title">
                    <i class="el-icon-setting"></i>基础数据</template>
                <el-menu-item index="projectManage">数据管理</el-menu-item>
                <!--<el-menu-item index="projectManage">项目管理</el-menu-item>-->
                <el-menu-item index="saleTarget">制作中</el-menu-item>
                <!--<el-menu-item index="saleCustmoer">客户管理</el-menu-item>-->
                <!--<el-menu-item index="basecharts">基础图表</el-menu-item>-->
                <!--<el-menu-item index="mixcharts">混合图表</el-menu-item>-->
            </el-submenu>
        </el-menu>
    </div>
</template>

<script>
export default {
       data() {
        return {
            permission: {
                tech_perm: false,
                tech_mang_perm: false,
                sale_perm: false,
                sale_mang_perm: false,
            },
        }
       },
       created(){
           const self = this;
           self.permission.tech_perm=localStorage.getItem('技术员工组');
           self.permission.tech_mang_perm=localStorage.getItem('技术主管组');
           self.permission.sale_perm=localStorage.getItem('销售员工组');
           self.permission.sale_mang_perm=localStorage.getItem('销售主管组');

       },
    computed: {
        onRoutes() {
            return this.$route.path.replace('/', '');
        }
    }
}
</script>

<style scoped>
.sidebar {
    display: block;
    position: absolute;
    width: 140px;
    left: 0;
    top: 70px;
    bottom: 0;
    background: #2E363F;
}

.sidebar>ul {
    height: 100%;
}
</style>
