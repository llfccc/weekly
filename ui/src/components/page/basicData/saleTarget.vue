<template>
  <div>
        未完成
      <div>
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" :model="filters">
          <el-col :span="7">
            <span class="demonstration">时间：</span>
            <el-date-picker v-model="filters.filter_date" type="week" format="yyyy-WW 周" @change="dateChange1" placeholder="选择周">
            </el-date-picker>
          </el-col>

          <el-col :span="6">
            <span class="demonstration">员工：</span>
            <el-select v-model="filters.employee_name" clearable filterable placeholder="员工名">
              <el-option v-for="item in filter_user_list" :key="item.id" :label="item.chinese_name" :value="item.chinese_name">
              </el-option>
            </el-select>
          </el-col>
          <el-col :span="8">
            <el-button type="primary" v-on:click="filter">查询</el-button>
          </el-col>
        </el-form>
      </el-col>
      </br>
      </br>
      </br>
      </br>

   <table border="1" class="table table-responsive table-bordered" width="100%" v-show="sale_target">
        <thead>
          <tr>
            <th>自然周</th>
                        <th>目标所属人 </th>
            <th>阶段名称 </th>
            <th>目标 </th>
            <th>最大拜访次数 </th>
            <th>销售目标备注 </th>

          </tr>
        </thead>
        <tbody>
          <tr v-for="item in sale_target">
             <td width="10%" :class="{hidden: true}">{{item.id}}</td>
            <td width="9%" :rowspan="item.span" :class="{hidden: item.dis}">{{item.natural_week}}</td>
          <td width="15%" :rowspan="item.span2" :class="{hidden: item.dis2}">{{item.sale_target_owner__chinese_name}}</td>
          <td width="8%">{{item.phase_name__phase_name}}</td>

            <td width="10%">{{item.target}}</td>
       <td width="8%">{{item.phase_count}}</td>
            <td width="20%">{{item.sale_target_remark}}</td>
          </tr>
        </tbody>
      </table>
    </div>
      </div>
</template>
<script>
export default {
    data() {
        return {
                sale_target:'',
                user_list: '',
             filters: {
        filter_date: '',
        employee_name: '',
        naturalWeek: '',
      },
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
    created() {
                this.get_users();
        this.get_sale_target();
    },
    methods: {
            dateChange1(val) {
      var self = this;
      self.filters.naturalWeek = val
    },
        handleEdit: function (index, row) {
            this.editFormVisible = true;
            this.editForm = Object.assign({}, row);
        },
            filter: function (params) {
      this.sale_target = [];
      this.get_sale_target();
    },
            get_users: function (params) {
      var self = this;
      this.$axios.get('/accounts/get_username/')
        .then(function (response) {
          self.user_list = eval(response.data.content);
        }
        );

    },
         get_sale_target: function (params) {
      var self = this;
//      var employee_name = localStorage.getItem("ms_username")
      this.$axios.get('/analysis/display_sale_target/', {
        params: {
          natural_week: self.filters.naturalWeek,
//          employee_name: employee_name,
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
                if (list[k]["natural_week"] == list[i]["natural_week"] && list[k]["natural_week"] != '') {
                  list[k]['span']++;
                  list[k]['dis'] = false;
                  list[i]['span'] = 1;
                  list[i]['dis'] = true;
                } else {
                  break;
                }
              }
              k = i;
            }
            return list;
          }
                    function combineCell2(list) {
            var k = 0;
            while (k < list.length) {
              list[k]['span2'] = 1;
              list[k]['dis2'] = false;
              for (var i = k + 1; i <= list.length - 1; i++) {
                if (list[k]["sale_target_owner__chinese_name"] == list[i]["sale_target_owner__chinese_name"] && list[k]["sale_target_owner__chinese_name"] != '') {
                  list[k]['span2']++;
                  list[k]['dis2'] = false;
                  list[i]['span2'] = 1;
                  list[i]['dis2'] = true;
                } else {
                  break;
                }
              }
              k = i;
            }
            return list;
          }
          self.sale_target = combineCell2(combineCell(responseContent))
            console.log(self.sale_target)
        }
        );
    },
    },
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

