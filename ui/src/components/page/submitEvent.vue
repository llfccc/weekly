<template>
    <div>
        <h1 class="logo">登记拜访</h1>
        <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
            <el-form :inline="true" :model="filters">
                <el-form-item>
                    <el-input v-model="filters.name" placeholder="姓名"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleAddCustomer">新增客户</el-button>
                    <el-button type="primary" @click="handleAddVisit">新增拜访</el-button>
                </el-form-item>
            </el-form>
        </el-col>
    
        <el-dialog title="新增客户" v-model="addCustomerVisible" :close-on-click-modal="false">
            <el-form ref="addCustomerForm" :model="addCustomerForm" label-width="90px">
    
                <el-form-item label="客户全称">
                    <el-input type="text" class="form-control" id="full_name" placeholder="客户全称" v-model="addCustomerForm.full_name">客户全称
                    </el-input>
                </el-form-item>
                <el-form-item label="客户简称">
                    <el-input type="text" class="form-control" id="short_name" placeholder="客户简称" v-model="addCustomerForm.short_name">客户简称
                    </el-input>
                </el-form-item>
    
                <el-form-item label="联系人">
                    <el-input type="text" class="form-control" id="contact_name" placeholder="主要联系人姓名" v-model="addCustomerForm.contact_name">主要联系人姓名
                    </el-input>
                    <el-input type="text" class="form-control" id="contact_post" placeholder="主要联系人职位" v-model="addCustomerForm.contact_post">主要联系人职位
                    </el-input>
                </el-form-item>
    
                <el-form-item label="联系方式">
                    <el-input type="text" class="form-control" id="contact_tel_num" placeholder="主要联系人电话号码" v-model="addCustomerForm.contact_tel_num">主要联系人电话号码
                    </el-input>
                    <el-input type="text" class="form-control" id="contact_mdn" placeholder="主要联系人手机号码" v-model="addCustomerForm.contact_mdn">主要联系人手机号码
                    </el-input>
                </el-form-item>
    
                <el-form-item label="其他：">
                    <el-input type="textarea" class="form-control" id="sale_customer_remark" placeholder="备注" v-model="addCustomerForm.sale_customer_remark">
                        备注
                    </el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="addCustomerVisible = false">取消</el-button>
                <el-button type="primary" @click.native="addCustomer" :loading="addLoading">提交</el-button>
            </div>
        </el-dialog>
    
        <el-dialog title="新增拜访" v-model="addEventVisible" :close-on-click-modal="false">
            <el-form ref="addEventForm" :model="addEventForm" label-width="90px">
                <el-form-item label="拜访对象">
                    <el-date-picker v-model="addEventForm.visit_date" type="date" placeholder="拜访时间" @change="dateChange" :picker-options="dateOption">
                    </el-date-picker>
                    <el-select v-model="addEventForm.sale_customer_id" clearable filterable placeholder="客户名">
                        <el-option v-for="item in customer_list" :key="item.id" :label="item.short_name" :value="item.id">
                        </el-option>
                    </el-select>
    
                </el-form-item>
                <el-form-item label="类型">
                    <el-select v-model="addEventForm.active_type_id" clearable filterable placeholder="拜访类型">
                        <el-option v-for="item in sale_event_type_list" :key="item.id" :label="item.active_type_name" :value="item.id">
                        </el-option>
                    </el-select>
                    <el-select v-model="addEventForm.sale_phase_id" clearable filterable placeholder="阶段">
                        <el-option v-for="item in sale_phase_list" :key="item.id" :label="item.phase_name" :value="item.id">
                        </el-option>
                    </el-select>
                </el-form-item>
    
                <el-form-item label="工作内容">
                    <el-col :span="8">
                        <el-input type="text" class="form-control" id="cus_con_post" placeholder="主要联系人电话号码" v-model="addEventForm.cus_con_post">主要联系人电话号码
                        </el-input>
                    </el-col>
    
                    <el-col :span="8">
    
                        <el-input type="text" class="form-control" id="cus_con_mdn" placeholder="手机号码" v-model="addEventForm.cus_con_mdn">手机号码
    
                        </el-input>
                    </el-col>
                </el-form-item>
                <el-form-item label="工作内容">
                    <el-col :span="8">
                        <el-input type="text" class="form-control" id="cus_con_tel_num" placeholder="客户联系方式" v-model="addEventForm.cus_con_tel_num">客户联系方式
                        </el-input>
    
                    </el-col>
                    <el-col :span="8">
    
                    </el-col>
                    <el-col :span="8">
                        <el-input type="text" class="form-control" id="cus_con_wechart" placeholder="客户的微信号" v-model="addEventForm.cus_con_wechart">客户的微信号
                        </el-input>
    
                    </el-col>
    
                </el-form-item>
    
                <el-form-item label="其他：">
                    <el-input type="textarea" class="form-control" id="communicate_record" placeholder="沟通成果" v-model="addEventForm.communicate_record">沟通成果
                    </el-input>
                    <el-col :span="8">    
                    </el-col>

                </el-form-item>
                <el-form-item label="其他：">
                    <el-input type="textarea" class="form-control" id="sale_event_remark" placeholder="备注" v-model="addEventForm.sale_event_remark">
                        备注
                    </el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="addEventVisible = false">取消</el-button>
                <el-button type="primary" @click.native="addWork" :loading="addLoading">提交</el-button>
            </div>
        </el-dialog>
    
        <el-table :data="sale_list" border style="width: 100%">
            <el-table-column prop="short_name" label="客户简称" width="150" fixed sortable>
            </el-table-column>
            <el-table-column prop="phase_name" label="拜访阶段" width="150" fixed sortable>
            </el-table-column>
            <el-table-column prop="cus_con_post" label="客户职位" width="150" sortable>
            </el-table-column>
            <el-table-column prop="visit_date" label="拜访时间" width="150" sortable>
            </el-table-column>
            <el-table-column prop="cus_con_mdn" label="手机号码" width="150" sortable>
            </el-table-column>
            <el-table-column prop="cus_con_tel_num" label="客户联系方式" width="190" sortable>
            </el-table-column>
            <el-table-column prop="cus_con_wechart" label="客户的微信号" width="190" sortable>
            </el-table-column>
    
            <el-table-column prop="communicate_record" label="沟通成果" width='170' sortable>
            </el-table-column>
            <el-table-column prop="sale_event_remark" label="备注" width="150">
            </el-table-column>
    
            <el-table-column label="操作" width="180" fixed="right">
                <template scope="scope">
                    <el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                    <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <!--编辑界面-->
        <el-dialog title="编辑" v-model="editFormVisible" :close-on-click-modal="false">
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
            dateOption: {
                disabledDate(time) {
                    return time.getTime() < Date.now() - 8.64e7 * 6;
                }
            },
            sale_list: [],
            sale_phase_list:[],
            customer_list: [],
            sale_event_type_list: [],
            user_list: [],
            addCustomerForm: {
                full_name: '',
                short_name: '',
                contact_post: '',
                contact_name: '',
                contact_mdn: '',
                contact_tel_num: '',
                sale_customer_remark: '',
            },
                addEventForm: {
                cus_con_post: '',
                visit_date: '',
                cus_con_mdn: '',
                cus_con_tel_num: '',
                cus_con_wechart: '',
                communicate_record: '',
                sale_event_remark: '',
                active_type_id: '',

                sale_customer_id:'',
                sale_phase_id:'',
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
            addEventVisible: false,//新增拜访界面是否显示
            addCustomerVisible: false,//新增客户界面是否显示
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
        this.get_customers()
        this.get_sale_phases()
        this.get_event_types()
        this.get_sale_event_types()
    },
    methods: {
          dateChange(val) {
            var self = this;
            self.addEventForm.visit_date = val
        },
        get_sale_event_types: function (params) {
            var self = this;
            this.$axios.get('/works/get_sale_event_types/')
                .then(function (response) {
                    self.sale_event_type_list = eval(response.data.content);
                    console.log(self.sale_event_type_list)

                }
                );
        },
        get_sale_phases: function (params) {
            var self = this;
            this.$axios.get('/works/get_sale_phases/')
                .then(function (response) {
                    self.sale_phase_list = eval(response.data.content);
                    console.log(self.sale_phase_list)
                }
                );
        },
        get_data: function (params) {
            var self = this;
            this.$axios.get('/works/get_saleevents/')
                .then(function (response) {
                    self.sale_list = eval(response.data.content);

                }
                );
        },
        get_customers: function (params) {
            var self = this;
            this.$axios.get('/works/get_customers/')
                .then(function (response) {
                    self.customer_list = eval(response.data.content);
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
        addCustomer: function () {
            var self = this;
            let str = 'full_name=' + self.addCustomerForm.full_name + '&short_name=' + self.addCustomerForm.short_name + '&contact_post=' + self.addCustomerForm.contact_post + '&contact_name=' + self.addCustomerForm.contact_name + '&contact_mdn=' + self.addCustomerForm.contact_mdn + '&contact_tel_num=' + self.addCustomerForm.contact_tel_num + '&sale_customer_remark=' + self.addCustomerForm.sale_customer_remark;
            this.$axios.post('/works/insert_customer/', str).then(function (response) {
                if (response.data.code == 0) {
                    // self.work_list.push(self.form);
                    self.$message({
                        message:  response.data.msg,
                        type: 'success'
                    });
                } else {
                    self.$message({
                        message: response.data.msg,
                        type: 'error'
                    });
                }

            });
            // this.addCustomerForm = Object.assign({},addCustomerForm);
            this.addFormVisible = false;
            this.get_customers();

        },

        addWork: function () {
            var self = this;
           
            let str = 'visit_date=' + self.addEventForm.visit_date + '&cus_con_post=' + self.addEventForm.cus_con_post + '&cus_con_mdn=' + self.addEventForm.cus_con_mdn + '&cus_con_tel_num=' + self.addEventForm.cus_con_tel_num + '&cus_con_wechart=' + self.addEventForm.cus_con_wechart + '&communicate_record=' + self.addEventForm.communicate_record + '&sale_event_remark=' + self.addEventForm.sale_event_remark + '&sale_event_owner_id=' + self.addEventForm.sale_event_owner_id + '&active_type_id=' + self.addEventForm.active_type_id+'&sale_customer_id=' + self.addEventForm.sale_customer_id+'&sale_phase_id=' + self.addEventForm.sale_phase_id;
            this.$axios.post('/works/insert_sale_event/', str).then(function (response) {

                if (response.data.code == 0) {
                    
                    self.get_data()
                    self.$message({
                        message: response.data.msg,
                        type: 'success'
                    });
                } else {
                    self.$message({
                        message: response.data.msg,
                        type: 'error'
                    });
                }

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
            this.editForm = Object.assign({}, row);
        },
        handleAddVisit: function () {
            this.addEventVisible = true;
            // this.addForm = {
            //     name: '',
            //     sex: -1,
            //     age: 0,
            //     birth: '',
            //     addr: ''
            // };
        },
        handleAddCustomer: function () {
            this.addCustomerVisible = true;
            // this.addForm = {
            //     name: '',
            //     sex: -1,
            //     age: 0,
            //     birth: '',
            //     addr: ''
            // };
        },
    },
}
</script>
