<template>
  <div>
    <h1 class="logo">工作内容</h1>
    <el-form ref="form" :model="form" label-width="80px" width="600px">

      <el-form-item label="工作内容">
        <el-input type="textarea" class="form-control" id="work_title" placeholder="工作内容"
                  v-model="form.work_title">工作内容
        </el-input>
      </el-form-item>

      <el-form-item label="工作时间">
        <el-col :span="11" class="block">
          <el-date-picker
            v-model="form.start_time"
            type="datetime"
            placeholder="选择日期时间">
          </el-date-picker>
        </el-col>
        <el-col class="line" :span="2">-</el-col>
        <el-col :span="11" class="block">
          <el-date-picker
            v-model="form.end_time"
            type="datetime"
            placeholder="选择日期时间">
          </el-date-picker>
        </el-col>

      </el-form-item>
      <el-form-item label="项目进度">

        <el-col :span="8">
          <el-input type="text" class="form-control" id="job_manager" placeholder="工作负责人" v-model="form.job_manager">
            工作负责人
          </el-input>
        </el-col>
        <el-col :span="8">
          <el-input type="text" class="form-control" id="work_auditor" placeholder="工作审核人"
                    v-model="form.work_auditor">工作审核人
          </el-input>

        </el-col>
                <el-col :span="8">
          <el-input type="text" class="form-control" id="complete_status" placeholder="进度"
                    v-model="form.complete_status">进度
          </el-input>
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
        width="80">
      </el-table-column>
      <!--<el-table-column-->
      <!--prop="id"-->
      <!--label="选择"-->
      <!--width="80">-->
      <!--</el-table-column>-->
      <el-table-column
        prop="work_title"
        label="id"
        width="380">
      </el-table-column>
      <el-table-column
        prop="start_time"
        label="开始时间"
        width="180">
      </el-table-column>
      <el-table-column
        prop="end_time"
        label="结束时间"
        width="180">
      </el-table-column>
      <el-table-column
        prop="complete_status"
        label="进度"
        width="70">
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
        form: {
          work_title: '',
          start_time: '',
          end_time: '',
          complete_status: '',
          job_manager: '',
          work_auditor: '',
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

        function convertDatetime(d) {
          var result = d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate() + ' ' + d.getHours() + ':' + d.getMinutes() + ':' + d.getSeconds();
          return result;
        }
        if (start_time){
                    var start_time = convertDatetime(v.form.start_time);
        }else{
            var start_time=''
        }
        if(end_time){
                    var end_time = convertDatetime(v.form.end_time);
        }else{
            var end_time=''
        }

        if (~isNaN(v.form.id) && v.form.work_title !== null) {   //有错误
          let str = 'start_time=' + start_time + '&end_time=' + end_time + '&work_title=' + v.form.work_title + '&complete_status=' + v.form.complete_status+'&job_manager='+v.form.job_manager+'&work_auditor='+v.form.work_auditor;
//          let workStr = {id: v.form.id, work_title: v.form.work_title,starttime:v.form.starttime}
          this.$http.post('/api/insert_work/', str).then(function (response) {
            console.log(response.data.content);
            v.form.push(v.form);
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
