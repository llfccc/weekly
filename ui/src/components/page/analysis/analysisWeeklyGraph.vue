<template>
  <div>
    <!--<h1 class="title" style="align:center;">周报分析</h1>-->
  
    <div>
      <el-form :inline="true" :model="filters">
  
        <el-col :span="7" class="toolbar" style="padding-bottom: 0px;">
          <el-form-item>
            <span class="demonstration">时间：</span>
            <el-date-picker v-model="filters.filter_date" type="daterange" align="right" placeholder="选择日期范围" @change='filterDateChange' :picker-options="pickerOptions2">
            </el-date-picker>
          </el-form-item>
        </el-col>
        <el-col :span="6" class="toolbar" style="padding-bottom: 0px;">
          <el-form-item>
            <span class="demonstration">项目：</span>
            <el-select v-model="filters.project_name" clearable filterable placeholder="项目名">
              <el-option v-for="item in project_list" :key="item.id" :label="item.project_name" :value="item.project_name">
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6" class="toolbar" style="padding-bottom: 0px;">
          <el-form-item>
            <span class="demonstration">员工：</span>
            <el-select v-model="filters.employee_name" clearable filterable placeholder="员工名">
              <el-option v-for="item in filter_user_list" :key="item.id" :label="item.chinese_name" :value="item.chinese_name">
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="3" class="toolbar" style="padding-bottom: 0px;">
          <el-button type="primary" @click="filter">筛选</el-button>
  
        </el-col>
      </el-form>
    </div>
    <br>
    </br>
    <el-row :gutter="24">
      <el-col :span="12">
        <div id="load" style="width: 1200px;height: 300px;"> </div>
      </el-col>
    </el-row>
    <el-row :gutter="24">
      <el-col :span="8">
        <div id="department" style="width: 400px;height: 300px;"> </div>
      </el-col>
      <el-col :span="8">
        <div id="personal" style="width: 400px;height: 300px;"> </div>
      </el-col>
      <el-col :span="8">
        <div id="project" style="width: 400px;height: 300px;"> </div>
      </el-col>
  
      <el-col :span="24">
        <div id="position" style="width: 1200px;height: 450px;"> </div>
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
      user_list: '',
      project_list: '',
      filters: {
        project_name: '',
        employee_name: '',
        project_id: '',
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
      echartsPosition: {
        charts: '',
        x_data: [],
        y_data: [],
        y_change_data: [],
      },
    }
  },
  computed: {
    filter_user_list() {
      var self = this;
      let department_id = localStorage.getItem('department_id');
      let ms_username = localStorage.getItem('ms_username');

      var filter_user_list = new Array();
      for (var i in self.user_list) {
        if (self.user_list[i].department == department_id & self.user_list[i].chinese_name != ms_username) {
          filter_user_list.push(self.user_list[i])
        }
      }
      return filter_user_list
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
      var self = this;
      this.charts = echarts.init(document.getElementById(id))
      this.charts.setOption({
        title: {
          text: '"' + self.filters.employee_name + '"' + '--耗时分布',
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
      var self = this;
      this.charts = echarts.init(document.getElementById(id))
      this.charts.setOption({
        title: {
          text: '"' + self.filters.project_name + '"' + '项目--耗时分布'
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
    drawPosition(id) {
      var self = this;
      this.charts = echarts.init(document.getElementById(id))
      this.charts.setOption(
        {
          title: {
            text: '"' + self.filters.project_name + '"' + '项目--各岗位耗时瀑布图',
            // subtext: 'From ExcelHome',
            // sublink: 'http://e.weibo.com/1341556070/AjQH99che'
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
              type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            },
            formatter: function (params) {
              var tar = params[1];
              return tar.name + '<br/>' + tar.seriesName + ' : ' + tar.value;
            }
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            splitLine: { show: false },
            data: this.echartsPosition.x_data
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              name: '辅助',
              type: 'bar',
              stack: '总量',
              itemStyle: {
                normal: {
                  barBorderColor: 'rgba(0,0,0,0)',
                  color: 'rgba(0,0,0,0)'
                },
                emphasis: {
                  barBorderColor: 'rgba(0,0,0,0)',
                  color: 'rgba(0,0,0,0)'
                }
              },
              data: this.echartsPosition.y_change_data
            },
            {
              name: '耗时（H）',
              type: 'bar',
              stack: '总量',
              label: {
                normal: {
                  show: true,
                  position: 'inside'
                }
              },
              data: this.echartsPosition.y_data
            }
          ]
        }

        // {
        //         title: {
        //           text: '项目各岗位耗时瀑布图'
        //         },
        //         color: ['#3398DB'],
        //         tooltip: {
        //           trigger: 'axis',
        //           axisPointer: {            // 坐标轴指示器，坐标轴触发有效
        //             type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        //           }
        //         },
        //         grid: {
        //           left: '3%',
        //           right: '4%',
        //           bottom: '3%',
        //           containLabel: true
        //         },
        //         xAxis: [
        //           {
        //             type: 'category',
        //             data: this.echartsPosition.x_data,
        //             axisTick: {
        //               alignWithLabel: true
        //             }
        //           }
        //         ],
        //         yAxis: [
        //           {
        //             type: 'value'
        //           }
        //         ],
        //         series: [
        //           {
        //             name: '平均每周工作时间（H）',
        //             type: 'bar',
        //             barWidth: '60%',
        //             data: this.echartsPosition.y_data
        //           }
        //         ]
        //       }
      )
    },
    filterDateChange(val) {
      var self = this;
      self.filters.filterDate = val;
    },
    filter: function (params) {
      this.analysis_department();
      this.analysis_employee();
      this.analysis_project();
      this.analysis_load();
      this.analysis_position();
    },
    analysis_department: function (params) {
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
    analysis_position: function (params) {
      var self = this;
      this.$axios.get('/analysis/analysis_position/', {
        params: {
          filter_date: self.filters.filterDate,
          project_name: self.filters.project_name,
          // project_name: self.filters.project_name,
          // department_name: self.filters.department_name,
        }
      })
        .then(function (response) {
          var responseContent = JSON.parse(response.data.content);
          self.echartsPosition.x_data = responseContent.x_data
          self.echartsPosition.y_data = responseContent.y_data
          self.echartsPosition.y_change_data = responseContent.y_change_data
          self.drawPosition('position');
        }
        );
    },
    analysis_employee: function (params) {
      var self = this;
      this.$axios.get('/analysis/analysis_employee/', {
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
    analysis_project: function (params) {
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
    analysis_load: function (params) {
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
      this.get_users();
      this.get_projects();
    })
  }
}
</script>
<style scoped>
.title {
  text-align: center;
  margin: 5px 0 40px 0;
}
</style>