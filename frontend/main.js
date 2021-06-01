import Vue from "vue";
import * as Sentry from "@sentry/vue";
import App from "./App.vue";
import router from "./router";
import store from './store'
import Axios from 'axios'
import VueAxios from 'vue-axios'
import VueGtag from "vue-gtag";

import Argon from "./plugins/argon-kit";
import * as backendAPI from './common/backendAPI'
import titleMixin from './mixins/titleMixin';


Vue.config.productionTip = false;
Vue.prototype.$api = backendAPI;

Vue.use(Argon);
Vue.use(VueAxios, Axios)
Vue.mixin(titleMixin);
Vue.use(VueGtag, {
  config: {id: 'G-LF0NFE38PY'},
  bootstrap: false,
}, router);
// Sentry.init({
//   Vue: Vue,
//   dsn: "https://d5d4f8ab79e44e238be6d6e0253e8144@o207892.ingest.sentry.io/5583101",
// })
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
