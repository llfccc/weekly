<template>
    <div>
        <!--<div>
                <h1 class="title">工作内容</h1>
            </div>-->

        <div class="filter">
            <el-row>
                <el-col :span="4" class="toolbar" style="padding-bottom: 0px;">
                </el-col>
                <el-col :span="16" class="toolbar" style="padding-bottom: 0px;">
                    <span class="demonstration">筛选项目</span>
                    <el-select v-model="filters.project_id" clearable filterable placeholder="项目名">
                        <el-option v-for="item in project_list" :key="item.id" :label="item.project_name" :value="item.id">
                        </el-option>
                    </el-select>
                    <span class="demonstration">筛选时间</span>
                    <el-date-picker v-model="filters.filter_date" type="daterange" align="right" placeholder="选择日期范围" @change='filterDateChange' :picker-options="pickerOptions2">
                    </el-date-picker>
                </el-col>
                <el-col :span="2" class="toolbar" style="padding-bottom: 0px;">

                    <el-button type="primary" v-on:click="get_data">查询</el-button>

                </el-col>
                <el-col :span="4" class="toolbar" style="padding-bottom: 0px;">

                    <el-button type="success" @click="handleAdd">新增</el-button>

                </el-col>
            </el-row>
        </div>

        <el-dialog title="新增" v-model="addFormVisible" :close-on-click-modal="false">
            <el-form ref="insertForm" :model="insertForm" label-width="90px">
                <el-form-item label="项目名称">
                    <el-col :span="12">
                        <el-select v-model="insertForm.dev_event_project_id" clearable filterable placeholder="项目名">
                            <el-option v-for="item in project_list" :key="item.id" :label="item.project_name" :value="item.id">
                            </el-option>
                        </el-select>
                    </el-col>
                    <el-col :span="12">
                        <el-select v-model="insertForm.dev_event_type_id" clearable filterable placeholder="类型">
                            <el-option v-for="item in event_type_list" :key="item.id" :label="item.event_type_name" :value="item.id">
                            </el-option>
                        </el-select>
                    </el-col>
                </el-form-item>

                <el-form-item label="工作内容">
                    <el-input type="textarea" class="form-control" id="description" placeholder="工作内容" v-model="insertForm.description">工作内容
                    </el-input>
                </el-form-item>

                <el-form-item label="工作时间">
                    <span class="demonstration"></span>
                    <el-col :span="12">
                        <el-date-picker v-model="insertForm.event_date" type="date" placeholder="选择日期" @change="dateChange" :picker-options="dateOption">
                        </el-date-picker>
                    </el-col>
                    <el-col :span="12">
                        <el-time-picker label="时间" is-range v-model="insertForm.event_time" range-separator='-' placeholder="选择时间范围" @input="timeChange">
                        </el-time-picker>
                    </el-col>

                </el-form-item>

                <el-form-item label="对接人：">
                    <el-col :span="12">
                        <el-select v-model="insertForm.up_reporter_id" clearable filterable placeholder="上游汇报人">
                            <el-option v-for="item in user_list" :key="item.id" :label="item.chinese_name" :value="item.id">
                            </el-option>
                        </el-select>
                    </el-col>
                    <el-col :span="12">
                        <el-select v-model="insertForm.down_reporter_ids" multiple clearable filterable placeholder="下游交接人">
                            <el-option v-for="item in user_list" :key="item.id" :label="item.chinese_name" :value="item.id">
                            </el-option>
                        </el-select>
                    </el-col>
                </el-form-item>
                <el-form-item label="进度：">
                    <el-col :span="10">
                        <el-input-number id="fin_percentage" default="100" v-model="insertForm.fin_percentage" :step="10" :min="0" :max="100">进度</el-input-number>
                        <!--<el-input type="text" class="form-control" id="fin_percentage" placeholder="进度" v-model="">-->
                        </el-input>
                    </el-col>
                </el-form-item>
                <el-form-item label="备注：">
                    <el-input type="textarea" class="form-control" id="dev_event_remark" placeholder="备注" v-model="insertForm.dev_event_remark">
                        备注
                    </el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="addFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="insertWork" :loading="addLoading">提交</el-button>
            </div>

        </el-dialog>
        <div class="filter">
            <el-table :data="work_list" border style="width: 100%">

                <el-table-column prop="event_date" label="事件日期" width="150" sortable>
                </el-table-column>
                <el-table-column prop="project_name" label="项目名称" width="150" fixed sortable>
                </el-table-column>
                <el-table-column prop="event_type_name" label="类型" width="150" sortable>
                </el-table-column>
                <el-table-column prop="description" label="事件描述" width="150" sortable>
                </el-table-column>
                <el-table-column prop="start_time" label="开始时间" width="150" sortable>
                </el-table-column>
                <el-table-column prop="end_time" label="结束时间" width="150" sortable>
                </el-table-column>
                <el-table-column prop="up_reporter_name" label="上游汇报人" width="190" sortable>
                </el-table-column>

                <el-table-column prop="down_reporter_name" label="下游汇报人" width="190" sortable>
                </el-table-column>

                <el-table-column prop="fin_percentage" label="完成百分比" width='170' sortable>
                </el-table-column>
                <el-table-column prop="dev_event_remark" label="备注" width="150">
                </el-table-column>
                <el-table-column prop="dev_event_id"  label="id" v-show="false" width="150" sortable>
                </el-table-column>
                <el-table-column label="操作" width="110" fixed="right">
                    <template scope="scope">
                        <!--<el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>-->
                        <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        </br>
        </br>
        </br>
        <p>不选日期则取最近一星期的内容</p>
        </br>

        <p>
            <!--<el-button type="primary" @click="handleAdd">下载excel</el-button>-->
            <a href='/works/get_event_excel/'>下载excel(缺参数)</a>
        </p>
        <!--编辑界面-->
        <!--<el-dialog title="编辑" v-model="editFormVisible" :close-on-click-modal="false">
                                                                                            <el-form ref="form" :model="editForm" label-width="80px">
                                                                                                <el-form-item label="工作内容">
                                                                                                    <el-input type="textarea" class="form-control" id="description" placeholder="工作内容" v-model="editForm.description">工作内容
                                                                                                    </el-input>
                                                                                                </el-form-item>

                                                                                                <el-form-item label="工作时间">

                                                                                                    <el-col :span="11" class="block">
                                                                                                        <el-date-picker v-model="editForm.start_time" type="datetime" placeholder="选择日期时间">
                                                                                                        </el-date-picker>
                                                                                                    </el-col>
                                                                                                    <el-col class="line" :span="2">-</el-col>
                                                                                                    <el-col :span="11" class="block">
                                                                                                        <el-date-picker v-model="editForm.end_time" type="datetime" placeholder="选择日期时间">
                                                                                                        </el-date-picker>
                                                                                                    </el-col>
                                                                                                </el-form-item>
                                                                                                <el-form-item label="项目情况：">

                                                                                                    <el-col :span="8">
                                                                                                        <el-input type="text" class="form-control" id="up_reporter_id" placeholder="上游汇报人" v-model="editForm.up_reporter_id">
                                                                                                            工作负责人
                                                                                                        </el-input>
                                                                                                    </el-col>
                                                                                                    <el-col :span="8">
                                                                                                        <el-input type="text" class="form-control" id="down_reporter_ids" placeholder="下游汇报人" v-model="editForm.down_reporter_ids">下游汇报人
                                                                                                        </el-input>

                                                                                                    </el-col>
                                                                                                    <el-col :span="8">
                                                                                                        <el-input type="text" class="form-control" id="fin_percentage" placeholder="进度" v-model="editForm.fin_percentage">进度
                                                                                                        </el-input>
                                                                                                    </el-col>
                                                                                                </el-form-item>
                                                                                            </el-form>
                                                                                            <div slot="footer" class="dialog-footer">
                                                                                                <el-button @click.native="addFormVisible = false">取消</el-button>
                                                                                                <el-button type="primary" @click.native="insertWork" :loading="addLoading">提交修改</el-button>
                                                                                            </div>
                                                                                        </el-dialog>-->

    </div>
