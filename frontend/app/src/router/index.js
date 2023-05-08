import Main from '@/pages/Main.vue'
import { createWebHistory, createRouter } from 'vue-router'
import cookie from '@/cookie'

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
    {
        path: '/groups',
        name: 'Groups',
        component: () =>
            import ('@/pages/Groups.vue'),
    },
    {
        path: '/group',
        name: 'Group',
        component: () =>
            import ('@/pages/Group.vue'),
    },
    {
        path: '/homework',
        name: 'Homework',
        component: () =>
            import ('@/pages/Homework.vue'),
    },
]

const router = new createRouter({
    history: createWebHistory(),
    routes
})


export default router