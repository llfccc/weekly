<template>
  <div class="echarts">
    <IEcharts :option="bar" :loading="loading" @ready="onReady" @click="onClick"></IEcharts>
    <button @click="doRandom">Random</button>
  </div>
</template>

<script type="text/babel">
import IEcharts from 'vue-echarts-v3/src/full.vue';
export default {
  name: 'view',
  components: {
    IEcharts
  },
  filters: {
    project_name: '',
    filter_date: '',
    start_date: '',
    end_date: '',
  },
  props: {
  },
  worker_type:[],
  data: () => ({
    loading: false,
    bar: {
      title: {
        text: '工作类型占比'
      },
      tooltip: {},
      xAxis: {
        data: ['Shirt', 'Sweater', 'Chiffon Shirt', 'Pants', 'High Heels', 'Socks']
      },
      yAxis: {},
      series: [{
        name: 'Sales',
        type: 'bar',
        data: [5, 20, 36, 10, 10, 20]
      }]
    }
  }),
      created() {
        // 组件创建完后获取数据
        this.get_data()
    },
  methods: {
    get_data() {
      const self = this;
      this.$axios.get('/analysis/analysis_worker/', {
        params: {
          filterDate: self.filters.filterDate,
          project_name: self.filters.project_name
        }
      })
        .then(function (response) {
          self.worker_type = eval(response.data.content);
          console.log(self.worker_type);
        }
        );
    },
    doRandom() {
      const that = this;
      let data = [];
      for (let i = 0, min = 5, max = 99; i < 6; i++) {
        data.push(Math.floor(Math.random() * (max + 1 - min) + min));
      }
      that.loading = !that.loading;
      that.bar.series[0].data = data;
    },
    onReady(instance) {
      // console.log(instance);
    },
    onClick(event, instance, echarts) {
      // console.log(arguments);
    }
  }
};
</script>

<style scoped>
.echarts {
  width: 400px;
  height: 400px;
}
</style>