<template>
    <div>
        <el-button type="primary" @click="handleAdd">新增</el-button>
        <el-table :data="summary_list" border style="width: 100%">
            <el-table-column prop="id" style="display:none" label="id" width="150" sortable>
            </el-table-column>
            <el-table-column prop="natural_week" label="自然周数" width="150" fixed sortable>
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
                <el-form-item label="周数:">
                    <div class="block">
                        <span class="demonstration">周</span>
                        <el-date-picker v-model="insertForm.natural_week" type="week" format="yyyy-WW 周" @change="dateChange1" placeholder="选择周">
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
                natural_week: '',
                // end_date: new Date().getFullYear() + '-' + (new Date().getMonth() + 1) + '-' + new Date().getDate(),
                summary: '',
                plan: '',
                self_evaluation: '',

            },
        }
    },
    created() {
        // 组件创建完后获取数据，这里和1.0不一样，改成了这个样子
        this.get_summary()

    },
    methods: {
        dateChange1(val) {
            var self = this;
            self.insertForm.naturalWeek = val
        },
        get_summary: function (params) {
            var self = this;
            this.$axios.get('/works/get_weekly_summary/', {
                params: {
                    filterDate: self.filters.filterDate,
                    // project_name: self.filters.project_name
                }
            })
                .then(function (response) {
                    self.summary_list = eval(response.data.content);
                }
                );
        },
        insertSummary: function () {
            var self = this;
            let str = 'natural_week=' + self.insertForm.naturalWeek + '&summary=' + self.insertForm.summary + '&self_evaluation=' + self.insertForm.self_evaluation + '&plan=' + self.insertForm.plan;
            this.$axios.post('/works/insert_summary/', str).then(function (response) {
                if (response.data.code == 0) {
                    self.get_summary();
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
            //this.$refs['addForm'].resetFields();
            this.addFormVisible = false;

        },
        // handleEdit: function (index, row) {
        //     this.editFormVisible = true;
        //     this.editForm = Object.assign({}, row);
        // },
        handleAdd: function () {
            this.addFormVisible = true;
        },
        handleDelete: function (index, row) {
            var self = this;
            let delID = row.id;

            let str = 'delID=' + delID
            this.$axios.post('/works/del_summary/', str)
                .then(function (response) {
                    if (response.data.code == 0) {
                        self.get_summary()
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
        handleEdit: function (index, row) {
            this.editFormVisible = true;
            this.editForm = Object.assign({}, row);
        },
    }
}
</script>
