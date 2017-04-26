<template>
  <div>
    <h1 class="logo">工作内容</h1>
    <el-form style="width: 1000px;">
      <el-form-item label="活动名称" prop="name">
        <el-col :span="5">
          <el-input type="text" class="form-control" id="work_id" placeholder="work_id" v-model="new_work.id">序号
          </el-input>
        </el-col>
        <el-col :span="5">
          <el-input type="text" class="form-control" id="work_title" placeholder="work_title"
                    v-model="new_work.work_title">工作内容
          </el-input>
        </el-col>
      </el-form-item>
      <el-form-item label="报名时间" required style="width: 750px;">
        <el-col :span="5">
          <el-form-item prop="signStartTimeDate">
            <el-date-picker
              v-model="ruleForm.signStartTimeDate"
              type="date"
              placeholder="报名开始日期">
            </el-date-picker>
          </el-form-item>
        </el-col>

        <el-col :span="5">
          <el-form-item prop="signStartTimeTime">
            <el-time-select
              placeholder="请选择时间点"
              v-model="ruleForm.signStartTimeTime"
              :picker-options="{start: '00:00',step: '00:15', end: '23:45'}">
            </el-time-select>
          </el-form-item>
        </el-col>

        <el-col :span="1" style="text-align: center;">—</el-col>

        <el-col :span="5">
          <el-form-item prop="signEndTimeDate">
            <el-date-picker
              v-model="ruleForm.signEndTimeDate"
              type="date"
              placeholder="报名结束日期">
            </el-date-picker>
          </el-form-item>
        </el-col>

        <el-col :span="5">
          <el-form-item prop="signEndTimeTime">
            <el-time-select
              placeholder="请选择时间点"
              v-model="ruleForm.signEndTimeTime"
              :picker-options="{start: '00:00',step: '00:15',end: '23:45'}">
            </el-time-select>
          </el-form-item>
        </el-col>
      </el-form-item>

      <el-form-item>
        <el-col :span="5">
          <el-button @click="addWork" class="js-add btn btn-default" type="button">添加工作内容!</el-button>
        </el-col>
      </el-form-item>
    </el-form>


    <el-table :data="work_lists" border stripe style="width: 100%">
      <el-table-column
        prop="name"
        label="选择"
        width="100">
      </el-table-column>
      <el-table-column
        prop="id"
        label="选择"
        width="80">
      </el-table-column>
      <el-table-column
        prop="work_title"
        label="id"
        width="380">
      </el-table-column>
      <el-table-column
        prop="name"
        label="操作"
        width="180">
      </el-table-column>

      <!--<td>-->
      <!--<el-button @click="delWork($event)" v-bind:hidedID="job.id" class="js-add btn btn-default" type="button">-->
      <!--Hide!-->
      <!--</el-button>-->
      <!--</td>-->
    </el-table>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        work_lists: '',
        new_work: {
          id: '',
          work_title: '',
        }
      }
    },
    created () {
      // 组件创建完后获取数据，这里和1.0不一样，改成了这个样子
      this.get_data()
    },
    methods: {
      get_data: function (params) {
        var v = this;
        this.$http.get('/api/get_works/')
          .then(function (response) {
              v.work_lists = eval(response.data.content);
            }
          );
      },
      addWork: function () {
        var v = this;
        if (~isNaN(v.new_work.id) && v.new_work.work_title !== null) {   //有错误
          let str = 'id=' + v.new_work.id + '&work_title=' + v.new_work.work_title;
          let workStr = {id: v.new_work.id, work_title: v.new_work.work_title}
          this.$http.post('/api/insert_work/', str).then(function (response) {
            console.log(response.data.content);
            v.work_lists.push(v.new_work);
            v.$message({
              message: '恭喜你，新增成功',
              type: 'success'
            });
          });
        }
      },
      delWork: function (e) {
        hidedid = e.currentTarget.getAttribute('hidedid');
        $.ajax({
          type: "POST",
          url: '/api/hide_work/',
          data: {hidedid: hidedid}, /* 注意参数的格式和名称 */
          dataType: "json",
          success: function (result) {
            this.jobs.push(this.new_work);
            console.log(response);
          }
        });
      }
      ,
    },
  }
</script>
