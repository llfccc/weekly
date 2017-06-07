<template>
  <div>
      {{name}}
      </div>
</template>
<script>
export default {
    data() {
        return {     
                name: '标题'   
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