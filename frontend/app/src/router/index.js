// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [{
        path: '/login',
        name: 'Login',
        component: () =>
            import ('@/views/Login.vue'),
    },
    {
        path: '/registaration',
        name: 'Registaration',
        component: () =>
            import ('@/views/Registration.vue')
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
})

export default router