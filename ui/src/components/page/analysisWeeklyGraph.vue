<template>
  <!--为echarts准备一个具备大小的容器dom-->
  <div>
  
    <div>
                  <el-form :inline="true" :model="filters">
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" :model="filters">
          <span class="demonstration">筛选时间</span>
          <el-date-picker v-model="filters.filter_date" type="daterange" align="right" placeholder="选择日期范围" @change='filterDateChange' :picker-options="pickerOptions2">
          </el-date-picker>
          <el-form-item>
            <el-button type="primary" @click="filter">筛选</el-button>

          </el-form-item>
        </el-form>
      </el-col>
                  </el-form>
    </div>
    <br>
    </br>
    <el-row :gutter="24">
      <el-col :span="12">
        <div id="load" style="width: 900px;height: 300px;"> </div>
      </el-col>
    </el-row>
    <el-row :gutter="24">
      <el-col :span="8">
        <el-input v-model="filters.project_name" placeholder="工作项目"></el-input>
        <div id="project" style="width: 300px;height: 300px;"> </div>
      </el-col>
      <el-col :span="8">
        <el-input v-model="filters.department_name" placeholder="部门"></el-input>
        <div id="department" style="width: 300px;height: 300px;"> </div>
      </el-col>
      <el-col :span="8">
        <el-input v-model="filters.employee_name" placeholder="员工姓名"></el-input>
        <div id="personal" style="width: 400px;height: 300px;"> </div>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import echarts from 'echarts'
export default {
  name: '',
  data() {
    return {
      filters: {
        project_name: '',
        employee_name: '',
        department_name: '技术服务中心',
        filter_date: '',
        // start_date: '',
        // end_date: '',
      },
      pickerOptions2: {
        shortcuts: [{
          text: '最近一周',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
            picker.$emit('pick', [start, end]);
          }
        },
        {
          text: '最近一个月',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
            picker.$emit('pick', [start, end]);
          }
        }, {
          text: '最近三个月',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
            picker.$emit('pick', [start, end]);
          }
        }]
      },
      echartsPerson: {
        charts: '',
        opinion: [],
        opinionData: []
      },
      echartsDepart: {
        charts: '',
        opinion: [],
        opinionData: []
      },
      echartsProject: {
        charts: '',
        x_data: [],
        y_data: []
      },
      echartsLoad: {
        charts: '',
        x_data: [],
        y_data: []
      },
    }
  },
  methods: {
    drawDepartPie(id) {
      this.charts = echarts.init(document.getElementById(id))
      this.charts.setOption({
        title: {
          text: '部门时间类型',
          subtext: '',
          x: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          data: this.echartsDepart.opinion
        },
        series: [
          {
            name: '访问来源',
            type: 'pie',
            radius: '55%',
            center: ['50%', '60%'],
            data: this.echartsDepart.opinionData,
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      })
    },
    drawPersonPie(id) {
      this.charts = echarts.init(document.getElementById(id))
      this.charts.setOption({
        title: {
          text: '个人时间类型',
          subtext: '',
          x: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          data: this.echartsPerson.opinion
        },
        series: [
          {
            name: '占比',
            type: 'pie',
            radius: '55%',
            center: ['50%', '60%'],
            data: this.echartsPerson.opinionData,
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      })
    },
    drawProject(id) {
      this.charts = echarts.init(document.getElementById(id))
      this.charts.setOption({
        color: ['#3398DB'],
        tooltip: {
          trigger: 'axis',
          axisPointer: {            // 坐标轴指示器，坐标轴触发有效
            type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [
          {
            type: 'category',
            data: this.echartsProject.x_data,
            axisTick: {
              alignWithLabel: true
            }
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: [
          {
            name: '项目耗时',
            type: 'bar',
            barWidth: '60%',
            data: this.echartsProject.y_data
          }
        ]
      })
    },
    drawLoad(id) {
      this.charts = echarts.init(document.getElementById(id))
      this.charts.setOption({
        color: ['#3398DB'],
        tooltip: {
          trigger: 'axis',
          axisPointer: {            // 坐标轴指示器，坐标轴触发有效
            type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [
          {
            type: 'category',
            data: this.echartsLoad.x_data,
            axisTick: {
              alignWithLabel: true
            }
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: [
          {
            name: '每周平均工作时间',
            type: 'bar',
            barWidth: '60%',
            data: this.echartsLoad.y_data
          }
        ]
      })
    },
    filterDateChange(val) {
      var self = this;
      self.filters.filterDate = val;
    },
    filter: function (params) {
      this.get_department_data();
      this.get_personal_data();
      this.get_project_data();
      this.get_load();
    },
    get_department_data: function (params) {
      var self = this;
      this.$axios.get('/analysis/analysis_sale_department/', {
        params: {
          filter_date: self.filters.filterDate,
          // employee_name: self.filters.employee_name,
          // project_name: self.filters.project_name,
          department_name: self.filters.department_name,
        }
      })
        .then(function (response) {
          var responseContent = JSON.parse(response.data.content);
          self.echartsDepart.opinionData = responseContent.type_count
          self.echartsDepart.opinion = responseContent.type_list
          self.drawDepartPie('department');
        }
        );
    },
    get_personal_data: function (params) {
      var self = this;
      this.$axios.get('/analysis/analysis_sale_worker/', {
        params: {
          filter_date: self.filters.filterDate,
          employee_name: self.filters.employee_name,
          // project_name: self.filters.project_name,
          // department_name: self.filters.department_name,
        }
      })
        .then(function (response) {
          var responseContent = JSON.parse(response.data.content);
          self.echartsPerson.opinionData = responseContent.type_count
          self.echartsPerson.opinion = responseContent.type_list

          self.drawPersonPie('personal');
        }
        );
    },
    get_project_data: function (params) {
      var self = this;
      this.$axios.get('/analysis/analysis_sale_project/', {
        params: {
          filter_date: self.filters.filterDate,
          // employee_name: self.filters.employee_name,
          project_name: self.filters.project_name,
          department_name: '技术服务中心',
        }
      })
        .then(function (response) {
          var responseContent = JSON.parse(response.data.content);
          self.echartsProject.x_data = responseContent.x_data
          self.echartsProject.y_data = responseContent.y_data
          self.drawProject('project')
        }
        );
    },
    get_load: function (params) {
      var self = this;
      this.$axios.get('/analysis/analysis_sale_load/', {
        params: {
          filter_date: self.filters.filterDate,
          // employee_name: self.filters.employee_name,
          // project_name: self.filters.project_name,
           department_name: '技术服务中心',
        }
      })
        .then(function (response) {
          var responseContent = JSON.parse(response.data.content);
          self.echartsLoad.x_data = responseContent.x_data
          self.echartsLoad.y_data = responseContent.y_data
          console.log(responseContent.x_data)
          self.drawLoad('load');
        }
        );
    },
  },
  //调用 
  mounted() {
    this.$nextTick(function () {
      this.get_department_data()
      this.get_project_data()
      this.get_load()
    })
  }
}
</script>
<style scoped>
* {
  margin: 0;
  padding: 0;
  list-style: none;
}
</style>