<template>
  <!--为echarts准备一个具备大小的容器dom-->
  <div>
  
    <div>
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" :model="filters">
          <el-col :span="8">
            <span class="demonstration">筛选时间</span>
            <el-date-picker v-model="filters.filter_date" type="week" format="yyyy-WW 周" @change="dateChange1" placeholder="选择周">
            </el-date-picker>
          </el-col>
  
          <!--<el-col :span="4">
                <el-input type="text" class="form-control" id="employee_name" placeholder="员工名" v-model="filters.employee_name">
                  总结
                </el-input>
              </el-col>-->
          <el-col :span="8">
            <el-button type="primary" v-on:click="filter">筛选</el-button>
          </el-col>
  
        </el-form>
      </el-col>
  
      <table border="1" class="table table-responsive table-bordered">
        <tr>
          <th rowspan="2">姓名 </th>
          <th colspan="2">A </th>
          <th colspan="2">B </th>
          <th colspan="2">C </th>
          <th colspan="2">D </th>
          <th colspan="2">E </th>
          <th colspan="2">F </th>
          <th colspan="2">G </th>
        </tr>
        <tr>
          <th> 实际</th>
          <th> 目标</th>
          <th> 实际</th>
          <th> 目标</th>
          <th> 实际</th>
          <th> 目标</th>
          <th> 实际</th>
          <th> 目标</th>
          <th> 实际</th>
          <th> 目标</th>
          <th> 实际</th>
          <th> 目标</th>
          <th> 实际</th>
          <th> 目标</th>  
        </tr>
        <tr v-for="item in sale_event_list">
          <td> {{item.visit_date}}</td>
          <td> {{item.visit_date}}</td>
          <td> {{item.active_type_name}}</td>
          <td> {{item.short_name}}</td>
          <td> {{item.phase_name}}</td>
          <td> {{item.communicate_record}}</td>
          <td> {{item.sale_event_remark}}</td>
          <!--<td> {{item.}}</td>-->
  
        </tr>
      </table>
      <table id="table"></table>
  
    </div>
    <br>
    </br>
  
    <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
      <el-col :span="8">
  
      </el-col>
      <el-col :span="8">
  
      </el-col>
      <el-col :span="8">
  
      </el-col>
    </el-col>
  
    <el-card class="box-card">
      <template v-if='summary'>
        <div slot="header" class="clearfix">
          <span style="line-height: 36px;">工作总结-----{{summary.natural_week}}周</span>
          <!--<el-button style="float: right;" type="primary">操作按钮</el-button>-->
        </div>
        <div class="text item">
          <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
            <el-col :span="8">
              <el-card class="box-card">
                <div slot="header" class="clearfix">
                  <span style="line-height: 16px;">周总结</span>
                </div>
                {{summary.summary}}
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card class="box-card">
                <div slot="header" class="clearfix">
                  <span style="line-height: 16px;">自我评价</span>
                </div>
                {{summary.self_evaluation}}
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card class="box-card">
                <div slot="header" class="clearfix">
                  <span style="line-height: 16px;">计划</span>
                </div>
                {{summary.plan}}
              </el-card>
            </el-col>
          </el-col>
  
        </div>
      </template>
  
    </el-card>
  </div>
</template>
<script>
import echarts from 'echarts'
export default {
  name: '',
  data() {
    return {
      sale_performance_list: '',
      filters: {
        filter_date: '',
        employee_name: '',
        naturalWeek: '',
      },
      summary: '',
    }
  },
  methods: {
    dateChange1(val) {
      var self = this;
      self.filters.naturalWeek = val
    },

    filter: function (params) {
      this.get_sale_performance();
      // this.get_summary();
    },
    get_sale_performance: function (params) {
      var self = this;
      console.log(self.filters.naturalWeek)
      this.$axios.get('/analysis/get_sale_performance/', {
        params: {
          filter_date: self.filters.naturalWeek,
          employee_name: self.filters.employee_name,
        }
      })
        .then(function (response) {
          var responseContent = JSON.parse(response.data.content);
          self.sale_performance_list = responseContent
          console.log(responseContent)

        }
        );
    },
    // get_summary: function (params) {
    //   var self = this;
    //   this.$axios.get('/works/get_weekly_summary/', {
    //     params: {
    //       filter_date: self.filters.naturalWeek,
    //       employee_name: self.filters.employee_name,
    //     }
    //   })
    //     .then(function (response) {
    //       var responseContent = JSON.parse(response.data.content);
    //       self.summary = responseContent[0]
    //       console.log(self.summary)
    //     }
    //     );
    // },

  },
  //调用 
  mounted() {
    this.$nextTick(function () {
      // this.get_weekly()
      // this.get_summary()
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