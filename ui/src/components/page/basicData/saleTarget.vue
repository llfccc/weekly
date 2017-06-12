<template>
  <div>
        未完成
      {{name}}
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
                name: '标题',
        }
    },
    created() {
        // 组件创建完后获取数据，这里和1.0不一样，改成了这个样子
//        this.get_data()
//        this.get_projects()
//        this.get_event_types()
//        this.get_sale_event_types()
    },
    methods: {
        handleEdit: function (index, row) {
            this.editFormVisible = true;
            this.editForm = Object.assign({}, row);
        },
         get_sale_events: function (params) {
      var self = this;
//      var employee_name = localStorage.getItem("ms_username")
      this.$axios.get('/analysis/display_sale_target/', {
        params: {
          natural_week: self.filters.naturalWeek,
//          employee_name: employee_name,
        }
      })
        .then(function (response) {
//          var responseContent = JSON.parse(response.data.content);
//          function combineCell(list) {
//            var k = 0;
//            while (k < list.length) {
//              list[k]['span'] = 1;
//              list[k]['dis'] = false;
//              for (var i = k + 1; i <= list.length - 1; i++) {
//                if (list[k]["visit_date"] == list[i]["visit_date"] && list[k]["visit_date"] != '') {
//                  list[k]['span']++;
//                  list[k]['dis'] = false;
//                  list[i]['span'] = 1;
//                  list[i]['dis'] = true;
//                  // list[k]['total_time'] += list[i]['duration_time'];
//                } else {
//                  break;
//                }
//              }
//              k = i;
//            }
//            return list;
//          }
//          self.sale_event_list = combineCell(responseContent)
            self.sale_target=response.data.content;
            console.log(self.sale_target)
        }
        );
    },
    },
}
</script>
