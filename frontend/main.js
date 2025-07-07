import Vue from "vue";
// import * as Sentry from "@sentry/vue";
import VueHtmlToPaper from "vue-html-to-paper";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import Axios from "axios";
import VueAxios from "vue-axios";

import Argon from "./plugins/argon-kit";
import * as backendAPI from "./common/backendAPI";
import titleMixin from "./mixins/titleMixin";

const print_options = {
  name: "_blank",
  specs: ["fullscreen=yes", "titlebar=yes", "scrollbars=yes"],
  styles: [
    "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css",
    "https://unpkg.com/kidlat-css/css/kidlat.css",
  ],
  timeout: 1000, // default timeout before the print window appears
  autoClose: true, // if false, the window will not close after printing
  windowTitle: window.document.title, // override the window title
};

Vue.config.productionTip = false;
Vue.prototype.$api = backendAPI;

Vue.use(Argon);
Vue.use(VueAxios, Axios);
Vue.mixin(titleMixin);
Vue.use(VueHtmlToPaper, print_options);
new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
