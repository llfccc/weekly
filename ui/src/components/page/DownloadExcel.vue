<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-date"></i> 表单</el-breadcrumb-item>
                <el-breadcrumb-item>Excel下载</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="content-title">当前导出所有</div>
        <div class="plugins-tips">
            XXX说明
        </div>
        <el-button @click="download">导出下载</el-button>
        <!--<el-upload-->
                <!--action="/api/posts/"-->
                <!--type="drag"-->
                <!--:thumbnail-mode="true"-->
                <!--:on-preview="handlePreview"-->
                <!--:on-remove="handleRemove"-->
                <!--:on-error="handleError"-->
                <!--:default-file-list="fileList"-->
        <!--&gt;-->
            <!--<i class="el-icon-upload"></i>-->
            <!--<div class="el-dragger__text">将文件拖到此处，或<em>点击上传</em></div>-->
            <!--<div class="el-upload__tip" slot="tip">只能上传jpg/png文件，且不超过500kb</div>-->
        <!--</el-upload>-->
        <!--<div class="content-title">支持裁剪</div>-->
        <!--<div class="plugins-tips">-->
            <!--Vue-Core-Image-Upload：一款轻量级的vue上传插件，支持裁剪。-->
            <!--访问地址：<a href="https://github.com/Vanthink-UED/vue-core-image-upload" target="_blank">Vue-Core-Image-Upload</a>-->
        <!--</div>-->
        <!--<img class="pre-img" :src="src" alt="">-->
        <!--<vue-core-image-upload :class="['pure-button','pure-button-primary','js-btn-crop']"-->
                               <!--:crop="true"-->
                               <!--text="上传图片"-->
                               <!--url="/api/posts/"-->
                               <!--extensions="png,gif,jpeg,jpg"-->
                               <!--@:imageuploaded="imageuploaded"-->
                               <!--@:errorhandle="handleError"></vue-core-image-upload>-->
    </div>
</template>

<script>
    import VueCoreImageUpload  from 'vue-core-image-upload';
    export default {
        data: function(){
            return {
                src: '../../../static/img/img.jpg',
                fileList: []
            }
        },
        components: {
                VueCoreImageUpload
        },
        methods:{
            download(){
                try{
                    var url="/works/get_excel/";
            var elemIF = document.createElement("iframe");
            elemIF.src = url;
            elemIF.style.display = "none";
            document.body.appendChild(elemIF);
        }catch(e){

        }
              console.log("dfdf");
            },
            imageuploaded(res) {
                console.log(res)
            },
            handleRemove(file, fileList) {
                console.log(file, fileList);
            },
            handlePreview(file) {
                console.log(file);
            },
            handleError(){
                this.$notify.error({
                    title: '上传失败',
                    message: '图片上传接口上传失败，可更改为自己的服务器接口'
                });
            }
        }
    }
</script>

<style scoped>
    .content-title{
        font-weight: 400;
        line-height: 50px;
        margin: 10px 0;
        font-size: 22px;
        color: #1f2f3d;
    }
    .pre-img{
        width:250px;
        height: 250px;
        margin-bottom: 20px;
    }
</style>
