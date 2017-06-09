<template> 
  <div>

    <!--<h1 class="title" style="align:center;">查看员工周报</h1>-->
    <div>
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" :model="filters">
          <el-col :span="6">
            <span class="demonstration">条件:</span>
            <el-date-picker v-model="filters.filter_date" type="week" format="yyyy-WW 周" @change="dateChange1" placeholder="选择周">
            </el-date-picker>
          </el-col>
  
          <el-col :span="6">
            <el-select v-model="filters.employee_name" clearable filterable placeholder="员工名">
              <el-option v-for="item in filter_user_list" :key="item.id" :label="item.chinese_name" :value="item.chinese_name">
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
      
      <table border="1" class="table table-responsive table-bordered" width="100%" v-show="weekly_dict">
        <thead>
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
            <th>完成比 </th>
            <th>备注 </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in weekly_dict">
            <td  width="9%" :rowspan="item.span" :class="{hidden: item.dis}">{{item.event_date}}</td>
            <td width="8%" :rowspan="item.span" :class="{hidden: item.dis}">{{item.which_day}}</td>
            <td width="8%" >{{item.project_name}}</td>
            <td width="10%">{{item.event_type_name}}</td>  
            <td width="8%" :rowspan="item.span" :class="{hidden: item.dis}">{{item.total_time}}</td>
            <td width="10%">{{item.description}}</td>  
            <td width="10%">{{item.duration_time}}</td>
            <td width="10%">{{item.up_reporter_name}}</td>
            <td width="10%">{{item.down_reporter_name}}</td>
            <td width="5%">{{item.fin_percentage}}</td>
            <td width="10%">{{item.dev_event_remark}}</td>
          </tr>
        </tbody>  
      </table>
  
    </div>
    </br>
    </br>
  
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
    computed: {
    filter_user_list() {
      var self = this;
      let department_id = localStorage.getItem('department_id');
      let ms_username= localStorage.getItem('ms_username');
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
          natural_week: self.filters.naturalWeek,
          employee_name: self.filters.employee_name,
        }
      })
        .then(function (response) {
          var responseContent = JSON.parse(response.data.content);

          // function combineCell(list) {
          //   for (field in list[0]) {
          //     var k = 0;
          //     while (k < list.length) {
          //       list[k][field + 'span'] = 1;
          //       list[k][field + 'dis'] = false;
          //       for (var i = k + 1; i <= list.length - 1; i++) {
          //         if (list[k][field] == list[i][field] && list[k][field] != '') {
          //           list[k][field + 'span']++;
          //           list[k][field + 'dis'] = false;
          //           list[i][field + 'span'] = 1;
          //           list[i][field + 'dis'] = true;
          //         } else {
          //           break;
          //         }
          //       }
          //       k = i;
          //     }
          //   }
          //   return list;
          // }
          function combineCell(list) {
            var k = 0;
            while (k < list.length) {
              list[k]['span'] = 1;
              list[k]['dis'] = false;
              list[k]['total_time'] = list[k]['duration_time'];
              for (var i = k + 1; i <= list.length - 1; i++) {
                if (list[k]["event_date"] == list[i]["event_date"] && list[k]["event_date"] != '') {
                  list[k]['span']++;
                  list[k]['dis'] = false;
                  list[i]['span'] = 1;
                  list[i]['dis'] = true;
                  list[k]['total_time'] += list[i]['duration_time'];
                } else {
                  break;
                }
              }
              k = i;
            }
            return list;
          }
          self.weekly_dict = combineCell(responseContent)
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

.table > thead > tr > th,
.table > tbody > tr > th,
.table > tfoot > tr > th,
.table > thead > tr > td,
.table > tbody > tr > td,
.table > tfoot > tr > td {
  padding: 8px;
  line-height: 1.428571429;

  border-top: 1px solid #dddddd;
}

.table > thead > tr > th {
  vertical-align: bottom;
  border-bottom: 2px solid #dddddd;
}

.table > caption + thead > tr:first-child > th,
.table > colgroup + thead > tr:first-child > th,
.table > thead:first-child > tr:first-child > th,
.table > caption + thead > tr:first-child > td,
.table > colgroup + thead > tr:first-child > td,
.table > thead:first-child > tr:first-child > td {
  border-top: 0;
}

.table > tbody + tbody {
  border-top: 2px solid #dddddd;
}

.table .table {
  background-color: #ffffff;
}

.table-condensed > thead > tr > th,
.table-condensed > tbody > tr > th,
.table-condensed > tfoot > tr > th,
.table-condensed > thead > tr > td,
.table-condensed > tbody > tr > td,
.table-condensed > tfoot > tr > td {
  padding: 5px;
}

.table-bordered {
  border: 1px solid #dddddd;
}

.table-bordered > thead > tr > th,
.table-bordered > tbody > tr > th,
.table-bordered > tfoot > tr > th,
.table-bordered > thead > tr > td,
.table-bordered > tbody > tr > td,
.table-bordered > tfoot > tr > td {
  border: 1px solid #dddddd;
}

.table-bordered > thead > tr > th,
.table-bordered > thead > tr > td {
  border-bottom-width: 2px;
}

.table-striped > tbody > tr:nth-child(odd) > td,
.table-striped > tbody > tr:nth-child(odd) > th {
  background-color: #f9f9f9;
}

.table-hover > tbody > tr:hover > td,
.table-hover > tbody > tr:hover > th {
  background-color: #f5f5f5;
}


</style>

