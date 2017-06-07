<template>
  <!--为echarts准备一个具备大小的容器dom-->
  <div>
    <h1 class="title" style="align:center;">周拜访分析</h1>
    <div>
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" :model="filters">
          <el-col :span="8">
            <span class="demonstration">筛选时间</span>
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


      <el-table :data="sale_event_list" stripe style="width: 100%">
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
      </el-table>
  
    </div>
    </br>
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
      sale_event_list: [],
      filters: {
        filter_date: '',
        employee_name: '',
        naturalWeek: '',
      },
      summary: '',
      user_list: [],
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
      console.log(self.filters.naturalWeek)
      this.$axios.get('/analysis/display_sale_event/', {
        params: {
          filter_date: self.filters.naturalWeek,
          employee_name: self.filters.employee_name,
        }
      })
        .then(function (response) {
          var responseContent = JSON.parse(response.data.content);
          self.sale_event_list = responseContent
          console.log(responseContent)

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
          console.log(self.summary)
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
</style>