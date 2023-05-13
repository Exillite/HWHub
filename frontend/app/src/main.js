import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import vuetify from "./plugins/vuetify";
import { loadFonts } from "./plugins/webfontloader";
import Vue3EasyDataTable from "vue3-easy-data-table";
import "vue3-easy-data-table/dist/style.css";
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";

loadFonts();

createApp(App)
    .use(router)
    .use(vuetify)
    .component("EasyDataTable", Vue3EasyDataTable)
    .component("VueDatePicker", VueDatePicker)
    .mount("#app");