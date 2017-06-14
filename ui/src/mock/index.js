import Mock from 'mockjs';
// import {vuetable} from './vuetable.js';
// import {datasource} from './datasource.js';

// let data = [].concat(vuetable,datasource);
let data = []
data.forEach(function(res){
    Mock.mock(res.path, res.data);
        // Mock.mock();
});

//export default Mock;
