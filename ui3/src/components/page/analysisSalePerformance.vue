<template>
  <!--为echarts准备一个具备大小的容器dom-->
  <div>
  
    <div>
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
  
        <el-form :inline="true" :model="filters">
          <el-col :span="18">
            <el-button type="primary" v-on:click="lastWeek">上一周（未完成）</el-button>       
            <span class="demonstration">筛选时间</span>
            <el-date-picker v-model="filters.filter_date" type="week" format="yyyy-WW 周" @change="dateChange1" placeholder="选择周">
            </el-date-picker>
                 <el-button type="primary" v-on:click="nextWeek">下一周（未完成）</el-button>
          </el-col>
  
          <el-col :span="6">
            <el-button type="primary" v-on:click="filter">筛选</el-button>
  
          </el-col>
  
        </el-form>
      </el-col>
      <div data-v-17064ad0="" class="el-table el-table--fit el-table--striped el-table--enable-row-hover el-table--enable-row-transition" style="width: 100%;">
        <div class="hidden-columns">
          <div data-v-17064ad0=""></div>
          <div data-v-17064ad0=""></div>
          <div data-v-17064ad0=""></div>
          <div data-v-17064ad0=""></div>
          <div data-v-17064ad0=""></div>
          <div data-v-17064ad0=""></div>
          <div data-v-17064ad0=""></div>
          <div data-v-17064ad0=""></div>
          <div data-v-17064ad0=""></div>
          <div data-v-17064ad0=""></div>
          <div data-v-17064ad0=""></div>
        </div>
        <div class="el-table__header-wrapper">
          <table cellspacing="0" cellpadding="0" border="0" class="el-table__header" style="width: 1042px;">
            <!--<colgroup>
                  <col name="el-table_1_column_1" width="80">
                  <col name="el-table_1_column_2" width="100">
                  <col name="el-table_1_column_3" width="100">
                  <col name="el-table_1_column_4" width="133">
                  <col name="el-table_1_column_5" width="133">
                  <col name="el-table_1_column_6" width="133">
                  <col name="el-table_1_column_7" width="133">
                  <col name="gutter" width="">
                </colgroup>-->
            <thead>
              <tr>
                <th colspan="1" rowspan="2" class="el-table_1_column_1 is-leaf">
                  <div class="cell">姓名</div>
                </th>
                <th colspan="2" rowspan="1" class="el-table_1_column_2 is-leaf">
                  <div class="cell">A</div>
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
          <table cellspacing="0" cellpadding="0" border="0" class="el-table__body" style="width: 1042px;">
            <colgroup>
              <col name="el-table_1_column_1" width="80">
              <col name="el-table_1_column_1" width="80">
              <col name="el-table_1_column_2" width="80">
              <col name="el-table_1_column_1" width="80">
              <col name="el-table_1_column_1" width="80">
              <col name="el-table_1_column_2" width="80">
              <col name="el-table_1_column_1" width="80">
              <col name="el-table_1_column_1" width="80">
              <col name="el-table_1_column_2" width="80">
  
            </colgroup>
            <tbody>
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
  <style type="text/css">
#yddContainer {
  display: block;
  font-family: Microsoft YaHei;
  position: relative;
  width: 100%;
  height: 100%;
  top: -4px;
  left: -4px;
  font-size: 12px;
  border: 1px solid
}

#yddTop {
  display: block;
  height: 22px
}

#yddTopBorderlr {
  display: block;
  position: static;
  height: 17px;
  padding: 2px 28px;
  line-height: 17px;
  font-size: 12px;
  color: #5079bb;
  font-weight: bold;
  border-style: none solid;
  border-width: 1px
}

#yddTopBorderlr .ydd-sp {
  position: absolute;
  top: 2px;
  height: 0;
  overflow: hidden
}

.ydd-icon {
  left: 5px;
  width: 17px;
  padding: 0px 0px 0px 0px;
  padding-top: 17px;
  background-position: -16px -44px
}

.ydd-close {
  right: 5px;
  width: 16px;
  padding-top: 16px;
  background-position: left -44px
}

#yddKeyTitle {
  float: left;
  text-decoration: none
}

#yddMiddle {
  display: block;
  margin-bottom: 10px
}

.ydd-tabs {
  display: block;
  margin: 5px 0;
  padding: 0 5px;
  height: 18px;
  border-bottom: 1px solid
}

.ydd-tab {
  display: block;
  float: left;
  height: 18px;
  margin: 0 5px -1px 0;
  padding: 0 4px;
  line-height: 18px;
  border: 1px solid;
  border-bottom: none
}

.ydd-trans-container {
  display: block;
  line-height: 160%
}

.ydd-trans-container a {
  text-decoration: none;
}

#yddBottom {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 22px;
  line-height: 22px;
  overflow: hidden;
  background-position: left -22px
}

.ydd-padding010 {
  padding: 0 10px
}

#yddWrapper {
  color: #252525;
  z-index: 10001;
  background: url(chrome-extension://eopjamdnofihpioajgfdikhhbobonhbb/ab20.png);
}

#yddContainer {
  background: #fff;
  border-color: #4b7598
}

#yddTopBorderlr {
  border-color: #f0f8fc
}

#yddWrapper .ydd-sp {
  background-image: url(chrome-extension://eopjamdnofihpioajgfdikhhbobonhbb/ydd-sprite.png)
}

#yddWrapper a,
#yddWrapper a:hover,
#yddWrapper a:visited {
  color: #50799b
}

#yddWrapper .ydd-tabs {
  color: #959595
}

.ydd-tabs,
.ydd-tab {
  background: #fff;
  border-color: #d5e7f3
}

#yddBottom {
  color: #363636
}

#yddWrapper {
  min-width: 250px;
  max-width: 400px;
}
</style>