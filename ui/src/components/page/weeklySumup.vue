<template>
    <div>
        <el-button type="primary" @click="handleAdd">新增</el-button>
        <el-table :data="summary_list" border style="width: 100%">
            <el-table-column prop="id" style="display:none" label="id" width="150" sortable>
            </el-table-column>
            <el-table-column prop="start_date" label="开始时间" width="150" fixed sortable>
            </el-table-column>
            <el-table-column prop="end_date" label="结束时间" width="150" sortable>
            </el-table-column>
            <el-table-column prop="summary" label="总结" width="150" sortable>
            </el-table-column>
            <el-table-column prop="self_evaluation" label="自我评价" width="150" sortable>
            </el-table-column>
            <el-table-column prop="plan" label="计划" width="150" sortable>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
                <template scope="scope">
                    <el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                    <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
    
        <el-dialog title="新增" v-model="addFormVisible" :close-on-click-modal="false">
            <el-form ref="insertForm" :model="insertForm" label-width="90px">
    
                <el-form-item label="时间范围:">
                    <div class="block">
                        <span class="demonstration"></span>
                        <el-date-picker v-model="insertForm.start_date" align="right" type="date" placeholder="开始日期" format="yyyy-MM-dd" @change="dateChange1">
                        </el-date-picker>
                        <el-date-picker v-model="insertForm.end_date" align="right" type="date"  placeholder="结束日期" format="yyyy-MM-dd" @change="dateChange2">
                        </el-date-picker>
                    </div>
    
                </el-form-item>
                <el-form-item label="总结：">
                    <el-input type="textarea" class="form-control" id="summary" placeholder="总结" v-model="insertForm.summary">
                        总结
                    </el-input>
                </el-form-item>
                <el-form-item label="自我评价：">
                    <el-input type="textarea" class="form-control" id="self_evaluation" placeholder="自我评价" v-model="insertForm.self_evaluation">
                        总结
                    </el-input>
                </el-form-item>
                <el-form-item label="计划：">
                    <el-input type="textarea" class="form-control" id="plan" placeholder="计划" v-model="insertForm.plan">
                        总结
                    </el-input>
                </el-form-item>
    
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="addFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="insertSummary" :loading="addLoading">提交</el-button>
            </div>
            <div>
                <p>**每个内容最多500字符 </p>
            </div>
        </el-dialog>
    </div>
</template>
<script>
export default {
    data() {
        return {
            name: '标题',
            addFormVisible: false,
            summary_list: [],
            filters: {
                project_name: '',
                filter_date: '',
                start_date: '',
                end_date: '',
            },
            addLoading: false,
            insertForm: {
                start_date: '',
                end_date: new Date().getFullYear() + '-' + (new Date().getMonth() + 1) + '-' + new Date().getDate(),
                summary:'',
                plan:'',
                self_evaluation:'',

            },
        }
    },
    created() {
        // 组件创建完后获取数据，这里和1.0不一样，改成了这个样子
        this.get_weekly()
        // this.get_projects()
        // this.get_event_types()
        // this.get_sale_event_types()
    },
    methods: {
        dateChange1(val) {
            var v = this;
            v.insertForm.start_date = val

        },
        dateChange2(val) {
            var v = this;
            v.insertForm.end_date = val

        },
        get_weekly: function (params) {
            var v = this;
            this.$axios.get('/works/get_weekly_summary/', {
                params: {
                    filterDate: v.filters.filterDate,
                    project_name: v.filters.project_name
                }
            })
                .then(function (response) {
                    v.summary_list = eval(response.data.content);
                    console.log(v.summary_list);
                }
                );
        },
        insertSummary: function () {
            var v = this;
            console.log(v.insertForm);
            let str = 'start_date=' + v.insertForm.start_date + '&end_date=' + v.insertForm.end_date + '&summary=' + v.insertForm.summary + '&self_evaluation=' + v.insertForm.self_evaluation + '&plan=' + v.insertForm.plan;
            this.$axios.post('/works/insert_summary/', str).then(function (response) {

                if (response.data.code == 0) {

                    v.$message({
                        message: '恭喜你，新增成功',
                        type: 'success'
                    });
                } else {
                    v.$message({
                        message: '插入失败',
                        type: 'error'
                    });
                }

            });
            //this.$refs['addForm'].resetFields();
            this.addFormVisible = false;
            v.get_weekly()
        },
        // handleEdit: function (index, row) {
        //     this.editFormVisible = true;
        //     this.editForm = Object.assign({}, row);
        // },
        handleAdd: function () {
            this.addFormVisible = true;
        },
    }
}
</script>
