import { createApp } from 'vue'
import App from './App.vue'
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
