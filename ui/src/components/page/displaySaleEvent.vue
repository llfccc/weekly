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
  
          <el-col :span="4">
            <el-input type="text" class="form-control" id="employee_name" placeholder="员工名" v-model="filters.employee_name">
              总结
            </el-input>
          </el-col>
          <el-col :span="8">
            <el-button type="primary" v-on:click="filter">筛选</el-button>
          </el-col>
  
        </el-form>
      </el-col>
  
      <!--<table class="table table-responsive table-bordered">
        <tr>
          <th>日期 </th>
          <th>星期 </th>
          <th>项目名称 </th>
          <th>类型 </th>
          <th>事件描述 </th>
          <th>持续时间 </th>
          <th>上游汇报人</th>
          <th>下游对接人 </th>
          <th>完成百分比 </th>
          <th>备注 </th>
        </tr>
        <tr v-for="item in weekly_dict">
          <td>
            {{item.event_date}}
          </td>
          <td>
            {{item.which_day}}
          </td>
          <td>
            <table class=" table-responsive table-bordered" width="100%" height="100%">
              <tr v-for="child in item.other_row">
                <td>{{child.project_name}}</td>
              </tr>
            </table>
          </td>
          <td>
            <table class=" table-responsive table-bordered" width="100%" height="100%">
              <tr v-for="child in item.other_row">
                <td>{{child.event_type_name}}</td>
              </tr>
            </table>
          </td>
          <td>
            <table class=" table-responsive table-bordered" width="100%" height="100%">
              <tr v-for="child in item.other_row">
                <td>{{child.description}}</td>
              </tr>
            </table>
  
          </td>
          <td>
            {{item.total_time}}
  
          </td>
          <td>
            <table class=" table-responsive table-bordered" width="100%" height="100%">
              <tr v-for="child in item.other_row">
                <td>{{child.up_reporter_id}}</td>
              </tr>
            </table>
          </td>
          <td>
            <table class=" table-responsive table-bordered" width="100%" height="100%">
              <tr v-for="child in item.other_row">
                <td>{{child.down_reporter_ids}}</td>
              </tr>
            </table>
          </td>
          <td>
            <table class=" table-responsive table-bordered" width="100%" height="100%">
              <tr v-for="child in item.other_row">
                <td>{{child.fin_percentage}}</td>
              </tr>
            </table>
          </td>
          <td>
            <table class=" table-responsive table-bordered" width="100%" height="100%">
              <tr v-for="child in item.other_row">
                <td>{{child.dev_event_remark}}</td>
              </tr>
            </table>
          </td>
        </tr>
      </table>-->
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
      weekly_dict: '',
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
      this.get_sale_events();
      this.get_summary();
    },
    get_sale_events: function (params) {
      var self = this;
      console.log(self.filters.naturalWeek)
      this.$axios.get('/analysis/display_sale_events/', {
        params: {
          filter_date: self.filters.naturalWeek,
          employee_name: self.filters.employee_name,
        }
      })
        .then(function (response) {
          var responseContent = JSON.parse(response.data.content);
          self.weekly_dict = responseContent
          // console.log(responseContent)

        }
        );
    },
    get_summary: function (params) {
      var self = this;
      this.$axios.get('/works/get_weekly_summary/', {
        params: {
          filter_date: self.filters.naturalWeek,
          employee_name: self.filters.employee_name,
        }
      })
        .then(function (response) {
          var responseContent = JSON.parse(response.data.content);
          self.summary = responseContent[0]
          console.log(self.summary)
        }
        );
    },

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