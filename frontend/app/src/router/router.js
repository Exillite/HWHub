import { createRouter, createWebHistory } from "vue-router";
import Login from "@/pages/LoginPage"
import Registration from "@/pages/RegistrationPage"
import StudentsGroup from "@/pages/StudentsGroup"


const routes = [
    {
        path: '/login',
        component: Login
    },
    {
        path: '/',
        component: Login
    },
    {
        path: '/registration',
        component: Registration
    },
    {
        path: '/dashbroad',
        component: StudentsGroup
    }


]
const router = createRouter({
    routes,
    history: createWebHistory(process.env.BASE_URL)
})

export default router;