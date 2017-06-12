<template>
    <div class="login-wrap">
        <div class="ms-title">周报管理系统</div>
        <div class="ms-login">
            <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="0px" class="demo-ruleForm">
                <el-form-item prop="username">
                    <el-input v-model="ruleForm.username" value="admin" placeholder="username"></el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input type="password" placeholder="password" value="lanzhong" v-model="ruleForm.password" @keyup.enter.native="submitForm('ruleForm')"></el-input>
                </el-form-item>
                <div class="login-btn">
                    <el-button type="primary" @click="submitForm('ruleForm')">登录</el-button>
                </div>
                <p style="font-size:12px;line-height:30px;color:#999;">Tips : 用户名admin 密码lanzhong</p>
                <p style="font-size:12px;line-height:30px;color:#999;">
                    <!--<a href="/register">注册新账号</a>-->
                </p>
            </el-form>
        </div>
    </div>
</template>

<script>
export default {
    data: function () {
        return {
            ruleForm: {
                username: 'admin',
                password: 'lanzhong'
            },
            rules: {
                username: [
                    { required: true, message: '请输入用户名', trigger: 'blur' }
                ],
                password: [
                    { required: true, message: '请输入密码', trigger: 'blur' }
                ]
            }
        }
    },
    methods: {
        submitForm(formName) {
            const self = this;
            self.$refs[formName].validate((valid) => {
                if (valid) {
                    let postdata = 'username=' + self.ruleForm.username + '&password=' + self.ruleForm.password;

                    this.$axios.post('/accounts/login/', postdata).then((res) => {
                        if (res.data.code == '0') {
                            var login_data = JSON.stringify(res.data.content);
                            var premission = res.data.content.group_list
                            localStorage.setItem('login_data', login_data);
                            localStorage.setItem('ms_username',res.data.content.chinese_name);
                            localStorage.setItem('department_id',res.data.content.department_id);
//                            var position = new Array("技术主管组", "销售主管组", "技术员工组", "销售员工组")
//                            for (var i in position) {
//                                if (premission.toString().indexOf(position[i]) > -1) {
//                                    localStorage.setItem(position[i], true);
//                                }
//                            }
                            if (premission.toString().indexOf("技术主管组") > -1) {
                                localStorage.setItem("技术主管组", true);
                                self.$router.push('/analysisWeekly');
                            }
                            else if (premission.toString().indexOf("销售主管组") > -1) {
                                  localStorage.setItem("销售主管组", true);
                                self.$router.push('/analysisSaleEvent');
                            }
                            else if (premission.toString().indexOf("技术员工组") > -1) {
                                localStorage.setItem("技术员工组", true);
                                self.$router.push('/insertDevWork');
                            }
                            else if (premission.toString().indexOf("销售员工组") > -1) {
                                  localStorage.setItem("销售员工组", true);
                                self.$router.push('/insertSaleEvent');

                            } else {
                                self.$router.push('/readme');
                            }
                        } else {
                            this.$message.error('密码或者用户名错误');
                            return false;
                        }
                    })
                } else {
                    console.log('error submit!!');
                    return false;
                }
            });
        }
    }
}
</script>

<style scoped>
.login-wrap {
    position: relative;
    width: 100%;
    height: 100%;
}

.ms-title {
    position: absolute;
    top: 50%;
    width: 100%;
    margin-top: -230px;
    text-align: center;
    font-size: 30px;
    color: #fff;
}

.ms-login {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 300px;
    height: 200px;
    margin: -150px 0 0 -190px;
    padding: 40px;
    border-radius: 5px;
    background: #fff;
}

.login-btn {
    text-align: center;
}

.login-btn button {
    width: 100%;
    height: 36px;
}
</style>
