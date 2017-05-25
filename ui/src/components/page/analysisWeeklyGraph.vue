<template>
  <div>
    <div>
      <el-form :inline="true" :model="filters">
  
        <el-col :span="8" class="toolbar" style="padding-bottom: 0px;">
          <el-form-item>
            <span class="demonstration">筛选时间</span>
            <el-date-picker v-model="filters.filter_date" type="daterange" align="right" placeholder="选择日期范围" @change='filterDateChange' :picker-options="pickerOptions2">
            </el-date-picker>
          </el-form-item>
        </el-col>
        <el-col :span="7" class="toolbar" style="padding-bottom: 0px;">
          <el-form-item>
            <span class="demonstration">筛选项目</span>
            <el-select v-model="filters.project_name" clearable filterable placeholder="项目名">
              <el-option v-for="item in project_list" :key="item.id" :label="item.project_name" :value="item.project_name">
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="7" class="toolbar" style="padding-bottom: 0px;">
          <el-form-item>
  
            <span class="demonstration">筛选员工</span>
            <el-select v-model="filters.employee_name" clearable filterable placeholder="员工名">
              <el-option v-for="item in user_list" :key="item.id" :label="item.chinese_name" :value="item.chinese_name">
              </el-option>
            </el-select>
            <el-button type="primary" @click="filter">筛选</el-button>
          </el-form-item>
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
        <div id="department" style="width: 300px;height: 300px;"> </div>
  
      </el-col>
      <el-col :span="8">
        <div id="project" style="width: 300px;height: 300px;"> </div>
  
      </el-col>
      <el-col :span="8">
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
      user_list: [],
      project_list: [],
      filters: {
        project_name: '',
        employee_name: '',
        project_id: '',
        project_name: '',
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
    get_users: function (params) {
      var self = this;
      this.$axios.get('/accounts/get_username/')
        .then(function (response) {
          self.user_list = eval(response.data.content);
        }
        );
    },
    get_projects: function (params) {
      var self = this;
      this.$axios.get('/works/get_projects/')
        .then(function (response) {
          self.project_list = eval(response.data.content);

        }
        );
    },
    drawDepartPie(id) {
      this.charts = echarts.init(document.getElementById(id))
      this.charts.setOption({
        title: {
          text: '部门耗时类型分布',
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
            name: '时间占比（H） ',
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
      var self=this;
      this.charts = echarts.init(document.getElementById(id))
      this.charts.setOption({
        title: {
          text: '"'+self.filters.employee_name+'"'+'--耗时分布',
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
            name: '时间占比（H） ',
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
      var self=this;
      this.charts = echarts.init(document.getElementById(id))
      this.charts.setOption({
        title: {
          text: '"'+self.filters.project_name+'"'+'项目--耗时分布'
        },
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
        title: {
          text: '部门人员负载图'
        },
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
            name: '平均每周工作时间（H）',
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
      this.$axios.get('/analysis/analysis_department/', {
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
      this.$axios.get('/analysis/analysis_worker/', {
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
      this.$axios.get('/analysis/analysis_project/', {
        params: {
          filter_date: self.filters.filterDate,
          // employee_name: self.filters.employee_name,
          project_name: self.filters.project_name,
          // department_name: '技术服务中心',
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
      this.$axios.get('/analysis/analysis_load/', {
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
      this.get_load();
      this.get_users();
      this.get_projects();
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