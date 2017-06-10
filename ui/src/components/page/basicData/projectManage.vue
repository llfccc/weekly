<template>
    <div class="admin">
        <iframe ref="iframe" src="../../admin" width="100%" height="700px"></iframe>
        <!--<iframe ref="iframe" src="http://www.baidu.com" width="100%" height="100%"></iframe>-->

        <!--<div class="filters row">
                <div class="form-group col-sm-3">
                    <label for="search-element">Product name</label>
                    <input v-model="searchKey" class="form-control" id="search-element" requred/>
                </div>
            </div>
            <table class="table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Price</th>
                        <th class="col-sm-2">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="product in filteredProducts">
                        <td>
                            <router-link :to="{name: 'product', params: {product_id: product.id}}">{{ product.name }}</router-link>
                        </td>
                        <td>{{ product.description }}</td>
                        <td>
                            {{ product.price }}
                            <span class="glyphicon glyphicon-euro" aria-hidden="true"></span>
                        </td>
                        <td>
                            <router-link class="btn btn-warning btn-xs" :to="{name: 'product-edit', params: {product_id: product.id}}">Edit</router-link>
                            <router-link class="btn btn-danger btn-xs" :to="{name: 'product-delete', params: {product_id: product.id}}">Delete</router-link>
                        </td>
                    </tr>
                </tbody>
            </table>
            <template id="product-edit">
        <section>
      <h2>Edit product</h2>
      <form v-on:submit="updateProduct">
        <div class="form-group">
          <label for="edit-name">Name</label>
          <input class="form-control" id="edit-name" v-model="product.name" required/>
        </div>
        <div class="form-group">
          <label for="edit-description">Description</label>
          <textarea class="form-control" id="edit-description" rows="3" v-model="product.description"></textarea>
        </div>
        <div class="form-group">
          <label for="edit-price">Price, <span class="glyphicon glyphicon-euro"></span></label>
          <input type="number" class="form-control" id="edit-price" v-model="product.price"/>
        </div>
        <button type="submit" class="btn btn-primary">Save</button>
        <router-link to="'/'" class="btn btn-default">Cancel</router-link>
      </form>
    </section>
    </template>-->
    </div>
</template>
<script>
export default {
    data() {
        return {
            name: '标题',
            searchKey: '',
            products: [
                { id: 1, name: 'Angular', description: 'Superheroic JavaScript MVW Framework.', price: 100 },
                { id: 2, name: 'Ember', description: 'A framework for creating ambitious web applications.', price: 100 },
                { id: 3, name: 'React', description: 'A JavaScript Library for building user interfaces.', price: 100 }
            ],
        }
    },
    created() {
        // 组件创建完后获取数据，这里和1.0不一样，改成了这个样子
        // this.get_data()
        // this.get_projects()
        // this.get_event_types()
        // this.get_sale_event_types()
    },
    methods: {
        // handleEdit: function (index, row) {
        //     this.editFormVisible = true;
        //     this.editForm = Object.assign({}, row);
        // },
    },
    computed: {
        // filteredProducts: function () {
        //     var self = this;
        //     console.log()
        //     return self.products.filter(function (product) {
        //         return product.name.indexOf(self.searchKey) !== -1
        //     })
        // }
    }
}


</script>
<style scoped>
/*.admin{
position:absolute;
/*margin-left:40px;
}*/
</style>
