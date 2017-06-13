<template>
  <!--为echarts准备一个具备大小的容器dom-->
  <div>
    <!--<h1 class="title" style="align:center;">周拜访分析</h1>-->
    <div>
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" :model="filters">
          <el-col :span="7">
            <span class="demonstration">时间：</span>
            <el-date-picker v-model="filters.filter_date" type="week" format="yyyy-WW 周" @change="dateChange1" placeholder="选择周">
            </el-date-picker>
          </el-col>

          <!--<el-col :span="6">
                <span class="demonstration">员工：</span>

                <el-select v-model="filters.employee_name" clearable filterable placeholder="员工名">
                  <el-option v-for="item in filter_user_list" :key="item.id" :label="item.chinese_name" :value="item.chinese_name">
                  </el-option>
                </el-select>
              </el-col>-->
          <el-col :span="8">
            <el-button type="primary" v-on:click="filter">查询</el-button>
          </el-col>

        </el-form>
      </el-col>
      </br>
      </br>
      </br>
      </br>

      <!--<el-table :data="sale_event_list" stripe style="width: 100%">
          <el-table-column prop="visit_date" label="日期" width="180">
          </el-table-column>
          <el-table-column prop="which_day" label="星期">
          </el-table-column>
          <el-table-column prop="active_type_name" label="活动类型" width="180">
          </el-table-column>
          <el-table-column prop="short_name" label="拜访客户">
          </el-table-column>
          <el-table-column prop="phase_name" label="阶段">
          </el-table-column>
          <el-table-column prop="communicate_record" label="沟通记录">
          </el-table-column>
          <el-table-column prop="sale_event_remark" label="备注">
          </el-table-column>
        </el-table>-->
      <table border="1" class="table table-responsive table-bordered" width="100%" v-show="sale_event_list">
        <thead>
          <tr>
            <th>日期 </th>
            <th>星期 </th>
            <th>活动类型 </th>
            <th>拜访客户 </th>
            <th>阶段 </th>
            <th>沟通记录 </th>
            <th>备注 </th>

          </tr>
        </thead>
        <tbody>
          <tr v-for="item in sale_event_list">
            <td width="9%" :rowspan="item.span" :class="{hidden: item.dis}">{{item.visit_date}}</td>
            <td width="8%" :rowspan="item.span" :class="{hidden: item.dis}">{{item.which_day}}</td>
            <td width="8%">{{item.active_type_name}}</td>
            <td width="10%">{{item.short_name}}</td>
            <td width="8%">{{item.phase_name}}</td>
            <td width="20%">{{item.communicate_record}}</td>
            <td width="15%">{{item.sale_event_remark}}</td>
          </tr>
        </tbody>
      </table>
    </div>
    </br>
    </br>

    <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
      <el-col :span="8">
      </el-col>
      <el-col :span="8">

      </el-col>
      <el-col :span="8">

      </el-col>
    </el-col>

    <el-card class="box-card" v-show="summary">
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
      sale_event_list: '',
      filters: {
        filter_date: '',
        employee_name: '',
        naturalWeek: '',
      },
      summary: '',
      user_list: [],
    }
  },
  computed: {
    filter_user_list() {
      var self = this;
      let department_id = localStorage.getItem('department_id');
      var filter_user_list = new Array();
      for (var i in self.user_list) {
        if (self.user_list[i].department == department_id) {
          filter_user_list.push(self.user_list[i])
        }
      }
      return filter_user_list
    }
  },
  methods: {
    dateChange1(val) {
      var self = this;
      self.filters.naturalWeek = val
    },
    get_users: function (params) {
      var self = this;
      this.$axios.get('/accounts/get_username/')
        .then(function (response) {
          self.user_list = eval(response.data.content);
        }
        );
    },
    filter: function (params) {
      this.get_sale_events();
      this.get_summary();
      this.get_users();
    },
    get_sale_events: function (params) {
      var self = this;
      var employee_name = localStorage.getItem("ms_username")
      this.$axios.get('/works/get_saleevents/', {
        params: {
          natural_week: self.filters.naturalWeek,
          employee_name: employee_name,
        }
      })
        .then(function (response) {
          var responseContent = JSON.parse(response.data.content);
          function combineCell(list) {
            var k = 0;
            while (k < list.length) {
              list[k]['span'] = 1;
              list[k]['dis'] = false;
              for (var i = k + 1; i <= list.length - 1; i++) {
                if (list[k]["visit_date"] == list[i]["visit_date"] && list[k]["visit_date"] != '') {
                  list[k]['span']++;
                  list[k]['dis'] = false;
                  list[i]['span'] = 1;
                  list[i]['dis'] = true;
                  // list[k]['total_time'] += list[i]['duration_time'];
                } else {
                  break;
                }
              }
              k = i;
            }
            return list;
          }
          self.sale_event_list = combineCell(responseContent)

        }
        );
    },
    get_summary: function (params) {
      var self = this;
      var employee_name = localStorage.getItem("ms_username")
      this.$axios.get('/works/get_weekly_summary/', {
        params: {
          natural_week: self.filters.naturalWeek,
//          employee_name: employee_name,
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

.hidden {
  display: none;
}

table {
  max-width: 100%;
  background-color: transparent;
}

th {
  text-align: center;
}

td {
  text-align: center;
}

.table {
  width: 100%;
  margin-bottom: 20px;
}

.table>thead>tr>th,
.table>tbody>tr>th,
.table>tfoot>tr>th,
.table>thead>tr>td,
.table>tbody>tr>td,
.table>tfoot>tr>td {
  padding: 8px;
  line-height: 1.428571429;

  border-top: 1px solid #dddddd;
}

.table>thead>tr>th {
  vertical-align: bottom;
  border-bottom: 2px solid #dddddd;
}

.table>caption+thead>tr:first-child>th,
.table>colgroup+thead>tr:first-child>th,
.table>thead:first-child>tr:first-child>th,
.table>caption+thead>tr:first-child>td,
.table>colgroup+thead>tr:first-child>td,
.table>thead:first-child>tr:first-child>td {
  border-top: 0;
}

.table>tbody+tbody {
  border-top: 2px solid #dddddd;
}

.table .table {
  background-color: #ffffff;
}

.table-condensed>thead>tr>th,
.table-condensed>tbody>tr>th,
.table-condensed>tfoot>tr>th,
.table-condensed>thead>tr>td,
.table-condensed>tbody>tr>td,
.table-condensed>tfoot>tr>td {
  padding: 5px;
}

.table-bordered {
  border: 1px solid #dddddd;
}

.table-bordered>thead>tr>th,
.table-bordered>tbody>tr>th,
.table-bordered>tfoot>tr>th,
.table-bordered>thead>tr>td,
.table-bordered>tbody>tr>td,
.table-bordered>tfoot>tr>td {
  border: 1px solid #dddddd;
}

.table-bordered>thead>tr>th,
.table-bordered>thead>tr>td {
  border-bottom-width: 2px;
}

.table-striped>tbody>tr:nth-child(odd)>td,
.table-striped>tbody>tr:nth-child(odd)>th {
  background-color: #f9f9f9;
}

.table-hover>tbody>tr:hover>td,
.table-hover>tbody>tr:hover>th {
  background-color: #f5f5f5;
}
</style>
