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
import { STUDENT_PROFILE_ROUTE } from "../utils/routeConstants";
import { STUDENT_DASHBOARD_ROUTE } from "../utils/routeConstants";
import StudentProfileView from "../views/StudentProfileView.vue";
import { STUDENT_APPLICATIONS_ROUTE } from "../utils/routeConstants";
import StudentApplicationsView from "../views/StudentApplicationsView.vue";
import { COMPANY_DASHBOARD_ROUTE } from "../utils/routeConstants";
import CompanyDashboardView from "../views/company/CompanyDashboardView.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/",
            redirect: LOGIN_ROUTE,

        },
        {
            path: LOGIN_ROUTE,
            name: "Login",
            component: LoginView,
            meta: {
                requiresAuth: false
            }
        },
        {
            path: STUDENT_REGISTER_ROUTE,
            name: "Student Register",
            component: StudentRegisterView,
            meta: {
                requiresAuth: false
            }
        },
        {
            path: COMPANY_REGISTER_ROUTE,
            name: "Company Register",
            component: CompanyRegisterView,
            meta: {
                requiresAuth: false
            }
        },
         {
            path: STUDENT_DASHBOARD_ROUTE,
            name: "Student Dashboard",
            component: StudentDashboardView,
            meta: {
                requiresAuth: true
            }
        },
        {
            path:STUDENT_APPLICATIONS_ROUTE,
            name: "Student Applications Page",
            component: StudentApplicationsView,
            meta: {
                requiresAuth: true
            }

        },
        {
            path:STUDENT_PROFILE_ROUTE,
            name: "Student Profile Page",
            component: StudentProfileView,
            meta: {
                requiresAuth: true
            }

        },
         {
            path:COMPANY_DASHBOARD_ROUTE,
            name: "Student Dashboard",
            component: CompanyDashboardView,
            meta: {
                requiresAuth: true
            }

        },

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