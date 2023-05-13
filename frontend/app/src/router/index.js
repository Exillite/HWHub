import Main from "@/pages/Main.vue";
import { createWebHistory, createRouter } from "vue-router";

const routes = [{
        path: "/",
        name: "Main",
        component: Main,
    },
    {
        path: "/error",
        name: "Error",
        component: () =>
            import ("@/pages/404.vue"),
    },
    {
        path: "/login",
        name: "Login",
        component: () =>
            import ("@/pages/Login.vue"),
    },
    {
        path: "/registration",
        name: "Registration",
        component: () =>
            import ("@/pages/Registration.vue"),
    },
    {
        path: "/groups",
        name: "Groups",
        component: () =>
            import ("@/pages/Groups.vue"),
    },
    {
        path: "/group/:id",
        name: "Group",
        component: () =>
            import ("@/pages/Group.vue"),
    },
    {
        path: "/homework/:id",
        name: "Homework",
        component: () =>
            import ("@/pages/Homework.vue"),
    },
];

const router = new createRouter({
    history: createWebHistory(),
    routes,
});

export default router;