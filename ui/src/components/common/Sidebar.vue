<template>
    <div class="sidebar">
        <el-menu :default-active="onRoutes" class="el-menu-vertical-demo" theme="dark" unique-opened router>
            <el-menu-item index="readme">
                <i class="el-icon-setting"></i>说明
            </el-menu-item>
            <el-submenu index="2">
                <template slot="title"><i class="el-icon-menu"></i>周报</template>
                <el-menu-item index="submitWork">添加工作</el-menu-item>
                <el-menu-item index="downloadExcel">导出Excel</el-menu-item>

            </el-submenu>
 
            <el-submenu index="4">
                <template slot="title"><i class="el-icon-star-on"></i>报表</template>
                                <el-menu-item index="weeklySumup">周报总览</el-menu-item>
                   <el-menu-item index="weeklyGraph">总表汇总图</el-menu-item>
                <!--<el-menu-item index="basecharts">基础图表</el-menu-item>-->
                <!--<el-menu-item index="mixcharts">混合图表</el-menu-item>-->
            </el-submenu>
        </el-menu>
    </div>
</template>

<script>
    export default {
        computed:{
            onRoutes(){
                return this.$route.path.replace('/','');
            }
        }
    }
</script>

<style scoped>
    .sidebar{
        display: block;
        position: absolute;
        width: 140px;
        left: 0;
        top: 70px;
        bottom:0;
        background: #2E363F;
    }
    .sidebar > ul {
        height:100%;
    }
</style>
