import Vue from 'vue'
import App from '@/App.vue'

import store from '@/store' 
import router from '@/router'

import VueQrcode from '@chenfengyuan/vue-qrcode';

import {getAvg} from './utils/filters.js'

Vue.config.productionTip = false

// Vue.use(VueRouter)

Vue.component(VueQrcode.name, VueQrcode);

Vue.filter('getAvg', getAvg);

const vue = new Vue({
  router,
  store,
  render: h => h(App)
})

vue.$mount('#app')
