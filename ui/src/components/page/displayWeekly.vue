<template>
  <!--为echarts准备一个具备大小的容器dom-->
  <div>
  
    <div>
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" :model="filters">
          <span class="demonstration">筛选时间</span>
          <el-date-picker v-model="filters.filter_date" type="daterange" align="right" placeholder="选择日期范围" @change='filterDateChange' :picker-options="pickerOptions2">
          </el-date-picker>
          <el-form-item>
            <el-button type="primary" v-on:click="filter">筛选</el-button>
          </el-form-item>
        </el-form>
      </el-col>
  
      <table class=" table-responsive table-bordered">
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
      </table>
  
    </div>
    <br>
    </br>
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
    <el-row :gutter="24">
  
      <el-col :span="12">
        <div id="load" style="width: 900px;height: 300px;"> </div>
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
      weekly_dict: '',
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

    }
  },
  methods: {

    filterDateChange(val) {
      var self = this;
      self.filters.filterDate = val;
    },
    filter: function (params) {
      // this.get_depart_data();
      // this.get_personal_data();
      // this.get_project_data();
      // this.get_load();
    },
    get_depart_data: function (params) {
      var self = this;
      this.$axios.get('/analysis/display_weekly/')
        .then(function (response) {
          var responseContent = JSON.parse(response.data.content);
          console.log(responseContent)
          self.weekly_dict = responseContent
          // self.echartsDepart.opinionData = responseContent.type_count
          // self.echartsDepart.opinion = responseContent.type_list
          //self.drawDepartPie('department');
        }
        );
    },


  },
  //调用 
  mounted() {
    this.$nextTick(function () {
      this.get_depart_data()

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