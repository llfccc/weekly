<template>
<div id="app" v-cloak class="container">
    <h1>工作日记</h1>

    <form class="form-inline">
        <div class="form-group">
            <label for="work_id">Name</label>
            <input type="text" class="form-control" id="work_id" placeholder="work_id" v-model="new_work.id">
        </div>
        <div class="form-group">
            <label for="work_title">Email</label>
            <input type="text" class="form-control" id="work_title" placeholder="work_title"
                   v-model="new_work.work_title">
        </div>
        <button @click="addWork" class="js-add btn btn-default" type="button">添加工作内容!</button>
    </form>

    <!--<table class="table table-bordered">-->
        <!--<thead>-->
        <!--<tr>-->
            <!--<td>选择</td>-->
            <!--<td>id</td>-->
            <!--<td>工作内容</td>-->
            <!--<td>操作</td>-->
        <!--</tr>-->
        <!--</thead>-->
        <!--<tbody>-->
        <!--<tr v-for="job in jobs" v-bind:class="{ 'removed': job.hided }">-->
            <!--<td><input type="checkbox"></td>-->
            <!--<td>{{job.id}}</td>-->
            <!--<td> {{ job.work_title }}</td>-->
            <!--<td>-->
                <!--<button @click="delWork($event)" v-bind:hidedID="job.id" class="js-add btn btn-default" type="button">-->
                    <!--Hide!-->
                <!--</button>-->
            <!--</td>-->
        <!--</tr>-->
        <!--</tbody>-->
    <!--</table>-->
    <div class="footer">
        <hr/>
        <em>llf Copyright 2017-4-21</em>
    </div>

</div>

  </template>

<script>
  import axios from 'axios';
    getUrl = 'http://127.0.0.1/api/get_works/';
    axios.get(getUrl)
        .then(function (response) {
            app.jobs = JSON.parse(response.data.content);   //eval(response.data.content);
        });

    var app = new Vue({
        el: '#app',
        data: {
            jobs: '',
            new_work: {
                id: '',
                work_title: '',
            }
        },
//        compiled: function () {
//            var self = this;
//            //在编译后即调用API接口取得服务器端数据
//
//        },
        methods: {
            addWork: function () {
                if (~isNaN(this.new_work.id) && this.new_work.work_title !== null) {   //有错误
                    console.log("post");
                    $.ajax({
                        type: "POST",
                        url: '/api/insert_work/',
                        data: this.new_work,//new_json, /* 注意参数的格式和名称 */
                        dataType: "json",
                        success: function (response) {
                           // this.jobs.push(this.new_work);  //push一直有问题，暂时用get代替
                            axios.get(getUrl)
                                .then(function (response) {
                                    app.jobs = JSON.parse(response.data.content);   //eval(response.data.content);
                                });
                        }
                    });
                }

                //                axios.post('/api/insertWork/', {
//                    firstName: 'Fred',
//                    lastName: 'Flintstone'
//                }, {
//                    headers: {
//                        'Content-Type': 'application/x-www-form-urlencoded',
//                        'Access-Control-Allow-Headers': '*',
//                    }
//                })
//                    .then(function (response) {
//                        this.jobs.push(this.new_work);
//                        console.log(response);
//                    })
//                    .catch(function (error) {
//                        console.log(error);
//                    });
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

            },
        }
    })
</script>
