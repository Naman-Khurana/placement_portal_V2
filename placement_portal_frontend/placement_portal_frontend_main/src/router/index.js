import { createRouter, createWebHistory } from "vue-router";

import LoginView from "../views/LoginView.vue";
import StudentRegisterView from "../views/StudentRegisterView.vue";
import { useAuthStore } from "../stores/AuthStore.js";
import { getDashboardRoute } from "../utils/navigation.js";
import { LOGIN_ROUTE } from "../utils/routeConstants";
import { STUDENT_REGISTER_ROUTE } from "../utils/routeConstants";
import { COMPANY_REGISTER_ROUTE } from "../utils/routeConstants";
import CompanyRegisterView from "../views/CompanyRegisterView.vue";
import StudentDashboardView from "../views/StudentDashboardView.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/",
            redirect: "/login",

        },
        {
            path: "/login",
            name: "Login",
            component: LoginView,
            meta: {
                requiresAuth: false
            }
        },
        {
            path: "/register",
            name: "Student Register",
            component: StudentRegisterView,
            meta: {
                requiresAuth: false
            }
        },
        {
            path: "/register-company",
            name: "Company Register",
            component: CompanyRegisterView,
            meta: {
                requiresAuth: false
            }
        },
         {
            path: "/student",
            name: "Student Dashboard",
            component: StudentDashboardView,
            meta: {
                requiresAuth: true
            }
        }
    ]
});

router.beforeEach((destination) => {
    const authStore = useAuthStore();

    console.log("Navigating to:", destination.path);
    console.log("requiresAuth:", destination.meta.requiresAuth);
    console.log("isAuthenticated:", authStore.isAuthenticated);

    if (destination.meta.requiresAuth && !authStore.isAuthenticated) {
        console.log("Redirecting to login");
        return "/login";
    }

    if (
        authStore.isAuthenticated &&
        (
            destination.path === LOGIN_ROUTE ||
            destination.path === STUDENT_REGISTER_ROUTE ||
            destination.path === COMPANY_REGISTER_ROUTE
        )
    ) {
        console.log("Redirecting to dashboard");
        return getDashboardRoute(authStore.userRole);
    }
});

export default router;