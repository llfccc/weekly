<template>
    <div>
        <h1 class="logo">工作内容</h1>
        <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
            <el-form :inline="true" :model="filters">
                <el-form-item>
                    <el-input v-model="filters.name" placeholder="姓名"></el-input>
                </el-form-item>
                <!--<el-form-item>
                              <el-button type="primary" v-on:click="getUsers">查询</el-button>
                          </el-form-item>-->
                <el-form-item>
                    <el-button type="primary" @click="handleAdd">新增</el-button>
                </el-form-item>
            </el-form>
        </el-col>

        <el-dialog title="新增" v-model="addFormVisible" :close-on-click-modal="false">
            <el-form ref="form" :model="form" label-width="90px">
                <el-form-item label="工作内容">
                    <el-input type="textarea" class="form-control" id="work_title" placeholder="工作内容"
                              v-model="form.work_title">工作内容
                    </el-input>
                </el-form-item>

                <el-form-item label="工作时间">
                    <el-col :span="11" class="block">
                        <el-date-picker v-model="form.start_time" type="datetime" placeholder="选择日期时间">
                        </el-date-picker>
                    </el-col>
                    <el-col class="line" :span="2">-</el-col>
                    <el-col :span="11" class="block">
                        <el-date-picker v-model="form.end_time" type="datetime" placeholder="选择日期时间">
                        </el-date-picker>
                    </el-col>
                </el-form-item>
                <el-form-item label="其他：">
                    <el-col :span="8">
                        <el-input type="text" class="form-control" id="job_manager" placeholder="工作负责人"
                                  v-model="form.job_manager">
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
                                <el-form-item label="其他：">
                                     <el-input type="textarea" class="form-control" id="remark" placeholder="备注" v-model="form.remark">
                                         备注
                                     </el-input>
                                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="addFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="addWork" :loading="addLoading">提交</el-button>
            </div>

        </el-dialog>
        <el-table :data="work_lists" border style="width: 100%" max-height="340">
            <el-table-column prop="work_title" label="工作内容" fixed sortable>
            </el-table-column>
            <el-table-column prop="start_time" label="开始时间" fixed sortable>
            </el-table-column>
                        <el-table-column prop="end_time" label="结束时间" fixed sortable>
            </el-table-column>
            <el-table-column prop="job_manager" label="工作负责人" fixed sortable>
            </el-table-column>

            <el-table-column prop="work_auditor" label="工作审核人" fixed sortable>
            </el-table-column>


            <el-table-column prop="complete_status" label="进度"   width='120' sortable>
            </el-table-column>
                        <el-table-column prop="remark" label="备注" width='120' >
            </el-table-column>

            <el-table-column label="操作" width="180">
                <template scope="scope">
                    <el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                    <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <!--编辑界面-->
        <el-dialog title="编辑" v-model="editFormVisible" :close-on-click-modal="false">
            <el-form ref="form" :model="form" label-width="80px">
                <el-form-item label="工作内容">
                    <el-input type="textarea" class="form-control" id="work_title" placeholder="工作内容"
                              v-model="form.work_title">工作内容
                    </el-input>
                </el-form-item>

                <el-form-item label="工作时间">
                    <el-col :span="11" class="block">
                        <el-date-picker v-model="form.start_time" type="datetime" placeholder="选择日期时间">
                        </el-date-picker>
                    </el-col>
                    <el-col class="line" :span="2">-</el-col>
                    <el-col :span="11" class="block">
                        <el-date-picker v-model="form.end_time" type="datetime" placeholder="选择日期时间">
                        </el-date-picker>
                    </el-col>
                </el-form-item>
                <el-form-item label="项目情况：">

                    <el-col :span="8">
                        <el-input type="text" class="form-control" id="job_manager" placeholder="工作负责人"
                                  v-model="form.job_manager">
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
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="addFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="addWork" :loading="addLoading">提交修改</el-button>
            </div>

        </el-dialog>

    </div>
</template>

<script>
    export default {
        data() {
            return {
                filters: {
                    name: ''
                },
                work_lists: [],
                form: {
                    work_title: '',
                    start_time: '',
                    end_time: '',
                    complete_status: '',
                    job_manager: '',
                    work_auditor: '',
                    remark: '',
                },
                addFormVisible: false,//新增界面是否显示
                addLoading: false,
                editFormVisible: false,//编辑界面是否显示
                editLoading: false,
                //新增界面数据
                addForm: {
                    name: '',
                    sex: -1,
                    age: 0,
                    birth: '',
                    addr: ''
                },
            }
        },
        created() {
            // 组件创建完后获取数据，这里和1.0不一样，改成了这个样子
            this.get_data()
        },
        methods: {
            get_data: function (params) {
                var v = this;
                this.$axios.get('/works/get_works/')
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

                if (v.form.start_time) {
                    var start_time = convertDatetime(v.form.start_time);
                } else {
                    var start_time = ''
                }
                if (v.form.end_time) {
                    var end_time = convertDatetime(v.form.end_time);
                } else {
                    var end_time = ''
                }

//后期改用此种方法合成json
//                    function transToJson(data) {
//                        // Do whatever you want to transform the data
//                        let ret = ''
//                        for (let it in data) {
//                            ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
//                        }
//                        return ret
//                    }
//                    console.log(transToJson(v.form));
                    let str = 'start_time=' + start_time + '&end_time=' + end_time + '&work_title=' + v.form.work_title + '&complete_status=' + v.form.complete_status + '&job_manager=' + v.form.job_manager + '&work_auditor=' + v.form.work_auditor+'&remark=' + v.form.remark;
                    this.$axios.post('/works/insert_work/', str).then(function (response) {
                        console.log(response.data.content);
                        v.work_lists.push(v.form);
                        v.$message({
                            message: '恭喜你，新增成功',
                            type: 'success'
                        });
                    });
                    //this.$refs['addForm'].resetFields();
                    this.addFormVisible = false;
                    this.get_data();

            },

            delWork: function (e) {
                hidedid = e.currentTarget.getAttribute('hidedid');
                // $.ajax({
                //   type: "POST",
                //   url: '/api/hide_work/',
                //   data: {hidedid: hidedid}, /* 注意参数的格式和名称 */
                //   dataType: "json",
                //   success: function (result) {
                //     this.jobs.push(this.new_work);
                //     console.log(response);
                //   }
                // });
            },
            handleEdit: function (index, row) {
                this.editFormVisible = true;
                this.form = Object.assign({}, row);
            },
            handleAdd: function () {
                this.addFormVisible = true;
                this.addForm = {
                    name: '',
                    sex: -1,
                    age: 0,
                    birth: '',
                    addr: ''
                };
            },
        },
    }
</script>