</template>

<script>
export default {
    data() {
        return {
            filters: {
                project_id: '',
                filter_date: '',
                start_date: '',
                end_date: '',
            },
            pickerOptions2: {
                shortcuts: [{
                    text: '最近一周',
                    onClick(picker) {
                        const end = new Date();
                        const start = new Date();
                        start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
                        picker.$emit('pick', [start, end]);
                    }
                }, {
                    text: '最近一个月',
                    onClick(picker) {
                        const end = new Date();
                        const start = new Date();
                        start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
                        picker.$emit('pick', [start, end]);
                    }
                }, {
                    text: '最近三个月',
                    onClick(picker) {
                        const end = new Date();
                        const start = new Date();
                        start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
                        picker.$emit('pick', [start, end]);
                    }
                }]
            },
            work_list: [],
            project_list: [],
            event_type_list: [],
            user_list: [],
            dateOption: {
                disabledDate(time) {
                    return time.getTime() < Date.now() - 8.64e7 * 6;
                }
            },
            insertForm: {
                description: '',
                event_date: new Date().getFullYear() + '-' + (new Date().getMonth() + 1) + '-' + new Date().getDate(),
                event_time: '',
                // start_time: '',
                // end_time: '',
                fin_percentage: '100',
                up_reporter_id: '',
                down_reporter_ids: '',
                dev_event_remark: '',
                dev_event_project_id: '',
                dev_event_type_id: '',
                project_name: '',
                // event_type_id: '',
            },
            editForm: {
                description: '',
                start_time: '',
                end_time: '',
                fin_percentage: '',
                up_reporter_ids: '',
                down_reporter_ids: '',
                dev_event_remark: '',
            },
            addFormVisible: false,//新增界面是否显示
            addLoading: false,
            editFormVisible: false,//编辑界面是否显示
            editLoading: false,
            testValue: '',
        }
    },
    created() {
        // 组件创建完后获取数据
        var self=this;
        this.get_data();
        this.get_projects();
        this.get_event_types();
        this.get_users();
        this.defaultData = JSON.parse(JSON.stringify(self.insertForm));
    },
    methods: {
        // projectChange(val){
        //     var self = this;
        //     self.insertForm.dev_event_project_id = val;

        // },
        // event_typeChange(val){
        //     var self = this;
        //     self.insertForm.dev_event_type_id = val;

        // },
        filterDateChange(val) {
            var self = this;
            self.filters.filterDate = val;
        },
        dateChange(val) {
            var self = this;
            self.insertForm.event_date = val
        },

        timeChange(val) {
            var self = this;
            function convertTime(d) {
                var result = d.getHours() + ':' + d.getMinutes() + ':' + d.getSeconds()
                return result
            }
            self.insertForm.start_time = convertTime(val[0])
            self.insertForm.end_time = convertTime(val[1])
        },
        get_users: function (params) {
            var self = this;
            this.$axios.get('/accounts/get_username/')
                .then(function (response) {
                    self.user_list = eval(response.data.content);
                }
                );
        },
        get_data: function (params) {
            var self = this;
            this.$axios.get('/works/get_dev_events/', {
                params: {
                    filter_date: self.filters.filterDate,
                    project_id: self.filters.project_id
                }
            })
                .then(function (response) {
                    self.work_list = eval(response.data.content);

                }
                );
        },
        get_projects: function (params) {
            var self = this;
            this.$axios.get('/works/get_projects/')
                .then(function (response) {
                    self.project_list = eval(response.data.content);

                }
                );
        },
        get_event_types: function (params) {
            var self = this;
            this.$axios.get('/works/get_event_types/')
                .then(function (response) {
                    self.event_type_list = eval(response.data.content);

                }
                );
        },
        insertWork: function () {
            var self = this;
            //后期改用此种方法合成json
            //                    function transToJson(data) {
            //                        // Do whatever you want to transform the data
            //                        let ret = ''
            //                        for (let it in data) {
            //                            ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
            //                        }
            //                        return ret
            //                    }

            let str = 'event_date=' + self.insertForm.event_date + '&start_time=' + self.insertForm.start_time + '&end_time=' + self.insertForm.end_time + '&description=' + self.insertForm.description + '&fin_percentage=' + self.insertForm.fin_percentage + '&up_reporter_id=' + self.insertForm.up_reporter_id + '&down_reporter_ids=' + self.insertForm.down_reporter_ids + '&dev_event_remark=' + self.insertForm.dev_event_remark + '&dev_event_project_id=' + self.insertForm.dev_event_project_id + '&dev_event_type_id=' + self.insertForm.dev_event_type_id;

            this.$axios.post('/works/insert_devevent/', str).then(function (response) {

                if (response.data.code == 0) {
                    self.$message({
                        message: '恭喜你，新增成功',
                        type: 'success'
                    });
                } else {
                    self.$message({
                        message: '插入失败',
                        type: 'error'
                    });
                }
            });
            // window.location.reload();
            this.addFormVisible = false;
            this.get_data()
            var clean_field = ['description', 'event_time','up_reporter_id','dev_event_remark','dev_event_project_id','project_name','dev_event_type_id']
            for (var i = 0; i < clean_field.length; i++) {
                self.insertForm[clean_field[i]] = '';
            }
            self.insertForm['fin_percentage'] = 100
            //delete self.insertForm['down_reporter_ids'];

        },

        handleDelete: function (index, row) {
            var self = this;
            this.$axios.get('/works/del_devevent/', {
                params: {
                    delID: row.dev_event_id,
                }
            })
                .then(function (response) {
                    if (response.data.code == 0) {
                        self.get_data()
                        self.$message({
                            message: '恭喜你，删除成功',
                            type: 'success'
                        });
                    } else {
                        self.$message({
                            message: '删除失败',
                            type: 'error'
                        });
                    }

                }
                );

        },
        // handleEdit: function (index, row) {
        //     this.editFormVisible = true;
        //     this.editForm = Object.assign({}, row);
        // },
        handleAdd: function () {
            this.addFormVisible = true;
            // this.addForm = {
            //     name: '',
            //     sex: -1,
            //     age: 0,
            //     birth: '',
            //     addr: ''
            // };
        },
        get_event_excel: function () {
            var self = this;
            this.$axios.get('/works/get_event_excel /', {
                params: {
                    filter_date: self.filters.filterDate,
                    project_id: self.filters.project_id
                }
            })
                .then(function (response) {
                    self.work_list = eval(response.data.content);
                }
                );
        },
    },
}
</script>
<style scoped>
.title {
    margin: 0 auto;
    text-align: center;
    margin: 5px 0
}

.filter {
    margin-top: 40px
}
.hidden {
  display: none;
}
</style>
