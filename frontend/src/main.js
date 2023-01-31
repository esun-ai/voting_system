import "bootstrap/dist/css/bootstrap.css";
import axios from "axios";
import router from "./router";
import { createApp } from "vue";
import App from "./App.vue";
import BootstrapVue3 from "bootstrap-vue-3";
import store from "./store";

axios.defaults.withCredentials = true;
axios.defaults.baseURL = import.meta.env.VITE_APP_ENV_API_URL;

export const app = createApp(App);
app.use(router, axios).use(BootstrapVue3).use(store);
app.config.globalProperties.$category = JSON.parse(import.meta.env.VITE_APP_CATEGORIES);
app.mount("#app");
