import { ADMIN_COMPANIES_ROUTE } from "./routeConstants";
import { ADMIN_APPLICATIONS_ROUTE } from "./routeConstants";
import { ADMIN_DRIVES_ROUTE } from "./routeConstants";
import { ADMIN_STUDENTS_ROUTE } from "./routeConstants";
import { ADMIN_DASHBOARD_ROUTE } from "./routeConstants";

export const adminSidebarItems = [

    {
        label: "Dashboard",
        route: ADMIN_DASHBOARD_ROUTE
    },

    {
        label: "Students",
        route: ADMIN_STUDENTS_ROUTE
    },

    {
        label: "Companies",
        route: ADMIN_COMPANIES_ROUTE
    },{
        label:"Drives",
        route:ADMIN_DRIVES_ROUTE

    },
    {
        label:"Applications",
        route:ADMIN_APPLICATIONS_ROUTE
    }

];