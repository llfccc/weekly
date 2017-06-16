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
          <tr v-for="item in sale_target">
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

    </div>

         <el-table :data="sale_target" stripe style="width: 100%">
          <el-table-column prop="natural_week" label="自然周" width="180">
          </el-table-column>
          <el-table-column prop="phase_name" label="阶段名称">
          </el-table-column>
          <el-table-column prop="target" label="目标" width="180">
          </el-table-column>
          <el-table-column prop="phase_count" label="最大拜访次数">
          </el-table-column>
          <el-table-column prop="sale_target_remark" label="备注">
          </el-table-column>

        </el-table>
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

//        this.get_event_types()
//        this.get_sale_event_types()
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
            self.sale_target=response.data.content;
            console.log(self.sale_target)
        }
        );
    },
    },
}
</script>
