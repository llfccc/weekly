<template>
    <div class="sidebar">
        <el-menu :default-active="onRoutes" class="el-menu-vertical-demo" theme="dark" unique-opened router>
            <el-menu-item index="readme">
                <i ></i>说明
            </el-menu-item>
            <el-submenu index="2">
                <template slot="title">
                    <i class="el-icon-menu"></i>办公周报</template>
                <el-menu-item index="submitWork">添加工作</el-menu-item>
                <el-menu-item index="insertWeeklySumup">添加总结</el-menu-item>
    
                <!--<el-menu-item index="downloadExcel">导出Excel</el-menu-item>-->
            </el-submenu>
                        <el-submenu index="3">
                <template slot="title">
                    <i class="el-icon-star-on"></i>办公报表</template>    
                <el-menu-item index="analysisWeekly">分析周报</el-menu-item>
                <el-menu-item index="analysisWeeklyGraph">可视周报</el-menu-item>    
            </el-submenu>
            <el-submenu index="4">
                <template slot="title">
                    <i class="el-icon-menu"></i>销售拜访</template>
                <el-menu-item index="submitEvent">添加拜访</el-menu-item>
                <!--<el-menu-item index="downloadExcel">导出Excel</el-menu-item>-->
            </el-submenu>


            <el-submenu index="5">
                <template slot="title">
                    <i class="el-icon-star-on"></i>销售报表</template>
                     <el-menu-item index="displaySaleEvent">销售周报</el-menu-item>
                <el-menu-item index="displaySalePerformance">销售业绩</el-menu-item>
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
            <el-submenu index="6">
                <template slot="title">
                    <i class="el-icon-setting"></i>基础数据</template>
                <el-menu-item index="projectManage">项目管理</el-menu-item>
                <el-menu-item index="saleTarget">销售目标管理</el-menu-item>
                <el-menu-item index="saleCustmoer">客户管理</el-menu-item>
                <!--<el-menu-item index="basecharts">基础图表</el-menu-item>-->
                <!--<el-menu-item index="mixcharts">混合图表</el-menu-item>-->
            </el-submenu>
        </el-menu>
    </div>
</template>

<script>
export default {
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
