import Main from "@/pages/Main.vue";
import { createWebHistory, createRouter } from "vue-router";
import control from "@/control.js";

function denyIfUnauthenticated() {
    if (!control.check_auth())
        return "/login";
}

const routes = [
    {
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
        beforeEnter: denyIfUnauthenticated,
        component: () =>
            import ("@/pages/Groups.vue"),
    },
    {
        path: "/group/:id",
        name: "Group",
        beforeEnter: denyIfUnauthenticated,
        component: () =>
            import ("@/pages/Group.vue"),
    },
    {
        path: "/homework/:id",
        name: "Homework",
        beforeEnter: denyIfUnauthenticated,
        component: () =>
            import ("@/pages/Homework.vue"),
    },
    {
        path: "/:pathMatch(.*)*",
        name: "404",
        component: () =>
            import ("@/pages/404.vue")
    },
];

const router = new createRouter({
    history: createWebHistory(),
    routes,
});

export default router;