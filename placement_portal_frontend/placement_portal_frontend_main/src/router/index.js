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
import { COMPANY_PLACEMENT_DRIVES_ROUTE } from "../utils/routeConstants";
import CompanyPlacementDrivesView from "../views/company/CompanyPlacementDrivesView.vue";
import { COMPANY_PROFILE_ROUTE } from "../utils/routeConstants";
import CompanyProfileView from "../views/company/CompanyProfileView.vue";
import { ADMIN_DASHBOARD_ROUTE } from "../utils/routeConstants";
import AdminDashboardView from "../views/admin/AdminDashboardView.vue";
import { ADMIN_STUDENTS_ROUTE } from "../utils/routeConstants";
import { ADMIN_COMPANIES_ROUTE } from "../utils/routeConstants";
import { ADMIN_DRIVES_ROUTE } from "../utils/routeConstants";
import { ADMIN_APPLICATIONS_ROUTE } from "../utils/routeConstants";
import AdminStudentsDashboardView from "../views/admin/AdminStudentsDashboardView.vue";
import AdminCompaniesDashboardView from "../views/admin/AdminCompaniesDashboardView.vue";
import AdminDrivesDashboardView from "../views/admin/AdminDrivesDashboardView.vue";
import AdminApplicationsDashboardView from "../views/admin/AdminApplicationsDashboardView.vue";

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
        //company
         {
            path:COMPANY_DASHBOARD_ROUTE,
            name: "Company Dashboard",
            component: CompanyDashboardView,
            meta: {
                requiresAuth: true
            }

        },
        {
            path:COMPANY_PLACEMENT_DRIVES_ROUTE,
            name: "Company drives",
            component: CompanyPlacementDrivesView,
            meta: {
                requiresAuth: true
            }

        },
        {
            path:COMPANY_PROFILE_ROUTE,
            name: "Company Profile",
            component: CompanyProfileView,
            meta: {
                requiresAuth: true
            }

        },
        // admin
        {
            path:ADMIN_DASHBOARD_ROUTE,
            name: "Admin Dashboard",
            component: AdminDashboardView,
            meta: {
                requiresAuth: true
            }

        },
        {
            path:ADMIN_STUDENTS_ROUTE,
            name: "Admin Students Dashboard",
            component: AdminStudentsDashboardView,
            meta: {
                requiresAuth: true
            }

        },
        {
            path:ADMIN_COMPANIES_ROUTE,
            name: "Admin Companies Dashboard",
            component: AdminCompaniesDashboardView,
            meta: {
                requiresAuth: true
            }

        },
        {
            path:ADMIN_DRIVES_ROUTE,
            name: "Admin Drives Dashboard",
            component: AdminDrivesDashboardView,
            meta: {
                requiresAuth: true
            }

        },
        {
            path:ADMIN_APPLICATIONS_ROUTE,
            name: "Admin Applications Dashboard",
            component: AdminApplicationsDashboardView,
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