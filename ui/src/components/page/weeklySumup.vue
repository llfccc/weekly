<template>
  <div>
 <el-dialog title="新增" v-model="addFormVisible" :close-on-click-modal="false">
            <el-form ref="form" :model="form" label-width="90px">
                <el-form-item label="项目名称">

                    <el-select v-model="form.dev_event_project_id" clearable filterable placeholder="项目名">
                        <el-option v-for="item in project_list" :key="item.id" :label="item.project_name" :value="item.id">
                        </el-option>
                    </el-select>
                    <el-select v-model="form.dev_event_type_id" clearable filterable placeholder="类型">
                        <el-option v-for="item in event_type_list" :key="item.id" :label="item.event_type_name" :value="item.id">
                        </el-option>
                    </el-select>

                </el-form-item>
                <el-form-item label="工作内容">
                    <el-input type="textarea" class="form-control" id="description" placeholder="工作内容" v-model="form.description">工作内容
                    </el-input>
                </el-form-item>

                <el-form-item label="工作时间">
                    <div class="block">
                        <span class="demonstration"></span>
                        <el-date-picker v-model="form.event_date" align="right" type="date" default-value="new Date()" placeholder="选择日期" format="yyyy-MM-dd" @change="dateChange" :picker-options="dateOption">
                        </el-date-picker>
                        <el-time-picker label="时间" is-range v-model="form.event_time" range-separator='*' placeholder="选择时间范围" @input="timeChange">
                        </el-time-picker>
                    </div>

                </el-form-item>
                <el-form-item label="其他：">
                    <el-col :span="8">
                        <el-select v-model="form.up_reporter_id" clearable filterable placeholder="上游汇报人">
                            <el-option v-for="item in user_list" :key="item.id" :label="item.chinese_name" :value="item.id">
                            </el-option>
                        </el-select>
                    </el-col>
                    <el-col :span="8">
                        <el-select v-model="form.down_reporter_ids" clearable filterable placeholder="下游汇报人">
                            <el-option v-for="item in user_list" :key="item.id" :label="item.chinese_name" :value="item.id">
                            </el-option>
                        </el-select>
                    </el-col>
                    <el-col :span="8">
                        <el-input type="text" class="form-control" id="fin_percentage" placeholder="进度" v-model="form.fin_percentage">进度
                        </el-input>
                    </el-col>
                </el-form-item>
                <el-form-item label="其他：">
                    <el-input type="textarea" class="form-control" id="dev_event_remark" placeholder="备注" v-model="form.dev_event_remark">
                        备注
                    </el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="addFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="addWork" :loading="addLoading">提交</el-button>
            </div>

        </el-dialog>
      </div>
</template>
<script>
export default {
    data() {
        return {
                name: '标题',
                addFormVisible:true,
        }
    },
    created() {
        // 组件创建完后获取数据，这里和1.0不一样，改成了这个样子
        this.get_data()
        this.get_projects()
        this.get_event_types()
        this.get_sale_event_types()
    },
    methods: {
        handleEdit: function (index, row) {
            this.editFormVisible = true;
            this.editForm = Object.assign({}, row);
        },
    },
}
</script>
