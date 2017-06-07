<template>
  <!--为echarts准备一个具备大小的容器dom-->
  <div>
    <h1 class="title" style="align:center;">查看员工周报</h1>
    <div>
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" :model="filters">
          <el-col :span="4">
            <span class="demonstration">条件:</span>
            <el-date-picker v-model="filters.filter_date" type="week" format="yyyy-WW 周" @change="dateChange1" placeholder="选择周">
            </el-date-picker>
          </el-col>
  
          <el-col :span="4">
            <el-select v-model="filters.employee_name" clearable filterable placeholder="员工名">
              <el-option v-for="item in user_list" :key="item.id" :label="item.chinese_name" :value="item.chinese_name">
              </el-option>
            </el-select>
          </el-col>
          <el-col :span="8">
            <el-button type="primary" v-on:click="filter">筛选</el-button>
          </el-col>
  
        </el-form>
      </el-col>
      </br>
      </br>
      </br>
      </br>
  
      <table border="1" class="table table-responsive table-bordered" width="100%" v-show="weekly_dict">
        <tr>
          <th>日期 </th>
          <th>星期 </th>
          <th>项目名称 </th>
          <th>类型 </th>
          <th>耗时 </th>
          <th>事件描述 </th>
          <th>工作时间 </th>
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
            <table border="1" class=" table-responsive table-bordered" width="100%" height="100%">
              <tr v-for="child in item.other_row">
                <td>{{child.project_name}}</td>
              </tr>
            </table>
          </td>
          <td>
            <table border="1" class=" table-responsive table-bordered" width="100%" height="100%">
              <tr v-for="child in item.other_row">
                <td>{{child.event_type_name}}</td>
              </tr>
            </table>
          </td>
          <td>
            <table border="1" class=" table-responsive table-bordered" width="100%" height="100%">
              <tr v-for="child in item.other_row">
                <td>{{child.duration_time}}</td>
              </tr>
            </table>
          </td>
          <td>
            <table border="1" class=" table-responsive table-bordered" width="100%" height="100%">
              <tr v-for="child in item.other_row">
                <td>{{child.description}}</td>
              </tr>
            </table>
  
          </td>
          <td>
            {{item.total_time}}
  
          </td>
          <td>
            <table border="1" class=" table-responsive table-bordered" width="100%" height="100%">
              <tr v-for="child in item.other_row">
                <td>{{child.up_reporter_name}}</td>
              </tr>
            </table>
          </td>
          <td>
            <table border="1" class=" table-responsive table-bordered" width="100%" height="100%">
              <tr v-for="child in item.other_row">
                <td>{{child.down_reporter_name}}</td>
              </tr>
            </table>
          </td>
          <td>
            <table border="1" class=" table-responsive table-bordered" width="100%" height="100%">
              <tr v-for="child in item.other_row">
                <td>{{child.fin_percentage}}</td>
              </tr>
            </table>
          </td>
          <td>
            <table border="1" class=" table-responsive table-bordered" width="100%" height="100%">
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
  
    <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
      <el-col :span="8">
  
      </el-col>
      <el-col :span="8">
  
      </el-col>
      <el-col :span="8">
  
      </el-col>
    </el-col>
  
    <el-card class="box-card"  v-show="summary">
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
      user_list: '',
    }
  },
  methods: {
    dateChange1(val) {
      var self = this;
      self.filters.naturalWeek = val
    },

    filter: function (params) {
      this.weekly_dict = [];
      this.summary = [];
      this.get_weekly();
      this.get_summary();
      this.get_users();
    },
    get_users: function (params) {
      var self = this;
      this.$axios.get('/accounts/get_username/')
        .then(function (response) {
          self.user_list = eval(response.data.content);
        }
        );
    },
    get_weekly: function (params) {
      var self = this;

      this.$axios.get('/analysis/analysis_devevent/', {
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

      this.$axios.get('/analysis/analysis_week_summary/', {
        params: {
          filter_date: self.filters.naturalWeek,
          employee_name: self.filters.employee_name,
        }
      })
        .then(function (response) {
          var responseContent = JSON.parse(response.data.content);
          self.summary = responseContent[0]

        }
        );
    },

  },
  //调用 
  mounted() {
    this.$nextTick(function () {
      this.get_users()
      // this.get_weekly()
      // this.get_summary()
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