<template>
  <!--为echarts准备一个具备大小的容器dom-->
  <div>
  
    <div>
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" :model="filters">
          <el-form-item>
            <el-input v-model="filters.project_name" placeholder="工作项目"></el-input>
          </el-form-item>
          <span class="demonstration">筛选时间</span>
          <el-date-picker v-model="filters.filter_date" type="daterange" align="right" placeholder="选择日期范围" @change='filterDateChange' :picker-options="pickerOptions2">
          </el-date-picker>
          <el-form-item>
            <el-button type="primary" v-on:click="get_data">查询</el-button>
          </el-form-item>
  
        </el-form>
      </el-col>
  
    </div>
    <br>
    </br>
    <div id="main" style="width: 600px;height: 400px;"> </div>
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
        filter_date: '',
        start_date: '',
        end_date: '',
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

      type_analysis_list:[],
      charts: '',
      opinion: [],
      opinionData: []
    }
  },
  methods: {
    drawPie(id) {
      this.charts = echarts.init(document.getElementById(id))
      this.charts.setOption({
        tooltip: {
          trigger: 'item',
          formatter: '{a}<br/>{b}:{c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          x: 'left',
          data: this.opinion
        },
        series: [
          {
            name: '类型占比',
            type: 'pie',
            radius: ['50%', '70%'],
            avoidLabelOverlap: false,
            label: {
              normal: {
                show: false,
                position: 'center'
              },
              emphasis: {
                show: true,
                textStyle: {
                  fontSize: '30',
                  fontWeight: 'blod'
                }
              }
            },
            labelLine: {
              normal: {
                show: true
              }
            },
            data: this.opinionData
          }
        ]
      })
    },
    filterDateChange(val) {
      var self = this;
      self.filters.filterDate = val;
    },
    get_data: function (params) {
      var self = this;
      this.$axios.get('/analysis/analysis_worker/', {
        params: {
          filter_date: self.filters.filterDate,
          project_name: self.filters.project_name
        }
      })
        .then(function (response) {
          var responseContent=JSON.parse(response.data.content) ;  

          self.opinionData=responseContent.type_count
          self.opinion=responseContent.type_list
          console.log(self.opinionData)
                    console.log(self.opinion)
          self.drawPie('main')
        }
        );
    },
  },
  //调用 
  mounted() {
    this.$nextTick(function () {
      this.get_data()
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