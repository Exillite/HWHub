<<<<<<< HEAD
import Main from '@/pages/Main.vue'
import { createWebHistory, createRouter } from 'vue-router'
import cookie from '@/cookie'


function check_is_login() {
    if (cookie.getCookie('user_id') === undefined) {
        return true;
    }
    return true;
}

const routes = [{
        path: '/',
        name: 'Main',
        component: Main,
    },
    {
        path: '/login',
        name: 'Login',
        component: () =>
            import ('@/pages/Login.vue'),
    },
    {
        path: '/registration',
        name: 'Registration',
        component: () =>
            import ('@/pages/Registration.vue'),
    },
]

const router = new createRouter({
    history: createWebHistory(),
    routes
})


=======
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

>>>>>>> parent of 14b8c8b (Added frontend)
export default router