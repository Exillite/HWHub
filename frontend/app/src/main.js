/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from './App.vue'

import { createApp } from 'vue'

import { createStore } from 'vuex';
import { registerPlugins } from '@/plugins'

const app = createApp(App)

registerPlugins(app)


app.mount('#app')