<template>
  <!--为echarts准备一个具备大小的容器dom-->
  <div>
    <!--<h1 class="title" style="align:center;">销售业绩分析</h1>-->
    <div>
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">

        <el-form :inline="true" :model="filters">
          <el-col :span="8">
            <!--<el-button type="primary" v-on:click="lastWeek">上一周（未完成）</el-button>-->
            <span class="demonstration">筛选时间</span>
            <el-date-picker v-model="filters.filter_date" type="week" format="yyyy-WW 周" @change="dateChange1" placeholder="选择周">
            </el-date-picker>
            <!--<el-button type="primary" v-on:click="nextWeek">下一周（未完成）</el-button>-->
          </el-col>

          <el-col :span="6">
            <el-button type="primary" v-on:click="filter">筛选</el-button>

          </el-col>
        </el-form>
      </el-col>
      </br>

      </br>
      </br>
      </br>
      <div data-v-17064ad0="" class="el-table el-table--fit el-table--striped el-table--enable-row-hover el-table--enable-row-transition">
        <div class="el-table__header-wrapper">
          <table cellspacing="0" cellpadding="0" border="0" class="el-table__header" style="width: 100%;">
            <thead>
              <tr>
                <th colspan="1" rowspan="2" class="el-table_1_column_1 is-leaf">
                  <div class="cell">姓名</div>
                </th>

                <th colspan="2" rowspan="1" class="el-table_1_column_3 is-leaf">
                  <div class="cell">B</div>
                </th>
                <th colspan="2" rowspan="1" class="el-table_1_column_4 is-leaf">
                  <div class="cell">C</div>
                </th>
                <th colspan="2" rowspan="1" class="el-table_1_column_5 is-leaf">
                  <div class="cell">D</div>
                </th>
                <th colspan="2" rowspan="1" class="el-table_1_column_6 is-leaf">
                  <div class="cell">E</div>
                </th>
                <th colspan="2" rowspan="1" class="el-table_1_column_7 is-leaf">
                  <div class="cell">F</div>
                </th>
                <th colspan="2" rowspan="1" class="el-table_1_column_2 is-leaf">
                  <div class="cell">G</div>
                </th>
                <th class="gutter" style="width: 0px;"></th>
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
              </tr>
            </thead>
          </table>
        </div>
        <div class="el-table__body-wrapper">
          <table cellspacing="0" cellpadding="0" border="0" class="el-table__body" style="width: 100%">

            <tbody>
              <tr v-for="item in sale_performance_list">
                <td> {{item.chinese_name}}</td>
                <td> {{item.B}}</td>
                <td> {{item.target_B}}</td>
                <td> {{item.C}}</td>
                <td> {{item.target_C}}</td>
                <td> {{item.D}}</td>
                <td> {{item.target_D}}</td>
                <td> {{item.E}}</td>
                <td> {{item.target_E}}</td>
                <td> {{item.F}}</td>
                <td> {{item.target_F}}</td>
                <td> {{item.G}}</td>
                <td> {{item.target_G}}</td>
                <!--<td> {{item.G}}</td>
                                <td> {{item.target_G}}</td>-->
              </tr>
            </tbody>
          </table>

        </div>

        <div class="el-table__column-resize-proxy" style="display: none;"></div>
        <div class="resize-triggers">
          <div class="expand-trigger">
            <div style="width: 1043px; height: 102px;"></div>
          </div>
          <div class="contract-trigger"></div>
        </div>
      </div>

      <!--<table border="2" class="am-table am-table-striped am-table-hover am-table-compact am-table-centered  am-text-nowrap">
              <tr>
                <th rowspan="2">姓名 </th>
                <th colspan="2">A </th>
                <th colspan="2">B </th>
                <th colspan="2">C </th>
                <th colspan="2">D </th>
                <th colspan="2">E </th>
                <th colspan="2">F </th>
                <!--<th colspan="2">G </th>
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

              </tr>
              <tr v-for="item in sale_performance_list">
                <td> {{item.chinese_name}}</td>
                <td> {{item.A}}</td>
                <td> {{item.target_A}}</td>
                <td> {{item.B}}</td>
                <td> {{item.target_B}}</td>
                <td> {{item.C}}</td>
                <td> {{item.target_C}}</td>
                <td> {{item.D}}</td>
                <td> {{item.target_D}}</td>
                <td> {{item.E}}</td>
                <td> {{item.target_E}}</td>
                <td> {{item.F}}</td>
                <td> {{item.target_F}}</td>
                <!--<td> {{item.G}}</td>
                                <td> {{item.target_G}}</td>
              </tr>
            </table>
            <table id="table"></table>-->

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

  </div>
</template>
<script>
import echarts from 'echarts'
export default {
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
      this.sale_performance_list = [];
      this.analysis_sale_performance();
      // this.get_summary();
    },
    lastWeek: function (params) {
    },
    nextWeek: function (params) {
    },
    analysis_sale_performance: function (params) {
      var self = this;
      console.log(self.filters.naturalWeek)
      this.$axios.get('/analysis/analysis_sale_performance/', {
        params: {
          natural_week: self.filters.naturalWeek,
          // employee_name: self.filters.employee_name,
        }
      })
        .then(function (response) {
          var responseContent = JSON.parse(response.data.content);
          self.sale_performance_list = responseContent
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
.title {
  text-align: center;
  margin: 5px 0 40px 0;
}
th{
  text-align: center;

}
td {
  text-align: center;

}
</style>
