/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from './App.vue'
<<<<<<< HEAD
<<<<<<< HEAD
import router from "@/router/router"
import "./styles/global.css"


createApp(App).use(router).mount("#app");
=======
import router from './router'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'

loadFonts()


createApp(App)
    .use(router)
    .use(vuetify)
    .mount('#app')
>>>>>>> a6e30e615dd691b7af8ccb08d2f53e38166c268f
=======

import { createApp } from 'vue'

import { createStore } from 'vuex';
import { registerPlugins } from '@/plugins'

const app = createApp(App)

registerPlugins(app)


app.mount('#app')
>>>>>>> parent of 14b8c8b (Added frontend)
